---
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
import copy
import datetime
import pprint
from pathlib import Path

import cartopy
import cartopy.crs
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pytz
import rasterio
from IPython.display import display
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from pyproj import CRS, Transformer
```

```{code-cell} ipython3
import a301_lib

pacific = pytz.timezone("US/Pacific")
date = datetime.datetime.today().astimezone(pacific)
print(f"written on {date}")
```

(assign6b_sol)=
# Solution: adding an image with features to a cartopy map

Here's a demo of adding features to an image.  The notebook does some extra work to
illustrate how to make a map that is bigger than the image, and how to reproject from
one raster crs to another using rasterio.

1) read in the `vancouver_345_refl.tiff` band 5 image  
2) find the image corners in utm10 and geodetic lat/lon (for the features)  
3) put the image on a map that extends 5 km beyond the image  
4) add the features to the big map  
5) create a new crs that is laea centered on lat=50 deg N, lon= -120 deg E  
6) use rasterio.reproject to reproject the utm10 image onto the laea crs  
7) draw a 50 row by 100 column box on the image

+++

## Read in the geotiff

First read in band 5 from the `vancouver_345_refl.tiff` image that was produced by
{ref}`rasterio_3bands`:

```{code-cell} ipython3
notebook_dir = a301_lib.data_share.resolve()
print(notebook_dir)
week10_scene = notebook_dir / "vancouver_345_refl.tiff"
```

```{code-cell} ipython3
with rasterio.open(week10_scene) as van_raster:
    b5_refl = van_raster.read(3)
    chan3_tags = van_raster.tags(3)
    crs_10 = van_raster.profile["crs"]
    profile=van_raster.profile
    affine_transform = profile["transform"]
    tags = van_raster.tags()
    print(f"\n\n{tags=}, \n\n{chan3_tags=},\n\n {profile=},\n\n {affine_transform=}\n")
```

## Set up the lat/lon UTM10N transform

I'll want to transform back and forth between UTM and lat/lon (since I think in lat/lon), so create
a transformer object for this.  Copy code from {ref}`image_zoom`

```{code-cell} ipython3
from pyproj import CRS, Transformer

p_utm10 = crs_10
p_latlon = CRS.from_epsg(4326)
crs_transform = Transformer.from_crs(p_latlon, p_utm10)
print(p_latlon.to_wkt())
```

## Find the corners of the image

I need the upper left and lower right corners to set the image extent for imshow.  This is
what the affine transform provides.  I'll use my crs_transform to also get the image_extent
in lon/lat coords to make sure I'm in the right place

```{code-cell} ipython3
ul_x_utm10, ul_y_utm10 = affine_transform*(0,0)
lr_x_utm10, lr_y_utm10 = affine_transform*(profile['width'],profile['height'])
print(f"{(ul_x_utm10,ul_y_utm10,lr_x_utm10,lr_y_utm10)=}")
image_extent_utm10 = (ul_x_utm10,lr_x_utm10, lr_y_utm10, ul_y_utm10)
```

```{code-cell} ipython3
ul_lon,ul_lat = crs_transform.transform(ul_x_utm10,ul_y_utm10,direction='INVERSE')
lr_lon,lr_lat = crs_transform.transform(lr_x_utm10,lr_y_utm10,direction='INVERSE')
print(f"{(ul_lon,ul_lat,lr_lon,lr_lat)=}")
```

## Make the map extent bigger than the image

In order show more context, I'll enlarge the map extent by 5 km on each size

```{code-cell} ipython3
map_ul_x = ul_x_utm10 - 5.e3
map_lr_x = lr_x_utm10 + 5.e3
map_ul_y = ul_y_utm10 + 5.e3
map_lr_y = lr_y_utm10 - 5.e3
map_extent_utm10 = (map_ul_x,map_lr_x,map_lr_y,map_ul_y)
print(f"{map_extent_utm10=}")
```

* Repeat the imshow code from {ref}`rasterio_3bands`:

```{code-cell} ipython3
cartopy_utm10 = cartopy.crs.epsg(crs_10.to_epsg())
fig, ax = plt.subplots(
        1, 1, figsize=(15,15), subplot_kw={"projection": cartopy_utm10}
    )

vmin = 0.0
vmax = 0.4
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
palette = "viridis"
pal = copy.copy(plt.get_cmap(palette))
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
col=ax.imshow(b5_refl, cmap=pal, norm=the_norm, origin="upper",
          extent=image_extent_utm10,transform=cartopy_utm10);
