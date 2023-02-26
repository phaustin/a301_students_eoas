# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     notebook_metadata_filter: all,-language_info,-toc,-latex_envs
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import numpy
from pathlib  import Path
import inspect
from pystac_client import Client
from shapely.geometry import Point
from matplotlib import pyplot as plt
import numpy as np
from copy import copy

# %%
# connect to the STAC endpoint
cmr_api_url = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD"
client = Client.open(cmr_api_url)

# %%
# setup search
search = client.search(
    collections=["HLSL30.v2.0"],
    intersects=Point(-123.120, 49.2827),
    datetime="2015-06-01/2015-06-30"
) # nasa cmr cloud cover filtering is currently broken: https://github.com/nasa/cmr-stac/issues/239
# retrieve search results
items = search.get_all_items()
print(len(items))
print(list(items))
item = items[1]
print(f"{item.datetime=}")
print(f"{item.geometry=}")
print(f"{item.properties}")
assets = items[1].assets  # first item's asset dictionary
print(assets.keys())
for key, asset in assets.items():
    print(f"{key}: {asset.title}")

# %%
import rioxarray

# %%
assets['browse'].href

# %%
band_name="B08"
assets[band_name].href

# %%
true_color_image = rioxarray.open_rasterio(assets["browse"].href) 

# %%
ax = true_color_image.plot.imshow(figsize=(14,14),origin="upper");
ax.axes.set_title("vancouver browse image");

# %%
true_color_image.shape

# %%
import a301_lib
outfile = a301_lib.data_share / "pha/vancouver_browse.png"
ax.write_png(outfile)

# %%
true_color_image

# %%
true_color_image.rio.transform()

# %%
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"

# %%
the_band_href = assets[band_name].href
the_band = rioxarray.open_rasterio(the_band_href,masked=True)
masked_raster = the_band.where(the_band > 0)
the_raster = masked_raster[...].squeeze()
the_raster = the_raster*the_band.scale_factor
the_band

# %%
the_band.to_numpy()

# %%
the_raster

# %%
the_raster.plot.hist()

# %%
writeit=True
if writeit:
    outfile = a301_lib.data_share / f"pha/vancouver_landsat8_{band_name}.tif"
    the_band.rio.to_raster(outfile)
the_band

# %%
pal = copy(plt.get_cmap("Greys_r"))
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
vmin = 0.0  #anything under this is colored black
vmax = 0.8  #anything over this is colored red
from matplotlib.colors import Normalize
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)

# %%
fig, ax = plt.subplots(1,1, figsize=(10,10))
the_band.plot(ax=ax, cmap=pal, norm = the_norm)
ax.set_title(f"Landsat band {band_name}")
