---
anaconda-cloud: {}
jupytext:
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"tags": [], "user_expressions": []}

(week10:radar_micro)=
# Cloudsat: liquid and ice precipitation and rain rate

It's useful to be able to combine multiple datasets into a single netcdf file to build a case study that makes it easy to track a data analysis.  In this notebook we'll do this for the Texas storm we've been looking at.
Below we combine the temperature perturbatio and reflectivity dataset from {ref}`week10:temperature_perturb` with
new radar cloud variables (surface rain rate and ice and liquid water concentrations) taken from the 2C-RAIN-PROFILE hdffile. 

New concepts: 

1) clipping all data arrays in a dataset to the same time slice using [xarray.isel](https://docs.xarray.dev/en/stable/generated/xarray.Dataset.isel.html)

2) dealing with coordinate differences when combining different datasets

```{code-cell} ipython3
import numpy as np
import datetime as dt
from datetime import timezone as tz
from matplotlib import pyplot as plt
import a301_lib
from sat_lib.cloudsat import read_cloudsat_var
import seaborn as sns
import xarray as xr
from sat_lib.cloudsat import add_storm_distance
```

+++ {"tags": [], "user_expressions": []}

## Read in the dataArrays

+++ {"tags": [], "user_expressions": []}

### Read in the storm we saved in week9

I've added an output cell at the bottom of  {ref}`week10:temperature_perturb` to produce the `week10_wind_temps.nc` file.  You'll need to 
rerun that notebook so we can read in the temperature perturbation data from Monday.

```{code-cell} ipython3
#
# we'll need  the storm reflectivities and temperatures we created the `temp_perturbation` notebook
#
infile_zvals = a301_lib.data_share / "pha/cloudsat/storm_zvals.nc"
storm_zvals = xr.open_dataset(infile_zvals)
infile_temp = a301_lib.data_share / "pha/cloudsat/week10_wind_temps.nc"
temp_ds = xr.open_dataset(infile_temp)
```

+++ {"tags": [], "user_expressions": []}

### Read in the radar rain rate, precipitation ice and liquid water content and the cloud liquid water

Since reflectivity goes as $D^6$, cloudsast gets a much stronger signal from 1000 micron rain drops than
10 micron cloud drops.

```{code-cell} ipython3
radar_dir = a301_lib.data_share / "pha/cloudsat"
rain_file = list(radar_dir.glob("20080820*RAIN*hdf"))[0].resolve()
print(f"{rain_file=}")
rain_ds = read_cloudsat_var('rain_rate',rain_file)
liquid_ds = read_cloudsat_var('precip_liquid_water',rain_file)
ice_ds = read_cloudsat_var('precip_ice_water',rain_file)
cloud_ds = read_cloudsat_var('cloud_liquid_water',rain_file)
#
# we'll need  the storm reflectivities and temperatures we created the `temp_perturbation` notebook
#
infile_zvals = a301_lib.data_share / "pha/cloudsat/storm_zvals.nc"
storm_zvals = xr.open_dataset(infile_zvals)
infile_temp = a301_lib.data_share / "pha/cloudsat/week10_wind_temps.nc"
temp_ds = xr.open_dataset(infile_temp)
```

```{code-cell} ipython3
cloud_ds
```

+++ {"tags": [], "user_expressions": []}

## add the new RΑΙΝ cloud variables to the rain_ds rainrate dataset

Since all the variables from the 2C-RAIN file are on the same time and height axes, we can merge them together with
a simple copy

```{code-cell} ipython3
rain_ds['precip_liquid_water'] = liquid_ds['precip_liquid_water']
rain_ds['precip_ice_water'] = ice_ds['precip_ice_water']
rain_ds['cloud_liquid_water'] = cloud_ds['cloud_liquid_water']
rain_ds
```

+++ {"tags": [], "user_expressions": []}

## Clip to the storm times using an xarray indexer

The [xarray.sel](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.sel.html) gives a 1-step way
to clip every dataArray in a dataset.  First decall how we clipped to the storm start and end using indexing in the {ref}`week9:cloudsat_ecmwf` notebook:


