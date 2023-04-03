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
toc-autonumbering: false
toc-showmarkdowntxt: false
---

+++ {"tags": [], "user_expressions": []}

(assign5_solution)=
# Assignment 5 Landsat + Marshall Palmer: Solution

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
import xarray

import datetime
```

+++ {"tags": [], "user_expressions": []}

# Preliminaries

There are two Landsat questions below with cells to place your code and comments.  Before you do that, you'll need to run the {ref}`week10:write_geotiff` notebook
to download your windowed landsat scenes into a folder.

There is a third question that can be uploaded as a handwritten pdf, with a cell to do the numerical integration## Preliminaries

There are two questions below with cells to place your code and comments.  Before you do that, you'll need to run the write_geotiffs.md notebook
to download your windowed landsat scenes into a folder.

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

## Make paths for input and output directories

It's a good idea to avoid clobbering your original data.  Since the files aren't huge,
it doesn't hurt to add the ndvi to the dataset and then write the new dataset into
an output folder, called `out_dir` in the sell below.  You've now got duplicate data for bands 4,5,6, and Fmask, 
but if you avoid the risk of stepping on your original files.

The `in_dir` is the directory holding your 39 downloaded 
ncfiles  written by `get_landsat_dataset`

The `out_dir` is the directory that holds the new nc files
that contain the original bands + Fmask and the ndvi dataArray
added by calc_ndvi

Note that sometimes you'll get permission and dimension errors when you try to overwrite
files in `output_dir` -- just delete the folder and rerun

+++ {"tags": [], "user_expressions": []}

## Write out the ndvi files into a new folder

### For Vancouver:

Adding some print stastements to the `calc_ndvi` loop shows that there are some problems for the Vancouver scene -- scenes
23, 31, 34 and 36 are all uncalibrated, with reflectivities that haven't been scaled to 0-> 1.
This shouldn't matter for the ndvi since the constant calibration constant is the same
for both Band 4 and Band 5 it will divide out.  

```{code-cell} ipython3
#
# my 39 geotiffs are in the folder "ndvi_geotiffs"
#
in_dir = a301_lib.data_share / "pha/landsat/ndvi_geotiffs"
#
#  I'll write my new datasets to ndvi_geotiffs_output
#
out_dir = a301_lib.data_share / "pha/landsat/ndvi_geotiffs_outdir"
in_dir.mkdir(exist_ok = True, parents=True)
out_dir.mkdir(exist_ok = True, parents=True)

write_it = False
if write_it:
    in_files = list(in_dir.glob("*nc"))
    for count,the_file in enumerate(in_files):
        the_ds = rioxarray.open_rasterio(the_file,mode = 'r',mask_and_scale = True)
        print(f"Scene {count}, Date: {the_ds.day}, maximum B05 {np.nanmax(the_ds['B05']):.2f}, cloud cover: {the_ds.cloud_cover}")
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

+++ {"tags": [], "user_expressions": []}

### Question 1 answer

My approach:  create two empty dictionaries keyed by dates.  The `scene_dict`dictionary holds each scene (so I can check the details, plot the image etc.) and the `ndvi_avg_dict` holds the average ndvi for the scene.  The dates are entered in the order
the files are listed.

```{code-cell} ipython3
def calc_avg(the_ds):
    #print(the_ds['ndvi'])
    ndvi = the_ds['ndvi'].squeeze()
    ndvi_avg = ndvi.mean(dim = ['x','y'])
    return ndvi_avg

ndvi_files = list(out_dir.glob("*.nc"))
scene_dict = {}
ndvi_avg_dict = {}
for a_file in ndvi_files:
    the_ds = rioxarray.open_rasterio(a_file,'r',mask_and_scale = True)
    the_avg = calc_avg(the_ds)
    the_date = datetime.datetime.strptime(the_ds.day,"%Y-%m-%d")
    scene_dict[the_date]=the_ds
    ndvi_avg_dict[the_date] = the_avg
    
                
```

```{code-cell} ipython3
:tags: []

len(ndvi_files)
```

+++ {"tags": [], "user_expressions": []}

## Question 2: Plot the ndvi time series

In the cell below, extract your dates from your ndvi dictionary into a list and sort them.  Then use those dates as
keys to loop over your `ndvi_avg_dict` and construct a corresponding list of ndvi values.

Plot the ndvi values as a function of date, and comment on what you see:  is there any trend?  Do the peaks
and troughs occur when you would expect them to?  Is the seasonal variablity smaller or larger than the
annual variablity?

+++ {"tags": [], "user_expressions": []}

