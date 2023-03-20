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
---

+++ {"user_expressions": []}

(week10:write_geotiff)=
# Writing the scenes for each season to geotiffs

## Introduction

This notebook starts with a replay of {ref}`week8:fetch` and extends it by showing how to 
write the first 5 scenes out as geottif files.

```{code-cell} ipython3
import numpy
from pathlib  import Path
import inspect

from matplotlib import pyplot as plt
import numpy as np
from copy import copy

import rioxarray
from pystac_client import Client
from shapely.geometry import Point
import a301_lib

from sat_lib.landsat_read import get_landsat_dataset
from rasterio.windows import Window
import xarray as xr
```

+++ {"user_expressions": []}

## Ask for all UBC scenes from 2013 to 2022

```{code-cell} ipython3
the_lon, the_lat = -123.2460, 49.2606
location = Point(the_lon, the_lat)
date_range = "2013-01-01/2022-12-31"
#
# filename to save the dataframe for future analysis
#
csv_filename = a301_lib.data_share / "pha/landsat/vancouver_search.csv"
```

```{code-cell} ipython3
# connect to the STAC endpoint
cmr_api_url = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD"
client = Client.open(cmr_api_url)
```

+++ {"user_expressions": []}

## Start the search

The client takes the search parameters as the following keywords:

```{code-cell} ipython3
search = client.search(
    collections=["HLSL30.v2.0"],
    intersects=location,
    datetime= date_range
) 
search
```

+++ {"user_expressions": []}

### get the metadata for search items

This search should find 388 scenes that contain UBC

```{code-cell} ipython3
items = search.get_all_items()
print(len(items))
```

+++ {"user_expressions": []}

### Put the results into a list of scenes

In this cell, we go over the properties for each scene
and store them in a dict -- converting the datetime
(which is retrieved as a string of characters) into
a python datetime object using the `str_to_datetime` function

```{code-cell} ipython3
import pystac
scene_list = []
for index, value in enumerate(items):
    props = value.properties
    the_date = pystac.utils.str_to_datetime(props['datetime'])
    scene_dict = dict(scene = index,
                      cloud_cover = props['eo:cloud_cover'],
                      datetime = the_date 
                       )
    scene_list.append(scene_dict)
    
```

```{code-cell} ipython3
scene_list[0]
```

+++ {"user_expressions": []}

## Creating the dataframe

We can make a dataframe from a list of dictionaries, using the `from_records` constructor

```{code-cell} ipython3
import pandas as pd
the_df = pd.DataFrame.from_records(scene_list)
the_df.head()
```

+++ {"user_expressions": []}

## Add seasons and month columns to the clear_df

The `make_seasoncol` function finds the season for each scene
by using the month number -- January-December are months 1-12

```{code-cell} ipython3
def make_seasoncol(row):
    seasons = {'djf':[12,1,2],
               'mam':[3,4,5],
               'jja':[6,7,8],
               'son':[9,10,11]}
    for season,months in seasons.items():
        month = row['datetime'].month
        year = row['datetime'].year
        if month in months:
            #
            # the winter of 2013 begins in
            # december 2012.  So the year of the
            # scene and the year of the season diverge
            #
            if month == 12:
                row['season_year'] = year + 1
            else:
                row['season_year'] = year
            row['season']=season
            row['year']= year
            row['month']= month
            row['day']= row['datetime'].day
    return row

new_df = the_df.apply(make_seasoncol,axis=1)
new_df = new_df[['scene','cloud_cover','season','year','season_year','month','day']]
new_df.head()
```

+++ {"tags": [], "user_expressions": []}

### Store this full list as a csv file

```{code-cell} ipython3
csv_filename = a301_lib.data_share / "pha/landsat/vancouver_search.csv"
new_df.to_csv(csv_filename,index=False)
```

+++ {"user_expressions": []}

## Find the low-cloud scenes

We don't have a huge number of scenes, so accept any that have less than 50% cloud cover and hope that UBC isn't under a cloud

