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

+++ {"user_expressions": []}

(week8:zoom_landsat)=
# Clipping and saving landsat scenes

In this notebook we read in the large (3660 x 3660 pixel) landsat band5 file we downloaded 
in the {ref}`week7:hls` notebook from week7.  That file is 14 Mbytes, and if we want a couple
dozen landsat scenes over the course of a decade, it would be good to reduce the file size
by a factor of 3-4 if possible.  One way to do that is to clip only that part of the scene
we're interested in, and write the clipped region out as a smaller geoiff.  That's what this notebook does, using the `rioxarray.rio.clip_box` method.

```{code-cell} ipython3
import numpy
from pathlib  import Path
from matplotlib import pyplot as plt
import numpy as np
from copy import copy
import rioxarray
import xarray
import a301_lib
```

+++ {"tags": [], "user_expressions": []}

## Open the band 5 image and read it in to a DataArray

```{code-cell} ipython3
band_name = 'B05'
infile = a301_lib.sat_data / f"pha/landsat/vancouver_landsat8_{band_name}.tif"
the_band = rioxarray.open_rasterio(infile,masked=True) 
the_band
```

+++ {"tags": [], "user_expressions": []}

## Scale and histogram the scene using the `scale_factor`

The data are stored as integer values, we need to divide by 10,000 to convert
to surface reflectivities.  Make sure the band 5 values look reasonable

```{code-cell} ipython3
the_band.scale_factor
```

```{code-cell} ipython3
scaled_band = the_band*the_band.scale_factor
masked_band = scaled_band
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
masked_band.plot.hist(ax = ax)
ax.set(title="band 5 reflectivities");
```

+++ {"tags": [], "user_expressions": []}

### Use imshow to make a grayscale image

Looks familiar

```{code-cell} ipython3
pal = copy(plt.get_cmap("Greys_r"))
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
vmin = 0.0  #anything under this is colored black
vmax = 0.8  #anything over this is colored red
from matplotlib.colors import Normalize
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1, figsize=(10,10))
masked_band.plot(ax=ax, cmap=pal, norm = the_norm)
ax.set_title(f"Landsat band {band_name}")
```

+++ {"tags": [], "user_expressions": []}

## Create the cartopy map projection

As in {ref}`week7:hls` we're going to need to add the image bounds to the cartopy crs

```{code-cell} ipython3
from pyresample.utils.cartopy import Projection
cartopy_crs = Projection(the_band.rio.crs, the_band.rio.bounds())
cartopy_crs
```

+++ {"tags": [], "user_expressions": []}

## Clip the raster to a 7 x 8 $km^2$ region centered on UBC

In the cells below we get the x,y corners of subset of the scene that
is centered on ubc and extends 8 km north/south and 7 km east/west.  To do this
we transform the lon,lat coordinate into map coordinates, which are given in meters.

```{code-cell} ipython3
import cartopy.crs as ccrs
import cartopy
```

```{code-cell} ipython3
#van_lon, van_lat = [-123.1207, 49.2827]
ubc_lon, ubc_lat = -123.2460, 49.2606
van_x, van_y = cartopy_crs.transform_point(ubc_lon,ubc_lat,ccrs.Geodetic())
van_x, van_y
```

+++ {"tags": [], "user_expressions": []}

### make the bounding box

crop this big scene so that we've got mostly Point Grey in the image.  We make a box that extends
2 km west, 5 km east, 3 km north and 5 km sounth of the center of UBC

```{code-cell} ipython3
ll_x = van_x - 2000
ll_y = van_y - 6000
ur_x = van_x + 5000
ur_y = van_y + 3000
```

```{code-cell} ipython3
bounding_box = ll_x, ll_y, ur_x, ur_y
```

+++ {"tags": [], "user_expressions": []}

### use a list expansion (*bounding_box) to pass the box

