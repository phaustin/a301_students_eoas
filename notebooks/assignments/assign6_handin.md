---
anaconda-cloud: {}
jupytext:
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
---

+++ {"tags": [], "user_expressions": []}

(assign6)=
# Assignment 6: Hurricane case study, Due Wednesday, April 12 9am

This notebook consolidates the following plots from the cloudsat notebook series into a case study for a hurricane.

Below, you are asked to recompute the following 4 plots, starting with the hdf files you've downloaded from the CDC:

1) hurricane location:  {ref}`week9:cloudsat`
1) Radar reflectivity with lidar cloudtop height (if the lidar was operating during your hurricane): {ref}`week9:cloudsat`
1) Temperature perturbation: {ref}`week10:temperature_perturb`
1) Horizontal windspeed: {ref}`week10:temperature_perturb`

and add the following 2 new plots:

1) ECMWF horizontal wind direction -- using the u and v components from the windspeed plot
1) ECMWF `Surface_pressure` and `rain_rate`

**For all plots include a title and axis labels**


I've made a fix in `read_cloudsat_var` to solve the problem of 
the missing radar bin heights at the start of some cloudsat orbits.  Do

```python
pip install -r requirements.txt --upgrade
```
to pick up this change.  You see a version greater than 0.6.0 when you do

```python
hdf4_inspect --version
```

+++ {"tags": []}

Your're asked to provide a brief discussion of the features as part of each plotting question.


All the packages you need should be imported in the cell below.

```{code-cell} ipython3
import numpy as np
import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import cm
import pandas as pd
import a301_lib
import cartopy.crs as ccrs
from sat_lib.cloudsat import add_storm_distance
from sat_lib.cloudsat import read_cloudsat_var
from sat_lib.utils.plotting import make_cmap
```

+++ {"tags": [], "user_expressions": []}

## Read and process the data to be used in the plots

### Question 1: Save all the variables you'll need for the plots in a dictionary

To make the data-processing part of the notebook as compact as possible, in the cell below
create a dictionary called `var_dict` that contains all your variables.  I did this by zipping together
my variable name list with a list of the file path for that variable, calling `read_cloudsat_var` on 
each `(path, varname)` pair, and saving the dataset in `var_dict` with the varname as key.  To see an example of
how this works, take a look at [the false color notebook](https://eoasubc.xyz/a301_2022/notebooks/week10/false_color.html#stretching-step-1-stretch-the-data-in-each-band-and-save-to-a-dictionary-with-the-band-name-as-key)

The 8 variables and their files:

- Radar_Reflectivity (from GEOPROF_GRANULE)
- LayerTop   (from GEOPROF_LIDAR if available)
- rain_rate   (from  RAΙΝ)
- Temperature  (from ECMWF-AUX)
- U_velocity   (from ECMWF-AUX)
- V_velocity   (from ECMWF-AUX)
- Surface_pressure (from ECMWF-AUX)
- rain_rate (from ECMWF-AUX)

**Note: `read_cloudsat_var` returns a dataset, not a dataArray.  To get the dataArray, you need to index by the 
variable name like this:**

```python
var_dict[varname]=read_cloudsat_var(varname,filepath)[varname]
```

Add the longitude and latitude to the dictionary.  These are available in the full dataset for any of the variables
so save them once using an arbitrary variable. Also save the day and granule_id attributes
so you can use them in titles below.

```python
the_var = read_cloudsat_var(varname,filepath)
var_dict['longitude'] = the_var['longitude']
var_dict['latitude'] = the_var['latitude']
day = the_var.day
granule_id = the_var.granule_id
```

```{code-cell} ipython3
:tags: []

#
# Question 1 code here
#
```

+++ {"tags": []}

### Question 2: clip to the storm times and add the storm distance coordinate

In the cell below, find the `time_hit` logical vector that is true only for the times between the start
and end time of your hurricane.  Using that vector, loop over your variable dictionary, and use
`xarray.isel` to 1) clip the datasets to the storm times, and 2) call `add_storm_distance` to add a new
cooridinate (see {ref}`week11:cloudsat_heat` for an example).  You can use the `.time` coordinate
from any of your variables to get the  all the timepoints for the orbit.

