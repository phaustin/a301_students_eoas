---
anaconda-cloud: {}
jupytext:
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(cloudsat-reflec)=
# Working with cloudsat data

This notebook shows how to read in the reflectivity, convert it to dbZe (dbZ equivalent,
which means the dbZ that the measured reflectivity would have it the cloud was made
of liquid water drops).

In the second part of the notebook, I compare the 0 deg C isotherm from the ECMWF forecast
model for the scene with the radar bright band, and show that the model tracks the
observed brightband height.

+++

## Plot the radar reflectivity

+++

### Read in the height and reflectivity fields

```{code-cell} ipython3
import h5py
import numpy as np
import datetime as dt
from datetime import timezone as tz
from matplotlib import pyplot as plt
import pyproj
from numpy import ma
import a301_lib
from sat_lib.cloudsat import get_geo
import seaborn as sns

z_file=(a301_lib.sat_data / 'cloudsat').glob('20080820*CS_2B-GEOPROF_GRANULE_*.h5')
z_file = list(z_file)[0]
meters2km=1.e3

lats,lons,date_times,prof_times,dem_elevation=get_geo(z_file)
    
with h5py.File(z_file,'r') as zin:
    zvals=zin['2B-GEOPROF']['Data Fields']['Radar_Reflectivity'][...]
    factor=zin['2B-GEOPROF']['Data Fields']['Radar_Reflectivity'].attrs['factor']
    missing=zin['2B-GEOPROF']['Data Fields']['Radar_Reflectivity'].attrs['missing']
    height=zin['2B-GEOPROF']['Geolocation Fields']['Height'][...]
```

#### 2. Make a masked array of the reflectivity so that pcolormesh will plot it

note that I need to find the missing data before I divide by factor=100 to
convert from int16 to float

```{code-cell} ipython3
hit=(zvals == missing)
zvals = zvals/factor
zvals[hit]=np.nan
zvals=ma.masked_invalid(zvals)
```

#### 3. Find the part of the orbing that corresponds to the 3 minutes containing the storm

You need to enter the start_hour and start_minute for the start time of your cyclone in the granule

```{code-cell} ipython3
first_time=date_times[0]
print('orbit start: {}'.format(first_time))
start_hour=6
start_minute=45
storm_start=starttime=dt.datetime(first_time.year,first_time.month,first_time.day,
                                        start_hour,start_minute,0,tzinfo=tz.utc)
#
# get 3 minutes of data from the storm_start
#
storm_stop=storm_start + dt.timedelta(minutes=3)
print('storm start: {}'.format(storm_start))
time_hit = np.logical_and(date_times > storm_start,date_times < storm_stop)
storm_lats = lats[time_hit]
storm_lons=lons[time_hit]
storm_prof_times=prof_times[time_hit]
storm_zvals=zvals[time_hit,:]
storm_height=height[time_hit,:]
storm_date_times=date_times[time_hit]
len(date_times)
```

#### 4. convert time to distance by using pyproj to get the greatcircle distance between shots

```{code-cell} ipython3
great_circle=pyproj.Geod(ellps='WGS84')
distance=[0]
start=(storm_lons[0],storm_lats[0])
for index in np.arange(1,len(storm_lons)):
    azi12,azi21,step= great_circle.inv(storm_lons[index-1],storm_lats[index-1],
                                       storm_lons[index],storm_lats[index])
    distance.append(distance[index-1] + step)
distance=np.array(distance)/meters2km
```

#### 5. Make the plot assuming that height is the same for every shot

i.e. assume that height[0,:] = height[1,:] = ...

in reality, the bin heights are depend on the details of the radar returns, so
we would need to historgram the heights into a uniform set of bins -- ignore that for this qualitative picture

```{code-cell} ipython3
import copy
fig,ax=plt.subplots(1,1,figsize=(40,4))

from matplotlib import cm
from matplotlib.colors import Normalize
vmin=-30
vmax=20
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
cmap_ref=copy.copy(cm.jet)
cmap_ref.set_over('w')
cmap_ref.set_under('b',alpha=0.2)
cmap_ref.set_bad('0.75') #75% grey
#
#
def plot_field(distance,height,field,ax,cmap=None,norm=None):
    if cmap is None:
        cmap=cm.jet
    col=ax.pcolormesh(distance,height,field,cmap=cmap,
                  norm=the_norm)
    fig.colorbar(col,extend='both',ax=ax)
    return ax

cloud_height_km=height[0,:]/meters2km
ax=plot_field(distance,cloud_height_km,storm_zvals.T,ax,cmap=cmap_ref,
              norm=the_norm)
ax.set(ylim=[0,17],xlim=(0,1200))
ax.set(xlabel='distance (km)',ylabel='height (km)')
fig.savefig('cloudsat.png')    
```

## Compare cloudsat and the ECMWF model

```{code-cell} ipython3
ecmwf_file=(a301_lib.sat_data / 'cloudsat').glob('20080820*ECMWF-AUX*_GRANULE_*.h5')
ecmwf= list(ecmwf_file)[0]
with h5py.File(ecmwf,'r') as ecmwf_in:
    tup_heights=ecmwf_in['ECMWF-AUX']['Geolocation Fields']['EC_height'][...]
    temps=ecmwf_in['ECMWF-AUX']['Data Fields']['Temperature'][...]
    missing=ecmwf_in['ECMWF-AUX']['Data Fields']['Temperature'].attrs['missing']
ec_heights=np.array([item[0] for item in tup_heights])
bad_temps = (temps == missing)
temps[bad_temps]=np.nan
temps=np.ma.masked_invalid(temps)
temps = temps - 273.15
temps=temps[time_hit,:]
```

```{code-cell} ipython3
plt.close('all')
fig, ax =plt.subplots(1,1,figsize=(40,4))
vmin=-30
vmax=30
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
cmap_ec=sns.diverging_palette(261, 153,sep=6, s=85, l=66,as_cmap=True)
cmap_ec.set_over('w')
cmap_ec.set_under('b',alpha=0.2)
cmap_ec.set_bad('0.75') #75% grey

height_km=ec_heights/meters2km
ax=plot_field(distance,height_km,temps.T,ax,cmap=cmap_ec,
                  norm=the_norm)
ax.set(ylim=[0,10],xlim=(0,1200))
ax.set(xlabel='distance (km)',ylabel='height (km)')
fig.savefig('temps.png')
```

```{code-cell} ipython3
#
#
#  find the vertical index where the ECMWF temperature field is closest to zero
#  we want to draw a line on the radar reflectivity at this height
#
abs_temps=np.abs(temps)
argmin=np.argmin(abs_temps,axis=1)
height_vec=[height_km[index] for index in argmin]
```

```{code-cell} ipython3
fig, (ax1,ax2) =plt.subplots(2,1,figsize=(40,8))
ax1=plot_field(distance,cloud_height_km,storm_zvals.T,ax1,cmap_ref)
ax2=plot_field(distance,cloud_height_km,storm_zvals.T,ax2,cmap_ref)
ax2.plot(distance,height_vec,'ro')
#
# we can loop over axes to set limits, labels
#
[ax.set(xlim=(0,1200),ylim=(0,17),xlabel='distance (km)',
        ylabel='height (km)') for ax in [ax1,ax2]]
fig.savefig('cloudsat_heights.png',dpi=200)
```