```python
#
# find the storm times
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

That's a lot of repetitive work to subset the data.  Below we write a couple of helper functions
to automate this using tthe [xarray.sel](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.sel.html) method.

+++ {"tags": [], "user_expressions": []}

We can do this in three steps

1) Get the start and end times from the `storm_zvals` dataset that's already been clipped, and  get the full orbit
   times from the rain_ds dataset

2) construct a logical vector which is true during the storm, and false otherwise

3) slice the storm using the logical vector and the [xarray.isel](https://docs.xarray.dev/en/stable/generated/xarray.Dataset.isel.html)

This will slice every varible in the dataset that has a time dimension.  The resulting arrays will all have 1125 time values for their
first coordinate

```{code-cell} ipython3
#
# start and end times for the storm 
#
start_time = storm_zvals.time[0]
end_time = storm_zvals.time[-1]
#
#  all orbit times from rain_ds
#
all_times = rain_ds.time
#
# create  the new dataset storm_slice using the isel methond
#
time_hit = np.logical_and(all_times >= start_time, all_times <= end_time)
storm_slice = rain_ds.isel(indexers = {'time':time_hit})
storm_slice
```

+++ {"tags": [], "user_expressions": []}

## Problem: make the two height dimensions agree

We want to add the radar reflectivity and temperature to the `storm_slice` dataset, but there's a problem,
the heights differ by about 18-20 meters at each level.  It's not clear why the level 2C (RAIN)
and 2B (GEOPROF) files have this difference (perhaps the difference between bin centers and bin edges), 
In the same way, the heights, taken from `temp_ds` differ from `rain_ds` by about -19 meters.
It's not crucial to the analysis, so we'll 
just overwrite the storm_zvals height dimension to force them to be equal.  If the difference was important,
I'd either have to interpolate the arrays onto a common grid, or maintain two separate height dimensions, at
the cost of not being able to subtract/add the arrays.

+++ {"tags": [], "user_expressions": []}

### The two radar field heights differ from each other by about 18 meters

```{code-cell} ipython3
#
# heights differ by 18 meters
#
np.array(storm_slice.height) - np.array(storm_zvals.height)
```

+++ {"tags": [], "user_expressions": []}

### The model heights differ from the radar by about 19 meters

```{code-cell} ipython3
np.array(rain_ds.height) - np.array(temp_ds.height)
```

+++ {"tags": [], "user_expressions": []}

## Question -- In the cell below plot a slice along the time axis ([:,100]) for rain_ds.full_heights at height index 100

How much variation in there in the radar height from timestep to timestep?

+++ {"tags": [], "user_expressions": []}

### Brute force solution -- give every dataset the same height vector

Again, since 20 meters isn't much of a difference, force agreement by overwriting the coordinate

```{code-cell} ipython3
#
# overwrite storm_zvals heights with the ones from storm_slice
#
storm_zvals = storm_zvals.assign_coords(coords={'height':('height',storm_slice.height.data)})
temp_ds = temp_ds.assign_coords(coords={'height':('height',storm_slice.height.data)})
```

```{code-cell} ipython3
#
# fixed
#
np.array(storm_slice.height) - np.array(storm_zvals.height)
```

+++ {"tags": [], "user_expressions": []}

Now that they have the same coordinates, we can add the radar reflectivity and temperature perturbation to the storm_slice dataset

```{code-cell} ipython3
#
# add the Radar_Reflectivity to the slice
# 
storm_slice['Radar_Reflectivity'] = storm_zvals['Radar_Reflectivity']
storm_slice['Temperature'] = temp_ds['Temperature']
storm_slice
```

+++ {"tags": [], "user_expressions": []}

### add the storm distance coordinate

As in {ref}`week10:temperature_perturb` we want to plot along storm distance, so add that coordinate to `storm_slice`

```{code-cell} ipython3
storm_slice = add_storm_distance(storm_slice)
temp_ds = add_storm_distance(temp_ds)
storm_slice.storm_distance
```

+++ {"tags": [], "user_expressions": []}

## Make some plots

Now that we have all the data in one place, see how the various radar fields compare with the model temperatures

### Radar Reflectivity

Replot the reflectivity to get the storm structure.  We use a palette that shows the difference between missing data (red) and very low values (blue).
We'll be looking below to see whether what the structure of the precipitation is inside the storm.

Make a convenience function to return the colormap with normalization

```{code-cell} ipython3
import copy
from matplotlib import cm
from matplotlib.colors import Normalize
def make_cmap(vmin, vmax, cmap = cm.viridis):
    the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
    cmap=copy.copy(cmap)
    cmap.set_over('w')
    cmap.set_under('b')
    cmap.set_bad('r') # grey
    return the_norm, cmap
```

```{code-cell} ipython3
vmin=-25
vmax=20
the_norm, cmap_ref = make_cmap(vmin, vmax)
fig, ax = plt.subplots(1,1,figsize=(14,4))
radar_z = storm_slice['Radar_Reflectivity']
radar_z.T.plot.pcolormesh(x='storm_distance',y='height_km',
                   ax=ax,cmap = cmap_ref, norm=the_norm)
