---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(week6:geotiffs)=
# Writing the 5km water vapor image to a geotiff file

The most common data format for satellite data is called geotiff, which is a contraction of "georeferenced tagged image file format".  

The details are outlined in this [geotiff explainer](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/fundamentals-raster-data/intro-to-the-geotiff-file-format/). 

Briefly -- the file format allows us to save the raster images for multiple bands, the crs used by the raster to
get back lats/lons for the grid, the extent and grid size of the raster, and possibly a palette to use to present
the plotted image in a geographic information system.

In this notebook we'll read in the image produced by the {ref}`week5:wv_resample` notebook, resample it once more
onto a grid with a uniform pixel size of 5500 x 5500 meters and a grid of 510 rows and 500 columns,
and write this out as geotiff.

+++

## Read in the `area_def` and raster written by `wv_resample.md`

```{code-cell} ipython3
import a301_lib
import numpy as np
import json
from copy import copy
import pprint
pp = pprint.PrettyPrinter(indent=4)

from matplotlib import pyplot as plt
import cartopy

from pyresample import kd_tree, SwathDefinition

from sat_lib.mapping import area_def_from_dict
```

```{code-cell} ipython3
infile = a301_lib.data_share / "pha/wv_5km_resampled.npz"
wv_raster = np.load(infile)
print("npz array names",list(wv_raster.keys()))
wv_raster = wv_raster['arr_0']
print(f"{wv_raster.shape=}")
```

## Read in the `area_def`

Our `area_def` was calculated "on the fly" by pyresample, and it gave us some pretty
ragged extents and pixel sizes.  Humans do better when the work with round numbers,
so we want to regrid to clean up these decimals.

```{code-cell} ipython3
infile = a301_lib.data_share / "pha/area_dict.json"
with open(infile,'r') as the_in:
    old_area_dict = json.load(the_in)
old_area_def = area_def_from_dict(old_area_dict)
pp.pprint(old_area_dict)
```

## create a more regular `area_def` for sharing

Here's a close approximation to the old `area_def`, produced by a new `sat_lib.mapping` function
called `sat_lib.mapping.make_areadef`

We'll give the new raster more easily used/uniform coordinates

```{code-cell} ipython3
from sat_lib.mapping import make_areadef_dict
lat_0 = 39.5
lon_0 = -121.5
ll_x = -1238500
ll_y = -1155500
pixel_size_x = 5500
pixel_size_y = 5500
x_size = 500
y_size = 510
area_dict = make_areadef_dict(lat_0,lon_0,ll_x, ll_y,pixel_size_x,pixel_size_y,
                        x_size, y_size)
pp.pprint(area_dict)
new_area_def = area_def_from_dict(area_dict)
print(f"\n\n{new_area_def=}")
```

## regrid onto the new `area_def`

We need to redo the resample with the SwathDefiniton set to the lons
and lats taken from the old grid using the `get_lonlats` method.

+++

### get lons and lats to make the SwathDefinition

```{code-cell} ipython3
lons, lats =old_area_def.get_lonlats()
print(f"{lons.shape=}, {lats.shape=}")
old_swath = SwathDefinition(lons, lats)
```

### resample from the old raster onto the new more uniform raster

```{code-cell} ipython3
fill_value = -9999.0
new_wv_raster = kd_tree.resample_nearest(
    old_swath,
    wv_raster.ravel(),
    new_area_def,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
new_wv_raster[new_wv_raster < -9000] = np.nan

print(f"{new_wv_raster.shape=}")
```