Recall in week 5 we went over [list expansion](https://note.nkmk.me/en/python-argument-expand/).
Use it here to pass 4 expanded list members to the `clip_box` function

The bounding box clipping takes the image size down from 3660 rows x 3660 columns
to 301 rows x 234 columns

```{code-cell} ipython3
ubc = masked_band.rio.clip_box(*bounding_box)
ubc
```

+++ {"tags": [], "user_expressions": []}

### Check the xarray to see if it's correct

Use rioxarray to make quick check on the clipped scene

```{code-cell} ipython3
fig, ax = plt.subplots(1,1, figsize=(10,10))
ubc.plot(ax=ax, cmap=pal, norm = the_norm)
ax.set_title(f"Landsat band {band_name}");
```

+++ {"tags": [], "user_expressions": []}

## Write a new geotiff

To write the clipped image as a geotiff, we need to construct a new xarray DataArray, with data, dims, coords and attrs.
After that is constructed we can use rioxarray to add the affine transform and the crs.

+++ {"tags": [], "user_expressions": []}

### Step 1: Construct the new affine transform

Recall how we constructed the  [affine transform](http://www.perrygeo.com/python-affine-transforms.html) in {ref}`week6:geotiffs`.  The pixel size
remains the same, but we've changed the upper left corner of the image, and so we need new corner coordinates for the uperleft corner values c and f of the transform.  Since the image is rectangular in map coords, we can just use the lower left and upper right coordinates of the bounding box
for the upper left corner.

```{code-cell} ipython3
from affine import Affine
orig = the_band.rio.transform()
a,b,d,e = orig.a, orig.b, orig.d, orig.e
c = ll_x  # upper left x
f = ur_y  # uper left y
new_transform = Affine(a,b,c,d,e,f)
new_transform
```

+++ {"tags": [], "user_expressions": []}

### Step 2: Construct the new coords

We need the map coordinates for the pixel x and y dimensions.  We could get these using the affine transform,
but rioxarray has a utility function that does this, called `affine_to_coords`.  It takes the affine transform
and the height and width of the clipped raster image and figures out the pixel coordinates.

```{code-cell} ipython3
from rioxarray.rioxarray import affine_to_coords
help(affine_to_coords)
```

```{code-cell} ipython3
band, height, width = ubc.data.shape
coords = affine_to_coords(new_transform,width,height)
```

+++ {"tags": [], "user_expressions": []}

### Step 3: create the data array

Make the xarray DataArray -- for the attrs, copy the full set of attributes that are attached to the `the_band` xarray.

```{code-cell} ipython3
clipped_ds=xarray.DataArray(ubc.data,coords=coords,
                            dims=ubc.dims,
                            attrs=the_band.attrs)
```

```{code-cell} ipython3
clipped_ds
```

+++ {"tags": [], "user_expressions": []}

### Step 4: add the crs and transform

`inplace=True` means overwrite the `clipped_ds` xarray instead of returning a new array.  This can
save memory for large arrays.

```{code-cell} ipython3
clipped_ds.rio.write_crs(the_band.rio.crs, inplace=True)
clipped_ds.rio.write_transform(new_transform, inplace=True);
```

+++ {"user_expressions": []}

### Write out the geotiff

Once we've got the full DataArray, we can write the geotiff out in one line

```{code-cell} ipython3
outfile = a301_lib.sat_data / "pha/week8_clipped_vancouver.tif"
clipped_ds.rio.to_raster(outfile)
```

+++ {"tags": [], "user_expressions": []}

## Read in the geotiff and plot to check

Double check to make sure we can open the cipped file and read it back in

```{code-cell} ipython3
test_ds = rioxarray.open_rasterio(outfile)
fig, ax= plt.subplots(1,1, figsize=(10,10))
test_ds.plot(ax=ax, norm=the_norm, cmap=pal)
ax.set(title="wv ir 5km using rioxarray");
```

```{code-cell} ipython3
test_ds.rio.bounds()
```
