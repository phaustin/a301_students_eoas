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

(week9:temperature_perturb)=
# Plotting ECMWF temperature and wind speed

In this notebook we extend the {ref}`week9:cloudsat_ecmwf` notebook by plotting the temperature perturbation and wind speed
to see if we can spot the effect of the storm.


+++ {"tags": [], "user_expressions": []}

## Step 1: Read in the week 9 reflectivity and temperature

```{code-cell} ipython3
import numpy as np
import datetime as dt
from datetime import timezone as tz
from matplotlib import pyplot as plt
import a301_lib
from sat_lib.cloudsat import read_cloudsat_var
import seaborn as sns
import xarray as xr
```

```{code-cell} ipython3
infile_zvals = a301_lib.data_share / "pha/cloudsat/storm_zvals.nc"
storm_zvals = xr.open_dataset(infile_zvals)
infile_temp = a301_lib.data_share / "pha/cloudsat/temperature.nc"
temperature = xr.open_dataset(infile_temp)
```

```{code-cell} ipython3
temperature
```

+++ {"tags": [], "user_expressions": []}

### Write a new function to add the "storm distance" as a coordinate

We're going to want to make several plots with the distance from the start of the storm as the x coordinate.  
In this case, we've already clipped the dataset to the storm start.  For new dataset, we'd like to
avoid having to make a new storm time axis every time we make a plot.

We can put the calculation in a function that makes a new coordinate by subtracting
the starting distance from every time value, so the "storm_distance" starts at 0 km.

```{code-cell} ipython3
def add_storm_distance(the_ds):
    """Add a new coordinate called "storm_distance" to the dataset the_ds that is the distance in
       km from the start of the storm
       
       Parameters
       ----------
       
       the_ds: xarray dataset
          dataset with a coordinate named "distance_km"
          
       Returns
       -------
       
       the_ds: xarray dataset
          same dataset with a new coordinate "storm_distance"
    """
    storm_distance = the_ds.distance_km - the_ds.distance_km[0]
    the_ds = the_ds.assign_coords(coords={'storm_distance':('time',storm_distance.data)})
    return the_ds 

storm_zvals = add_storm_distance(storm_zvals)
```

```{code-cell} ipython3
storm_zvals
```

+++ {"tags": [], "user_expressions": []}

### Plotting using xarray.plot

Now that we've added the storm_distance coordinate, we can use it in the plotting command.
Compare this plot with the one we did in {ref}`week9:cloudsat_ecmwf` to see how this
simplifies the plot

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
fig, ax = plt.subplots(1,1,figsize=(14,4))
radar_z = storm_zvals['Radar_Reflectivity']
radar_z.T.plot.pcolormesh(x='storm_distance',y='height_km',
                   ax=ax,cmap = cmap_ref, norm=the_norm)
ax.set(ylim=[0,17],xlabel = "distance (km)",ylabel="height (km)",
       title = f"radar reflectivity (dbZ) on {storm_zvals.day}, granule {storm_zvals.granule_id}");
```

+++ {"user_expressions": []}

## Plot the temperature perturbation


In the {ref}`week9:cloudsat_ecmwf` we found the 0 degree isotherm from the model temperature field.  To see
whether the storm is affecting the temperature of the environment, we need to subtract the time-averaged mean
temperature to get the perturbation.  To find that average, just give the mean function the dimension
you want to averge over:

```{code-cell} ipython3
temp_profile=temperature.mean(dim='time')
temp_perturb = temperature - temp_profile
temp_perturb = add_storm_distance(temp_perturb)
```

```{code-cell} ipython3
vmin=-2
vmax=2
cmap = copy.copy(cm.coolwarm)
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
fig2, ax2 = plt.subplots(1,1,figsize=(14,4))
col = temp_perturb['Temperature'].T.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax2, cmap = cmap, norm=the_norm)
ax2.set(ylim = [0,17], xlabel = "distance (km)", ylabel = "height (km)",
         title = f"temperature perturbation (K) on {storm_zvals.day}, granule {storm_zvals.granule_id}");
```

+++ {"tags": [], "user_expressions": []}

Comparing the radar plot and the region of warmer temperatures, it look like the model has the storm about 300 km to the
right of the radar location

+++ {"tags": [], "user_expressions": []}

## Plot the wind speed

To see the wind speed for this storm, we need to get the horizontal velocity components from the ECMWF hdf

```{code-cell} ipython3
ecmwf_file=(a301_lib.data_share / 'pha/cloudsat').glob('20080820*ECMWF-AUX*_GRANULE_*.hdf')
ecmwf_file = list(ecmwf_file)[0]
```

```{code-cell} ipython3
u_ds = read_cloudsat_var('U_velocity',ecmwf_file)
v_ds = read_cloudsat_var('V_velocity',ecmwf_file)
```

+++ {"tags": [], "user_expressions": []}

### Clip the orbit to the storm times

The velocity datasets cover the full orbit.  We need to clip them to the storm start and end 
times, which we can get from the temperture (or radar) datasets.

```{code-cell} ipython3
time_hit = np.logical_and(u_ds.time >= temperature.time[0],u_ds.time <= temperature.time[-1])
```

```{code-cell} ipython3
uvel = u_ds['U_velocity'][time_hit,:]
vvel = v_ds['V_velocity'][time_hit,:]
```

+++ {"tags": [], "user_expressions": []}

### Add the storm distance

```{code-cell} ipython3
uvel = add_storm_distance(uvel)
vvel = add_storm_distance(vvel)
```

+++ {"tags": [], "user_expressions": []}

### Find the wind speed

```{code-cell} ipython3
wind_speed = np.sqrt(uvel**2. + vvel**2.)
wind_speed
```

+++ {"tags": [], "user_expressions": []}

### make the plot

Not too dramatic for this storm

```{code-cell} ipython3
vmin=0
vmax=15
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
#
# use a seaborn palette with blue-green colors
#
fig3, ax3 = plt.subplots(1,1,figsize=(14,4))
col = wind_speed.T.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax3, norm=the_norm,
                                  cbar_kwargs={"label":"wind speed (m/s)"})
ax3.set(ylim=[0,17],
       xlabel='distance (km)',ylabel='height (km)',
       title=f"ECMWF wind speed (m/s) for granule {u_ds.granule_id} on {u_ds.day}");
```
