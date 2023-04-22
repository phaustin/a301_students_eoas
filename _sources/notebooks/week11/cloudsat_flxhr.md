---
jupytext:
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

(week11:cloudsat_heat)=
# Cloudsat heating rate

Cloudsat uses radiation models plus the radar and Modis data to estimate the long and shortwave fluxes at each
radar height level.  The the datasets are called [2B-FLXHR](https://www.cloudsat.cira.colostate.edu/data-products/2b-flxhr)
and [2B-FLXHR-LIDAR](https://www.cloudsat.cira.colostate.edu/data-products/2b-flxhr-lidar) and the heating rate
variable `QR` (K/day) is returned as a 3 dimensional array of shape `[2,time,height]`, with `[0,time,height]` holding
the longwave heating rates and `[1,time,height]` holding the sortwave heating rates.

In this notebook we look at the longwave, shortwave and net=longwave + shortwave heating rates for the Texas storm.
The figures show that during the day, there is large cooling at cloudtop, with strong shortwave heating just below the
cooling layer and smaller warming through most of the atmosphere.  

Note that climate models need to estimate the heating rate with many fewer vertical levels (45 instead of 125) and much
coarser horizontal resolution (100 km/gridcell instead of 1 km/pixel)

```{code-cell} ipython3
import a301_lib
from sat_lib.cloudsat import read_cloudsat_var
from pathlib import Path
import xarray
import datetime as dt
import pandas as pd
import numpy as np
from sat_lib.cloudsat import add_storm_distance
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import copy
```

```{code-cell} ipython3
cloudsat_dir = a301_lib.data_share / "pha/cloudsat"
flxhr_file = list(cloudsat_dir.glob("*2008*FLXHR*hdf"))[0]
print(flxhr_file)
```

```{code-cell} ipython3
qr_ds = read_cloudsat_var('QR',flxhr_file)
```

+++ {"tags": [], "user_expressions": []}

## Clip to the storm

```{code-cell} ipython3
start_hour=6
start_minute=45
all_times=pd.to_datetime(qr_ds.time)
first_time = all_times[0]
storm_start=starttime=dt.datetime(first_time.year,first_time.month,first_time.day,
                                        start_hour,start_minute,0)
storm_stop=storm_start + dt.timedelta(minutes=3)
storm_start, storm_stop
```

```{code-cell} ipython3
time_hit = np.logical_and(all_times >= storm_start, all_times <= storm_stop)
qr_slice = qr_ds.isel(indexers = {'time':time_hit})
```

+++ {"tags": [], "user_expressions": []}

## Add storm distance

using the function we wrote last week

```{code-cell} ipython3
qr_slice = add_storm_distance(qr_slice)
```

+++ {"tags": [], "user_expressions": []}

## Set up the colormap

```{code-cell} ipython3
def make_cmap(vmin, vmax, cmap = cm.viridis,
              over = 'w',under='k',missing='0.4'):
    """
    return Normalization and colormap

    Parameters
    ----------

    vmin, vmax: float
       colormap max and min values
    cmap: cm.colormap
       optional, default - cm.viridis
    over,under,missing: str
       colors for data large, small, missing data
       defaults: over = 'w',under='k',missing='0.4'

    Returns
    -------

    the_norm:  Normalization for vmin and vmax
    cmap: colormap with over, under and missing 
    
    """
    the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
    cmap=copy.copy(cmap)
    cmap.set_over(over)
    cmap.set_under(under)
    cmap.set_bad(missing) # grey
    return the_norm, cmap
```

+++ {"tags": [], "user_expressions": []}

## Plot the longwave heating rate

```{code-cell} ipython3
lw_heating = qr_slice['QR'][1,:,:]
fig, ax = plt.subplots(1,1,figsize=(14,4))
the_norm, cmap  = make_cmap(-4,4, cmap = cm.coolwarm,under = 'c',missing='y')
lw_heating.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax, cmap = cmap, norm = the_norm)
ax.set(ylim=(0,17),title="longwave heating rate (K/day)");
```

+++ {"tags": [], "user_expressions": []}

## Plot the shortwave heating rate

```{code-cell} ipython3
sw_heating = qr_slice['QR'][0,:,:]
fig, ax = plt.subplots(1,1,figsize=(14,4))
the_norm, cmap  = make_cmap(-4,4, cmap = cm.coolwarm,under = 'c',missing='y')
sw_heating.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax, cmap = cmap, norm = the_norm)
ax.set(ylim=(0,17),title="shortwave heating rate (K/day)");
```

+++ {"tags": [], "user_expressions": []}

## Plot the net heating rate

```{code-cell} ipython3
net_heating = qr_slice['QR'][0,:,:] + qr_slice['QR'][1,:,:]
fig, ax = plt.subplots(1,1,figsize=(14,4))
the_norm, cmap  = make_cmap(-4,4, cmap = cm.coolwarm,under = 'c',missing='y')
net_heating.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax, cmap = cmap, norm = the_norm)
ax.set(ylim=(0,17),title="net heating rate (K/day)");
```
