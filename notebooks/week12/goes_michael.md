---
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

(week12:goes_review)=
# GIS image processing review

In this notebook we go over the steps needed to

1) Download a GOES image as an xarray dataset
2) Clip the image to isolate [Hurricane Michael on October 9, 2018](https://www.jpl.nasa.gov/images/pia22753-nasas-cloudsat-passes-over-hurricane-michael)
3) Regrid the clipped image from a geostationary coordinate reference to UTΜ Ζone 16N
4) Plot the cloudsat orbit on top of the image with cartopy
6) Add a pair of study questions

+++ {"tags": [], "user_expressions": []}

## Step 1 read in the GOES and Cloudsat files

```{code-cell} ipython3
from goes2go.data import goes_nearesttime
import rioxarray
import xarray
import a301_lib
from datetime import datetime, timedelta
from pathlib import Path
import cartopy
from pyresample.utils.cartopy import Projection
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path
from sat_lib.cloudsat import read_cloudsat_var
```

+++ {"tags": [], "user_expressions": []}

### Read in cloudsat lats and lons

Save the latitude and longitude for the orbit plot

```{code-cell} ipython3
:tags: []

cloudsat_dir = a301_lib.data_share / "pha/cloudsat"
rain_file = list(cloudsat_dir.glob("*2018*RAIN*hdf"))[0]
rain_ds = read_cloudsat_var('rain_rate',rain_file)
cloudsat_lons = rain_ds['longitude']
cloudsat_lats = rain_ds['latitude']
```

+++ {"tags": [], "user_expressions": []}

### Read in the GOES ConUS cloud moisture product for October 9, 2018, 19:13 UCT

```{code-cell} ipython3
g = goes_nearesttime(
    datetime(2018, 10, 9, 19, 13), satellite="goes16",product="ABI-L2-MCMIP", domain='C', 
      return_as="xarray"
)
```

+++ {"tags": [], "user_expressions": []}

By default the files are written into a folder called `~/data`

```{code-cell} ipython3
full_path = Path.home() / "data" / g.path[0]
full_path
```

+++ {"tags": [], "user_expressions": []}

### Open the GOES nc file with rioxarray

Squeeze out the band dimension, since every variable has just 1 band

```{code-cell} ipython3
rioC = rioxarray.open_rasterio(full_path,'r',mask_and_scale = True)
rioC = rioC.squeeze()
rioC
```

+++ {"tags": [], "user_expressions": []}

## Make the cartopy crs projection

