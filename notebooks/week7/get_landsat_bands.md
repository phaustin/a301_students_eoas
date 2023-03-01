---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: -all
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

(week7:hls)=
# Dowloading Landsat and Sentinel data from NASA

This notebook goes over the procedure to locate and download 30 meter resolution
Landsat and Sentinel data using NASA's Harmonized Landsat and Sentinel-2  dataset.
These two satellites have very similar radiometer bands, fly in similar orbits and
have similar resolutions and swath widths.  NASA (Landsat) and the European Space Agency (ESA)
have collaborated on a common dataset that gives corrected surface reflectivity and brightness
temperatures for the two satellites.

To download this data, you'll need to get an [Earthdata Login](https://urs.earthdata.nasa.gov/).  Once you've got your username and password, go to the [a301hub](https://a301hub.eoasubc.xyz/) and open a terminal.  In the terminal, run this command:

     set_nasa_password
     
At the prompts, enter your username and password.  You should see a file called /home/jovyan/.netrc, which NASA uses below to authenticate you on their server.

```{code-cell} ipython3
import numpy
from pathlib  import Path
import inspect
from pystac_client import Client
from shapely.geometry import Point
from matplotlib import pyplot as plt
import numpy as np
from copy import copy
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
band_name="B05"
assets[band_name].href
```

```{code-cell} ipython3
true_color_image = rioxarray.open_rasterio(assets["browse"].href) 
```

```{code-cell} ipython3
ax = true_color_image.plot.imshow(figsize=(14,14),origin="upper");
ax.axes.set_title("vancouver browse image");
```

```{code-cell} ipython3
true_color_image.shape
```

```{code-cell} ipython3
import a301_lib
outfile = a301_lib.data_share / "pha/vancouver_browse.png"
ax.write_png(outfile)
```

```{code-cell} ipython3
true_color_image
```

```{code-cell} ipython3
true_color_image.rio.transform()
```

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

```{code-cell} ipython3
the_band_href = assets[band_name].href
the_band = rioxarray.open_rasterio(the_band_href,masked=True)
the_raster = the_band.squeeze()
the_raster = the_raster*the_band.scale_factor
the_band
```

```{code-cell} ipython3
the_band.to_numpy()
```

```{code-cell} ipython3
the_raster
```

```{code-cell} ipython3
the_raster.plot.hist()
```

```{code-cell} ipython3
writeit=True
if writeit:
    outfile = a301_lib.data_share / f"pha/landsat/vancouver_landsat8_{band_name}.tif"
    the_band.rio.to_raster(outfile)
the_band
```

```{code-cell} ipython3
pal = copy(plt.get_cmap("Greys_r"))
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
vmin = 0.0  #anything under this is colored black
vmax = 0.8  #anything over this is colored red
from matplotlib.colors import Normalize
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1, figsize=(10,10))
the_raster.plot(ax=ax, cmap=pal, norm = the_norm)
ax.set_title(f"Landsat band {band_name}")
```
