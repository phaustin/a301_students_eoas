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

(week5:longwave_resample)=
# Resampling channel 31

This notebook shows how to resample the 1 km MYD02 channel 31 radiance onto the 5 km `area_def`
that we created in the `wv_resample.md` notebook.  Reuses code from `cartopy_resample_ch30.md`

+++

Thi notebook resamples the 5 km water vapor datasets onto a 5km area_def. Note how I adapted code from 
week5/cartopy_resample_ch30.md

```{code-cell} ipython3
import warnings

from matplotlib import pyplot as plt
import numpy as np
import json
import cartopy.crs as ccrs
import cartopy
from pyresample import kd_tree, SwathDefinition
import pprint
pp = pprint.PrettyPrinter(indent=4)

from sat_lib.modischan_read import sd_open_file, read_plainvar, readband_lw
#
# new function for week 5
#
from sat_lib.mapping import area_def_from_dict
import a301_lib

warnings.filterwarnings('ignore')
hdf4_dir = a301_lib.sat_data / "pha"
geom_file = list(hdf4_dir.glob("MYD03*2105*hdf"))[0]
print(geom_file)
radiance_file = list(hdf4_dir.glob("MYD02*2105*hdf"))[0]
print(radiance_file)
```

## Get the 1 km lats and lons

```{code-cell} ipython3
lat_1km = read_plainvar(geom_file,'Latitude')
lon_1km = read_plainvar(geom_file,'Longitude')
print(f"{lat_1km.shape=},{lon_1km.shape=}")
```

## Get the channel 31 calibrated radiances

plot a histogram to make sure they are reasonable

```{code-cell} ipython3
ch31 = readband_lw(radiance_file,31)
ch31.shape
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
ax.hist(ch31.flat[:5000]);
```

## Read in the `area_def` from the 5 km water vapor ir image

```{code-cell} ipython3
areafile = a301_lib.data_share / "pha/area_dict.json"
with open(areafile,"r") as infile:
    area_dict = json.load(infile)
    
area_def = area_def_from_dict(area_dict)
pp.pprint(area_dict)
```

## Create the `swath_def` from the 1 km lons and lats

```{code-cell} ipython3
swath_def = SwathDefinition(lon_1km, lat_1km)
```

## Now resample using the swath_def onto the 5 km area def

```{code-cell} ipython3
fill_value = -9999.0
area_name = "channel 31 5 km resample"
image_31 = kd_tree.resample_nearest(
    swath_def,
    ch31.ravel(),
    area_def,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
image_31[image_31 == -9999.0] = np.nan
print(f"resampled image shape: {image_31.shape}")
```

## make a plot

```{code-cell} ipython3
pal = plt.get_cmap("plasma")
pal.set_bad("0.6")  # 75% grey for out-of-map cells
pal.set_over("r")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
vmin = 1  #anything under this is colored black
vmax = 14  #anything over this is colored red
from matplotlib.colors import Normalize
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
```

```{code-cell} ipython3
crs = area_def.to_cartopy_crs()
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": crs})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
ax.set_extent(crs.bounds, crs)
cs = ax.imshow(
    image_31,
    transform=crs,
    extent=crs.bounds,
    origin="upper",
    alpha=0.8,
    cmap=pal,
    norm=the_norm,
)
ax.set(title="modis channel 31 radiance (W/m^2/um/sr) 5km resolution for 2013.222.2105")
fig.colorbar(cs, extend="both");
outfile = a301_lib.data_share / "pha/ch31_resampled.png"
fig.savefig(outfile)
```

## For Assignment 3b by Friday

+++

1) In the cells below, get channel 32 and resample to the same area_def as channel 31
2) Get the brightness temperature for both of the resampled images and the brightness tempereature difference 
   for ch32 - ch31
3) Read in the wv_ir image you get by running the wv_resample notebook, and make a scatter plot of
   ch32 - ch31 brightness temperature (in K) on the y axis and the column water vapor in cm on the x axis.  Note that
   you will need to mask the brightness temperature pixels so that only pixels which also have column water vapor are
   plotted
4) comment on the correlation you see, if any
