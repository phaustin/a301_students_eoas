---
anaconda-cloud: {}
jupytext:
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
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

(week12:assign6_solution)=
# Assignment 6: Hurricane case study solution
This notebook consolidates the following plots from the cloudsat notebook series into a case study for a hurricane.

Below, you are asked to recompute the following 6 plots, starting with the hdf files you've downloaded from the CDC:

1) hurricane location:  {ref}`week9:cloudsat`
1) Radar reflectivity with lidar cloudtop height (if the lidar was operating during your hurricane): {ref}`week9:cloudsat`
1) Surface Rainrate and liquid water precipitation with zero degree isotherm:  {ref}`week10:radar_micro`
1) Temperature perturbation and horizontal windspeed: {ref}`week10:temperature_perturb`

and add the following 3 new plots:

1) ECMWF horizontal wind direction -- using the u and v components from the windspeed plot
1) ECMWF `Surface_pressure`
1) ECMWF `Sea_surface_temperature`


I've made a fix in `read_cloudsat_var` to solve the problem of 
the missing radar bin heights at the start of some cloudsat orbits.  Do

```python
pip install -r requirements.txt --upgrade
```
to pick up this change.  You see a version greater than 0.6.0 when you do

```python
hdf4_inspect --version
```

+++ {"user_expressions": []}

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

+++ {"user_expressions": []}

## Read and process the data to be used in the plots

### Question 1: Save all the variables you'll need for the plots in a dictionary

To make the data-processing part of the notebook as compact as possible, in the cell below
create a dictionary called `var_dict` that contains all your variables.  I did this by zipping together
my variable name list with a list of the file path for that variable, calling `read_cloudsat_var` on 
each `(path, varname)` pair, and saving the dataset in `var_dict` with the varname as key.  To see an example of
how this works, take a look at [the false color notebook](https://eoasubc.xyz/a301_2022/notebooks/week10/false_color.html#stretching-step-1-stretch-the-data-in-each-band-and-save-to-a-dictionary-with-the-band-name-as-key)

The nine variables and their files:

- Radar_Reflectivity (from GEOPROF_GRANULE)
- LayerTop   (from GEOPROF_LIDAR if available)
- rain_rate   (from  RAΙΝ)
- precip_liquid_water  (from RAIN)
- Temperature  (from ECMWF-AUX)
- U_velocity   (from ECMWF-AUX)
- V_velocity   (from ECMWF-AUX)
- Surface_pressure (from ECMWF-AUX)
- Sea_surface_temperature (from ECMWF-AUX)

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

+++ {"user_expressions": []}

#### Question 1 answer

The for loop zips together the variables and their files, and then fills a dictionary
with the xarray for each varable.  The Calypso lidar wasn't working for Hurricane Michael, so no LayerTop variable.

```{code-cell} ipython3
#
#Question 1 code here
#
cloudsat_dir = a301_lib.data_share / "pha/cloudsat"
rain_file = list(cloudsat_dir.glob("*2018*RAIN*hdf"))[0]
radar_file = list(cloudsat_dir.glob("*2018*GEOPROF*hdf"))[0]
ecmwf_file = list(cloudsat_dir.glob("*2018*ECMWF*hdf"))[0]
var_list = ['Radar_Reflectivity','rain_rate','precip_liquid_water','Temperature','U_velocity',
                    'V_velocity','Surface_pressure','Sea_surface_temperature']
file_paths =[radar_file,rain_file,rain_file,ecmwf_file,ecmwf_file,ecmwf_file,ecmwf_file,ecmwf_file]
var_dict={}
for varname,filepath in zip(var_list,file_paths):
    var_dict[varname]=read_cloudsat_var(varname,filepath)[varname]

the_var = read_cloudsat_var(varname,filepath)
var_dict['longitude'] = the_var['longitude']
var_dict['latitude'] = the_var['latitude']
day = the_var.day
granule_id = the_var.granule_id
```

```{code-cell} ipython3
radar_file
```

+++ {"user_expressions": []}

### Question 2: clip to the storm times and add the storm distance coordinate

In the cell below, find the `time_hit` logical vector that is true only for the times between the start
and end time of your hurricane.  Using that vector, loop over your variable dictionary, and use
`xarray.isel` to 1) clip the datasets to the storm times, and 2) call `add_storm_distance` to add a new
cooridinate (see {ref}`week11:cloudsat_heat` for an example).  You can use the `.time` coordinate
from any of your variables to get the  all the timepoints for the orbit.

+++ {"user_expressions": []}

#### Question 2 Answer

From the Orbit 66309 quicklook I get a start time of 19:13:20 UCT, and a length of about 3 minutes.
The for-loop below clips each of the DataArrays to that interval using isel.

