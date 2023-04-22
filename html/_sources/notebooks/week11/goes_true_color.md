---
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

(week11:goes_true_color)=
# GOES-16: True Color Images from GOES ABI

## Introduction

This is a modified version of [Brian Blaylock's](http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/home.html)
[UCAR python gallery](https://unidata.github.io/python-gallery/examples/mapping_GOES16_TrueColor.html) notebook. 
Blaylock is the author of the GOES download package [goes2go](https://goes2go.readthedocs.io/en/latest/) used below.
I've made some changes to the notebook to expand the explanations and to port to rioxarray.

The notebook shows how to make a true color image from the GOES-16
Advanced Baseline Imager (ABI) level 2 data. We will plot the image with
matplotlib and Cartopy. The image can be displayed on any map projection after
applying a transformation.

Some background:  Take a look at the 16 channels described on page 230 of [Stull Chapter 8](https://www.eoas.ubc.ca/books/Practical_Meteorology/prmet102/Ch08-satellite_radar-v102b.pdf).  Note that
unlike Modis or Landsat OLI, the ABI doesn't have a visible channel at green wavelengths, substituting
the near-ir 0.846--0.885  $\mu m$ wavelength range for green.  Since that channel is very responsive to
plant chlorophyll it's possible to still  use that as part of a proxy for green as shown below.  As of this
January, GOES 18 is now GOES West, and GOES 16 is GOES East, with GOES 17 moved into a parking position.
For more background on GOES, see [NOAA's beginner guide to GOES](https://www.goes-r.gov/downloads/resources/documents/Beginners_Guide_to_GOES-R_Series_Data.pdf).  

We will be using the [Advanced Baseline Imager Level 2 Cloud and Moisture Product](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C01502) from the [Amazon AWS GOES repository](https://registry.opendata.aws/noaa-goes/).  The
full list of available GOES products on AWS is [here](https://github.com/awslabs/open-data-docs/tree/main/docs/noaa/noaa-goes16).

The file we'll download is the "Cloud Moisture Imagery" dataset -- abbreviated `ABI-L2-MCMIPC`
which expands to "Advanced Baseline Imager level 2 Cloud Moisture Imagery Product for the
Continental US".  It's  about 68 Mbytes, compared to the full disk file (`ABI-L2-MCMIPC`) which
is about 305 Mbytes.  A folder called `~/data` will be created to hold the download.

+++ {"user_expressions": []}

## Relationship to previous notebooks

* For a review of working with mapping using the cartopy crs and an image: 
  - {ref}`week7:geotiff_xarray`
  - {ref}`week9:test_dataset`
  
* For a review of using an indexer and xarray.isel to clip a dataset to a coordinate

  - {ref}`week10:radar_micro`
  
* For a review of false color and image stacking

  - {ref}`week10:false_color`

+++ {"user_expressions": []}

## Channels and workflow

+++ {"user_expressions": []}

These are the channels that contribute to the true-color composite:


|        --| Wavelength   | Channel | Description |
|----------|:------------:|:-------:|:-----------:|
| **Red**  | 0.64 &#181;m |    2    | Red Visible |
| **Green**| 0.86 &#181;m |    3    | Veggie Near-IR|
| **Blue** | 0.47 &#181;m |    1    | Blue Visible|


The workflow for the notebook:

0) Download a scene using [goes2go](https://goes2go.readthedocs.io/en/latest/)

1) Read the metadata and channels into xarray datasets using xarray and rioxarray

2) Create a cartopy crs for the scene using the crs and extent of the image

3) Produce a weighted "pseudo-green" image using a weighted combination of the 3 bands

4) Clip the band values to 0-1 and apply a "gamma correction" (an alternative to histogram equalization, we used
in {ref}`week10:false_color`)

5) Stack the 3 bands in rgb order using [numpy depth stacking](https://numpy.org/doc/stable/reference/generated/numpy.dstack.html)

6) Plot the mapped image using cartopy

7) Zoom the image by changing the axis extent

```{code-cell} ipython3
from goes2go.data import goes_nearesttime
import rioxarray
import xarray
import a301_lib
from datetime import datetime, timedelta
from pathlib import Path
import cartopy
from pyresample.utils.cartopy import Projection
import numpy as np

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path
```

+++ {"user_expressions": []}

## Read in the data

We're going to need to read the data twice -- once with `xarray.open_dataset` to get all the channel wavelengths
and once with `rioxarray.open_rasterio` to get the crs and transform.  The bands are labeled `CMI_C01`, `CMI_C02` etc.
Each band has data quality flag file `DQF_C01`, `DQF_C02` etc.

```{code-cell} ipython3
g = goes_nearesttime(
    datetime(2020, 6, 25, 18), satellite="goes16",product="ABI-L2-MCMIP", domain='C', 
      return_as="xarray"
)
```

+++ {"user_expressions": []}

By default the files are written into a folder called `~/data`

```{code-cell} ipython3
full_path = Path.home() / "data" / g.path[0]
full_path
```

+++ {"user_expressions": []}

This example uses the **level 2 _multiband_ formatted file for the continental US (C)
domain** 

Here's the naming scheme for files

    OR_ABI-L2-MCMIPC-M3_G16_s20181781922189_e20181781924562_c20181781925075.nc

    OR     - Indicates the system is operational  
    ABI    - Instrument type  
    L2     - Level 2 Data  
    MCMIP  - Multichannel Cloud and Moisture Imagery products  
    C     - CONUS file (created every 5 minutes) or F (full disk)
    M3     - Scan mode  
    G16    - GOES-16  
    s##### - Scan start: 4 digit year, 3 digit day of year (Julian day), hour, minute, second, tenth second  
    e##### - Scan end  
    c##### - File Creation  
    .nc    - NetCDF file extension

+++ {"user_expressions": []}

Note that goesC has the `rio` has the `goes_imager_projection` variable, while
`goesC` has many more variables.

Open both rio and dataset verisons of the file

```{code-cell} ipython3
goesC = xarray.open_dataset(full_path,mode = 'r',mask_and_scale = True)
rioC = rioxarray.open_rasterio(full_path,'r',mask_and_scale = True)
goesC = goesC.squeeze()
rioC = rioC.squeeze()
rioC
```

```{code-cell} ipython3
goesC
```

+++ {"user_expressions": []}

### data crs

This is the "Geostationary Satellite" projection, centered over the central US (where GOES 16 is stationed) at a longitude of -75 degrees

```{code-cell} ipython3
rioC.rio.crs
```

```{code-cell} ipython3
rioC['CMI_C01'].shape
```

+++ {"user_expressions": []}

## Get the extent and the crs, and create a cartopy crs

The data projection is

```{code-cell} ipython3
ll_x, ll_y, ur_x, ur_y = rioC.rio.bounds()
original_extent = (ll_x,ur_x, ll_y, ur_y)
```

```{code-cell} ipython3
cartopy_crs = Projection(rioC.rio.crs, bounds=original_extent)
cartopy_crs
```

```{code-cell} ipython3
cartopy_crs.bounds
```

```{code-cell} ipython3
goesC.time_coverage_start
```

+++ {"user_expressions": []}

## Get Date and Time Information

Each file represents the data collected during one scan sequence for the
domain. There are several different time stamps in this file, which are also
found in the file's name.

```{code-cell} ipython3

```

```{code-cell} ipython3
# Scan's start time, converted to datetime object
scan_start = datetime.strptime(goesC.time_coverage_start, "%Y-%m-%dT%H:%M:%S.%fZ")

# Scan's end time, converted to datetime object
scan_end = datetime.strptime(goesC.time_coverage_end, "%Y-%m-%dT%H:%M:%S.%fZ")

# File creation time, convert to datetime object
file_created = datetime.strptime(goesC.date_created, "%Y-%m-%dT%H:%M:%S.%fZ")
#
# arithmetic on datetime objects
#
duration = (scan_end - scan_start).seconds / 60
midpoint = scan_start + timedelta(minutes = duration/2.)
```

```{code-cell} ipython3
print(f"Scan Start    : {scan_start}")
print(f"Scan End      : {scan_end}")
print(f"File Created  :  {file_created}")
print(f"Scan midpoint :  {midpoint}")
```

+++ {"user_expressions": []}

## True Color Recipe

### Gamma correction

Color images are a Red-Green-Blue (RGB) composite of three different
channels. We will assign the following channels as our RGB values:


RGB values must be between 0 and 1, same as the range of values of the
reflectance channels. A gamma correction is applied to control the brightness
and make the image not look too dark, where for input and output values brightness values
V the gamma correction is:

$$
V_{out} = V_{in}^{1/\gamma}
$$ (eq:gamma)

This correction will enhance the distance between smaller values ov $V_{in}$ (i.e. more levels for darker colors)

To see why this is, suppose $\gamma = 2$, so $1/\gamma$=0.5.  Take the derivative of {eq}`eq:gamma`:

$$
\frac{dV_{out}}{dV_{in}} = \frac{1}{\gamma V_{in}^{0.5}} 
$$
so the smaller the magnitude of $V_{in}$, the larger the difference between $dV_{out}$ and $dV_{in}$


Most displays have a decoding gamma of 2.2.  See
[wikipedia](https://en.wikipedia.org/wiki/Gamma_correction), and this
[tutorial](https://www.cambridgeincolour.com/tutorials/gamma-correction.htm) if you'd like to know more.

+++ {"user_expressions": []}

### Natural vs. veggie green

The GREEN "veggie" channel on GOES-16 does not measure visible green
light. Instead, it measures a near-infrared band sensitive to chlorophyll. We
could use that channel in place of green, but it would make the green in our
image appear too vibrant. Instead, we will tone-down the green channel by
interpolating the value to simulate a natural green color.

\begin{equation}
pseudoGreen = (0.48358168*RED) + (0.06038137*GREEN) + (0.45706946*BLUE)
\end{equation}

or, a simple alternative ([CIMSS Natural True
Color](http://cimss.ssec.wisc.edu/goes/OCLOFactSheetPDFs/ABIQuickGuide_CIMSSRGB_v2.pdf)):

\begin{equation}
pseudoGreen = (0.45*RED) + (0.1*GREEN) + (0.45*BLUE)
\end{equation}

The multiband formatted file we loaded is convenient because all the GOES
channels are in the same NetCDF file. Next, we will assign our variables R, G,
and B as the data for each channel.

+++ {"user_expressions": []}

## Check the band wavelengths

```{code-cell} ipython3
# Confirm that each band is the wavelength we are interested in
for band in [2, 3, 1]:
    band_wavelength = f"band_wavelength_C{band:02d}"
    long_name = goesC[band_wavelength].long_name
    wavelength = goesC[band_wavelength].data
    units = goesC[band_wavelength].units
    print(f"{long_name} is {wavelength:.2f} {units}")
```

+++ {"user_expressions": []}

## Clip the bands and apply the gamma correction

```{code-cell} ipython3
######################################################################
#

# Load the three channels into appropriate R, G, and B variables
R = goesC["CMI_C02"].data
G = goesC["CMI_C03"].data
B = goesC["CMI_C01"].data

######################################################################
#

# Apply range limits for each channel. RGB values must be between 0 and 1
R = np.clip(R, 0, 1)
G = np.clip(G, 0, 1)
B = np.clip(B, 0, 1)

######################################################################
#

# Apply a gamma correction to the image
gamma = 2.2
R = np.power(R, 1 / gamma)
G = np.power(G, 1 / gamma)
B = np.power(B, 1 / gamma)

######################################################################
```

+++ {"user_expressions": []}

## Make "true" green from the three bands

```{code-cell} ipython3
# Calculate the "True" Green
G_true = 0.45 * R + 0.1 * G + 0.45 * B
G_true = np.maximum(G_true, 0)
G_true = np.minimum(G_true, 1)
```

+++ {"user_expressions": []}

## Plot the raw images

First, we plot each channel individually. The deeper the color means the
satellite is observing more light in that channel. Clouds appear white becuase
they reflect lots of red, green, and blue light. You will also notice that the
land reflects a lot of "green" in the veggie channel becuase this channel is
sensitive to the chlorophyll.

```{code-cell} ipython3
fig, ([ax1, ax2, ax3, ax4]) = plt.subplots(1, 4, figsize=(16, 3))

ax1.imshow(R, cmap="Reds", vmax=1, vmin=0)
ax1.set_title("Red", fontweight="semibold")
ax1.axis("off")

ax2.imshow(G, cmap="Greens", vmax=1, vmin=0)
ax2.set_title("Veggie", fontweight="semibold")
ax2.axis("off")

ax3.imshow(G_true, cmap="Greens", vmax=1, vmin=0)
ax3.set_title('"True" Green', fontweight="semibold")
ax3.axis("off")

ax4.imshow(B, cmap="Blues", vmax=1, vmin=0)
ax4.set_title("Blue", fontweight="semibold")
ax4.axis("off")

plt.subplots_adjust(wspace=0.02)
```

+++ {"user_expressions": []}

## Stack the tree images using dstack

Compare a stack with "veggie green" with  "true green" using false color images

```{code-cell} ipython3
######################################################################
# The addition of the three channels results in a color image. We combine the
# three channels in a stacked array and display the image with `imshow` again.
#

# The RGB array with the raw veggie band
RGB_veggie = np.dstack([R, G, B])

# The RGB array for the true color image
RGB = np.dstack([R, G_true, B])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# The RGB using the raw veggie band
ax1.imshow(RGB_veggie)
ax1.set_title("GOES-16 RGB Raw Veggie", fontweight="semibold", loc="left", fontsize=12)
ax1.set_title("%s" % scan_start.strftime("%d %B %Y %H:%M UTC "), loc="right")
ax1.axis("off")

# The RGB for the true color image
ax2.imshow(RGB)
ax2.set_title("GOES-16 RGB True Color", fontweight="semibold", loc="left", fontsize=12)
ax2.set_title("%s" % scan_start.strftime("%d %B %Y %H:%M UTC "), loc="right")
ax2.axis("off");
```

+++ {"user_expressions": []}

## Plot the mapped image using cartopy

```{code-cell} ipython3
fig = plt.figure(figsize=(15, 12))

ax = fig.add_subplot(1, 1, 1, projection=cartopy_crs)

ax.imshow(
    RGB,
    origin="upper",
    extent= original_extent,
    transform=cartopy_crs,
    interpolation="nearest",
    vmin=162.0,
    vmax=330.0,
)
ax.coastlines(resolution="50m", color="black", linewidth=2)
ax.add_feature(ccrs.cartopy.feature.STATES)

plt.title("GOES-16 True Color", loc="left", fontweight="semibold", fontsize=15)
plt.title("%s" % scan_start.strftime("%d %B %Y %H:%M UTC "), loc="right");
```

+++ {"user_expressions": []}

## Changing the map projection and plot extent

The next two cells show how to change the plotting crs and boundaries (extent) on a plot

The plot below changes the crs to [LambertConformal](https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html#lambertconformal)
and sets the plotting extent to between -130- -60 deg lon and 10 - 65 deg lat

```{code-cell} ipython3
fig = plt.figure(figsize=(15, 12))

lc = ccrs.LambertConformal(central_longitude=-97.5)

ax = fig.add_subplot(1, 1, 1, projection=lc)
#
# lat/lons are given in "flat-square" projection
#
ax.set_extent([-135, -60, 10, 65], crs=ccrs.PlateCarree())

ax.imshow(
    RGB,
    origin="upper",
    extent=original_extent,
    transform=cartopy_crs,
    interpolation="none",
)
ax.coastlines(resolution="50m", color="black", linewidth=1)
ax.add_feature(ccrs.cartopy.feature.STATES)

plt.title("GOES-16 True Color", loc="left", fontweight="semibold", fontsize=15)
plt.title("%s" % scan_start.strftime("%d %B %Y %H:%M UTC "), loc="right");
```

+++ {"user_expressions": []}

## Change the axis extent (not the original image extent)

We can zoom the map to a lon/lat box by specifying a new extent for the axis
between -114.5 - -108.25 deg Lon and 36-43 deg Lat  -- Salt Lake City, Utah
The map crs is switched to PlateCarree, which is ok at the small scale (where the lat/lon parallels are basically straight lines)

```{code-cell} ipython3
fig = plt.figure(figsize=(8, 8))

#
# GOES 
#
pc = ccrs.PlateCarree()

ax = fig.add_subplot(1, 1, 1, projection=pc)
#
# utah
#
ax.set_extent([-114.75, -108.25, 36, 43], crs=pc)

ax.imshow(RGB, 
          origin='upper',
          extent=original_extent,
          transform=cartopy_crs,
          interpolation='none')

ax.coastlines(resolution='50m', color='black', linewidth=1)
ax.add_feature(ccrs.cartopy.feature.STATES)

plt.title('GOES-16 True Color', loc='left', fontweight='bold', fontsize=15)
plt.title('{}'.format(scan_start.strftime('%d %B %Y %H:%M UTC ')), loc='right');
```

+++ {"user_expressions": []}

## Practice questions (takehome)

+++ {"user_expressions": []}

### Practice question 1

Use a seaborn jointplot to compare the channel 1 (blue) histogram before and after the gamma correction

+++ {"user_expressions": []}

### Practice question 2

Use xarray.isel to clip just the portion of the abi scene that's in the [-114.75, -108.25, 36, 43] lon/lat bounding
box and save it to disk as a netcdf file with the correct affine transform and crs

+++ {"user_expressions": []}

### Practice question 3

Change the map projection in from lambert to azimuthal equal area -- does it look less weird?
