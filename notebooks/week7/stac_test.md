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

```{code-cell} ipython3
import numpy
from pathlib  import Path
from sat_lib.landsat.landsat_metadata import landsat_metadata
import inspect
from pystac_client import Client
from shapely.geometry import Point
```

```{code-cell} ipython3
# connect to the STAC endpoint
cmr_api_url = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD"
client = Client.open(cmr_api_url)
```

```{code-cell} ipython3
# setup search
search = client.search(
    collections=["HLSL30.v2.0"],
    intersects=Point(-123.120, 49.2827),
    datetime="2015-06-01/2015-06-30"
) # nasa cmr cloud cover filtering is currently broken: https://github.com/nasa/cmr-stac/issues/239
# retrieve search results
items = search.get_all_items()
print(len(items))
print(list(items))
item = items[1]
print(f"{item.datetime=}")
print(f"{item.geometry=}")
print(f"{item.properties}")
assets = items[1].assets  # first item's asset dictionary
print(assets.keys())
for key, asset in assets.items():
    print(f"{key}: {asset.title}")
```

```{code-cell} ipython3
import rioxarray
```

```{code-cell} ipython3
assets['browse'].href
```

```{code-cell} ipython3
assets["B01"].href
```

```{code-cell} ipython3
true_color_image = rioxarray.open_rasterio(assets["browse"].href) 
```

```{code-cell} ipython3
ax = true_color_image.plot.imshow(figsize=(14,14),origin="upper");
ax.axes.set_title("vancouver browse image");
```

```{code-cell} ipython3
import a301_lib
outfile = a301_lib.data_share / "pha/vancouver_browse.png"
ax.write_png(outfile)
```

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

```{code-cell} ipython3
b01_href = assets["B01"].href
b01 = rioxarray.open_rasterio(b01_href)
```

```{code-cell} ipython3
help(b01.rio.write_grid_mapping)
```