```{code-cell} ipython3
#
# Question 2 code here
#
all_times = pd.to_datetime(var_dict['precip_liquid_water'].time)
first_time = all_times[0]
print(f'orbit start: {first_time}')
#
# clipping index 6:45 - 6:48
#
start_hour=19
start_minute=13
storm_start=starttime=dt.datetime(first_time.year,first_time.month,first_time.day,
                                        start_hour,start_minute,20)
#
# get 3 minutes of data from the storm_start
#
storm_stop=storm_start + dt.timedelta(minutes=3)

time_hit = np.logical_and(all_times >= storm_start, all_times <= storm_stop)
for key, the_ds in var_dict.items():
    clipped_ds = the_ds.isel(indexers = {'time':time_hit})
    clipped_ds = add_storm_distance(clipped_ds)
    var_dict[key] = clipped_ds
```

+++ {"user_expressions": []}

## Plots

+++ {"user_expressions": []}

### Question 3: Huricane location, granule_id and date

Copy the code from the {ref}`week9:cloudsat` notebook.  You won't have the full orbit since you clipped it
to the hurricane times, so just plot green and red markers for the start and stop location.  Add a title with
the name of the storm, the date and the granule id

+++ {"user_expressions": []}

#### Question 3 answer

Cloudsat is in the ascending part of its orbit, crossing the equator from south to north.  From the 
[goes_michael](https://eoasubc.xyz/a301_2022/notebooks/week12/goes_michael.html#add-the-cloudsat-ground-track)
notebook in week 12 we know that the ground track passes on the east side of the eyewall.

```{code-cell} ipython3
#
# Question 3 code here
#
projection=ccrs.Robinson()
transform = ccrs.Geodetic()
fig, ax = plt.subplots(1,1,figsize=(12,6.5), subplot_kw = {'projection': projection})
# make the map global rather than have it zoom in to
# the extents of any plotted data
ax.set_global()
ax.stock_img()
ax.coastlines()
longitude = var_dict['longitude']
latitude = var_dict['latitude']
ax.plot(longitude,latitude,'r',lw=5,transform =  transform);
ax.plot(longitude[0],latitude[0],'go',markersize=10, transform=transform)
ax.plot(longitude[-1],latitude[-1],'ro',markersize=10, transform=transform)
ax.set_title(f"Hurricane Michael on {day}, granule_id={granule_id}");
```

+++ {"user_expressions": []}

### Question 4: Plot `Radar_Reflectivity` and `LayerTop` (if available)

Label the x and y axis, and include a title with  date and granule id

Hint: I used `make_cmap` in my pcolormesh plots to save some lines of code setting my normalization and colormap for these figures.

**Add a brief discussion: what is the maximum radar reflectivity according to cloudsat?  How does the structure you see compare to the
idealized tropical cyclone structure of Stull Figure  16.5?  Is the radar missing significant cloud amounts that the lidar sees?**

+++ {"user_expressions": []}

#### Q4 Answer

The part of the hurricane imaged by cloudsat is about 900 km long (including the anvil), with one convective overshooting plume and several high reflectivity bands of about 20-30 km width.  This
is similar to the idealized picture in Stull Figure 16.5, with cloudsat passing to one side of the eyewall. The histogram below shows reflectivities greater than 150 dbZ, but that looks like noise, since here is a large gap between 50 dbZ and 150 dbZ.  Excluding those values  in the cell below I get a maximum reflectivity of about 53 dBz.

+++ {"user_expressions": []}

```{figure} figures/stull_hurricane.png
:width: 50%
:name: Stull Chapter 16 hurricane

Idealized hurricane structure (Stull Figure 16.5)
```

```{code-cell} ipython3
#
# Question 4 code here
#
vmin=-5
vmax= 25
fig1, ax1 = plt.subplots(1,1,figsize=(14,4))
radar_z = var_dict['Radar_Reflectivity']
the_norm, cmap = make_cmap(vmin,vmax,missing='0.7')
radar_z.T.plot.pcolormesh(x='storm_distance',y='height_km',
                   ax=ax1,cmap = cmap, norm=the_norm)
ax1.set(ylim=[0,17],xlabel = "distance (km)",ylabel="height (km)",
       title = f"radar reflectivity (dbZ) on {day}, granule {granule_id}");
```

```{code-cell} ipython3
plt.hist(radar_z.data.ravel());
```

```{code-cell} ipython3
hit = radar_z.data < 100
maxz = np.max(radar_z.data[hit])
print(f"max radar reflectivity: {maxz} dbZ")
```

+++ {"user_expressions": []}

### Question 5 -- Plot the temperture perturbation

Use the `cm.coolwarm` colormap to plot the temperture perturbation from the ECMWF-AUX model data.

**Add a brief discussion:  Does the hurricane appear to affect the model temperture profile?  Does the location
of the minimum and maximum perturbation correspond to features in the radar reflectivity or the idealized picture of a hurricane?***

+++ {"user_expressions": []}

#### Question 5 answer

There is a large positive temperature perturbation in the eyewall at 610 km due to condensation heating.  In the anvil, there's a
8 degree temperature contrast as the satellite passes the eye of the hurricane from the south to the north.

```{code-cell} ipython3
#
# Question 5 code here
#
temperature = var_dict['Temperature']
temperature = temperature - 273.15
temp_profile=temperature.mean(dim='time')
temp_perturb = temperature - temp_profile
```

```{code-cell} ipython3
vmin=-4
vmax=4
the_norm, cmap = make_cmap(vmin,vmax, cmap= cm.coolwarm)
fig2, ax2 = plt.subplots(1,1,figsize=(14,4))
col = temp_perturb.T.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax2, cmap = cmap, norm=the_norm)
ax2.set(ylim = [0,20], xlabel = "distance (km)", ylabel = "height (km)",
         title = f"temperature perturbation (K) on {day}, granule {granule_id}");
```

+++ {"user_expressions": []}

### Question 6: Plot the windspeed with title

**Add a brief discussion: what is the maximum windspeed?  Does the horizontal/vertical structure aggee with the other fields above**

+++ {"user_expressions": []}

#### Question 6 answer

The circulation around the eye is clearly visible in the model. Maximum windspeed of 40 m/s (144 km/hour).

```{code-cell} ipython3
uvel = var_dict['U_velocity']
vvel = var_dict['V_velocity']
wind_speed = np.sqrt(uvel**2. + vvel**2.)
np.nanmax(wind_speed)
```

```{code-cell} ipython3
vmin=0
vmax= 43
the_norm, cmap = make_cmap(vmin,vmax)
fig3, ax3 = plt.subplots(1,1,figsize=(14,4))
col = wind_speed.T.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax3, cmap = cmap,  norm  = the_norm,
                                  cbar_kwargs={ "label":"wind speed (m/s)"})
ax3.set(ylim=[0,17],
       xlabel='distance (km)',ylabel='height (km)',
       title=f"ECMWF wind speed (m/s) for granule {granule_id} on {day}");
```

+++ {"user_expressions": []}

### Question 7: Plot the horizontal wind direction (degrees)

Plot the wind direction along the track.

**Brief discsussion:  Can you see any evidence of
cyclonic circulation in the plot?**

+++ {"user_expressions": []}

#### Question 7 answer

The wind-direction is consistent with the groundtrack going from south to north with a counter-clockwise circulation.  For the the first half of the track 
the wind is from about 225 degrees, that is, from the southwest.  Once the track passes the eye it shifts abruptly to about 45 degrees from the northeast.

+++ {"user_expressions": []}

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

+++ {"user_expressions": []}

##### Wind direction table examples


| wind from | v,u wind vector  | compass heading |
| --------- | ---------------- | --------------- |
| north     | (-1,0): -90 deg  | 0 deg, 360 deg  |
| east      | (0,-1): -180 deg | +90             |
| west      | (0,1): 0 deg     | +270 deg        |
| south     | (1,0): +90 deg   | +180 deg        |

```{code-cell} ipython3
wind_dir = np.arctan2(vvel,uvel)*180./np.pi
the_data = wind_dir.data
the_data = 270 - the_data
hit = the_data > 360
the_data[hit] = the_data[hit] - 360
wind_dir.data = the_data
```

```{code-cell} ipython3
vmin=0
vmax= 360
the_norm, cmap = make_cmap(vmin, vmax, under = 'r', over='r',cmap=cm.coolwarm)
fig4, ax4 = plt.subplots(1,1,figsize=(14,4))
col = wind_dir.T.plot.pcolormesh(x='storm_distance',y='height_km',ax=ax4, cmap = cmap,  norm  = the_norm,
                                  cbar_kwargs={ "label":"wind direction (degrees)"})
ax4.set(ylim=[0,17],
       xlabel='distance (km)',ylabel='height (km)',
       title=f"ECMWF wind direction (arctan2 degrees) for granule {granule_id} on {day}");
```

+++ {"user_expressions": []}

### Question 8: Plot the Surface_pressure and Sea_surface_temperature

Make a 2-row plot of the Surface_pressure and Sea_surface temperature variables, i.e. create subplots that look like

```python
fig6, (ax6,ax7) = plt.subplots(2,1,figsize=(14,4))
```

**Add a brief discussion: Do you see any features in these plot consistent with the hurricane structure?**

+++ {"user_expressions": []}

#### Question 8 answer

The minimum pressure is located right at the point the wind direction changes sign, as expected.  The rain rate is higher on the north side of the of the
ground track, because the much of the south side exceeeded the limits of the cloudsat precipitation retrieval.

```{code-cell} ipython3
fig6, (ax6,ax7) = plt.subplots(2,1,figsize=(14,4))
storm_pressure = var_dict['Surface_pressure']
storm_pressure.plot(x="storm_distance",ax=ax6)
ax6.set(title = "ECMWF Surface_pressure (PA)",ylabel="pressure (Pa)",xlabel="distance (km)");
rain_rate = var_dict['rain_rate']
rain_rate.plot(x="storm_distance",ax=ax7)
ax7.set(title = "Rain rate (mm/hour)",ylabel="rain rate",xlabel="distance (km)")
ax7.set(ylim=(0,10))
fig6.tight_layout()
```

```{code-cell} ipython3

```
