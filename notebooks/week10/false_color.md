---
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

(week10:false_color)=
# Making color composite ("false color") images

+++ {"tags": [], "user_expressions": []}

## Definitions: "24 bit color", "true color", "false color"


Up to now we have been showing images using "8 bit color", where pixel values are scaled from 0 to 255 and mapped to a palette with
256 different color values.
The finished images that we will create towards the end of this notebook will instead have three layers to drive the red, green and blue levels of a computer/phone display.  Each layer is an 8 bit unsigned integer that can take on $2^8$ = 256 different levels.  The whole image therefore takes
$3 \times 8$ = 24 bits per pixel, or "24 bit color". When the red, green and blue bands are mapped to red, green and blue levels, the image is
called "true color".  When other bands are mapped to display red, green and blue levels the image is called "false color"

+++ {"tags": [], "jp-MarkdownHeadingCollapsed": true, "user_expressions": []}

## Introduction

Color composite images are a useful tool in remote sensing. They map
arbitrary image wavelengths to the primary colors (for example landsat 8 band 5 (near-ir, 0.86 microns) mapped to red,
landsat 8 band 4 (red, 0.66 microns) mapped to blue, and landsat band 3 (green, 0.55 microns) mapped to blue).
In such a "color ir" image, vegetation, which is very bright in the near-ir, will show up as bright red, while
water, different types of soils, etc. will show up as other colors.  Here are some examples of [popular band combinations](https://www.usgs.gov/media/images/common-landsat-band-combinations) for the [landsat 8 bands](https://www.usgs.gov/faqs/what-are-best-landsat-spectral-bands-use-my-research)

*Something to note:  one point of confusion is that the red, green and blue bands for landsat 8 are label band 4, band 3 and band
2 respectively, so remember that an rgb landsat image is desiginated by the band combination 432.*


In this notebook we will generate a "color ir" image from bands 5, 4, 3 using a clipped vancouver scene, reprocessing
them into a false color composite.  The final
format needs to follow the "portable network graphics (png) truecolor" standard: 

1) the pixels in each band have values between 0-255 (i.e. one 8 bit byte)
2) the bands are packed into 3 dimensional array with shape [3,nrows,ncols]
3) the band order needs to be red=index 0, blue=index 1 and green=index 2

We will also need to rewrite the images so that each band makes use of all the available 255 levels.  This means we need to change
the data values significantly, for the images below the reflectivities in bands 3 and 4 are below 0.2, which means if we
just converted them to 0-255 we'd only be using 20% of the 255 levels.  Fixing this problem by redistributing the data is called "stretching".
Below we'll show how to do a "histogram stretch".  Since the underlying data is changed in the image, false color composites are a qualitative, rather than a quantitative tool.

+++ {"tags": [], "user_expressions": []}

## Read in the clipped image

We use numpy.squeeze() to squeeze out the band dimension, so arrays with 3 dimensions (1,nrows,ncols)
become 2 dimensional with shape (nrows,ncols)

```{code-cell} ipython3
import a301_lib
import xarray
import rioxarray
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from skimage import exposure, img_as_ubyte
from IPython.display import Image
```

```{code-cell} ipython3
file_path = a301_lib.data_share / "pha/landsat"
infile = file_path / "vancouver_543_clipped.nc"
do_write=False
if do_write:
    bands_543.to_netcdf(infile, mode = 'w')
else:
    bands_543 = rioxarray.open_rasterio(infile, mask_and_scale=True)
    bands_543 = bands_543.squeeze()
bands_543
```

+++ {"tags": [], "user_expressions": []}

Here is the code that fetched the original dataset from NASA

+++ {"tags": [], "user_expressions": []}

```python
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"


date = "2015-06-14"
lon, lat  = -123.2460, 49.2606
do_write = True
if do_write:
    from rasterio.windows import Window
    the_window = Window(col_off=2637, row_off=951, width=400, height=600)
    bands_543 = get_landsat_dataset(date, lon, lat, the_window, bands=['B03','B04','B05']) 

bands_543 = bands_543.squeeze()
bands_543.to_netcdf(infile, mode= 'w')
```

+++ {"tags": [], "user_expressions": []}

