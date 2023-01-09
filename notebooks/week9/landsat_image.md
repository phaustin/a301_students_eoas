---
jupytext:
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
import datetime
import pytz
pacific = pytz.timezone('US/Pacific')
date=datetime.datetime.today().astimezone(pacific)
print(f"written on {date}")
```

(landsat1)=
# Landsat image processing 1

+++

* My source for the AWS download workflow I outline here is

[geology and python](http://geologyandpython.com/get-landsat-8.html)

* Rasterio examples

[geospatial raster data](https://medium.com/@mommermiscience/dealing-with-geospatial-raster-data-in-python-with-rasterio-775e5ba0c9f5)


* A good explanation of the python affine package


[affine transform](https://www.perrygeo.com/python-affine-transforms.html)

+++

## Bulk image download from AWS

Notes drawing on http://geologyandpython.com/get-landsat-8.html

```{code-cell} ipython3
import pandas as pd
import a301_lib
import datetime as dt
import dateutil.parser
import numpy as np
from pathlib import Path
```

```{code-cell} ipython3
!pwd
```

```{code-cell} ipython3
download_catalog=False
if download_catalog:
    s3_scenes = pd.read_csv('http://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz', compression='gzip')
else:
    s3_scenes = pd.read_csv(a301_lib.sat_data / 'landsat/scene_list.gz', compression='gzip')
```

## Get images from Vancouver

Filter out cloud cover > 20% and preprocessed images with ids ending in T2 or RT

```{code-cell} ipython3
path, row = 47, 26

print('Path:',path, 'Row:', row)

# Filter the Landsat Amazon S3 table for images matching path, row, cloudcover and processing state.
scenes = s3_scenes[(s3_scenes.path == path) & (s3_scenes.row == row) &
                   (s3_scenes.cloudCover <= 20) &
                   (~s3_scenes.productId.str.contains('_T2')) &
                   (~s3_scenes.productId.str.contains('_RT'))]
print(' Found {} images\n'.format(len(scenes)))
scenes.head()
```

* In order to change parts of this dataframe, we make another copy using
  the dataframe constructor.

```{code-cell} ipython3
scenes_van = pd.DataFrame(scenes)
```

* Here are the columns in for the first row of the dataframe

```{code-cell} ipython3
columns = scenes_van.iloc[0].index
columns
```

```{code-cell} ipython3
timestamp = scenes_van.iloc[0].acquisitionDate
timestamp
```

* the aquistion date is a text string.  We need to turn it into a datetime
  object in order to use it for filtering.

```{code-cell} ipython3
the_date = dateutil.parser.parse(timestamp)
the_date
```

* this cell runs the convert_times function on every row of the dataframe
  returning a new column

```{code-cell} ipython3
def convert_times(row):
    return dateutil.parser.parse(row.acquisitionDate)

the_times = scenes_van.apply(convert_times,axis=1)
the_times.head()
```

* save the datetime column, and elete the acquistionDate column which is now
  redundant

```{code-cell} ipython3
scenes_van['datetime']=the_times
del scenes_van['acquisitionDate']
scenes_van.head()
```

```{code-cell} ipython3
scenes_van.datetime.iloc[0].day,scenes_van.datetime.iloc[0].month, scenes_van.datetime.iloc[0].year
```

* Now apply the new make_date function to chop off the hours, minutes and seconds.
  We will use this to get exact matches on the year, month, day.  With landsat there
  are never two passes over the same wrs row column in a single day, so date-only
  is good enough for a unique identifier.

```{code-cell} ipython3
def make_date(row):
    year,month,day = row.datetime.year, row.datetime.month, row.datetime.day
    the_date = dt.date(year,month,day)
    return the_date
date_vals = scenes_van.apply(make_date, axis=1)
scenes_van['the_date']=date_vals
```

```{code-cell} ipython3
hit = scenes_van.the_date == dt.date(2015,6,14)
np.sum(hit)
my_scene = scenes_van[hit]
my_scene
```

```{code-cell} ipython3
scene_url = my_scene.iloc[0].download_url
```

* Now use the requests module to download the index.html file for the image
  and retrieve the individual bands, plus the metadata mtl file.

```{code-cell} ipython3
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
    good_bands = ['B3.TIF','B4.TIF','B5.TIF']
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
```

```{code-cell} ipython3

```
