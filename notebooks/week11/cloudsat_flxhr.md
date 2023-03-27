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

# Cloudsat heating rate

```{code-cell} ipython3
import a301_lib
from sat_lib.cloudsat import read_cloudsat_var
from pathlib import Path
import xarray
import datetime as dt
import pandas as pd
import numpy as np
from sat_lib.cloudsat import add_storm_distance
from sat_lib.utils.plotting import make_cmap
from matplotlib import pyplot as plt
from matplotlib import cm
```

```{code-cell} ipython3
cloudsat_dir = a301_lib.data_share / "pha/cloudsat"
flxhr_file = list(cloudsat_dir.glob("*2008*FLXHR*hdf"))[0]
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

```{code-cell} ipython3
qr_slice = add_storm_distance(qr_slice)
```

+++ {"tags": [], "user_expressions": []}

## Plot the longwave heating rate

```{code-cell} ipython3
lw_heating = qr_slice['QR'][1,:,:]
fig, ax = plt.subplots(1,1,figsize=(14,4))
the_norm, cmap  = make_cmap(-4,4, cmap = cm.coolwarm)
lw_heating.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax, cmap = cmap, norm = the_norm)
ax.set(ylim=(0,17),title="longwave heating rate (K/day)");
```

+++ {"tags": [], "user_expressions": []}

## Plot the shortwave heating rate

```{code-cell} ipython3
sw_heating = qr_slice['QR'][0,:,:]
fig, ax = plt.subplots(1,1,figsize=(14,4))
the_norm, cmap  = make_cmap(-4,4, cmap = cm.coolwarm)
sw_heating.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax, cmap = cmap, norm = the_norm)
ax.set(ylim=(0,17),title="shortwave heating rate (K/day)");
```