Note the low reflectivity in band 3

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
bands_543['B03'].plot.imshow(ax=ax);
ax.set(title="band3 (green, 0.55 um)");
```

+++ {"tags": [], "user_expressions": []}

## Apply the Fmask

To show histograms of the data that exclude missing values we'll need to apply the
Fmask.  We'll also generate a mask of zeros and ones (a boolean mask) for the
histogram equalization routine below

```{code-cell} ipython3
b3, b4, b5, Fmask = bands_543['B03'], bands_543['B04'], bands_543['B05'], bands_543['Fmask']
```

```{code-cell} ipython3
masked_b3 = b3*Fmask.data
masked_b4 = b4*Fmask.data
masked_b5 = b5*Fmask.data
```

+++ {"tags": [], "user_expressions": []}

### Create a boolean mask

Below we are going to also require a separate mask that is
1 where the pixel is good, and 0 where the pixel is missing.
Be sure you understand how we get this mask from the code below

```{code-cell} ipython3
#
# create an empty array with the same shape as Fmask
#
bool_mask = np.empty_like(Fmask,dtype = np.int8)
#
# Below is True for all nan pixels
#
nan_mask = np.isnan(Fmask)
#
# flip this with logical_not so good pixels 
# are flagged True
#
good_mask = np.logical_not(nan_mask)
#
# assign 0 to nans, 1 to good values
#
bool_mask[nan_mask] = 0
bool_mask[good_mask] = 1
bool_mask
```

+++ {"tags": [], "user_expressions": []}

## Plotting joint histograms

+++ {"tags": [], "user_expressions": []}

Below we plot some joint histograms of using [seaborn.jointplot](https://seaborn.pydata.org/generated/seaborn.jointplot.html).  This is
a very powerful way to look for correlations between datasets, showing the both the 2-dimensional histogram (darker colors mean more pixels
in the bin) and the band histograms.

The plots show that bands 3 and 4 (green and red) have reflectivities below about 20%, while band 5 (near-ir) as expected is much brighter, with
reflectivites up to about 50%.  The images are much more interesting if every band has reflectivities ranging
between 0 and 1. When we plot using a color palette and 0-255 color values (8 bit color) we use Normalize with vmin and vmax to stretch
the colors between a minimum and maximum and ignore low and high values. This is called a "linear stretch".  There is a more sophisticated way
to assign color levels by manipulating the probability density distributions of the pixels, as described in the next section.

```{code-cell} ipython3
fig = sns.jointplot(
    x=masked_b3.data.ravel(),
    y=masked_b4.data.ravel(),
    xlim=(0, 0.2),
    ylim=(0.0, 0.2),
    kind="hex",
    color="#4CB391"
)
fig.fig.suptitle("green (band 3) vs red (band 4)");
axes = fig.fig.get_axes()
axes[0].set(xlabel = "band 3 reflectivity",
            ylabel = "band 4 reflectivity");
```

```{code-cell} ipython3
fig = sns.jointplot(
    x=masked_b4.data.ravel(),
    y=masked_b5.data.ravel(),
    kind="hex",
    xlim=(0, 0.2),
    ylim=(0.0, 0.5),
    color="#4CB391",
)
fig.fig.suptitle("red (band 4) vs near ir (band 5)");
axes = fig.fig.get_axes()
axes[0].set(xlabel = "band 4 reflectivity",
            ylabel = "band 5 reflectivity");
```

+++ {"tags": [], "user_expressions": []}

## Histogram equalization

Histogram equalization is a technique for changing the image data while preserving part of its character as represented
in its histogram.  It uses the **cumulative distribution** which is defined as the cumulative sum of the histogram of the image.  That is,
if the nuber of pixels with levels between $l^\prime$ and $l^\prime + dl^\prime$ is $n(l^\prime)\,dl^\prime$, then the cumulative
distribution $N(l)$ is given by:

$$
N(l) = \int_0^l n(l^\prime) dl^\prime
$$
In words, $N(l)$ is the number of pixels with level less than $l$L

The idea is to change ("stretch") the histogram bins so that $N(l) \approx$ constant for values of $l$ that contain most of the pixels.

Here's the cumulative distribution for the pdf for a gaussian distribution (bell curve):

```{code-cell} ipython3
x = np.random.randn(100000) # generate samples from normal distribution (discrete data)
fig, ax = plt.subplots(1,1)
#
# cumulative distribution N(l)
#
ax.hist(x,bins=200,density=True, cumulative=True)
#
# probability density n(l)
#
ax.hist(x,bins=200,density=True)
ax.set(title="gaussian pdf n(l) and cumulative distribution N(l)",
       xlabel="pixel level",
       ylabel = "n(l) (#pixels/(bin width)) and N(l) (#pixels with level < l)");

