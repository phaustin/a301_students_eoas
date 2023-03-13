# ---
# jupyter:
#   jupytext:
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

# %% [markdown] tags=[] user_expressions=[]
# # xarray datasets

# %% [markdown] user_expressions=[]
# ## Introduction

# %% [markdown] tags=[] user_expressions=[]
# In this notebook, we take code from {ref}`week8:test_landsat` and use it to call a new function:
# [sat_lib.landsat_read.read_landsat_dataset](https://phaustin.github.io/a301_web/full_listing.html#sat_lib.landsat_read.get_landsat_dataset).  This is very similar
# to the `get_landsat_scene` function used in {ref}`week8:test_landsat`, with two improvements:
#
# 1) It takes an optional list of bands in the form `['B01','B02',...]` with the default being `['B04','B05,'B06']`.  The
#    `Fmask` cloud mask is also returned.
#
# 2) Instead of returning a dictionary it returns an [xarray.Dataset](https://foundations.projectpythia.org/core/xarray/xarray-intro.html#the-dataset-a-container-for-dataarrays-with-shared-coordinates) which is a collection of xarrays sharing 
# the same coordinates (in this case x,y in the map projection).  Datasets have a variety of useful features, but the most
# important one for work in this class is the ability to write the Dataset to disk, via [xarray.Dataset.to_netcdf](https://docs.xarray.dev/en/stable/generated/xarray.Dataset.to_netcdf.html) -- demonstrated below.
#
# Below we repeat the plot from {ref}`week8:test_landsat` using the new function and saving all channels to disk in a file called `week9_landsat.nc`

# %%
from matplotlib import pyplot as plt
from sat_lib.landsat_read import get_landsat_dataset
from rasterio.windows import Window
import a301_lib

# %% [markdown] tags=[] user_expressions=[]
# ## function arguments
#
# You can put any combination of valid 

# %%
help(get_landsat_dataset)

# %% [markdown] tags=[] user_expressions=[]
# ## Reading the default bands

# %%
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"

# %%
date = "2015-06-14"
lon, lat  = -123.2460, 49.2606
the_window = Window(col_off=2671, row_off=1352, width=234, height=301)
the_dataset = get_landsat_dataset(date, lon, lat, the_window) 

# %%
the_dataset

# %% [markdown] tags=[] user_expressions=[]
# ## Plotting the mask

# %%
list(the_dataset.keys())

# %%
fig, ax = plt.subplots(1,1)
#get the first 10 characters of the time attribute for the title
the_date = the_dataset.attrs['day']
the_dataset['Fmask'].plot()
ax.set_title(f"Land/cloud mask for Landsat {the_date}");

# %% [markdown] tags=[] user_expressions=[]
# ## Writing the dataset to disk
#
# Change the initials in outfile before you turn `do_write=True`

# %%
do_write = False
if do_write:
    outfile = a301_lib.data_share / "pha/week9_landsat.nc"
    the_dataset.to_netcdf(outfile)

# %%
# !ncdump -h ~/shared_files/pha/week9_landsat.nc