```{code-cell} ipython3
clear_df = the_df[the_df['cloud_cover'] < 50]
len(clear_df)
```

+++ {"user_expressions": []}

## Separate the seasons with groupby

Below we use the pandas groupby operator https://realpython.com/pandas-groupby/
to produce a new set of dataframes that all have the same season

```{code-cell} ipython3
season_df = new_df.groupby(['season_year','season'])
season_dict = dict(list(season_df))
```

```{code-cell} ipython3
season_dict[(2014,'jja')]['cloud_cover']
season_dict[(2014,'jja')].iloc[2]
```

+++ {"tags": [], "user_expressions": []}

## New for week10: Write one scene for each season
Take the code from {ref}`week8:pandas_worksheet` to locate the lowest cloud fraction for each season
and save to a new dataset

```{code-cell} ipython3
def find_min(a_df):
    """
    What does this function do?
    """
    min_row = a_df['cloud_cover'].argmin()
    return min_row

#
# explain this loop
#
out_list = []
for the_key, a_df in season_dict.items():
    min_row = find_min(a_df)
    min_scene = a_df.iloc[min_row]
    the_series = pd.Series(min_scene)
    out_list.append(the_series)
    
new_frame = pd.DataFrame.from_records(out_list, index='scene')

new_frame.head()
```

+++ {"tags": [], "user_expressions": []}

### Get the windowed region and write to netcdfs

+++ {"tags": [], "user_expressions": []}

We can take the code from {ref}`week9:test_dataset` to loop over the rows of the data frame
and grab the scenes.  Here's how to do it for the first 5 rows:

+++ {"user_expressions": []}

### Move the write code from {ref}`week9:test_dataset` to a function

+++ {"user_expressions": []}

def write_dataset(the_ds,filepath,date, lon, lat, the_window):
    scenes_data = get_landsat_dataset(date, lon, lat, the_window) 
    #
    # write out the file for reuse
    #
    scenes_data.to_netcdf(filepath)
    return None

+++ {"tags": [], "user_expressions": []}

### Make a directory to hold the datasets

```{code-cell} ipython3
geotiff_dir = a301_lib.data_share / "pha/landsat/ndvi_geotiffs"
geotiff_dir.mkdir(exist_ok = True, parents=True)
```

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

+++ {"tags": [], "user_expressions": []}

### Loop over each row in the dataframe and write the files

```{code-cell} ipython3
date = "2015-06-14"
lon, lat  = -123.2460, 49.2606
the_window = Window(col_off=2671, row_off=1352, width=234, height=301)
for row_num in np.arange(0,5):
    row = new_frame.iloc[row_num]
    year,month,day = row['year'],row['month'],row['day']
    the_date = f"{year:02d}-{month:02d}-{day:02d}"
    the_scene = get_landsat_dataset(the_date, lon, lat, the_window) 
    file_path = geotiff_dir / f"landsat_{the_date}_vancouver.nc"
    print(f"saving to {file_path}")
    the_scene.to_netcdf(file_path)
```

+++ {"user_expressions": []}

## Check: read the datasets back into a dictionary

Make sure we can read these back into a dictionary indexed by the date

```{code-cell} ipython3
all_files = list(geotiff_dir.glob("landsat*vancouver*nc"))
print(all_files)
```

```{code-cell} ipython3
scene_dict = {}
for the_file in all_files:
    the_ds = rioxarray.open_rasterio(the_file)
    the_key = the_ds.day
    scene_dict[the_key] = the_ds
```

```{code-cell} ipython3
scene_dict.keys()
```

### Sort the keys by date

Note that the file listing code doesn't sort the dates in time order
We can fix that by defining a sort function that returns a datetime object
instead of a character string using [datetime.strptime](https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime)

```{code-cell} ipython3
def date_sort(x):
    the_date = datetime.datetime.strptime(x,"%Y-%m-%d")
    return the_date
```

```{code-cell} ipython3
sorted_keys = list(scene_dict.keys())
sorted_keys.sort(key=date_sort)
print(sorted_keys)
```
