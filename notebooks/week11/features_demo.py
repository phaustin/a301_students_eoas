# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
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
import a301_lib
from pathlib import Path
from matplotlib import pyplot as plt
import pprint
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy
from pathlib import Path
import pprint
import numpy as np
from pyproj import CRS, Transformer
import datetime
import pytz
from IPython.display import display
pacific = pytz.timezone("US/Pacific")
date = datetime.datetime.today().astimezone(pacific)
print(f"written on {date}")

# %% [markdown]
# # Adding features to a cartopy map
#
# This is an updated version of the [first mapping notebook](https://a301_web.eoas.ubc.ca/week4/cartopy_mapping_h5.html#geographic-coordinate-systems) with two
# changes:
#
# 1. Change the coordinate transformation code from cartopy's [transform_points](https://scitools.org.uk/cartopy/docs/latest/crs/index.html) to pyproj's [Transformer](https://pyproj4.github.io/pyproj/stable/api/transformer.html)
#
# 2. Add features from a geojson file that maps North American rivers, which I downloaded from [natural earth](https://github.com/nvkelso/natural-earth-vector/tree/master/geojson)
#
# Why am I changing the code for CRS transformation from cartopy to pyproj?  Basically because cartopy is planning
# to move from its own transformation code to the newer pyproj format, but it's 
# [still in underway](https://github.com/SciTools/cartopy/pull/1023).  Eventually, we won't have to switch between
# cartopy's coordinate objects and pyprojs, but for now, I need to create separate versions for each package:
#    
#    
#    1. Lambert Azimuthal Equal Area for cartopy: cartopy_laea
#    1. Lambert Azimuthal Equal Area for pyproj:  proj_laea
#    1. Geodetic lat/lon for cartopy: cartopy_latlon (cartopy.crs.PlateCarree())
#    1. Geodetic lat/lon for pyproj:  proj_latlon
#    
# Note the different formats when I print them out below -- pyproj is much fancier.

# %% scrolled=false
#
cartopy_laea = ccrs.LambertAzimuthalEqualArea(
    central_latitude= 45, central_longitude=-123
)

proj_laea = CRS.from_proj4(cartopy_laea.proj4_init)
proj_latlon = CRS.from_proj4("+proj=latlon")
cartopy_latlon = cartopy.crs.PlateCarree()
print(f"{cartopy_latlon.proj4_params=}\n")
print(f"{cartopy_laea.proj4_params=}\n")
print(f"{proj_latlon=}")
print(f"{proj_laea=}")
print(f"{proj_latlon.to_wkt()=}")

# %% [markdown]
# ## Checking the coordinates
#
# In this cell I set up the bounding box.  As a santity check, I make sure that
# the upper left and lower right corner coordinates are in the correct order
# (left more negative than right, bottom more negative than top) and that
# Vancouver is inside the box.

# %%
ul_corner = (-135,52)
lr_corner = (-105,35)
transform = Transformer.from_crs(proj_latlon, proj_laea)
laea_x, laea_y = transform.transform([ul_corner[0],lr_corner[0]],
                                           [ul_corner[1],lr_corner[1]])
ul_corner = laea_x[0],laea_y[0]
lr_corner = laea_x[1], laea_y[1]
print(f"{[ul_corner,lr_corner]}=")
van_lon, van_lat = [-123.1207, 49.2827]
van_x, van_y = transform.transform(van_lon, van_lat)
print(f"{van_x=},{van_y=}")

# %%
fig, ax = plt.subplots(1, 1, figsize=(15, 15), subplot_kw={"projection": cartopy_laea})
#
# extent order  [xleft, xright, ybot, ytop]
#
laea_extent = [ul_corner[0], lr_corner[0], lr_corner[1], ul_corner[1]]
ax.set_extent(laea_extent, cartopy_laea)
#
# the simple lon,lat projection is called "geodetic"
#
ax.plot(van_x, van_y, "ro", markersize=10)
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]));
ax.coastlines(resolution="10m", color="red", lw=2);

# %% [markdown]
# ## Adding a new set of features
#
# Here are the shape files I've downloaded.  See the Readme_gshhs_wdbII.md for details.  The
# "10m" in the file names mean:  1:10 million -- i.e. 1 meter on a map is 10 million meters
# in the real world, or equivalently, 1 cm on the map is 100 km in the real world.

# %% scrolled=false
openstreetmap_dir = a301_lib.data_share / 'openstreetmap'
all_shapes = list(openstreetmap_dir.glob("*"))
[print(item.name) for item in all_shapes];

# %% [markdown]
# ## Read the North American Rivers geojson file

# %% scrolled=true
map_folder = a301_lib.data_share / 'openstreetmap'
na_rivers = list(map_folder.glob("*rivers*north*"))[0]
df_rivers=gpd.read_file(na_rivers)
print(f"{df_rivers.crs=}\n")
print(f"\n{df_rivers.head()=}\n")

# %% [markdown]
# * Here is the first row in the dataframe

# %%
df_rivers.iloc[0].geometry

# %% [markdown]
# ## Add rivers to the map
#
# Now put the rivers on the map and redraw.

# %% scrolled=false
ax.add_geometries(df_rivers['geometry'],cartopy_latlon,facecolor="none",edgecolor="green")
display(fig)
