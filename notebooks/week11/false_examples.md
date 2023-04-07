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

(week11:false_color_examples)=
# Landsat 8 false color examples

In the {ref}`week10:false_color` notebook we showed how to make a false color composite with Landsat 8 bands 5, 4, 3 mapped to 
red, blue and green (color infrared)

In this notebook we move that code into a function called `make_false_color`, and show a Vancouver scene with some different band combinations

```{code-cell} ipython3
import a301_lib
import xarray
import rioxarray
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from skimage import exposure, img_as_ubyte
from IPython.display import Image
from sat_lib.landsat_read import get_landsat_dataset
from sat_lib.false_color import make_false_color
```

```{code-cell} ipython3
help(make_false_color)
```

+++ {"user_expressions": []}

## Understanding Landsat band location

The figure below shows average reflectances for various surface types. Compare some of thse
reflectance values with the landsat band locations in microns

1) coastal aerosol: 0.44, 2)  blue: 0.47, 3) green: 0.55, 4) red:  0.65, 5) near-ir:  0.86, 6) swir1  1.6, 7) swir2: 2.2

+++ {"user_expressions": []}

```{figure} figures/hou_reflectance.png
:name: fig:reflectance_spectra
:width: 80%

Reflectance spectra
```

+++ {"user_expressions": []}

## Landsat bands by surface type

+++ {"user_expressions": []}

```{figure} figures/landsat8_bands.png
:name: landsat_8_bands![landsat8_bands.png](attachment:9454ecea-8cba-488a-87ec-110fb2b5d57f.png)
:width: 80%

Landsat 8 band wavelengths
```

+++ {"user_expressions": []}

## Landsat false color combinations

+++ {"user_expressions": []}

```{figure} figures/arc_gis_bands.png
:width: 80%
:name: landsat_8_bands


```

+++ {"user_expressions": []}

## Show some of these below

```{code-cell} ipython3
:user_expressions: []

write_it = False
file_path = a301_lib.data_share / "pha/landsat"
infile = file_path / "vancouver_6bands.nc"
if write_it:
    
    import os
    os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
    os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"


    date = "2015-06-14"
    lon, lat  = -123.2460, 49.2606
    do_write = True
    if do_write:
        from rasterio.windows import Window
        the_window = Window(col_off=2637, row_off=951, width=400, height=600)
        six_bands = get_landsat_dataset(date, lon, lat, the_window, bands=['B02','B03','B04','B05','B06','B07']) 
    six_bands.to_netcdf(infile, mode= 'w')
```

```{code-cell} ipython3
if not write_it:
    six_bands = rioxarray.open_rasterio(infile, mask_and_scale=True)
six_bands
```

+++ {"user_expressions": []}

Here is the code that fetched the original dataset from NASA

+++ {"user_expressions": []}

## True color (red, green, blue)

```{code-cell} ipython3
true_color = make_false_color(six_bands, band_names=["B04","B03","B02"])
fig1, ax1 = plt.subplots(1,1,figsize=(6,9))
true_color.plot.imshow(ax=ax1);
ax1.set(title="True color 432");
```

+++ {"user_expressions": []}

## Color infrared: near-ir, red, green

Add the 5-4 red edge for vegetation, plus green (also vegetation). See [band543 detail](https://eos.com/make-an-analysis/color-infrared/)

```{code-cell} ipython3
color_ir = make_false_color(six_bands, band_names=["B05","B04","B03"])
fig2, ax2 = plt.subplots(1,1,figsize=(6,9))
color_ir.plot.imshow(ax=ax2);
ax2.set(title="color ir 543");
```

+++ {"user_expressions": []}

## Vegetation swir-1, near-ir, red

Add swir-1 for moisture content, keep the 5-4 red edge. Less contrast for turbid/fresh water.  See [band654 detail](https://eos.com/make-an-analysis/vegetation-analysis/)

```{code-cell} ipython3
veg_ir = make_false_color(six_bands, band_names=["B06","B05","B04"])
fig3, ax3 = plt.subplots(1,1,figsize=(6,9))
veg_ir.plot.imshow(ax=ax3);
ax3.set(title="veg ir 654");
```

+++ {"user_expressions": []}

## Agriculture swir-1, near-ir, blue

Swap out red for blue.  See [band652 detail](https://eos.com/make-an-analysis/agriculture-band/)

```{code-cell} ipython3
agri = make_false_color(six_bands, band_names=["B06","B05","B02"])
fig4, ax4 = plt.subplots(1,1,figsize=(6,9))
agri.plot.imshow(ax=ax4);
ax4.set(title="Agri 652");
```

+++ {"user_expressions": []}

## Urban swir-2, swir-1, red

concreate and bare soil have approximately constant reflectivities between 1.6 and 2.2 microns,
while vegetation reflects more in swir-1 than swir-2.  This combination distinguishes between
types of urban development.  Less contrast for turbid/fresh water.  See: [band764 detail](https://eos.com/make-an-analysis/shortwave-infrared/)

```{code-cell} ipython3
urban = make_false_color(six_bands, band_names=["B07","B06","B04"])
fig5, ax5 = plt.subplots(1,1,figsize=(6,9))
urban.plot.imshow(ax=ax5);
ax5.set(title="Urban 764");
```