### set up the palette and plot the new raster

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
crs = new_area_def.to_cartopy_crs()
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": crs})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
ax.set_extent(crs.bounds, crs)
cs = ax.imshow(
    new_wv_raster,
    transform=crs,
    extent=crs.bounds,
    origin="upper",
    alpha=0.8,
    cmap=pal,
    norm=the_norm,
)
ax.set(title="wv ir 5km resolution for 2013.222.2105")
fig.colorbar(cs, extend="both");
```

## Write this out as a geotiff using rasterio and read it back in to check

We need to use a python module called [rasterio](https://rasterio.readthedocs.io/en/latest/) to write this image out as
a geotiff.  We'll do this in three steps:

1) Define the [affine transform](http://www.perrygeo.com/python-affine-transforms.html)
2) Write out the new_wv_raster 
3) Read it back in and plot using rasterio

+++

### The role of the affine transform

We can move back and forth from geodetic lons/lats to mapx/mapy using [cartopy's transform_point](https://eoasubc.xyz/a301_2022/notebooks/assignments/assign2b_solution.html).  The affine transform does the next step,
which is to move back and forth from mapx/mapy to row/column on the raster.  We need to specify both the crs and the
affine transform when we write our raster out as a geotiff.

+++

### Defining the affine transform

+++

The affine transform requires the following information:

    a = width of a pixel
    b = row rotation (typically zero)
    c = x-coordinate of the upper-left corner of the upper-left pixel
    d = column rotation (typically zero)
    e = height of a pixel (typically negative)
    f = y-coordinate of the of the upper-left corner of the upper-left pixel

Looking at help(new_area_def) shows that these are available as attributes:

     |  width : int
     |      x dimension in number of pixels, aka number of grid columns
     |  height : int
     |      y dimension in number of pixels, aka number of grid rows
     |  rotation: float
     |      rotation in degrees (negative is cw)
     |  size : int
     |      Number of points in grid
     |  area_extent_ll : tuple
     |      Area extent in lons lats as a tuple (lower_left_lon, lower_left_lat, upper_right_lon, upper_right_lat)
     |  pixel_size_x : float
     |      Pixel width in projection units
     |      Pixel height in projection units
     |  pixel_upper_left : tuple
     |      Coordinates (x, y) of center of upper left pixel in projection units

+++

### Pull the values from `area_def` to create an Affine instance

```{code-cell} ipython3
from affine import Affine
a = new_area_def.pixel_size_x
b = 0
c, f = new_area_def.pixel_upper_left
d = 0
#
# pixel height is negative, because we are
# starting in the ul corner and going down
#
e = -1*new_area_def.pixel_size_y
the_transform = Affine(a,b,c,d,e,f)
print(f"{the_transform=}")
```

### Write out the geotiff

In addition to the raster, the crs, and the affine transform, you can also 
add comments/history etc. as arbitrary tags using update_tags.  This allows us to
write arbitrary metadata (dates, titles, units etc.) into the geotiff file

See [rasterio tagging](https://rasterio.readthedocs.io/en/latest/topics/tags.html)

```{code-cell} ipython3
new_wv_raster.dtype
```

```{code-cell} ipython3
import rasterio
import datetime
tif_filename = a301_lib.data_share / "pha/wv_ir_5km.tif"
num_chans = 1
with rasterio.open(
    tif_filename,
    "w",
    driver="GTiff",
    height=new_area_def.height,
    width=new_area_def.width,
    count=num_chans,
    dtype=new_wv_raster.dtype,
    crs=crs,
    transform=the_transform,
    nodata=np.nan
) as outtif:
    outtif.write(new_wv_raster,1)
    outtif.update_tags(
        title ="5 km ir water vapor, Modis Aqua",
        history="written by week6/writing_geotiffs.md",
        written_on=str(datetime.date.today()),
    )
    band_tag = "ir_wv (cm/m^2)"
    outtif.update_tags(1,label= band_tag)
    
    
    
```

## Read the geotiff back in using rasterio

In addition to the raster, the crs, and the affine transform, you can also 
add comments/history etc. as arbitrary tags

```{code-cell} ipython3
tif_filename = a301_lib.data_share / "pha/wv_ir_5km.tif"

with rasterio.open(tif_filename,'r') as wv_tif:
    #
    # get tags for entire file
    #
    file_tags = wv_tif.tags()
    #
    # get raster and tags for band 1
    #
    wv_raster = wv_tif.read(1)
    band_tags = wv_tif.tags(1)
    #
    # get the laea crs
    #
    crs = wv_tif.profile["crs"]
    #
    # get the affine transform
    #
    transform = wv_tif.profile["transform"]
    
print((f"\n{file_tags=}\n"
    f"\n{band_tags=}\n"
    f"\n{crs=}\n"
    f"\n{transform=}"))
            
        
```

### Get the pyresample `area_def` from the geotiff

We don't need my `area_def_from_dict` function when working with geotiffs, pyresample has
a utility for getting the `area_def` from the file in case you want to resample other rasters
to the same grid

```{code-cell} ipython3
import pyresample
with rasterio.open(tif_filename) as wv_tif:
    area_def = pyresample.utils.rasterio.get_area_def_from_raster(wv_tif)
area_def
```

### Plot the image using rasterio

Rasterio works with matplotlib axes -- you can pass an axis to rasterio's `show_hist` or `show`
commands and it will plot into that axis.

Below we use the tags we retrieved from the geotiff to set the title and legend label

See [rasterio plotting](https://rasterio.readthedocs.io/en/latest/topics/plotting.html)

```{code-cell} ipython3
from rasterio.plot import show_hist, show
fig, ax = plt.subplots(1,1)
with rasterio.open(tif_filename) as src:
    show_hist(src,ax=ax, title = file_tags['title'],
              label=band_tags['label'])

    
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize=(8,8))
with rasterio.open(tif_filename) as src:
    show(src, ax=ax, cmap='plasma')
```

```{code-cell} ipython3

```
