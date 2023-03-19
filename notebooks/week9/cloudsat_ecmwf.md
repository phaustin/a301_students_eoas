---
anaconda-cloud: {}
jupytext:
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"user_expressions": []}

(week9:cloudsat_ecmwf)=
# Working with cloudsat data

In this notebook we'll combine the cloudsat reflectivity with the ECMWF modeled temperatures to see whether
the bright band measured by cloudsat matches the 0-degree isotherm in the model.

I step 1 we select radar reflectivities for a tropical cloud, and in step 2 we overlay the forecast model
isotherm on top of the reflectivities.

I'll use the [seaborn color palette module](https://seaborn.pydata.org/tutorial/color_palettes.html) to pick a palette that
emphasizes the freezing level in the temperature plot

+++ {"user_expressions": []}

## Step 1: Plot the radar reflectivity for a storm

+++ {"user_expressions": []}

### Read in the radar reflectivity using `read_cloudsat_var`

```{code-cell} ipython3
import numpy as np
import datetime as dt
from datetime import timezone as tz
from matplotlib import pyplot as plt
import pyproj
from numpy import ma
import a301_lib
from sat_lib.cloudsat import read_cloudsat_var
import seaborn as sns

z_file=(a301_lib.data_share / 'pha/cloudsat').glob('20080820*CS_2C*RAIN*hdf')
z_file = list(z_file)[0]
meters2km=1.e3
print(z_file)

radar_ds = read_cloudsat_var('precip_liquid_water',z_file)
    
radar_ds
```

+++ {"user_expressions": []}

#### I know the storm covers 3 minutes of data starting at 6:45 UTC

From the quicklook plot for granule 10105 on 2008-03-22 I know there's a storm starting at 6:45 UTC near Indonesia. To get 
the correct section of cloudsat data, I'll bracket the 3 minutes from 6:45-6:48.

There are about 1125 measurements in those 3 minutes.  We use the logical index "time_hit"
clip the data from the full dataset.

```{code-cell} ipython3
import pandas as pd
#
# use pandas to convert the timestamp (a 64 bit number) to datetime objects
#
orbit_times=pd.to_datetime(radar_ds.coords['time'])
first_time = orbit_times[0]
print(f'orbit start: {first_time}')
#
# clipping index 6:45 - 6:48
#
start_hour=6
start_minute=45
storm_start=starttime=dt.datetime(first_time.year,first_time.month,first_time.day,
                                        start_hour,start_minute,0,tzinfo=tz.utc)
#
# get 3 minutes of data from the storm_start
#
storm_stop=storm_start + dt.timedelta(minutes=3)
print('storm start: {}'.format(storm_start))
#
# create a logical index that has the right time interval
#
time_hit = np.logical_and(orbit_times > storm_start,orbit_times < storm_stop)
#
# use it to clip the data
# 
storm_lats = radar_ds['latitude'][time_hit]
storm_lons=radar_ds['longitude'][time_hit]
storm_prof_times=radar_ds.coords['profile_time'][time_hit]
storm_zvals=radar_ds['Radar_Reflectivity'][time_hit,:]
distance_km = radar_ds['distance_km'][time_hit]
storm_date_times=orbit_times[time_hit]
```

+++ {"user_expressions": []}

#### Use pcolormeash to plot the reflectivity image

[pseudo color mesh](https://matplotlib.org/stable/gallery/images_contours_and_fields/pcolor_demo.html) is a plotting routine that can be used to plot either regular or irregularly gridded
images using a color palette

Notice the bright band visible at a height of 5 km

```{code-cell} ipython3
import copy

from matplotlib import cm
from matplotlib.colors import Normalize
vmin=-25
vmax=20
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
cmap_ref=copy.copy(cm.viridis)
cmap_ref.set_over('w')
cmap_ref.set_under('0.5')
cmap_ref.set_bad('0.75') #75% grey
day = orbit_times[0].date()
cloud_height_km=storm_zvals.coords['height']/meters2km
distance_km = storm_zvals.coords['distance_km']
distance_km = distance_km - distance_km[0]
fig, ax = plt.subplots(1,1,figsize=(14,4))
col = ax.pcolormesh(distance_km,cloud_height_km,storm_zvals.T,
                   cmap = cmap_ref, norm=the_norm)
ax.set(ylim=[0,17],xlabel = "distance (km)",ylabel="height (km)",
       title = f"radar reflectivity (dbZ) on {day}, granule {radar_ds.granule_id}")
fig.colorbar(col,extend='both',ax=ax);
```

+++ {"user_expressions": []}

## Step 2: Compare cloudsat and the ECMWF model

The `ECMWF-AUX` file holds the model data from the European Centre for Medium Range Forecasting, interpolated
to the cloudsat radar grid.  Below we read the temperature field and convert to centigrade.  We also clip
it to the storm time values.

```{code-cell} ipython3
ecmwf_file=(a301_lib.data_share / 'pha/cloudsat').glob('20080820*ECMWF-AUX*_GRANULE_*.hdf')
ecmwf_file = list(ecmwf_file)[0]
temperature_ds = read_cloudsat_var('Temperature',ecmwf_file)
temperature = temperature_ds['Temperature'][time_hit,:]
temperature = temperature - 273.15
temperature
```

+++ {"user_expressions": []}

### Plot the temperature

The palette we'll use goes through white at zero, which makes it easy to see the isotherm.
This is called a "diverging palette"

```{code-cell} ipython3
vmin=-30
vmax=30
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
#
# use a seaborn palette with blue-green colors
#
cmap_ec=sns.diverging_palette(261, 153,sep=6, s=85, l=66,as_cmap=True)
cmap_ec.set_over('w')
cmap_ec.set_under('b',alpha=0.2)
cmap_ec.set_bad('0.75') #75% grey
fig2, ax2 = plt.subplots(1,1,figsize=(14,4))
height_km=temperature.coords['height']/meters2km
distance_km = temperature.coords['distance_km'] 
distance_km = distance_km - distance_km[0]
col = ax2.pcolormesh(distance_km,cloud_height_km,temperature.T,
                   cmap = cmap_ec, norm=the_norm)
fig2.colorbar(col,extend='both',ax=ax2);
ax2.set(ylim=[0,10],xlim=(0,1200),
       xlabel='distance (km)',ylabel='height (km)',
       title="ECMWF temperture (deg C)")
```

+++ {"user_expressions": []}

## Find the 0 degree isotherm

A trick to find the index where the temperature changes sign is to take the absolute value of the temperature
then find the index of the minimum value, which will be zero.  We need to use the numpy nanargmin function for this
since the model temperature field has nan values above 10 km

```{code-cell} ipython3
#
#  find the vertical index where the ECMWF temperature field is closest to zero
#  we want to draw a line on the radar reflectivity at this height
#
abs_temps=np.abs(temperature.data)
abs_temps.shape
index_vals=np.nanargmin(abs_temps,axis=1)
height_vec=[height_km.data[index] for index in index_vals]
```

+++ {"user_expressions": []}

### Redraw figure 1 with the isotherm

It looks like the model and the radar agree on the freezing level for this storm

+++

ax.plot(distance_km,height_vec,'r')
display(fig)
