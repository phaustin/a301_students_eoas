---
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
toc-autonumbering: true
toc-showmarkdowntxt: false
toc-showtags: true
---

(week5:wv_resample)=
# Resampling the water vapor

+++

Thi notebook resamples the 5 km water vapor datasets onto a 5km area_def. Note how I adapted code from 
week5/cartopy_resample_ch30.md

```{code-cell} ipython3
:trusted: true

import warnings

from matplotlib import pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)
from pyresample import kd_tree, SwathDefinition

from sat_lib.modischan_read import sd_open_file, read_plainvar
#
# new get_proj_params function
#
from sat_lib.mapping import get_proj_params, area_def_to_dict
from sat_lib.modismeta_read import parseMeta
import a301_lib

warnings.filterwarnings('ignore')
hdf4_dir = a301_lib.sat_data / "pha"
granules = list(hdf4_dir.glob("MYD05*2105*hdf"))
the_file = granules[0]
print(the_file)
```

## get the metadata

```{code-cell} ipython3
:trusted: true

meta_dict = parseMeta(the_file)
meta_dict
```

## new function to calibrate the wv dataset

```{code-cell} ipython3
:trusted: true

def readband_wv(the_file, band_name):
    """
    see: https://atmosphere-imager.gsfc.nasa.gov/sites/default/files/ModAtmo/MYD05_L2.C6.CDL.fs
       for file format
       
    read and calibrate a MODIS level 2 water vapor file
    
    Parameters
    ----------
    
       the_file: str
           path to the hdf file
       band_name: str
           either 'Water_Vapor_Near_Infrared` or `Water_Vapor_Infrared` 
           
    Returns
    -------
       the_chan_calibrated: ndarray
           column water vapor in cm
    """
    sd_file = sd_open_file(the_file)
    wv_data = sd_file.select(band_name)  # select sds
    wv_image = wv_data.get()
    #
    # convert from int16 to float64
    #
    wv_image = wv_image.astype('float64')
    wv_scale = wv_data.attributes()['scale_factor']
    wv_offset = wv_data.attributes()['add_offset']
    fill_value = wv_data.attributes()['_FillValue']
    #
    # convert fill values = -9999 to np.nan
    #
    wv_image[wv_image == fill_value] = np.nan
    wv_calibrated = (wv_image * wv_scale) + wv_offset
    sd_file.end()
    return wv_calibrated
```

## check the values and make a raw image

```{code-cell} ipython3
:trusted: true

wv_data = readband_wv(the_file,'Water_Vapor_Infrared')
fig, ax = plt.subplots(1,1)
ax.hist(wv_data.flat);
```

```{code-cell} ipython3
:trusted: true

fig, ax = plt.subplots(1,1)
ax.imshow(wv_data);
```

## Check the lats and lons

```{code-cell} ipython3
:trusted: true

lons = read_plainvar(the_file, 'Longitude')
lats = read_plainvar(the_file, 'Latitude')
fig, ax = plt.subplots(1,1)
ax.plot(lons,lats,'r+');
```

## Create the swath and area definitoins

```{code-cell} ipython3
:trusted: true

projection = get_proj_params(meta_dict)
proj_params =  projection.proj4_params
swath_def = SwathDefinition(lons, lats)
area_def = swath_def.compute_optimal_bb_area(proj_dict=proj_params)
```

```{code-cell} ipython3
:trusted: true

print(
    (
        f"\nx and y pixel dimensions in meters:"
        f"\n{area_def.pixel_size_x}\n{area_def.pixel_size_y}\n"
    )
)
```

## resample the image

```{code-cell} ipython3
:trusted: true

fill_value = -9999.0
image_wv = kd_tree.resample_nearest(
    swath_def,
    wv_data.ravel(),
    area_def,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
image_wv[image_wv < -9000] = np.nan
```

## make a plot

```{code-cell} ipython3
:trusted: true

pal = plt.get_cmap("plasma")
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("r")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
vmin = 0.0  #anything under this is colored black
vmax = 4.0  #anything over this is colored red
from matplotlib.colors import Normalize
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
```

```{code-cell} ipython3
:trusted: true

crs = area_def.to_cartopy_crs()
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": crs})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
ax.set_extent(crs.bounds, crs)
cs = ax.imshow(
    image_wv,
    transform=crs,
    extent=crs.bounds,
    origin="upper",
    alpha=0.8,
    cmap=pal,
    norm=the_norm,
)
ax.set(title="wv ir 5km resolution for 2013.222.2105")
fig.colorbar(cs, extend="both");
outfile = a301_lib.data_share / "pha/wv_ir_5km.png"
fig.savefig(outfile)
```

## write the `area_def` out for reuse

This will write out the file `~/shared_files/pha/area_dict.json`

```{code-cell} ipython3
:trusted: true

area_dict = area_def_to_dict(area_def)
outfile = a301_lib.data_share / "pha/area_dict.json"
with open(outfile,"w") as out:
    json.dump(area_dict,out,indent=4)
    
pp.pprint(area_dict)
```

## Save the resampled image as an npz file

This will write out the file `~/shared_files/pha/wv_5km_resampled.npz`

```{code-cell} ipython3
:trusted: true

outfile = a301_lib.data_share / "pha/wv_5km_resampled.npz"
np.savez(outfile,image_wv)
```

```{code-cell} ipython3
:trusted: true

a301_lib.data_share
```

```{code-cell} ipython3
:trusted: true

infile = a301_lib.data_share / "pha/wv_5km_resampled.npz"
the_npz = np.load(infile)
print(f"{list(the_npz.keys())=}")
the_raster = the_npz['arr_0']
print(f"{the_raster.shape=}")
```
