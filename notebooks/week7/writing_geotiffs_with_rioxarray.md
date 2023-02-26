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
way to read and write geotiffs, and to clip, merge and reproject rasters.  Using rioxarray, we can eliminate about 80% of the boilerplate of working with raster data.

Below we read the geotiff back in as an xarray Dataset, make a plot, and write it out as a new geotiff.

+++

## xarray introduction

An [xarray](https://foundations.projectpythia.org/core/xarray/xarray-intro.html) is a python container that wraps a numpy array.  It adds some additional features:

- the_array.data:  the original numpy array (in our case, the raster)
- the_array.dims:  named dimensions for the array, for example a 3 dimensional remote sensing DataArray might have dimensions named ["channel","lons","lats"] or ["band","y","x"]
- the_array.coords: the coordinates for each dimension.  In our case the lons and lats coordinates of the center of each pixel, and the band numbers.
- the_array.attrs:  a dictionary of keys and values for metadata -- in our case this would be all the geotiff tags


+++

## rioxarray

The [rioxarray](https://corteva.github.io/rioxarray/stable/getting_started/getting_started.html) library is an xarray plugin that 
uses rasterio to handle the gis attributes like the map projection and affine_transform and passes data back and forth
between rasterio and xarray.  In the cells below we open the geotiff we wrote in {ref}`week6:geotiffs` and read it in as an
xarray.DataArray using rasterio.  We'll print out data, dims, coords, and attrs and gis attributes like the crs and the affine_transform

```{code-cell} ipython3
from copy import copy
import a301_lib
import rioxarray
import cartopy
from matplotlib import pyplot as plt


the_tif  = a301_lib.data_share / "pha/wv_ir_5km.tif"
xds = rioxarray.open_rasterio(the_tif)
```

## Anatomy of a rioxarray

Here are some of the import attributes of a rioxarray

+++

### The raster data

```{code-cell} ipython3
xds.data.shape, xds.data.dtype, type(xds.data)
```

### The named dimensions

```{code-cell} ipython3
xds.dims
```

### The pixel center coordinates

These pixel centers are given in the map projection coordinates

```{code-cell} ipython3
xds.coords
```

### The geotiff tags

```{code-cell} ipython3
print(f"{type(xds.attrs)=}\n\n{xds.attrs=}")
```

### Rasterio specific metadata

There are also rasterio specific attributes that can be obtained using `xds.rio`

+++

#### The coordinate reference system

```{code-cell} ipython3
xds.rio.crs
```

#### The affine transform

```{code-cell} ipython3
xds.rio.transform()
```

```{code-cell} ipython3
out = xds.rio.transform()
out.f
```

#### The raster bounds (or extent)

This is ll_x, ur_x, ll_y, ur_y in map coordinates

```{code-cell} ipython3
xds.rio.bounds()
```

#### Image width, height

```{code-cell} ipython3
xds.rio.width, xds.rio.height
```

#### x and y dimension names

```{code-cell} ipython3
xds.rio.x_dim, xds.rio.y_dim
```

## Reading the raster

Since we only have one channel, it's simpler to just convert the raster to 2 dimensions using numpy's `squeeze` method

```{code-cell} ipython3
wv_raster = xds.data
print(f"{wv_raster.shape=}")
#
# squeeze out the unneeded dimension
#
wv_raster = wv_raster.squeeze()
print(f"{wv_raster.shape=}")
```

+++ {"tags": []}

### calculating the image extent for cartopy 

Recall that cartopy needs the extent of the image, defined as `[ll_x,ur_x,ll_y,ur_y]`.  Here are two ways to get the extent.

+++

#### The hard way

We can use the `affine_transform` by putting in
the (column,row) of (column 0, row 0) and (column ncols+1, row nrows+1) for the ll and ur corners.   We need to add one cell to the nrows and ncols because
we want the left, bottom, top and right edges of the cells,
to get the distance from the ll_x, ll_y edges to the ur_x, ur_y edges.

```{code-cell} ipython3
nrows, ncols = wv_raster.shape
ll_x, ll_y = xds.rio.transform()*(0,nrows+1)
ur_x, ur_y = xds.rio.transform()*(ncols+1,0)
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
bounds (i.e. full raster extent in map coordinates) be included in the crs. In the cell below we use a  pyresample  utility `pyresample.utils.cartopy.Projection` to create
the cartopy crs with bounds included.

```{code-cell} ipython3
from pyresample.utils.cartopy import Projection
cartopy_crs = Projection(xds.rio.crs, bounds=extent)
cartopy_crs.bounds
```

```{code-cell} ipython3
cartopy_crs
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

### Quick plots with xarray -- test

If you don't need the cartopy map, then xarray can handle the plot setup for you using the `plot` wrapper that calls matplotlib to do the plotting.

```{code-cell} ipython3
fig2, ax = plt.subplots(1,1, figsize=(10,10))
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

## Writing a quick-look png

You can also matplotlib save the image as a png file for browsing

```{code-cell} ipython3
from skimage.io import imsave, imread
png_file = a301_lib.data_share / "pha/wv_ir_5km_rioxarray.png"
```

```{code-cell} ipython3
fig.savefig(png_file)
```

### Read the geotif back in to check

```{code-cell} ipython3
xds = rioxarray.open_rasterio(the_tif)
xds.attrs
```

## Summary

rioxarray provides a well-designed container that can hold a raster image along with all of the gis attributes and geotiff tags.  It has become
a standard way of working with geotiffs, and we'll use it extensively going forward.
