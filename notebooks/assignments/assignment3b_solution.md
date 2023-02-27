---
celltoolbar: Create Assignment
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
toc-autonumbering: true
---

+++ 

(assign3b_solution)=
# Assignment 3b -- Solution

1) In the cells below, get channel 32 and resample to the same area_def as channel 31
2) Get the brightness temperature for both of the resampled images and the brightness tempereature difference 
   for ch32 - ch31
3) Read in the wv_ir image you get by running the wv_resample notebook, and make a scatter plot of
   ch32 - ch31 brightness temperature (in K) on the y axis and the column water vapor in cm on the x axis.  Note that
   you will need to mask the brightness temperature pixels so that only pixels which also have column water vapor are
   plotted
4) comment on the correlation you see, if any


```{code-cell} ipython3
:trusted: true

import json
from pathlib import Path
import pprint
pp = pprint.PrettyPrinter(indent=4)
import warnings
warnings.filterwarnings('ignore')
import json


import matplotlib.pyplot as plt
import numpy as np
import a301_lib
from pyresample import kd_tree, SwathDefinition

import sat_lib
from sat_lib.modischan_read import readband_lw, read_plainvar
from sat_lib import modischan_dict
from rad_lib.radiation import radiance_invert

from sat_lib.mapping import area_def_from_dict
```


+++

## Read in the channel 31 and 32 radiances and the 1 km MYD03 lons/lats

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-72f81cf1d97e3cf1
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGIN SOLUTION
geom_filelist = list(a301_lib.sat_data.glob("pha/MYD03*2105*hdf"))
radiance_filelist = list(a301_lib.sat_data.glob("pha/MYD02*2105*hdf"))
geom_file_name = geom_filelist[0]
print(geom_file_name)
radiance_file_name = radiance_filelist[0]
print(radiance_file_name)
### END SOLUTION
```

## Read in the `wv_image` raster you stored in `wv_5km_resampled.npz`

- this is the file you created in week5/wv_resample.md

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-1e0c4a33927abff3
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGIN SOLUTION
infile = a301_lib.data_share / "pha/wv_5km_resampled.npz"
the_dict = np.load(infile)
wv_image = the_dict['arr_0']
### END SOLUTION
```

## Recreate the area_def saved in your area_def json file 

- use `area_dict.json` for the 5km resample you created in
   week5/wv_resample.md and used in week5/longwave_resample.md

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-4153b9a1ac404277
  locked: false
  points: 0
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGIN SOLUTION
area_file = a301_lib.data_share / "pha/area_dict.json"
with open(area_file,'r') as infile:
    area_dict = json.load(infile)

pp.pprint(area_dict)   
area_def = area_def_from_dict(area_dict)
### END SOLUTION
```

## Get the swat_def from the 1 km lons/lats

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-7a13e107bd1d4c0d
  locked: false
  points: 1
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGIN SOLUTION
lat_1km = read_plainvar(geom_file_name,'Latitude')
lon_1km = read_plainvar(geom_file_name,'Longitude')
print(f"{lat_1km.shape=},{lon_1km.shape=}")
swath_def = SwathDefinition(lon_1km, lat_1km)
### END SOLUTION
```

## Read in channel 31 and 32 resample using your `area_def` and `swath_def`

* As in in the wv_resample notebook, use a fill_value of -9999. and replace those
  missing values with np.nan

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-5fa681cc360d1db2
  locked: false
  points: 3
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGIN SOLUTION
ch31 = readband_lw(radiance_file_name,31)
ch32 = readband_lw(radiance_file_name,32)
fill_value = -9999.
ch31_raster= kd_tree.resample_nearest(
    swath_def,
    ch31.ravel(),
    area_def,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
ch31_raster[ch31_raster == -9999.0] = np.nan
ch32_raster= kd_tree.resample_nearest(
    swath_def,
    ch32.ravel(),
    area_def,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
ch32_raster[ch32_raster == -9999.0] = np.nan
### END SOLUTION
```

## Convert the resampled ch31 and ch32 rasters to brightness temperature

- Remember that we have channel wavelenghts in `sat_lib.modischan_dict`
- I used [radiance_invert](https://phaustin.github.io/a301_web/full_listing.html#rad_lib.radiation.radiance_invert) here

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-e546d59afe09e896
  locked: false
  points: 3
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGIN SOLUTION
low31,hi31 = modischan_dict['31']['wavelength_um']
center31=(low31 + hi31)/2.
low32,hi32 = modischan_dict['32']['wavelength_um']
center31=(low31 + hi31)/2.
center32=(low32 + hi32)/2.
Tbright31_raster = radiance_invert(center31*1.e-6,ch31_raster*1.e6)
Tbright32_raster = radiance_invert(center32*1.e-6,ch32_raster*1.e6)
### END SOLUTION
```

## Plot separate histograms of your Tbright31 and Tbright32 resampled rasters

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-935a517202ab269c
  locked: false
  points: 3
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGIN SOLUTION
bins = np.arange(220,350,10)
fig, ax = plt.subplots(1,1,figsize=(6,6))
ax.hist(Tbright31_raster.flat,alpha=0.4,color='blue',label='ch31',bins=bins)
ax.hist(Tbright32_raster.flat,alpha=0.4,color='red',label='ch32',bins=bins)
ax.legend();
### END SOLUTION
```

## make a scatterplot of (Tbright32 - Tbright31) vs. wv_image

* Plot only those points which have a valid water vapor retrieval using
a  mask like this:

    hit = wv_image > 0
    wv_image[hit], Tbright31_raster[hit], Tbright32_raster[hit]
    
* Put the MYD05 IR water vapor on x axis and the Tbright32 - Tbright31 brightness temperature
  difference on the y axis
  
* Include a title and x and y axis labels with units

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-de6c7c54956ad71c
  locked: false
  points: 3
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGIN SOLUTION
hit = wv_image > 0
wv_good, Tb31good, Tb32good = wv_image[hit], Tbright31_raster[hit], Tbright32_raster[hit]
fig, ax = plt.subplots(1,1,figsize=(8,8))
ax.plot(wv_good, Tb32good - Tb31good,'r+')
ax.set(title = 'water vapor vs. Chan 32 - Chan 31 BTD for MODIS', xlabel='water vapor (cm/m^2)',
       ylabel = 'Channel 32 - Channel 31 BTD (K)');
### END SOLUTION
                
```

+++ {"nbgrader": {"grade": false, "grade_id": "cell-cdafe0dcc98fb2b6", "locked": true, "schema_version": 3, "solution": false, "task": false}}

##  Comment on any correlation you see

Answer in the cell below (convert to markdown instead of python)
If you find a correlation, how does it compare with what you would expect for the dirty window?

+++ {"nbgrader": {"grade": true, "grade_id": "cell-2fa687be02a858c6", "locked": false, "points": 3, "schema_version": 3, "solution": true, "task": false}}

Answer:  Channel 32 has more water vapor absorption, so increasing water vapor content increases the absorption in Channel 31.  Because the vapor is colder than the surface,'
emission to space is reduced, and the channel 31 brightness temperature is lower than
the surface temperature as seen in the clearer Channel 3..  This explains the negative values, and the fact that the negative magnitude becomes larger at large vapor concentrations.  There's a lot of scatter, however.