```{code-cell} ipython3
#
# Question 2 code here
#
```

+++ {"tags": []}

## Plots

+++ {"tags": []}

### Question 3: Huricane location, granule_id and date

Copy the code from the {ref}`week9:cloudsat` notebook.  You won't have the full orbit since you clipped it
to the hurricane times, so just plot green and red markers for the start and stop location.  Add a title with
the name of the storm, the date and the granule id

```{code-cell} ipython3
#
# Question 3 code here
#
```

+++ {"tags": []}

### Question 4: Plot `Radar_Reflectivity` and `LayerTop` (if available)

Label the x and y axis, and include a title with  date and granule id

Hint: I used `make_cmap` in my pcolormesh plots to save some lines of code setting my normalization and colormap for these figures.

**Add a brief discussion: what is the maximum radar reflectivity according to cloudsat?  How does the structure you see compare to the
idealized tropical cyclone structure of Stull Figure  16.5?  Is the radar missing significant cloud amounts that the lidar sees?**

```{code-cell} ipython3
#
# Question 4 code here, plus markdown cell for discussion
#
```

+++ {"tags": []}

### Question 5 -- Plot the temperture perturbation with title and axis labels

Use the `cm.coolwarm` colormap to plot the temperture perturbation from the ECMWF-AUX model data.

**Add a brief discussion:  Does the hurricane appear to affect the model temperture profile?  Does the location
of the minimum and maximum perturbation correspond to features in the radar reflectivity or the idealized picture of a hurricane?***

```{code-cell} ipython3
:tags: []

#
# Question 5 code here, plus markdown code for discussion
#
```

+++ {"tags": []}

### Question 6: Plot the windspeed with title and axis labels

**Add a brief discussion: what is the maximum windspeed?  Does the horizontal/vertical structure aggee with the other fields above**

```{code-cell} ipython3
:tags: []

#
# Question 6 code here, plus markdown code for discussion
#
```

+++ {"tags": []}

### Question 7: Plot the horizontal wind direction (degrees)

Plot the wind direction along the track.

**Brief discsussion:  Can you see any evidence of
cyclonic circulation in the plot?**

#### Question 7 Details


Make a xarray.plot.pcolormesh plot of the horizontal wind direction in degrees (not radians), using the [numpy arctan2](https://numpy.org/doc/stable/reference/generated/numpy.arctan2.html), i.e.

```python
wind_direction = np.arctan2(v,u)
```



The regular trigonometric angle returned by `arctan2` is not the the compass wind heading used in meteorology. 
As explained in class, these two angles are out of phase by 270 degrees.
To convert to the meteorological direction you need to adjust the phase:
$$
windangle_{met} = 270 - windangle_{trig}
$$
with the additional step that you also need to subtract 360 degrees from all $windangle_{met}$ angles larger than 360 degrees.

The table below shows how this works for the 4 principal compass points

+++ {"tags": []}

##### Wind direction table examples


| wind from | v,u wind vector  | compass heading |
| --------- | ---------------- | --------------- |
| north     | (-1,0): -90 deg  | 0 deg, 360 deg  |
| east      | (0,-1): -180 deg | +90             |
| west      | (0,1): 0 deg     | +270 deg        |
| south     | (1,0): +90 deg   | +180 deg        |

```{code-cell} ipython3
:tags: []

#
# Question 7 code here, plus markdown cell for discussion
#
```

+++ {"tags": []}

### Question 8: Plot the Surface_pressure and rain_rate

Make a 2-row plot of the Surface_pressure and rain_rate variables, i.e. create subplots that look like

```python
fig6, (ax6,ax7) = plt.subplots(2,1,figsize=(14,4))
```


**Add a brief discussion: Do you see any features in these plot consistent with the hurricane structure?**

```{code-cell} ipython3
:tags: []

#
# Question 8 code here, plus markdown code for discussion
# 
```
