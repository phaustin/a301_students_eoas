---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: -all
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
toc-autonumbering: true
---

(week7:zoom_landsat)=
# Using rioaxarray to zoom a landsat image

In this notebook we read in a landsat image geotiff for Band 5, which is in the near infrared:

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

```{code-cell} ipython3
band_name = 'B05'
infile = a301_lib.data_share / f"pha/landsat/vancouver_landsat8_{band_name}.tif"
the_band = rioxarray.open_rasterio(infile,masked=True) 
the_band
```

```{code-cell} ipython3
np.sum(np.isnan(the_band.data))
```

```{code-cell} ipython3
scaled_band = the_band*the_band.scale_factor
masked_band = scaled_band
```

```{code-cell} ipython3
masked_band.plot.hist()
```

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

## Create the cartopy map projection

```{code-cell} ipython3
from pyresample.utils.cartopy import Projection
cartopy_crs = Projection(the_band.rio.crs, the_band.rio.bounds())
cartopy_crs
```

## Clip the raster to a 100 $km^2$ region centered on UBC

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

```{code-cell} ipython3
ll_x = van_x - 5000
ll_y = van_y - 6000
ur_x = van_x + 5000
ur_y = van_y + 6000
```

```{code-cell} ipython3
ll_x, ll_y, ur_x, ur_y
```

```{code-cell} ipython3
ubc = masked_band.rio.clip_box(ll_x, ll_y, ur_x, ur_y)
ubc
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1, figsize=(10,10))
ubc.plot(ax=ax, cmap=pal, norm = the_norm)
ax.set_title(f"Landsat band {band_name}")
```

## Write a new geotiff

To write the clipped image as a geotiff, we need to construct a new DataArray, with data, dims, coords and attrs.
After that is constructed we can use rioxarray to add the affine transform and the crs.

+++

### Construct the new affine transform

Recall how we constructed the  [affine transform](http://www.perrygeo.com/python-affine-transforms.html) in {ref}`week6:geotiffs`.  The pixel size
remains the same, but we've moved the upper left corner of the image, and so we need a new for the c and f variables.  Since the image is rectangular in map coords, we can just use the lower left and upper right coordinates
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

### Construct the new coords

We need the map coordinates for the pixel x and y dimensions.  We could get these using the affine transform,
but rioxarray has a utility function that does this, called `affine_to_coords`.  It takes the affine transform
and the height and width of the raster image and figures out the pixel coordinates.

```{code-cell} ipython3
from rioxarray.rioxarray import affine_to_coords
help(affine_to_coords)
```

```{code-cell} ipython3
band, height, width = ubc.data.shape
coords = affine_to_coords(new_transform,width,height)
```

### create the data array

```{code-cell} ipython3
clipped_ds=xarray.DataArray(ubc.data,coords=coords,dims=ubc.dims,attrs=the_band.attrs)
clipped_ds.rio.write_crs(the_band.rio.crs, inplace=True)
clipped_ds.rio.write_transform(new_transform, inplace=True)
```

### Write out the geotiff

```{code-cell} ipython3
outfile = a301_lib.data_share / "pha/week7_clipped_vancouver.tif"
clipped_ds.rio.to_raster(outfile)
```

```{code-cell} ipython3
test_ds = rioxarray.open_rasterio(outfile)
fig, ax = plt.subplots(1,1, figsize=(10,10))
xds.plot(ax=ax, norm=the_norm, cmap=pal)
ax.set(title="wv ir 5km using rioxarray");
```