cbar_ax = fig.add_axes([0.85, 0.2, 0.05, 0.6])
cbar = ax.figure.colorbar(col, extend="both", cax=cbar_ax, orientation="vertical")
cbar.set_label("band 5 reflectance")
```

## Now set the map extent

From the {ref}`demo_cartopy_extent` notebook we can repeat the ax.set_extent call to make the map
larger than the image

```{code-cell} ipython3
ax.set_extent(map_extent_utm10,crs=cartopy_utm10)
display(fig)
```

## Add features

Use the {ref}`subset_map` code to put features on this axis.  I need the cartopy_latlon
crs to do this (since p_latlon, the pyproj crs, doesn't work with cartopy)

```{code-cell} ipython3
gpd_dict = {}
read_files=True
if read_files:
    all_cia = a301_lib.data_share / "openstreetmap/WDBII_shp/f"
    all_cia = list(all_cia.glob("*"))
    for item in all_cia:
        gpd_dict[item.name] = gpd.read_file(item)
        print(f"read {item.name}")

    all_gshhs = a301_lib.data_share / "openstreetmap/GSHHS_shp/f"
    all_gshhs = list(all_gshhs.glob("*"))

    for item in all_gshhs:
        gpd_dict[item.name] = gpd.read_file(item)
        print(f"read {item.name}")
else:
    shape_files = list(small_shapes.glob("*"))
    for item in shape_files:
        key = item.stem
        gpd_dict[key] = gpd.read_file(item)
        print((f"reading saved shapefile {item} with\n"
               f"{len(gpd_dict[key])} rows"))
```

```{code-cell} ipython3
def find_features(extent, df):
    """
    given an extent and a dataframe, return a new dataframe
    containing only features that fall within the extent

    Parameters
    ----------

    extent:  list -- geographic extent in lon (deg E)/lat (deg N)
    df:  the geopandas dataframe to slice
    """
    xleft, xright, ybot, ytop = extent
    hit_rows = df.cx[xleft:xright, ybot:ytop]
    return hit_rows

extent = [-124, -122, 48, 50]
if read_files:
    subset_dict = {}
    for key, df in gpd_dict.items():
        df_subset = find_features(extent, df)
        if len(df_subset) > 0:
            subset_dict[key] = df_subset
            print(f"clipping {key}")
else:
    subset_dict=gpd_dict
```

* now put the features on -- they are defined in geodetic (lat/lon) crs

```{code-cell} ipython3
cartopy_latlon = cartopy.crs.PlateCarree()
for key, df in subset_dict.items():
    print(f"adding {key} with {len(df)} features")
    if key.find("river") > -1:
        ax.add_geometries(
            df["geometry"], cartopy_latlon, facecolor="none", edgecolor="green",lw=3,
        )
    else:
        ax.add_geometries(
            df["geometry"], cartopy_latlon, facecolor="none", edgecolor="blue",lw=3,
        )
display(fig)
```

## Putting images from different utm zones on a map

(not part of the assignment)

Suppose you're working on a project that spans BC and Alberta, and you need
to put images on a map that are either UTM zone 10 (-126 to -120 deg E) or
UTM zone 11 (-120 to - 114 deg E).  To show both images on the same map, you
need to reproject them onto a common crs. As a compromise, let's use a laea
projection centered on `lon_0`= -120 deg E, `lat_0`=50 deg N

Here are the rasterio reprojection module docs: [rasterio](https://rasterio.readthedocs.io/en/latest/topics/reproject.html)

### Step 1 is to create [the new pyproj crs](https://pyproj4.github.io/pyproj/dev/api/crs/crs.html).

I'll just borrow the pyproj parameters from our earlier notebooks.

```{code-cell} ipython3
lat_0=50
lon_0 = -120
laea_proj = {'datum': 'WGS84', 'lat_0': '50', 'lon_0': '-120', 'no_defs': 'None',
             'proj': 'laea', 'type': 'crs', 'units': 'm', 'x_0': '0', 'y_0': '0'}
p_laea = CRS(laea_proj)
p_laea.to_wkt()
```

### Step 2 is to reproject the extent in the new coordinate system

Remember that extent order is:  [xleft, xright, ybot, ytop].  We need to get these values in the new laea crs.

Here are the two extents for the image"

```{code-cell} ipython3
crs_transform = Transformer.from_crs(p_utm10, p_laea)
extent_utm10 = [ul_x_utm10,lr_x_utm10,lr_y_utm10,ul_y_utm10]
ul_x_laea,ul_y_laea = crs_transform.transform(ul_x_utm10,ul_y_utm10)
lr_x_laea,lr_y_laea = crs_transform.transform(lr_x_utm10,lr_y_utm10)
extent_laea=[ul_x_laea,lr_x_laea,lr_y_laea,ul_y_laea]
print(f"{extent_utm10=}")
print(f"{extent_laea=}")
```

### step 3: create the affine transform

We need the pixel size, then we can use the Affine constructor as we did in {ref}`image_zoom`
(don't forget to make the pixel height negative). Notice that the pixel size has
changed slightly in the laea crs.  Also notice that the correct denominator is (#pixels - 1), not #pixels.  That's
because the extents go from the left side of the first pixel to the right side of the last pixel.  Dividing
by #pixels would put the right boundary 1 pixel less than it needs to be.

```{code-cell} ipython3
pixel_x_size = (lr_x_laea - ul_x_laea)/(profile['width'] -1)
pixel_y_size = (ul_y_laea - lr_y_laea)/(profile['height'] - 1)
print(f"{pixel_x_size=},{pixel_y_size=}")
```

```{code-cell} ipython3
from affine import Affine

