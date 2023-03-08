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

+++ {"tags": [], "user_expressions": []}

(week8:windowed)=
# Reading landsat data with a rasterio window

## Introduction

In this notebook we demonstrate a new function called `get_landsat_scene` that
takes a geometry lon/lat, a date, and a rasterio window and creates a dictionary
with 3 DataArrays:  band4_ds, band5_ds and fmask_ds.  The fmask_ds DataArray is
processed with a new function called `get_clear_mask` that is filled with
1 where the pixel is underneath clear sky and on land, and np.nan if cloudy or over water.

In the first part we show how to create a window using our original full image and clipped image
from {ref}`week8:zoom_landsat`.  We check the window offsets by using it to make row and
column indexes for  the
raster and showing that it returns the clipped region.  Once we've got the window, we
can use it to clip from the origin scene with `rio.isel_window`

In the final part, we write `get_landsat_scene` and use it to download just the windowed
DataArrays for band4, band5 and the Fmask.

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

## Find the window

From {ref}`week8:zoom_landsat` we've got a new clipped geotiff over a much smaller area of Point Grey.  We can teach rioxarray to only fetch data that fitis into this clipped
window by using a [rasterio.window](https://rasterio.readthedocs.io/en/latest/topics/windowed-rw.html) which uses row and column offsets to specify the location of our
window on the original raster.

+++ {"user_expressions": []}

### Step 1: read in the original image and the clipped image

```{code-cell} ipython3
import a301_lib
```

```{code-cell} ipython3
#
# big original
#
landsat_dir = a301_lib.data_share / "pha/landsat"
orig_file = landsat_dir / f"vancouver_landsat8_B05.tif"
orig_ds = rioxarray.open_rasterio(orig_file,mask_and_scale=True)
orig_transform = orig_ds.rio.transform()

#
# Point Grey clipped region
#
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

+++ {"tags": [], "user_expressions": []}

### Step 3: turn the clipped image bounds into a rasterio window

Windows are constructed by passing row and column offests, the raster width and the raster
height, all in pixel counts.

We can use a rasterio utility function [rasterio.windows_from_bounds](https://rasterio.readthedocs.io/en/stable/api/rasterio.windows.html#rasterio.windows.from_bounds)
to create a window from the clipped region coordinates
and the original image transform

```{code-cell} ipython3
import rasterio
the_window = rasterio.windows.from_bounds(*clipped_bounds, 
                                        transform=orig_transform)
the_window
```

+++ {"tags": [], "user_expressions": []}

rasterio is telling us that our clipped window starts 2761 columns to the right
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

+++ {"tags": [], "user_expressions": []}

Next turn these into array slices using [windows.toslices](https://rasterio.readthedocs.io/en/latest/api/rasterio.windows.html#rasterio.windows.Window.toslices)

A python slice object allows us to pass around index ranges like `1353:1673` as objects
like `slice(1352, 1653, None)` and use them to index arrays.  The three values of
a slice object are `start,stop,step`, and `None` is the same as a stepsize of +1

```{code-cell} ipython3
row_slice, col_slice = the_window.toslices()
row_slice, col_slice
```

+++ {"user_expressions": []}

And finally use these slice objects to index the full landsat scene and see if we get our windowed
image back:

```{code-cell} ipython3
check_window = orig_ds[0,row_slice,col_slice]  #same as orig_ds[0,1352:1652,2671:2905]
check_window.plot();
```

+++ {"user_expressions": []}

So it looks like the window is correct.

+++ {"tags": [], "user_expressions": []}

## Reading data using the window

+++ {"tags": [], "user_expressions": []}

The payoff for defining the window region is that you can use it to reduce the landsat band to your clipped region with a single line of code. 

Here is how to use [rioxarray.isel_window](https://corteva.github.io/rioxarray/html/rioxarray.html#rioxarray.rioxarray.XRasterBase.isel_window)
to clip an image -- it's pretty simple:

```{code-cell} ipython3
new_clip = orig_ds.rio.isel_window(the_window)
new_clip
```

+++ {"tags": [], "user_expressions": []}

## Wrapping things up in functions

This is now getting complicated enough to write a function to encapsulate it and add to sat_lib.
Below we define `get_landsat_scene` which takes a string date,lon, lat and a rasterio window
and returns a dictionary with clipped landsat bands 4, 5 and a mask that identifies all the
clear pixels over land

+++ {"user_expressions": []}

The cell below has to be run before fetching scenes from NASA

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

+++ {"tags": [], "user_expressions": []}

### Function to mark all clear pixels over land

This function takes the fmask DataArray and returns a new array of the
same shape, but with 1 where there is no cloud over land and np.nan
otherwise

```{code-cell} ipython3
import copy
def get_clear_mask(fmask_ds):
    """
    return a DataArray copy of fmask_ds but with the pixel values set to
    1 where there is both no cloud and pixel is land, and np.nan where there is cloud
    or the pixel is water
    
    The bit patterns from the HSL QA mask are:
     
    Bits are listed from the MSB (bit 7) to the LSB (bit 0): 
    7-6    aerosol:
           00 - climatology
           01 - low
           10 - average
           11 - high
    5      water
    4      snow/ice
    3      cloud shadow
    2      adjacent to cloud
    1      cloud
    0      cirrus cloud
    
    so a bit mask of 0b00100011 when anded with a QA value
    will return non-zero when there is water, a cloud, or a cirrus cloud
    """
    #
    # convert float32 to unsigned 8 bit integer
    #
    bit_mask = fmask_ds.data.astype(np.uint8)
    ref_mask = np.zeros_like(bit_mask)
    #
    # don't destroy original fmask DataArray
    #
    clearmask_ds = copy.deepcopy(fmask_ds)
    #
    # work with unsigned 8 bit values instead of
    # base 10 floats
    #
    bit_mask = fmask_ds.data.astype(np.uint8)
    #
    # create a reference mask that will select
    # bits 5, 1 and 0, which we want tocheck
    #
    ref_mask = np.zeros_like(bit_mask)
    ref_mask[...] = 0b00100011  #find water (bit 5), cloud (bit 1) , cirrus (bit 0)
    #
    # if all three of those bits are 0, then bitwise_and will return 0
    # otherwise it will return either a value greater than 0
    #
    cloudy_values = np.bitwise_and(bit_mask,ref_mask)
    cloudy_values[cloudy_values>0]=1  #cloud or water
    cloudy_values[cloudy_values==0]=0 #rest of scene
    #
    # now invert this, writing np.nan where there is 
    # cloud or water.  Go back to float32 so we can use np.nan
    #
    clear_mask = cloudy_values.astype(np.float32)
    clear_mask[cloudy_values == 1]=np.nan
    clear_mask[cloudy_values == 0]=1
    clearmask_ds.data = clear_mask
    return clearmask_ds
    
```

+++ {"tags": [], "user_expressions": []}

### Function to get band 4, band 5 and fmask from NASA 

```{code-cell} ipython3
from pystac_client import Client
from shapely.geometry import Point
from rasterio.windows import Window

def get_landsat_scene(date, lon, lat, window):
    """
    retrieve windowed band4, band5 and Fmask for a given day and save
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
        #
        # now read the window
        #
        clipped_ds = lazy_ds.rio.isel_window(window)
        #
        # add some custom attributes
        #
        clipped_ds.attrs['date'] = props['datetime'] #date and time
        clipped_ds.attrs['cloud_cover'] = props['eo:cloud_cover']
        clipped_ds.attrs['band_name'] = chan
        utm_zone = clipped_ds.attrs['HORIZONTAL_CS_NAME'][-3:].strip()
        clipped_ds.attrs['cartopy_epsg_code'] = find_epsg_code(utm_zone)
        clipped_ds.attrs['day']=props['datetime'][:10]  #yyyy-mm-dd
        out_dict[array_name] = clipped_ds
    #
    # convert the mask to 1=no cloud over land, np.nan=otherwise
    #
    out_dict['fmask_ds'] = get_clear_mask(out_dict['fmask_ds'])
    return out_dict

from pyproj import CRS
def find_epsg_code(utm_zone, south=False):
    """
    https://gis.stackexchange.com/questions/365584/convert-utm-zone-into-epsg-code
    
    cartopy wants crs names as epsg codes, i.e. UTM zone 10N is EPSG:32610, 10S is EPSG:32710
    """
    crs = CRS.from_dict({'proj': 'utm', 'zone': utm_zone, 'south': south})
    epsg, code = crs.to_authority()
    cartopy_epsg_code = code
    return cartopy_epsg_code
```

+++ {"tags": [], "user_expressions": []}

## Fetch a date from NASA

+++ {"user_expressions": [], "tags": []}

### Add secret key file to environment

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

+++ {"user_expressions": [], "tags": []}

### download for a date, lon/lat and window

```{code-cell} ipython3
date = "2015-06-14"
#date = "2019-04-29"
lon, lat  = -123.2460, 49.2606
the_window = Window(col_off=2671, row_off=1352, width=234, height=301)
scenes_dict = get_landsat_scene(date, lon, lat, the_window)
    
```

+++ {"tags": [], "user_expressions": []}

### Check fmask 

Looks like the land pixels are correctly identified, and there are no clouds
in the scene

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
#get the first 10 characters of the time attribute for the title
the_date = scenes_dict['fmask_ds'].attrs['day']
scenes_dict['fmask_ds'].plot()
ax.set_title(f"Land/cloud mask for Landsat {the_date}");
```

```{code-cell} ipython3
scenes_dict['fmask_ds']
```
