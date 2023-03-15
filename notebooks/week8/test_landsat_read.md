---
jupytext:
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

+++

(week8:test_landsat)=
# simple test of `get_landsat_scene`

See [landsat_read source code](https://phaustin.github.io/a301_web/full_listing.html#sat_lib.landsat_read.get_landsat_scene)
for details

```{code-cell} ipython3
from matplotlib import pyplot as plt
from sat_lib.landsat_read import get_landsat_scene
from rasterio.windows import Window
```

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

```{code-cell} ipython3
date = "2015-06-14"
lon, lat  = -123.2460, 49.2606
the_window = Window(col_off=2671, row_off=1352, width=234, height=301)
scenes_dict = get_landsat_scene(date, lon, lat, the_window) 
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
#get the first 10 characters of the time attribute for the title
the_date = scenes_dict['fmask_ds'].attrs['day']
scenes_dict['fmask_ds'].plot()
ax.set_title(f"Land/cloud mask for Landsat {the_date}");
```