laea_affine = Affine(pixel_x_size,0,ul_x_laea,0,-pixel_y_size,ul_y_laea)
```

### step 4: do the reprojection from p_utm10 to p_laea

First make a numpy array to hold the reprojected image.  We're keeping the row and column numbers the same as i the original tiff.

```{code-cell} ipython3
width=profile['width']
height=profile['height']
b5_refl_laea = np.ones([height,width],dtype=np.float32)
```

### Now reproject from utm10 to laea

```{code-cell} ipython3
from rasterio.warp import Resampling, reproject

reproject(
        b5_refl,
        b5_refl_laea,
        src_transform=affine_transform,
        src_crs=p_utm10,
        dst_transform=laea_affine,
        dst_crs=p_laea,
        resampling=Resampling.nearest);
plt.imshow(b5_refl_laea);
```

### step 5: Make a cartopy map

As of cartopy 0.18 we also need to create a cartopy version of the laea crs,
since it doesn't accept the pyproj version.   See [cartopy projections](https://scitools.org.uk/cartopy/docs/latest/crs/projections.html#cartopy-projections).  One difference is
that cartopy requires that the datum be specified separately from the projection, using a `globe` object.
You can track progress on making cartopy more compatible with pyproj [here](https://github.com/SciTools/cartopy/pull/1023#discussion_r168395702) [and here](https://github.com/SciTools/cartopy/issues/1477)

```{code-cell} ipython3
dir(cartopy.crs.CRS)
globe = cartopy.crs.Globe(datum='WGS84',ellipse='WGS84')
laea_cartopy_crs = cartopy.crs.LambertAzimuthalEqualArea(central_longitude=lon_0,
                                                    central_latitude=lat_0,
                                                    globe=globe)
print(f"proj4 string: {laea_cartopy_crs.proj4_init=}")
```

**now plot it with features**

Note the boundaries are slightly skewed at the top and bottom of the reprojection. In the laea projection all locations are referenced to the point at (`lon_`,`lat_0`), while for the UTM projection all locations are referenced to the longitude line going through the middle of the zone. The UTM preserves angles and shapes over small regions (i.e. it's conformal), but the scale changes with location.  The laea preserves scale, but distorts angles and shapes.  See [wikpedia lambert](https://en.wikipedia.org/wiki/Lambert_azimuthal_equal-area_projection) and [wikipedia conformal](https://en.wikipedia.org/wiki/Conformal_map_projection)

```{code-cell} ipython3
fig, ax = plt.subplots(
        1, 1, figsize=(10,15), subplot_kw={"projection": laea_cartopy_crs}
    )

vmin = 0.0
vmax = 0.4
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
palette = "viridis"
pal = copy.copy(plt.get_cmap(palette))
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
col=ax.imshow(b5_refl_laea, cmap=pal, norm=the_norm, origin="upper",
          extent=extent_laea,transform=laea_cartopy_crs)
cbar_ax = fig.add_axes([0.90, 0.2, 0.05, 0.6])
cbar = ax.figure.colorbar(col, extend="both", cax=cbar_ax, orientation="vertical")
cbar.set_label("band 5 reflectance")
```

### Add a coastline/rivers

```{code-cell} ipython3
for key, df in subset_dict.items():
    print(f"adding {key} with {len(df)} features")
    if key.find("river") > -1:
        ax.add_geometries(
            df["geometry"], cartopy_latlon, facecolor="none", edgecolor="red",lw=5,
        )
    else:
        ax.add_geometries(
            df["geometry"], cartopy_latlon, facecolor="none", edgecolor="blue",lw=3,
        )
display(fig)
```

## draw a red box in the middle of the scene

We want a box that's 50 rows by 100 columns. I'll center it at row 300, column 200, and move up 25 rows and
down 50 rows to find the corners.

```{code-cell} ipython3
ul_x, ul_y = laea_affine*(150,275)
lr_x, lr_y = laea_affine*(250,325)
delta_x = lr_x - ul_x
delta_y = ul_y - lr_y
print(f"{(ul_x,ul_y,lr_x,lr_y)=}")
#
# circle clockwise from upper left corner
#
box_x = [ul_x, ul_x + delta_x, ul_x + delta_x, ul_x,          ul_x]
box_y = [ul_y, ul_y          , ul_y - delta_y, ul_y - delta_y,ul_y]
ax.plot(box_x,box_y,'r-',lw=4)
display(fig)
```

## More mapping tools for meteorology

Check out [metpy](https://unidata.github.io/MetPy/latest/examples/index.html#plotting) for meteorologically oriented maps.