ax.set(ylim=[0,17],xlabel = "distance (km)",ylabel="height (km)",
       title = f"radar reflectivity (dbZ) on {storm_zvals.day}, granule {storm_zvals.granule_id}");
```

+++ {"tags": [], "user_expressions": []}

### Model Temperature

```{code-cell} ipython3
vmin=-2
vmax=2
the_norm, cmap = make_cmap(vmin, vmax,cmap = cm.coolwarm)
fig2, ax2 = plt.subplots(1,1,figsize=(14,4))
col = storm_slice['Temperature'].T.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax2, cmap = cmap, norm=the_norm)
ax2.set(ylim = [0,17], xlabel = "distance (km)", ylabel = "height (km)",
         title = f"model temperature perturbation (K) on {storm_zvals.day}, granule {storm_zvals.granule_id}");
```

+++ {"tags": [], "user_expressions": []}

### Radar Rain rate


Note some problems with the radar rainrates -- those
negative values are definitely unphysical.  The record for heaviest 1 hour rainfall is 30 cm, so 6 cm/hour is  definitely possible for a large storm.
The precipitation spikes line up with the highest reflectivity regions of the radar image.

```{code-cell} ipython3
rain_rate = storm_slice['rain_rate']
fig1, ax1 = plt.subplots(1,1,figsize=(11,4))
rain_rate.plot(x="storm_distance", ax=ax1)
ax1.set_title(f'rain rate (mm/hour)  on {storm_zvals.day}, granule {storm_zvals.granule_id}');
```

+++ {"tags": [], "user_expressions": []}

### Radar Liquid water precipitation


The model carries cloud water (droplets too small to precipitate) and liquid precipitation (falling rain drops). If you
compare the figure below with the temperature pertubation plot it looks like the 
the cool perturbations may be lining up with  evaporating precipitation below the freezing level.

The red bands are missing data where the radar algorithm couldn't infer a precipitation content.  That makes the
spike at 450 km a little suspect.

```{code-cell} ipython3
vmin=0
vmax=0.4
the_norm, cmap_ref = make_cmap(vmin, vmax)
fig, ax = plt.subplots(1,1,figsize=(14,4))
liquid_precip = storm_slice['precip_liquid_water']
liquid_precip.T.plot.pcolormesh(x='storm_distance',y='height_km',
                   ax=ax,cmap = cmap_ref, norm=the_norm)
ax.set(ylim=[0,10],xlabel = "distance (km)",ylabel="height (km)",
       title = f"liquid water precip (g/m^3) on {storm_zvals.day}, granule {storm_zvals.granule_id}");
```

+++ {"tags": [], "user_expressions": []}

In the two cells below, the radar is showing ice in the convective updrafts above the freezing level
and cloud water down to the ground.  Inside the cloud itself, it can only see the larger precipitation drops.

```{code-cell} ipython3
vmin=0
vmax=0.4
the_norm, cmap_ref = make_cmap(vmin, vmax)
fig, ax = plt.subplots(1,1,figsize=(14,4))
ice_precip = storm_slice['precip_ice_water']
ice_precip.T.plot.pcolormesh(x='storm_distance',y='height_km',
                   ax=ax,cmap = cmap_ref, norm=the_norm)
ax.set(ylim=[0,10],xlabel = "distance (km)",ylabel="height (km)",
       title = f"Radar ice water precip (g/m^3) on {storm_zvals.day}, granule {storm_zvals.granule_id}");
```

```{code-cell} ipython3
vmin=0
vmax=0.05
the_norm, cmap_ref = make_cmap(vmin, vmax)
fig, ax = plt.subplots(1,1,figsize=(14,4))
ice_precip = storm_slice['cloud_liquid_water']
ice_precip.T.plot.pcolormesh(x='storm_distance',y='height_km',
                   ax=ax,cmap = cmap_ref, norm=the_norm)
ax.set(ylim=[0,10],xlabel = "distance (km)",ylabel="height (km)",
       title = f"Radar cloud_liquid_water (g/m^3) on {storm_zvals.day}, granule {storm_zvals.granule_id}");
```

+++ {"tags": [], "user_expressions": []}

## save the file to disk

```{code-cell} ipython3
do_write = False
if do_write:
    outfile = a301_lib.data_share / "pha/cloudsat/week10_cloudsat_case_study.nc"
    storm_slice.to_netcdf(outfile)
```

+++ {"tags": [], "user_expressions": []}

## Summary

+++ {"tags": [], "user_expressions": []}

In general, the precipitation structure looks reasonable, and evaporating precipitation may be driving the cooling
perturbations in the model.  Some next steps:

1) add the surface temperature and 10 meter wind fields

2) add the rain rate uncertainty to see how confident the algorithm is in the spike values