This uses the `pyresample.utils.cartopy.Projection` helper function introduced in week8 to
add the image extent in crs.  We also print out the crs in well-known-text
format.  Note that it's "unnamed" which means that it doesn't have a standard
[espsg](https://epsg.io/) code.  Below we'll regrid into a better known
universal transferse mercator crs using rioxarray.reproject

```{code-cell} ipython3
ll_x, ll_y, ur_x, ur_y = rioC.rio.bounds()
original_extent = (ll_x,ur_x, ll_y, ur_y)
cartopy_crs = Projection(rioC.rio.crs, bounds=original_extent)
cartopy_crs
```

```{code-cell} ipython3
:tags: []

cartopy_crs.to_wkt()
```

+++ {"tags": [], "user_expressions": []}

## Get the pixel size from the transform

Note the pixel size:  2004 meters x 2004 meters

```{code-cell} ipython3
:tags: []

rioC.rio.transform()
```

+++ {"tags": [], "user_expressions": []}

## Cloud top temperature: band 13 (10.3 $\mu m$) 

The thick clouds are radiating as blackbodies, and there isn't much vapor above the cloud
top, so this is a good estimate of cloud top temperature.

```{code-cell} ipython3
:tags: []

rioC["CMI_C13"].plot.imshow(cmap=cm.Greys);
```

+++ {"user_expressions": []}

## Clip the image to the hurricane

From the band 13 plot it looks like, in x,y coordinates, the
hurricane is between 2.4e6 -> 3.e6 meters in the y dimension
and -1.5e6 -> -0.5e6 meters in the x dimension.

Use that to slice the dataset using isel

```{code-cell} ipython3
:tags: []

hit_x = np.logical_and(rioC.x > -1.5e6, rioC.x < -0.5e6)
hit_y = np.logical_and(rioC.y > 2.4e6, rioC.y < 3.0e6)
slice_michael = rioC.isel(indexers={'x':hit_x,'y':hit_y})
slice_michael.dims
```

+++ {"tags": [], "user_expressions": []}

## Gamma correct band 1 (blue, 0.47 $\mu m$) and check the new slice

Here's a before and after plot of the slice showing the impact of the gamma correction.  The correction 
brightens the image at the expense of contrast.

```{code-cell} ipython3
:tags: []

fig1, ax1 = plt.subplots(1,1)
slice_michael['CMI_C01'].plot.imshow(cmap=cm.Greys_r,ax=ax1)
ax1.set(title = "michael: no gamma correction");
```

```{code-cell} ipython3
:tags: []

#
# stretch with gamma = 2.2
#
band1=slice_michael['CMI_C01'].data
band1 = np.clip(band1,0,1)
gamma=2.2
band1_stretch = np.power(band1,1/gamma)
slice_michael['CMI_C01'].data = band1_stretch
```

```{code-cell} ipython3
:tags: []

fig2, ax2 = plt.subplots(1,1)
slice_michael['CMI_C01'].plot.imshow(cmap = cm.Greys_r,ax = ax2)
ax2.set(title="michael with gamma correction");
```

```{code-cell} ipython3
#help(slice_michael.rio)
```

+++ {"tags": [], "user_expressions": []}

## Reproject from geostationary to UTM

The geostationary crs is a little unusual -- in some cases (to compare with landsat or other satellites, mapping)
we might want to reproject 
from that crs to something standard like universal transfer mercator.

`rioxarray.estimate_utm_crs()` gives  you its best guess, based on the image corners, about which UTM zone we're in.  It correctly
says that Michael is in [UTM zone 16N](https://epsg.io/32616)

```{code-cell} ipython3
:tags: []

utm_crs = slice_michael.rio.estimate_utm_crs()
utm_crs
```

+++ {"tags": [], "user_expressions": []}

## Reproject to UTM Zone 16N

Reprojecting is much simpler that the resampling of ungridded lons/lats we did for the Modis swaths in week 5.  `rioxarray.rio.reproject` does it in a single step

```{code-cell} ipython3
:tags: []

slice_utm16N = slice_michael.rio.reproject(utm_crs)
slice_utm16N.dims
```

+++ {"tags": [], "user_expressions": []}

Note that the reprojection has increased the pixel size to 2.3 km x 2.3 km and
changed  the array shape to from 'x': 499, 'y': 299 to 'x': 491, 'y': 317

As you'll see below, the clip we made of the GOES image isn't a perfect fit to 
the UTM grid box that is just big enough to contain it, so we need some extra
space on the left and right.

```{code-cell} ipython3
:tags: []

slice_utm16N.rio.transform()
```

+++ {"tags": [], "user_expressions": []}

### Mapping with the new projection

Once again we'll use the `pyresample.utils.cartopy.Projection()` method to
convert the rio crs to something that works with cartopy

```{code-cell} ipython3
:tags: []

ll_x, ll_y, ur_x, ur_y = slice_utm16N.rio.bounds()
original_extent = (ll_x,ur_x, ll_y, ur_y)
cartopy_crs = Projection(slice_utm16N.rio.crs, bounds=original_extent)
cartopy_crs
```

```{code-cell} ipython3
:tags: []

#set the figure size to match the rows/columns ration of 317/491
fig3, ax3  = plt.subplots(figsize=(12, 7.8), subplot_kw={"projection": cartopy_crs})
slice_utm16N['CMI_C01'].plot.imshow(
    extent= original_extent,
    transform=cartopy_crs,
    interpolation="nearest",
    cmap=cm.Greys_r
)
ax3.coastlines(resolution="50m", color="r", linewidth=2)
ax3.add_feature(ccrs.cartopy.feature.STATES)
ax3.set_title("Hurricane Michael, band 01 normalized reflectance")
```

+++ {"tags": [], "user_expressions": []}

## Add the Cloudsat ground track

Finally, we need to convert the Cloudsat geodetic lons/lats to x,y in UTM16N.  We can do this
with the `cartopy_crs.transform_points()` method.

```{code-cell} ipython3
:tags: []

geodetic = ccrs.Geodetic()
out = cartopy_crs.transform_points(geodetic,rain_ds['longitude'],rain_ds['latitude'])
x = out[:,0]
y = out[:,1]
```

```{code-cell} ipython3
:tags: []

help(cartopy.crs.PlateCarree)
```

```{code-cell} ipython3
:tags: []

#
# make a blue line and redisplay
#
ax3.plot(x,y,'b-',lw=3)
ax3.plot(x[0],y[0],'go',markersize=4)
display(fig3)
```

+++ {"tags": [], "user_expressions": []}

## Study questions

1) How could I use the affine transform to find the point at which cloudsat first enters the image, and denote it by a green dot?

2) How could I find the GOES band01 reflectance (or cloudtop temperature, etc.) directly below the cloudsat track?

Hint:  you'll need to use a `logical_and` on the x and y coordinates
