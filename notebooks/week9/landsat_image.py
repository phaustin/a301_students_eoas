# ---
# jupyter:
#   jupytext:
#     notebook_metadata_filter: all,-language_info,-toc,-latex_envs
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.1-dev
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# (landsat1)=
# # Landsat image processing 1

# %% [markdown]
# https://medium.com/@mommermiscience/dealing-with-geospatial-raster-data-in-python-with-rasterio-775e5ba0c9f5
#
# https://www.perrygeo.com/python-affine-transforms.html
#
# http://geologyandpython.com/get-landsat-8.html

# %% [markdown]
# ## Bulk image download from AWS
#
# Notes drawing on http://geologyandpython.com/get-landsat-8.html

# %%
import pandas as pd
import a301_lib
import datetime as dt
import dateutil.parser
import numpy as np
from pathlib import Path

# %%
# !pwd

# %%
download_catalog=True
if download_catalog:
    s3_scenes = pd.read_csv('http://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz', compression='gzip')
else:
    s3_scenes = pd.read_csv(a301_lib.sat_data / 'landsat/scene_list.gz', compression='gzip')

# %% [markdown]
# ## Get images from Vancouver
#
# Filter out cloud cover > 20% and preprocessed images with ids ending in T2 or RT

# %%
path, row = 47, 26

print('Path:',path, 'Row:', row)

# Filter the Landsat Amazon S3 table for images matching path, row, cloudcover and processing state.
scenes = s3_scenes[(s3_scenes.path == path) & (s3_scenes.row == row) & 
                   (s3_scenes.cloudCover <= 20) & 
                   (~s3_scenes.productId.str.contains('_T2')) &
                   (~s3_scenes.productId.str.contains('_RT'))]
print(' Found {} images\n'.format(len(scenes)))
scenes.head()

# %%
scenes_van = pd.DataFrame(scenes)

# %%
columns = scenes_van.iloc[0].index
columns

# %%
timestamp = scenes_van.iloc[0].acquisitionDate
timestamp

# %%
the_date = dateutil.parser.parse(timestamp)
the_date


# %%
def convert_times(row):
    return dateutil.parser.parse(row.acquisitionDate)

the_times = scenes_van.apply(convert_times,axis=1)
the_times.head()

# %%
scenes_van['datetime']=the_times
del scenes_van['acquisitionDate']
scenes_van.head()

# %%
scenes_van.datetime.iloc[0].day,scenes_van.datetime.iloc[0].month, scenes_van.datetime.iloc[0].year


# %%
def make_date(row):
    year,month,day = row.datetime.year, row.datetime.month, row.datetime.day
    the_date = dt.date(year,month,day)
    return the_date
date_vals = scenes_van.apply(make_date, axis=1)
scenes_van['the_date']=date_vals

# %%
hit = scenes_van.the_date == dt.date(2015,6,14)
np.sum(hit)
my_scene = scenes_van[hit]
my_scene

# %%
scene_url = my_scene.iloc[0].download_url

# %%
import requests
from bs4 import BeautifulSoup
import os
import shutil


# Request the html text of the download_url from the amazon server. 
# download_url example: https://landsat-pds.s3.amazonaws.com/c1/L8/139/045/LC08_L1TP_139045_20170304_20170316_01_T1/index.html
response = requests.get(scene_url)
print(f"response: {response}, {type(response)}")
landsat_path = Path() / 'landsat_scenes' / my_scene.iloc[0].productId
landsat_path.mkdir(parents=True,exist_ok=True)
# # If the response status code is fine (200)
if response.status_code == 200:

    # Import the html to beautiful soup
    html = BeautifulSoup(response.content, 'html.parser')

    # Create the dir where we will put this image files.
    entity_dir = os.path.join(landsat_path, my_scene.iloc[0].productId)
    os.makedirs(entity_dir, exist_ok=True)

    # Second loop: for each band of this image that we find using the html <li> tag
    good_bands = ['B4.TIF', 'B5.TIF']
    good_list = []
    for li in html.find_all('li'):

        # Get the href tag
        the_file = li.find_next('a').get('href')
        for keyword in good_bands:
            if the_file.find(keyword) > 0:
                good_list.append(the_file)
        if the_file.find('MTL.txt') > 0:
            good_list.append(the_file)
    print(f"here is goodlist: {good_list}")
        
download=True
if download:
    for the_file in good_list:
        print(f'  Downloading: {the_file}')

        # Download the files
        # code from: https://stackoverflow.com/a/18043472/5361345
        image_path = scene_url.replace('index.html', the_file)
        print(image_path)
        response = requests.get(image_path, stream=True)

        with open(landsat_path / the_file, 'wb') as output:
            shutil.copyfileobj(response.raw, output)
        del response
    

# %%
