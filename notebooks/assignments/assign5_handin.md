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
numbering:
  heading_2: true
  heading_3: true
toc-autonumbering: true
---

+++ {"tags": [], "user_expressions": []}

(assign5)=
# Assignment 5 Landsat handin

+++ {"tags": [], "user_expressions": []}

## Preliminaries

There are two questions below with cells to place your code and comments.  Before you do that, you'll need to run the {ref}`week10:write_geotiff` notebook
to download your windowed landsat scenes into a folder.

(Hand in the Marshall-Palmer question in a separate notebook)

```{code-cell} ipython3
import numpy
from pathlib  import Path

from matplotlib import pyplot as plt
import numpy as np
from copy import copy
import datetime

import rioxarray
import xarray
import a301_lib

from sat_lib.landsat_read import get_landsat_dataset
```

```{code-cell} ipython3
geotiff_dir = a301_lib.data_share / "pha/landsat/ndvi_geotiffs"
all_files = list(geotiff_dir.glob("*nc"))
```

+++ {"tags": [], "user_expressions": []}

## Headstart: use this function to add masked ndvi to the dataset

Since I had some issues writing a robust ndvi function,
I've provided a working version in the cell below, with comments explaining the 
trouble points

```{code-cell} ipython3
def calc_ndvi(the_ds):
    #
    # xarray was unhappy with the extra third dimension
    # for the landsat bands:  [1, nrows, ncols]
    # so squeeze it out
    #
    the_ds = the_ds.squeeze()
    fmask = the_ds['Fmask']
    band_5 = the_ds['B05']*fmask.data
    band_4 = the_ds['B04']*fmask.data
    ndvi  = (band_5 - band_4)/(band_5 + band_4)
    #
    # Fmask doesn't find every bad pixel, so go ahead
    # and set pixels to np.nan for any ndvi not between 0-1
    #
    ndvi.data[ndvi.data < 0] = np.nan
    ndvi.data[ndvi.data > 1] = np.nan
    #
    # Make a new dataArray 
    #
    ndvi_array = xarray.DataArray(data = ndvi, dims = ["y","x"])
    #
    # you'll get nan conversion errors unless you specifiy nan as
    # your missing value
    #
    ndvi_array.rio.write_nodata(np.nan, inplace=True)
    #
    # copy the crs and affine transform from band 4
    #
    ndvi_array.rio.write_crs(band_4.rio.crs, inplace=True)
    ndvi_array.rio.write_transform(band_4.rio.transform(), inplace=True)
    #
    # add some attributes
    #
    ndvi_array = ndvi_array.assign_attrs({'day':the_ds.day,
                                          'band_name':'ndvi',
                                          'history':'written by write_ndvi notebook'})
    #
    # add the ndvi_array to the dataset and return
    #
    ndvi_dataset = the_ds.assign(variables = {'ndvi' : ndvi_array})
    return ndvi_dataset
```

+++ {"tags": [], "user_expressions": []}

## Housekeeping: separate your input and output directories

It's a good idea to avoid clobbering your original data.  Since the files aren't huge,
it doesn't hurt to add the ndvi to the dataset and then write the new dataset into
an output folder, called `out_dir` in the sell below.  You've now got duplicate data for bands 4,5,6, and Fmask, 
but if you avoid the risk of stepping on your original files.

The `in_dir` is the directory holding your 39 downloaded 
ncfiles  written by `get_landsat_dataset`

The `out_dir` is the directory that holds the new nc files
that contain the original bands + Fmask and the ndvi dataArray
added by calc_ndvi.  I use the same name, which pathlilib provides
as the `filepath.name` attribute below.

**Note that sometimes you'll get permission and dimension errors when you try to overwrite
files in `output_dir` -- just delete the folder and rerun**

```{code-cell} ipython3
#
# my 39 geotiffs are in the folder "ndvi_geotiffs"
#
in_dir = a301_lib.data_share / "pha/landsat/ndvi_geotiffs"
#
#  I'll write my new datasets to ndvi_geotiffs_output
#
out_dir = a301_lib.data_share / "pha/landsat/ndvi_geotiffs_output"
in_dir.mkdir(exist_ok = True, parents=True)
out_dir.mkdir(exist_ok = True, parents=True)

write_it = True
if write_it:
    in_files = list(in_dir.glob("*nc"))
    for the_file in in_files:
        the_ds = rioxarray.open_rasterio(the_file,mode = 'r',mask_and_scale = True)
        #
        # Give the file the same name, but put it in the new folder
        #
        out_file = out_dir / the_file.name
        new_ds = calc_ndvi(the_ds)
        new_ds.to_netcdf(out_file)
```

+++ {"tags": [], "user_expressions": []}

## Question 1: Calculate the average ndvi

In the cell below write a function takes a dataset with an ndvi array and returns
the area average ndvi (consult the docs for `xarray.DataArray.mean`)

Use it to loop through all of the datasets and create two dictionaries,
one holding the datasets (with the datetime date as the key) and one holding the
ndvi average for that dataset (also with the datetime date as the key).

Recall from the write_geotiffs notebook that you can convert the `dataset.day` attribute
to a datetime object using `strptime`:

```python
the_date = datetime.datetime.strptime(x,"%Y-%m-%d")
```

Don't forget to open your files with `mask_and_scale = True` so you get floating point
values with np.nan for missing pixels

```python
the_ds = rioxarray.open_rasterio(a_file,'r',mask_and_scale = True)
```

```{code-cell} ipython3
# Question 1 answer here
```

+++ {"tags": [], "user_expressions": []}

## Question 2: Plot the ndvi time series

In the cell below, extract your dates from your ndvi dictionary into a list and sort them.  Then use those dates as
keys to loop over your `ndvi_avg_dict` and construct a corresponding list of ndvi values.

Plot the ndvi values as a function of date, and comment on what you see:  is there any trend?  Do the peaks
and troughs occur when you would expect them to?  Is the seasonal variablity smaller or larger than the
annual variablity?

```{code-cell} ipython3
# Question 2 answer here
```


## Marshall-Palmer question

2) Integrate $Z=\int D^6 n(D) dD$ on paper, assuming a Marshall Palmer size distribution and show that it integrates to:

$$
Z \approx 300 RR^{1.5}
$$

with Z in $mm^6\,m^{-3}$ and RR in mm/hr.  It's helpful to know that:

$$
\int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}
$$

2) Repeat using numerical integration in python (i.e. np.diff and np.sum) and show that the
   the result agrees.
