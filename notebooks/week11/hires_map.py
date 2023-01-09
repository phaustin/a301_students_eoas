# ---
# jupyter:
#   jupytext:
#     notebook_metadata_filter: all,-language_info,-toc,-latex_envs
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import copy

# %%
import datetime

# %%
import pprint
from pathlib import Path

import cartopy

# %%
import geopandas as gpd
import pytz
import rasterio

# %%
from IPython.display import display
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize

# %%
from pyproj import CRS, Transformer

import a301_lib  # noqa

pacific = pytz.timezone("US/Pacific")
date = datetime.datetime.today().astimezone(pacific)
print(f"written on {date}")

# %% [markdown]
# (vancouver_hires)=
# # Adding a high resolution map
#
# Below we read band 5 from the small Vancouver image we wrote out in the {ref}`rasterio_3bands` notebook, and put it on a map with a UTM-10N crs.  We then add a high resolution coastline read from the openstreetmap coastline database.  I use geopandas to inspect the shapefile that
# holds the streetmap coastline shapes.
# %% [markdown]
# ## Read the geotiff with rasterio
#
# I'm going to map Band 5, which is layer 3 in the tiff file.
# %%
notebook_dir = Path().resolve().parent
print(notebook_dir)
week10_scene = notebook_dir / "week10/vancouver_345_refl.tiff"
with rasterio.open(week10_scene) as raster:
    affine_transform = raster.transform
    crs = raster.crs
    profile = raster.profile
    refl = raster.read(3)
plt.hist(refl.flat)
plt.title("band 5 reflectance for Vancouver section")

# %%
print(f"profile: \n{pprint.pformat(profile)}")

# %% [markdown]
# ## Locate UBC on the map
#
# We need to project the center of campus from lon/lat to UTM 10N x,y using pyproj.Transformer.transform
# https://pyproj4.github.io/pyproj/stable/examples.html?highlight=transform
#
# I create a geodetic lat/lon transform (`p_latlon`) so a I can
# move from the UTM10 crs to lat/lon and back.

# %%
p_utm = crs
print(f"\nutm projection:\n\n{p_utm.to_wkt()}")
p_latlon = CRS.from_proj4("+proj=latlon")
print(f"\ngeodetic (latlon) projection: \n\n{p_latlon.to_wkt()}\n")
transform = Transformer.from_crs(p_latlon, p_utm)
ubc_lon = -123.2460
ubc_lat = 49.2606
ubc_x, ubc_y = transform.transform(ubc_lon, ubc_lat)
height, width = refl.shape
ubc_ul_xy = affine_transform * (0, 0)
ubc_lr_xy = affine_transform * (width, height)
print(f"here are the ul and lr corners: \n" f"{ubc_ul_xy=}, {ubc_lr_xy=}")

# %% [markdown]
# ## Higher resolution coastline

# %% [markdown]
# Here is what Point Grey looks like with the [open street maps](https://automating-gis-processes.github.io/site/notebooks/L6/retrieve_osm_data.html) coastline database.
#
# Optional: If you want to do this for your own image your're going to need to reduce the size of the coastlines database.  There is a good article about different sources for map data on the blog [python4oceanographers](
# https://ocefpaf.github.io/python4oceanographers/blog/2015/06/22/osm/).  The basic steps that worked for me:
#
# 1. Download the 700 Mbyte shape file of the WGS84 coastline database from [openstreetmap](https://osmdata.openstreetmap.de/data/coastlines.html)
#
# 2. Unzipping the file (it will be about 800 Mbytes) will create a folder called
#    coastlines-split-4326  (4326 is the epsg number for WGS84 lon/lat)
#
# 3. Figure out the lon/lat coordinates of a bounding box that contains your scene
#
# 4. Get a fiona prompt, which provides the command line program ogr2ogr
#    (ogr stands for"OpenGIS Simple Features Reference Implementation"). Just as rasterio has `rio insp`
#    to look at metadata, etc., fiona as `fio insp`.  To use it, open a terminal and point fiona
#    at coastlines-split-4326 by typing
#
#        fio insp coastlines-split-4326
#
#    in the directory where you unzipped the folder.
#
#
#    For Vancouver, I used this command at the prompt (all one line, lons are negative,
#    lats are positive).  Substitute your own lons and lats (note all - signs are single, not double hyphens)
#
#        ogr2ogr -skipfailures -f "ESRI Shapefile"  -clipsrc -123.5 49 -123.1 49.4   ubc_coastlines coastlines-split-4326
#
#    this extracts the segments and writes them to a new  folder called [ubc_coastlines](https://github.com/phaustin/a301_2020/tree/master/sat_data/openstreetmap) which is less than 140 K and which provides the coastlines below.

# %% [markdown]
# ## Mapped image with no coastline
#
# Sanity check to make sure we've got the right image.  I set the

# %%
vmin = 0.0
vmax = 0.5
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
palette = "viridis"
pal = copy.copy(plt.get_cmap(palette))
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
#
# cartopy needs it's own flavor of the crs
#
cartopy_crs = cartopy.crs.epsg(crs.to_epsg())
fig, ax = plt.subplots(1, 1, figsize=[15, 25], subplot_kw={"projection": cartopy_crs})
image_extent = [ubc_ul_xy[0], ubc_lr_xy[0], ubc_lr_xy[1], ubc_ul_xy[1]]
ax.imshow(
    refl,
    origin="upper",
    extent=image_extent,
    transform=cartopy_crs,
    cmap=pal,
    norm=the_norm,
)
ax.plot(ubc_x, ubc_y, "ro", markersize=25)
ax.set_extent(image_extent, crs=cartopy_crs)

# %% [markdown]
# ## Read the shape file and add the coastline to the image
#
# Note that PlateCarree is another name for WGS84 datum, simple lat/lon which is the projection of the coastlines-split-4326 shapefile.
#
# https://desktop.arcgis.com/en/arcmap/10.3/guide-books/map-projections/plate-carr-e.htm
#
# The cell below reads the coastlines into a geopandas dataframe.  The
# part we want is the column called "geometry" which lists the linestring
# objects that form the coastline.  Here is the first row:

# %%
coastline_dir = a301_lib.sat_data / "openstreetmap/ubc_coastlines"
df_coast = gpd.read_file(coastline_dir)
print(len(df_coast))
print(df_coast.head())
print(df_coast.crs)
df_coast["geometry"]

# %%
df_coast.iloc[0].geometry

# %% [markdown]
# ## Make the map
#
# To put on thecoastlines, I just add all the shapes to the axis

# %%
shape_project = cartopy.crs.Geodetic()
ax.add_geometries(
    df_coast["geometry"], shape_project, facecolor="none", edgecolor="red", lw=2
)
display(fig)