### Question 2 answer
mall
No evidents of a longterm trend. The seasonal variablily is evident, but there are some larger fluctuations in 2014, 2022.
In most years the ndvi increases in the spring, summer and even the fall, with winter minimum values as expected, with
the exception of 2019. There are two outliers in the summer of 2015 and the winter of 2023 that look like data problems

```{code-cell} ipython3
#
# sort the datetimes so the plot values are time-ordered
#

sorted_dates = list(scene_dict.keys())
sorted_dates.sort()
```

```{code-cell} ipython3
#
# get the average ndvis in ordered by time
#
the_ndvi = []
for key in sorted_dates:
    the_ndvi.append(ndvi_avg_dict[key])
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
ax.plot(sorted_dates,the_ndvi)
ax.plot(sorted_dates,the_ndvi,'ro')
ax.grid(True)
```

+++ {"tags": [], "user_expressions": []}

### The two problem datapoints

Look at the ndvi images for winter 2023 and summer 2015 a

```{code-cell} ipython3
:tags: []

sorted_dates[-1]
```

```{code-cell} ipython3
:tags: []

last_scene = sorted_dates[-1]
dec_2022 = datetime.datetime(2022, 12, 1, 0, 0)
last_ds = scene_dict[dec_2022].squeeze()
print(f"{last_ds.cloud_cover=}")
last_ds['ndvi'].plot.imshow()
plt.title('december 2022')
```

+++ {"tags": [], "user_expressions": []}

What's the problem with 2015-07-07?  Compare July 2015 with May 2015 -- it looks like cirrus cloud went undetected by the
cloud cover algorithm and shaded the scene

```{code-cell} ipython3
:tags: []

date = datetime.datetime(2015, 7, 7, 0, 0)
july_2015_ds = scene_dict[date].squeeze()
july_2015_ds['ndvi'].plot.imshow()
plt.title('july 2015');
```

```{code-cell} ipython3
:tags: []

date = datetime.datetime(2015, 5, 20, 0, 0)
may_2015_ds = scene_dict[date].squeeze()
may_2015_ds['ndvi'].plot.imshow()
plt.title('may 2015');
```

+++ {"tags": [], "user_expressions": []}

## Question 3

+++ {"tags": [], "user_expressions": []}

 Integrate $Z=\int D^6 n(D) dD$ on paper, assuming a Marshall Palmer size distribution and show that it integrates to:

$$
Z \approx 300 RR^{1.5}
$$

with Z in $mm^6\,m^{-3}$ and RR in mm/hr.  It's helpful to know that:

$$
\int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}
$$

+++ {"tags": [], "user_expressions": []}

### Question 3 answer


$$
n(D) = n_0 \exp(-4.1 RR^{-0.21} D )
$$

with $n_0=8000$ in units of $m^{-3}\,mm^{-1}$, D in mm,
so that $\Lambda=4.1 RR^{-0.21}$ has to have units
of $mm^{-1}$.

If we use this to integrate:

$$
Z=\int D^6 n(D) dD
$$

and use the hint that

$$
\int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}
$$

with n=6 we get:

$$
Z=\frac{n_0\, 6!}{\Lambda^7}
$$

with units of  $m^{-3}\,mm^{-1}/(mm^{-1})^7=mm^6\,m^{-3}$ as required.  Since
$n_0=8000m^{-3}\,mm^{-1}$ and 6!=720, the
numerical coeficient is `8000x720/(4.1**7)=295.75` and  the final form is:

$$
Z=296 RR^{1.47}
$$

+++ {"tags": [], "user_expressions": []}

### Numerical approximation

```{code-cell} ipython3
:tags: []

#
# Marshall Palmer distribution
#
def calc_num_dist(Dvals,RR,n0=8000):
    the_dist = n0*np.exp(-4.1*RR**(-0.21)*Dvals)
    return the_dist

Dvals = np.linspace(0.01,5,1000)
dD = np.diff(Dvals)
#
# need the midpoint diameters for the rectangular integration
#
Dmid = (Dvals[1:] + Dvals[0:-1])/2.

#
# loop over 100 rain rates
#
RRvals = np.linspace(0.1,5,100)

#
# Brute force integration
#
Zvals = []
for the_RR in RRvals:
    num_dist = calc_num_dist(Dvals,the_RR)
    bin_heights = (num_dist[1:] + num_dist[0:-1])/2.
    theZ = np.sum(Dmid**6.*bin_heights*dD)
    Zvals.append(theZ)
    
fig, ax = plt.subplots(1,1)
ax.plot(RRvals,Zvals,'ro',alpha=0.4,label='numeric')
Z_math = 296*RRvals**1.47
ax.plot(RRvals,Z_math,'bx',label="math")
ax.set(xlabel="RR (mm/hour)",ylabel="Z mm^6/m^3")
ax.grid(True)
ax.legend(loc='best');
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
