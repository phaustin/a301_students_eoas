---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
numbering:
  heading_2: true
  heading_3: true
toc-autonumbering: true
---

+++ {"user_expressions": []}

(week10:write_geotiff)=
# Landsat: Writing the scenes for each season to netcdf files

## Introduction

This notebook starts with a replay of {ref}`week8:fetch` and extends it by showing how to 
write the first 5 scenes out as netcdf files that store bands 4,5 and 6 plus the Fmask

Starting in section [](#sec:week10) we demonstrate how to go through a dataframe a row at a time, fetching
the geotiffs with `get_landsat_datasets` and saving them to disk as netcdf files.  We also show
how to sort files by date in a list, using a sort key.

Edit the variables in [](#sec:loop) with your landsat specifics and rerun

At the end of a full run 10 year run, you should have about (depending on coverage)
40 separate season files in your folder.  If your window is about 230 x 300 pixels each file
should take about 0.5 Mbytes, so about 20 Mbytes for the whole folder.

```{code-cell} ipython3
import numpy
from pathlib  import Path
import inspect

from matplotlib import pyplot as plt
import numpy as np
from copy import copy
import datetime

import rioxarray
from pystac_client import Client
from shapely.geometry import Point
import a301_lib

from sat_lib.landsat_read import get_landsat_dataset
from rasterio.windows import Window
import xarray as xr

import datetime
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

+++ {"user_expressions": []}

### Store this full list as a csv file

```{code-cell} ipython3
csv_filename = a301_lib.data_share / "pha/landsat/vancouver_search.csv"
new_df.to_csv(csv_filename,index=False)
```

+++ {"user_expressions": []}

## Find the low-cloud scenes

We don't have a huge number of scenes, so accept any that have less than 50% cloud cover and hope that UBC isn't under a cloud

```{code-cell} ipython3
clear_df = new_df[new_df['cloud_cover'] < 50]
len(clear_df)
```

+++ {"user_expressions": []}

## Separate the seasons with groupby

Below we use the pandas groupby operator [https://realpython.com/pandas-groupby/](https://realpython.com/pandas-groupby/)
to produce a new set of dataframes that all have the same season

```{code-cell} ipython3
season_df = clear_df.groupby(['season_year','season'])
season_dict = dict(list(season_df))
```

```{code-cell} ipython3
season_dict[(2014,'jja')]['cloud_cover']
season_dict[(2014,'jja')].iloc[2]
```

+++ {"user_expressions": []}

(sec:week10)=
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
season_list = Path() / "save_seasons.csv"
new_frame.to_csv(season_list)
new_frame.head()
```

+++ {"user_expressions": []}

(sec:windowed_write)=
### Get the windowed region and write to netcdfs

+++ {"user_expressions": []}

We can take the code from {ref}`week9:test_dataset` to loop over the rows of the data frame
and grab the scenes.  Here's how to do it for the first 5 rows:

```{code-cell} ipython3
geotiff_dir = a301_lib.data_share / "pha/landsat/ndvi_geotiffs"
geotiff_dir.mkdir(exist_ok = True, parents=True)
```

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

+++ {"user_expressions": []}

(sec:loop)=
### Loop over each row in the dataframe and write the files

Change the `ate, lon, lat and window` for your case and turn
`do_write` to `True`

```{code-cell} ipython3
do_write=False
if do_write:
    lon, lat  = -123.2460, 49.2606
    the_window = Window(col_off=2671, row_off=1352, width=234, height=301)
    for row_num in np.arange(5,len(new_frame)):
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
all_files = list(geotiff_dir.glob("*nc"))
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

+++ {"user_expressions": []}

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
