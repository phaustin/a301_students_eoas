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
---

+++ {"user_expressions": []}

(week8:fetch)=
# Getting multiple scenes using stac

## Introduction

In this notebook we construct a set of pandas dataframes that contains a list
of all low-cloudcover satellite scenes for ubc, along with their datetime,
month, and season (winter, spring, summer, fall).  Before starting on this
notebook, it would be good to review {ref}`week6:pandas_intro`.


March 17, 2023:  introduced "season_year" column to account for the fact that winter begins december but
continues into the next year.

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

```{code-cell} ipython3
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
season_dict
```

+++ {"user_expressions": []}

## Storing the dataframe as a csv file

Since it takes a while to do this search, we'll save a copy of the dataframe for future reference

```{code-cell} ipython3
csv_filename = a301_lib.data_share / "pha/landsat/vancouver_search.csv"
the_df.to_csv(csv_filename,index=False)
```

```{code-cell} ipython3
season_dict
```

```{code-cell} ipython3
season_dict[(2014,'jja')]['cloud_cover']
season_dict[(2014,'jja')].iloc[2]
```
