---
jupytext:
  cell_metadata_filter: -all
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

(week9:cloudsat)=
# Reading cloudsat data

This notebook demonstrates how to read the radar reflectivity (GEOPROF-GRAΝULE) and the lidar layer top (GEOPROF-LIDAR-GRANULE)
from cloudsat files.  We create two plots below: one showing the orbit with the location of a thundercloud, and one
showing the reflectivity and cloudtop through the cloud transect.  

```{code-cell} ipython3
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sat_lib.cloudsat import read_cloudsat_var

import a301_lib
```

## Find the radar and lidar files

```{code-cell} ipython3
radar_dir = a301_lib.data_share / "pha/cloudsat"
radar_file = list(radar_dir.glob("2008291*2B-GEOPROF_GR*hdf"))[0].resolve()
print(f"{radar_file=}")
lidar_file = list(radar_dir.glob("2008291*2B-GEOPROF-LIDAR*GR*hdf"))[0].resolve()
print(f"{lidar_file=}")
```

## Read the radar reflectivity dataset

```{code-cell} ipython3
refl_ds = read_cloudsat_var('Radar_Reflectivity',radar_file)
refl_ds
```

## Get the radar reflectivity (dbZ)

Note the difference between the height coordinate (1 dimensional, length 125, height bins of the first pulse) and the full heights
of all pulses (the variable full height, which has shape (37082,15)

```{code-cell} ipython3
refl_array = refl_ds['Radar_Reflectivity']
dem_elevation = refl_ds['dem_elevation']
distance_km = refl_ds['distance_km']
longitude = refl_ds['longitude']
latitude = refl_ds['latitude']
height = refl_ds.coords['height']
```

## Get the lidar layer top height (highest cloud top, in meters)

```{code-cell} ipython3
lidar_ds = read_cloudsat_var('LayerTop',lidar_file)
lidar_ds
```

```{code-cell} ipython3
layer_top = lidar_ds['LayerTop']
```

## Plot the orbit, with the location of a thunderstorm 

```{code-cell} ipython3
import cartopy.crs as ccrs
start=21500  #seconds in orbit --this is storm starting point
stop=22000
projection=ccrs.Robinson()
transform = ccrs.Geodetic()
fig, ax = plt.subplots(1,1,figsize=(15,8), subplot_kw = {'projection': projection})
# make the map global rather than have it zoom in to
# the extents of any plotted data
ax.set_global()
ax.stock_img()
ax.coastlines()
ax.plot(longitude,latitude,'r',lw=5,transform =  transform);
ax.plot(longitude[0],latitude[0],'go',markersize=20, transform=transform)
ax.plot(longitude[-1],latitude[-1],'ro',markersize=20, transform=transform)
ax.plot(longitude[start:stop],latitude[start:stop],"k-",lw=8,transform=transform);
```

## Plot the radar reflectivity and the cloud top height

We need to transfrom from Geodetic (lon/lat) to Robinson (the cartopy map projection) each time
we plot lon/lat values

```{code-cell} ipython3
from matplotlib.colors import Normalize
from copy import copy
fig, axis1 =plt.subplots(1,1,figsize=(14,4))
meters2km = 1.e-3
storm_distance = distance_km[start:stop]
storm_distance = storm_distance - storm_distance[0]
vmin=-6
vmax=4
pal = copy(plt.get_cmap("viridis"))
pal.set_bad("0.2")  # 75% grey for out-of-map cells
pal.set_under("0.75")
pal.set_over("r")  # color cells > vmax red
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
im=axis1.pcolor(storm_distance,height*meters2km,refl_array[start:stop,:].T,
                norm=the_norm)
axis1.set_xlabel('storm distance (km)')
axis1.set_ylim([0,15])
axis1.set_ylabel('height (km)')
cb=fig.colorbar(im,ax=axis1)
cb.set_label('reflectivity (dbZ)')

axis1.plot(storm_distance,layer_top[start:stop]*meters2km,'r',lw=3)
axis1.set_title("radar reflectivity and lidar cloud top (red line)");
```