```

+++ {"tags": [], "user_expressions": []}

For this fake image, almost all the values are between -2 and 2, but the whole data range goes between -4 - 4.
If we use the blue curve to map xaxis values between -2 and 2 to y axis values between 0.1-0.99, we are "stretching" the
data to fill a range that is proportial to how many of these values actually occur in the image.  Values between -4 and -4 
are still represented, but they only get levels between about 1% of the levels after the stetch, instead of 25%.

+++ {"tags": [], "user_expressions": []}

### Here's the cumulative distribution for band 5

If we stretch the band 5 values to this cumulative distribution, 50% of the data range (0-125) is going to get essentially
100% of the levels between 0-1.

```{code-cell} ipython3
from skimage import exposure
#
# want 256 levels from 0-255
#
bins=256
img_cdf, bins = exposure.cumulative_distribution(b5.data.ravel(), bins)
plt.plot(img_cdf)
plt.grid(True);
```

+++ {"tags": [], "user_expressions": []}

### Stretching step 1: stretch the data in each band and save to a dictionary with the band name as key

To do the histogram stretch we'll use  the [scikit-image equalization module](https://scikit-image.org/docs/dev/auto_examples/color_exposure/plot_equalize.html).  It uses our boolean mask
to ignore np.nan values when it calculates the distribution.

```{code-cell} ipython3
stretched_dict = dict()
keys = ['b3','b4','b5']
images = [masked_b3, masked_b4, masked_b5]
for key, image in zip(keys,images):
    stretched_dict[key] = exposure.equalize_hist(image.data, mask = bool_mask )
    #
    # uncomment to try this without the mask
    #
    # stretched_dict[key] = exposure.equalize_hist(image.data)
```

+++ {"tags": [], "user_expressions": []}

### Before and after stretching

Pretty dramatic difference

```{code-cell} ipython3
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.imshow(masked_b3);
ax2.imshow(stretched_dict['b3']);
```

+++ {"tags": [], "user_expressions": []}

### Stretching step 2: check the stretched histograms

Redo the histogram plots to show the stretched distributions.  Note that they still contain information
about the correlation between bands, but the distributions are much broader than their unstretched versions.  Also note that
in each of the joint plot there are clusters of pixels that share similar values in the two bands.  These clusters
correspond to similar surface types (grass fields, golf courses, concrete pavement etc.)

```{code-cell} ipython3
fig = sns.jointplot(
    x=stretched_dict['b3'].ravel(),
    y=stretched_dict['b4'].ravel(),
    xlim=(0, 1),
    ylim=(0.0, 1),
    kind="hex",
    color="#4CB391"
)
fig.fig.suptitle("stretched green (band 3) vs red (band 4)");
axes = fig.fig.get_axes()
axes[0].set(xlabel = "stretched band 3 reflectivity",
            ylabel = "stretched band 4 reflectivity");
```

```{code-cell} ipython3
fig = sns.jointplot(
    x=stretched_dict['b4'].ravel(),
    y=stretched_dict['b5'].ravel(),
    xlim=(0, 1),
    ylim=(0.0, 1),
    kind="hex",
    color="#4CB391"
)
fig.fig.suptitle("stretched red (band 4) vs near ir (band 5)");
axes = fig.fig.get_axes()
axes[0].set(xlabel = "stretched band 4 reflectivity",
            ylabel = "stretched band 5 reflectivity");
```

+++ {"tags": [], "user_expressions": []}

one byte## Write the false color image into 3-dimensional array called "band_values"

We need to fill a new array of shape [3,nrows,ncols] and dtype=unsigned integer (byte)
with the
bands in the correct order -- red, blue, green.  The cell below does this
using the `img_as_ubyte` function, which scales and converts the floating point reflectivities to "unsigned bytes"
which are postive 8 bit numbers with range 0-255. The
output array needs to have the same number of rows and columns as the original image. I'll use
b3.shape to get those.

```{code-cell} ipython3
nrows, ncols = b3.shape
band_values = np.empty([3, nrows, ncols], dtype=np.uint8)
for index, key in enumerate(['b5', 'b4', 'b3']):
    stretched = stretched_dict[key]
    band_values[index, :, :] = img_as_ubyte(stretched)
