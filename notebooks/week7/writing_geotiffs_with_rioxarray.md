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
toc-autonumbering: true
toc-showmarkdowntxt: false
---

+++ {"tags": []}

(week6:geotiff_xarray)=
# Using xarray to work with geotiffs

In the week6 {ref}`week6:geotiffs` notebook we wrote a geotiff file for the 5km water vapor data resampled at 5500 x 5500 m on a Lambert aziumthal crs.  Suppose we want to
crop that dataset, or use it in a machine learning pipeline, or combine it with other data?  How do we work with the raster in python without losing all of the
extra information about the affine transform, crs, etc?  The most useful tool for this is an [xarray DataArray](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.html#xarray.DataArray), which extends numpy arrays by adding coordinates, named dimensions and attributes.
In this notebook, we'll first create an xarray using the `wv_ir_5km.tif` and use it to show a slice of the data.  Then we'll create an xarray from scratch given
the numpy array, affine transform, and crs.

The module that we'll use for this is called [the rasterio xarray extension](https://corteva.github.io/rioxarray/html/readme.html) or rioxarray.  It provides a natural
way to read and write geotiffs, and to clip, merge and reproject rasters.

Below we read the geotiff back in as an xarray Dataset, make a plot, and write it out as a new geotiff.

+++

## Reading in the geotiff to a DataArray

rioxarray uses rasterio to handle the gis attributes like the map projection and affine_transform

```{code-cell} ipython3
from copy import copy
import a301_lib
import rioxarray
import cartopy
from matplotlib import pyplot as plt


the_tif  = a301_lib.data_share / "pha/wv_ir_5km.tif"
xds = rioxarray.open_rasterio(the_tif)
```

## DataArray attributes and coordinates

+++

If you look at the coordnates below, you can see that x and y are the map coords for the center of each pixel.
x,y values for the center of each pixel.  These same coordinates are also written out as pandas indexes
for [compatibility with pandas](https://docs.xarray.dev/en/stable/user-guide/pandas.html)

```{code-cell} ipython3
xds
```

## Getting GIS metadata from rasterio

In this section we'll extract the information we need to put the raster on a map.  rioxarray has access to many of the rasterio methods via the xds.rio shortcut.

+++

### Getting the tags/attributes

The `attrs` attribute returns the tags as a dictionary.

```{code-cell} ipython3
xds.attrs
```

### getting the affine transform

To get the transform and the crs we need to go through the `rio` attribute, which was added to the DataArray when we imported `rioxarray`

```{code-cell} ipython3
affine_transform = xds.rio.transform()
affine_transform
```

### getting coordinate reference system

rioxarray uses the rasterio crs, which it represents as well known text (wkt)

```{code-cell} ipython3
rio_crs= xds.rio.crs
print(f"{rio_crs=}\n\n")
```

### reading the raster

To get the numpy array out of the DataArray, we can use standard numpy indexing, or there's a `to_numpy` method if we want to change the dtype, assign missing values etc.
Note that the raster array is three dimensional, so that it can hold multiple bands.  Since we are only working with 1 band, we can
use the `squeeze` method to make it two dimensional.

```{code-cell} ipython3
wv_raster = xds[...]
print(f"{wv_raster.shape=}")
#
# squeeze out the unneeded dimension
#
wv_raster = wv_raster.squeeze()
print(f"{wv_raster.shape=}")
```

+++ {"tags": []}

### calculating the image extent for cartopy 

Recall that cartopy needs the extent of the image, defined as `[ll_x,ur_x,ll_y,ur_y]`.  We can get that from the `affine_transform` by putting in
the (column,row) of (column 0, row 0) and (column ncols+1, row nrows+1) for the ll and ur corners.   We need to add one cell to the nrows and ncols because
we want the left, bottom, top and right edges of the cells,
to get the distance from the ll_x, ll_y edges to the ur_x, ur_y edges.

+++

#### The hard way

```{code-cell} ipython3
nrows, ncols = wv_raster.shape
ll_x, ll_y = affine_transform*(0,nrows+1)
ur_x, ur_y = affine_transform*(ncols+1,0)
extent = (ll_x,ur_x, ll_y, ur_y)
extent
```

#### The easy way

This same information is also available from rasterio via the `bounds()` method

```{code-cell} ipython3
xds.rio.bounds()
```

## Making a cartopy map

+++

### Convert the rasterio crs to a cartopy crs



One friction point is that cartopy has a slightly different form of the crs than rasterio.  Cartopy requires that the
bounds (i.e. full raster extent in map coordinates) be included in the crs. In the cell below we use a  pyresample  utility `pyresample.utils.cartopy.Projection` to make
the cartopy crs with bounds included.

```{code-cell} ipython3
from pyresample.utils.cartopy import Projection
cartopy_crs = Projection(rio_crs, bounds=extent)
cartopy_crs.bounds
```

### Copy code from `week6/wv_resample.md`

Below is a straight copy of last week's plotting code.  Note that if we wanted to plot only a part of the scene,
we could change the extent argument to imshow to crop the image.  In the next notebook we'll go over the
standard way to crop/clip a raster.

```{code-cell} ipython3
pal = copy(plt.get_cmap("plasma"))
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("r")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
vmin = 0.0  #anything under this is colored black
vmax = 4.0  #anything over this is colored red
from matplotlib.colors import Normalize
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
```

```{code-cell} ipython3
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": cartopy_crs})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
ax.set_extent(cartopy_crs.bounds, cartopy_crs)
cs = ax.imshow(
    wv_raster,
    transform=cartopy_crs,
    extent=extent,
    origin="upper",
    alpha=0.8,
    cmap=pal,
    norm=the_norm,
)
ax.set(title="wv ir 5km using cartopy")
fig.colorbar(cs, extend="both");
```

### Quick plots with xarray

If you don't need the cartopy map, then xarray can handle the plot setup for you:

```{code-cell} ipython3
fig, ax = plt.subplots(1,1, figsize=(10,10))
xds.plot(ax=ax, norm=the_norm, cmap=pal)
ax.set(title="wv ir 5km using rioxarray");
```

## Writing the geotiff

Using rasterio to write the geotiff is just a one-liner, because all of the GIS metadata is available in the `xds` variable. Any new or modified tags we want to add
to the file can be included in a dictionary.  All the old tags will remain if not modified.

```{code-cell} ipython3
the_tif  = a301_lib.data_share / "pha/wv_ir_5km_rioxarray.tif"
tags=dict(label = "ir_wv -- rioxarray (cm/m^2)")
xds.rio.to_raster(the_tif,tags=tags)
```

### Read it back in to check

```{code-cell} ipython3
xds = rioxarray.open_rasterio(the_tif)
xds.attrs
```
