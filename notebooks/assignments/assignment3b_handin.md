---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: -all
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

(assign3b)=
# Assignment 3b -- Due Wednesday, Feb. 22 midnight

(This notebook will be replaced by the official handin notebook on Tuesday)

1) In the cells below, get channel 32 and resample to the same area_def as channel 31
2) Get the brightness temperature for both of the resampled images and the brightness tempereature difference 
   for ch32 - ch31
3) Read in the wv_ir image you get by running the wv_resample notebook, and make a scatter plot of
   ch32 - ch31 brightness temperature (in K) on the y axis and the column water vapor in cm on the x axis.  Note that
   you will need to mask the brightness temperature pixels so that only pixels which also have column water vapor are
   plotted
4) comment on the correlation you see, if any

+++

## resample channels 31 and 32

```{code-cell} ipython3
import json
from pathlib import Path
import pprint
pp = pprint.PrettyPrinter(indent=4)
import warnings
warnings.filterwarnings('ignore')


import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import a301_lib
from pyresample import kd_tree, SwathDefinition

from sat_lib.modismeta_read import parseMeta
from sat_lib.modischan_read import readband_lw, read_plainvar
```

## Read in the channel 31 and 32 radiances and the 1 km MYD03 lons/lats

```{code-cell} ipython3
geom_filelist = list(a301_lib.sat_data.glob("pha/MYD03*2105*hdf"))
radiance_filelist = list(a301_lib.sat_data.glob("pha/MYD02*2105*hdf"))
geom_file_name = geom_filelist[0]
print(geom_file_name)
radiance_file_name = radiance_filelist[0]
print(radiance_file_name)
```