```

+++ {"tags": [], "user_expressions": []}

### Note that we've lost our missing values

There's no way to write an np.nan as a missing value in a datatype that can only take on
values between 0 and 255, so all missing values have been converted to 0

```{code-cell} ipython3
figt, ax = plt.subplots(1,1,figsize=(12,8))
ax.imshow(band_values[0, :, :]);
```

+++ {"user_expressions": []}



+++ {"tags": [], "user_expressions": []}

### Create the dataArray

Now that I have 3 bands scaled from 0-255, I can write them out as
a png file, with new tags.  Recall from the {ref}`week8:zoom_landsat` that I need
to supply the array, dimensions, coordinates and attributes.

For the coordinate dictionary, I can borrow the 'x' and 'y' coordinates from band 3.

```{code-cell} ipython3
dims = ('band','y','x')
coords={'band':('band',[5,4,3]),
        'x': ('x',b3.x.data),
        'y': ('y',b3.y.data)}
```

+++ {"tags": [], "user_expressions": []}

### Add attributes

I'll keep some of the old attributes from the original `bands_543` dataset, and
add two new ones: history and landsat_rgb_bands.

```{code-cell} ipython3
band_names=['B05','B04','B03']
keep_attrs = ['cloud_cover','date','day','target_lat','target_lon']
all_attrs = bands_543.attrs
attr_dict = {key: value for key, value in all_attrs.items() if key in keep_attrs}
attr_dict['history']="written by false_color.md"
attr_dict["landsat_rgb_bands"] = band_names
```

+++ {"tags": [], "user_expressions": []}

### Create the falsecolor dataArray

Just copy this from the `zoom_landsat` notebook

```{code-cell} ipython3
false_color=xarray.DataArray(band_values,coords=coords,
                            dims=dims,
                            attrs=attr_dict)
false_color.rio.write_crs(b3.rio.crs, inplace=True)
false_color.rio.write_transform(b3.rio.transform(), inplace=True);
```

```{code-cell} ipython3
false_color
```

+++ {"tags": [], "user_expressions": []}

The final image -- the imshow function interprets any array with shape [3, nrows, ncols] as
a false color image and presents it with rgb colors.  One striking thing about the image
is how distinct the more undeveloped forest (dark green) is from the urban tree canopy.

Question -- would it be useful to provide a mask for this image?

```{code-cell} ipython3
false_color.plot.imshow(figsize=(6,9));
```

+++ {"tags": [], "user_expressions": []}

### Save as a png file

If the filename ends in png, rioxarray will save it in the standard png format.

```{code-cell} ipython3
png_filename = file_path / "vancouver_543.png"
false_color.rio.to_raster(png_filename)
```

+++ {"tags": [], "user_expressions": []}

### Read it back in to check

Here's the finished image -- read back in from the png file

```{code-cell} ipython3
Image(filename=png_filename)
```

+++ {"tags": [], "user_expressions": []}

## Repeat with the raw reflectivities

How much difference does the histogram stretch make?  Take a look at what the false color composite
looks like when we use the masked images without stretching

```{code-cell} ipython3
#
# fill an array with the unstretched data
#
nrows, ncols = b3.shape
raw_values = np.empty([3, nrows, ncols], dtype=np.uint8)
for index, raw_image in enumerate([masked_b5,masked_b4,masked_b3]):
    raw_values[index, :, :] = img_as_ubyte(raw_image)
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1, figsize=(6,9))
false_color.data = raw_values
false_color.plot.imshow(ax=ax)
```

```{code-cell} ipython3
import datetime
from pathlib import Path

import numpy as np
import seaborn as sns
from IPython.display import Image
import rioxarray
import xarray
import copy
import a301_lib
from sat_lib.landsat_read import get_landsat_dataset
```

```{code-cell} ipython3
from matplotlib import pyplot as plt
from skimage import exposure, img_as_ubyte
```
