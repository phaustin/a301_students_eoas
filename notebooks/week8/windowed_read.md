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

(week8:windowed)=
# Getting multiple scenes using stac

## Introduction

In this notebook we construct a set of pandas dataframes that contains a list
of all low-cloudcover satellite scenes for ubc, along with their datetime,
month, and season (winter, spring, summer, fall).  Before starting on this
notebook, it would be good to review {ref}`week6:pandas_intro`.

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

## Find the window

From {ref}`week8:zoom_landsat` we've got a new clipped geotiff over a much smaller area of Point Grey.  We can teach rioxarray to only fetch data that fitis into this clipped
window by using a [rasterio.window](https://rasterio.readthedocs.io/en/latest/topics/windowed-rw.html) which uses row and column offsets to specify the location of our
window on the original raster.

+++

### Step 1: read in the original image and the clipped image

```{code-cell} ipython3
import a301_lib
a301_lib.sat_data
dir(a301_lib)
```

```{code-cell} ipython3
landsat_dir = a301_lib.data_share / "pha/landsat"
orig_file = landsat_dir / f"vancouver_landsat8_B05.tif"
orig_ds = rioxarray.open_rasterio(orig_file,mask_and_scale=True)
orig_transform = orig_ds.rio.transform()


clipped_file = a301_lib.data_share / "pha/week8_clipped_vancouver.tif"
clipped_ds = rioxarray.open_rasterio(clipped_file, mask_and_scale=True)
clipped_transform = clipped_ds.rio.transform()
clipped_bounds = clipped_ds.rio.bounds()
```

+++ {"user_expressions": []}

### Step 2: check the orig and clipped transforms

Note that the upper left clipped window corner is east (480 km  instead of 399 km)
and south (5459 km  instead of 5500 km) of the original upper left corner, as expected

```{code-cell} ipython3
orig_transform
```

```{code-cell} ipython3
clipped_transform
```

```{code-cell} ipython3
clipped_bounds
```

### Step 3: turn the clipped image bounds into a rasterio window

We can use a rasterio utility function to create a window from the clipped region coordinates
and the original image tansform

```{code-cell} ipython3
import rasterio
the_window = rasterio.windows.from_bounds(*clipped_bounds, 
                                        transform=orig_transform)
the_window
```

+++ {"user_expressions": []}

rasterio is telling us that our clipped window starts 2761 coluumns to the right
and 1352 rows down from the upper left corner of the original raster.

+++ {"user_expressions": []}

### Step 4: make sure the window column and row offsets give us back our region

+++ {"user_expressions": []}

Here is a quick way to check that our offsets make sense.

First turn row and column  offsets, the width and the height into integers using
[window.round_offsets](https://rasterio.readthedocs.io/en/latest/api/rasterio.windows.html#rasterio.windows.Window.round_offsets)
and [window.round_lengths](https://rasterio.readthedocs.io/en/latest/api/rasterio.windows.html#rasterio.windows.Window.round_lengths)

```{code-cell} ipython3
the_window = the_window.round_lengths()
the_window = the_window.round_offsets()
the_window
```

+++ {"user_expressions": []}

Next turn these into array slices using [windows.toslices](https://rasterio.readthedocs.io/en/latest/api/rasterio.windows.html#rasterio.windows.Window.toslices)

```{code-cell} ipython3
row_slice, col_slice = the_window.toslices()
row_slice, col_slice
```

+++ {"user_expressions": []}

And finally use these slice objects to index the full landsat scene and see if we get our windowed
image back:

```{code-cell} ipython3
check_window = orig_ds[0,row_slice,col_slice]
check_window.plot();
```

So it looks like the window is correct.

+++ {"user_expressions": []}

## Reading data with the window

+++ {"user_expressions": []}

The payoff for defining the window region is that you can use it to reduce the landsat band to your clipped region with a single line of code. 

Here is how to use [rioxarray.isel_window](https://corteva.github.io/rioxarray/html/rioxarray.html#rioxarray.rioxarray.XRasterBase.isel_window)
to clip an image -- pretty simple:

```{code-cell} ipython3
new_clip = orig_ds.rio.isel_window(the_window)
new_clip
```

+++ {"user_expressions": []}

## Wrapping things up in a function

This is now getting complicated enough to write a function to encapsulate it and add to sat_lib.
Below we define `get_landsat_scene` which takes a string date,lon, lat and a rasterio window
and returns a dictionary with clipped landsat bands 4, 5 and the cloud mask

+++ {"user_expressions": []}

The cell below has to be run before fetching scenes from NASA

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

```{code-cell} ipython3
from pystac_client import Client
from shapely.geometry import Point
from rasterio.windows import Window

def get_landsat_scene(date, lon, lat, window):
    """
    retrieve band4, band5 and Fmask for a given day and save
    the clipped geotiffs into three DataArrays, returned
    in a dictionary
    
    Parameters
    ----------
    
    date: str
       date in the form yyy-mm-yy
    lon: float
       longitude of point in the scene (degrees E)
    lat: 
        latitude of point in the scene (degrees N)
    window: rasterio.Window
        window for clipping the scene to a subscene
  
    Returns
    -------
    out_dict: dict
       dictionary with three xarray DataArraysband4, band5, Fmask: rioxarrays with the data
    """
    #
    # set up the search -- we are looking for only 1 scene per date
    #
    the_point = Point(lon, lat)
    cmr_api_url = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD"
    client = Client.open(cmr_api_url)
    
    search = client.search(
        collections=["HLSL30.v2.0"],
        intersects=the_point,
        datetime= date
    )
    items = search.get_all_items()
    print(f"found {len(items)} item")
    #
    # get the metadata and add date, cloud_cover and band_name to the new DataArrays
    #
    props = items[0].properties
    out_dict = {}
    chan_names = ['B04','B05','Fmask']
    array_names = ['b4_ds','b5_ds','fmask_ds']
    for chan,array_name in zip(chan_names, array_names):
        print(f"inside get_landsat_scene: reading {chan} into {array_name}")
        href = items[0].assets[chan].href
        lazy_ds = rioxarray.open_rasterio(href,mask_and_scale=True)
        clipped_ds = lazy_ds.rio.isel_window(window)
        clipped_ds.attrs['date'] = props['datetime']
        clipped_ds.attrs['cloud_cover'] = props['eo:cloud_cover']
        clipped_ds.attrs['band_name'] = chan
        out_dict[array_name] = clipped_ds
    return out_dict
    
    
date = "2015-06-14"
date = "2019-04-29"
lon, lat  = -123.2460, 49.2606
the_window = Window(col_off=2671, row_off=1352, width=234, height=301)
scenes_dict = get_landsat_scene(date, lon, lat, the_window)
    
```

## Dump the band_4 DataArray

```{code-cell} ipython3
scenes_dict['fmask_ds']
```
