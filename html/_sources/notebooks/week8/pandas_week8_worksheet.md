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

(week8:pandas_worksheet)=
# Week8 worksheet -- using pandas 

## Introduction

Feel free to work in groups or individually on this.  For each of the three questions below, the idea
is to figure out what the code is doing and explain it.  Upload the notebook with answers to the `~/shared_files/your_initials` folder on a301hub

To produce your own version of my "vancouver_search.csv" file, rerun the current version of {ref}`week8:fetch`
with your own lat/lon point.  You can stick with mine for this tutorial or use your own.

The notebook, groups all the satellite scenes by year and season, then goes over all the grouped dataframes,
finding the scene in each season with the smallest cloud fraction, and builds a new dataframe with
just those scenes.

```{code-cell} ipython3
import numpy
from pathlib  import Path
import inspect

from matplotlib import pyplot as plt
import numpy as np
from copy import copy

import rioxarray
import pandas as pd
import a301_lib
```

+++ {"user_expressions": []}

## Read in the dataframe

We saved the dataframe from {ref}`week8:fetch` as a csv file.  We'll set the dataframe index to the scene column
to make it easier to locate particular scenes

```{code-cell} ipython3
csv_filename = a301_lib.data_share / "pha/landsat/vancouver_search.csv"
the_df = pd.read_csv(csv_filename)
the_df = the_df.set_index('scene', drop=False)
the_df.head()
```

+++ {"user_expressions": []}

## Question 1:  What does "drop" do in the cell above?

`




`

+++ {"user_expressions": []}

## Find the low-cloud scenes

We don't have a huge number of scenes, so accept any that have less than 50% cloud cover and hope that UBC isn't under a cloud

```{code-cell} ipython3
clear_df = the_df[the_df['cloud_cover'] < 50]
len(clear_df)
```

+++ {"user_expressions": []}

## Separate the seasons with groupby

Below we use the [pandas groupby operator](https://realpython.com/pandas-groupby/)
to produce a new set of dataframes that all have the same season

```{code-cell} ipython3
season_groups = clear_df.groupby(['year','season'])
#
# season_groups is a set of dataframes, each also having a tuple giving their year and season
# we can read them into a list, and then turn that list into a dictionary of dataframes
#
season_dict = dict(list(season_groups))
season_dict.keys()
```

+++ {"user_expressions": []}

Uncomment the code below to dump the full dictionary

```{code-cell} ipython3
# for the_key, a_df in season_dict.items():
#     print(the_key, a_df)
```

+++ {"user_expressions": []}

## Find the "most interesting" scene for each season

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

+++ {"user_expressions": []}

## Question 2: Explain in words what is happening in the for loop above
`








`

```{code-cell} ipython3
def sort_col(row):
    sort_dict = {'djf':1,'mam':2,'jja':3,'son':4}
    sort_key = sort_dict[row['season']]
    row['sort_key'] = sort_key
    return row

sort_frame = new_frame.apply(sort_col,axis=1)

    
```

```{code-cell} ipython3
sorted_df = sort_frame.sort_values(by=['year','sort_key'])
sorted_df.drop('sort_key',axis=1,inplace=True)
sorted_df.head()
```

+++ {"user_expressions": []}

## Question 3: describe how the sorting works in the two cells above

Also, why is the scene index now out of chronological order?
`






`

`

```{code-cell} ipython3

```
