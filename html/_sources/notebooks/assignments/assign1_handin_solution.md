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
---

(assign1_solution)=
# Assignment 1 solution-- brightness temperatures

Upload this notebook to canvas by 11:59pm Friday January 27.

In addition, upload your MYD02 hdf file, your `chan30_31.npz` file 
and your `lonlat.npz` file (described below) to a folder that has your initials in the `sat_data` folder
in the a301hub.

+++

## Problem 1 -- lat/lon scatter plot

In the cell below, delete the text, and replace it with code that reads in your `lonlat.npz` file 
and makes a plot that shows the individual lat/lon points for the first 50 rows and columns of your Modis
granule.


To do this first modify `modis_level1b_read.md` to add a cell to dump these latitudes to a numpy npz file called `lonlat.npz`  
(you don't have to hand in the modified md file).

Then in this notebook, read in the lat/lon arrays from the `lonlat.npz` file 
and plot them.

Here is an excerpt of my code for the `modis_level1b_read.md`:
         
         # get the latitude variable
         latitude = the_file.select("Latitude")
         ...
         #read the first 50 rows and columns into a numpy array
         latitude = latitude_data[:50,:50]
         ...
         #save them to a npz file
         np.savez('lonlat.npz',longitude=longitude,latitude=latitude)
         
4 points for a correctly labeled plot with lat lon data and a title


```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-616c10d44f60728d
  locked: false
  points: 4
  schema_version: 3
  solution: true
  task: false
---
### BEGIN SOLUTION
import numpy as np
import a301_lib
from matplotlib import pyplot as plt
sat_data = a301_lib.sat_data / "pha"
lat_lon = list(sat_data.glob("lonlat.npz"))[0]
lat_lon_data = np.load(lat_lon)
longitude = lat_lon_data['longitude']
latitude = lat_lon_data['latitude']
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(longitude,latitude,'k+')
ax.set(title="lat/lons for first 50 rows and columns",
       xlabel = "longitude (degrees east)",ylabel="latitude (degrees north)");
### END SOLUTION
```

## Problem 2

In the cell below, remove the text and replace it
with a function that takes an array of MODIS radiances (MKS) and inverts each array value for the "brightness temperature.`

i.e. the top of the cell should look like:

```python
def radiance_invert(wavelength, L):
   etc.
   return Btemp
```

where L is an array of observed radiances (W/m^2/m/sr), wavelength (m) is the central wavelength of that 
satellite channel and  the function returns Btemp (K), the temperature
that a blackbody would have to have to emit that observed radiance (the brightness temperature) at each pixel.

NOTE!!-- my autograder doesn't work with `%%writefile`, so make sure you don't have that line in the cell.

I'll test the `radiance_invert` function you defined above by roundtripping it with a blackbody radiance for a particular 
temperature.

4 points for a correct function that documents the input parameters and the return value, including units.

+++





```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: cell-1f6fd5bf5abc209f
  locked: false
  schema_version: 3
  solution: true
  task: false
---
### BEGIN SOLUTION 
import numpy as np


def radiance_invert(wavel, Lstar):
    """
    Calculate the brightness temperature
    
    Parameters
    ----------

      wavel: float
           wavelength (meters)

      Lstar: float or array
           Blackbody radiance (W/m^2/m/sr)
    Returns
    -------

    Tbright:  float or arr
           brightness temperature (K)
    """
    c, h, k = 299792458.0, 6.62607004e-34, 1.38064852e-23
    c1 = 2.0 * h * c ** 2.0
    c2 = h * c / k
    sigma = 2.0 * np.pi ** 5.0 * k ** 4.0 / (15 * h ** 3.0 * c ** 2.0)
    Tbright = c2 / (wavel * np.log(c1 / (wavel ** 5.0 * Lstar) + 1.0))
    return Tbright
### END SOLUTION
```

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-5b689bd47ff974c3
  locked: true
  points: 4
  schema_version: 3
  solution: false
  task: false
---
from radiation import Elambda
wavel=10.e-6  #10 micron wavelength
the_temp = 300  #temp in K
the_flux = Elambda(wavel,the_temp)
the_radiance = the_flux/np.pi  #E = L/pi
the_new_temp = radiance_invert(wavel,the_radiance)
np.allclose(the_temp,the_new_temp);
```

+++ {"jp-MarkdownHeadingCollapsed": true, "tags": []}

## Getting the channel 30 and 31 radiance

Next, go back to {ref}`modis_level1b:function` and call the readband function again with
channel 31 to get the calibrated channel 31 radiances.  Use np.savez in the modis notebook to write
a new file with the first 50 rows and first 50 columns of the chan30 and chan31
radiances and name it `chan30_31.npz`.

+++

## Problem 3

Read in the radiances for channel 30 and channel 31 from the file `chan30_31.npz`
you created above.
In cell below use your `radiance_invert function` from  problem 2 to turn the calibrated
radiances (W/m^2/m/sr) into brightness temperatures
in Kelvins.  According to the [modis channel listings](https://modis.gsfc.nasa.gov/about/specifications.php)
the central wavelength for channel 30 is 9.73 $\mu m$ and for channel 31 it's 11.03 $\mu m$.

Make 3 plots of the temperature as an image, using a colorbar as in {ref}`modis_level1b:plot`.

* First plot:  channel 30 temperatures
* Second plot: channel 31 temperatures
* Third plot: channel 31 - channel 30 temperatures

Discuss: What is the sign of channel 31 - channel 30?  Why do you think the temperatures
are different in the two channels?

6 points for the three plots and a brief discussion.

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-0650c5eadd5c26ec
  locked: false
  points: 6
  schema_version: 3
  solution: true
  task: false
scrolled: false
---
from planck_invert import radiance_invert
import a301_lib
from matplotlib import pyplot as plt

chan_file = list(sat_data.glob("chan30_31.npz"))[0]
chan_data = np.load(chan_file)
list(chan_data.keys())
chan30 = chan_data['chan30']
chan31 = chan_data['chan31']

wavel = 9.73e-6  # wavelength in meters from Modis channel table
ch30_radiances = chan30 * 1.0e6  # convert to W/m^2/m/sr
# # convert radiance to MKS
ch30_Tbright = radiance_invert(wavel, ch30_radiances)
wavel = 11.03e-6
ch31_radiances = chan31 * 1.0e6  #convert to W/m^2/m/sr
ch31_Tbright = radiance_invert(wavel, ch31_radiances)


fig, ax = plt.subplots(1, 1, figsize=(8, 6))
CS = ax.imshow(ch30_Tbright)
cax = fig.colorbar(CS)
ax.set_title("channel 30 brightness temperature")
out = cax.ax.set_ylabel("Chan 30 Tbright (K)")
out.set_verticalalignment("bottom")
out.set_rotation(270)

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
CS = ax.imshow(ch31_Tbright)
cax = fig.colorbar(CS)
ax.set_title("channel 31 brightness temperature")
out = cax.ax.set_ylabel("Chan 31 Tbright (K)")
out.set_verticalalignment("bottom")
out.set_rotation(270)

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
CS = ax.imshow(ch31_Tbright - ch30_Tbright)
cax = fig.colorbar(CS)
ax.set_title("ch31 - ch30 ")
out = cax.ax.set_ylabel("Chan 31 - 30 Tbright difference (K)")
out.set_verticalalignment("bottom")
out.set_rotation(270)

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
CS = ax.imshow((ch31_Tbright - ch30_Tbright)/(ch31_Tbright + ch30_Tbright))
cax = fig.colorbar(CS)
ax.set_title("normalized difference")
out = cax.ax.set_ylabel("(ch31 - ch30)/(ch31 + ch30)")
out.set_verticalalignment("bottom")
out.set_rotation(270)
```
