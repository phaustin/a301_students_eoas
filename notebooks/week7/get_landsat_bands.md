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
toc-autonumbering: true
---

(week7:hls)=
# Dowloading Landsat and Sentinel data from NASA

## Introduction

This notebook goes over the procedure to locate and download 30 meter resolution
Landsat and Sentinel data using NASA's Harmonized Landsat and Sentinel-2  dataset.
These two satellites have very similar radiometer bands, fly in similar orbits and
have similar resolutions and swath widths.  NASA (Landsat) and the European Space Agency (ESA)
have collaborated on a common dataset that gives corrected surface reflectivity and brightness
temperatures for the two satellites.

In the first few sections, we'll go over how to select a Landsat scene for a particular place and range of dates, and look at the true-color browse image.  This image is available as jpg file  without having to
authenticate with an earthdata id.  

In the final section, we'll show how to download a Band 5 landsat geotiff, either on the a301hub (or for mac users) on your laptop.

To use either the a301hub or your laptop to get a geotiff from Amazon, you'll need to get an [Earthdata Login](https://urs.earthdata.nasa.gov/).  Once you've got your username and password, go to the [a301hub](https://a301hub.eoasubc.xyz/) and open a terminal.  In the terminal, run this command:

     set_nasa_password
     
At the prompts, enter your username and password.  You should see a file created called `~/.netrc` which NASA uses to authenticate you on their server.


If you're working on a Mac latop, you'll also need to do:
   
    conda activate a301
    mamba install pystac-client, shapely

```{code-cell} ipython3
import numpy
from pathlib  import Path
import inspect
from pystac_client import Client
from shapely.geometry import Point
from matplotlib import pyplot as plt
import numpy as np
from copy import copy

import rioxarray
```

##  Doing an image search using pystac_client

STAC is an acronym for "Spatio-temporal asset catalog", which is a standard way of cataloging
GIS resources in the cloud.  A STAC catalog hold metadata, including web addresses, for geotiff
files like those uploaded by the [NASA harmonized landsat-sentinel project](https://www.earthdata.nasa.gov/learn/articles/hls-cloud-efforts) (HLS) to Amazon Web Services.

+++

We get the url for the stac catalog from the [NASA CMR page](https://nasa-openscapes.github.io/2021-Cloud-Hackathon/tutorials/02_Data_Discovery_CMR-STAC_API.html). The HLS project catalog is called "LPCLOUD"  (for land processes cloud and is available at [https://cmr.earthdata.nasa.gov/stac/LPCLOUD](https://cmr.earthdata.nasa.gov/stac/LPCLOUD).  This is called a "stac endpoint" and will receive
and process requests sent to it by the pystac Client.

+++

We'll also need the [shapely](https://towardsdatascience.com/geospatial-adventures-step-1-shapely-e911e4f86361) library to specify a point on the earth that we want to be included in our search. In addition, we need to specify a date range to search.

```{code-cell} ipython3
van_lon, van_lat = -123.120, 49.2827
vancouver = Point(van_lon, van_lat)
june_2015 = "2015-06-01/2015-06-30"
```

```{code-cell} ipython3
# connect to the STAC endpoint
cmr_api_url = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD"
client = Client.open(cmr_api_url)
```

### setup the search

```{code-cell} ipython3
search = client.search(
    collections=["HLSL30.v2.0"],
    intersects=vancouver,
    datetime= june_2015
) 
```

### get the metadata for search items

This search should find 4 scenes -- 2 of which have 4% cloud cover.

```{code-cell} ipython3
items = search.get_all_items()
for index, the_scene in enumerate(items):
    print(f"\n\n{index=}\nproperties: {the_scene.properties}")
```

### Get the assets for scene 1 (June 14, 2015)

Once we decide on the scene, we can access its assets.  It contains the href (url) for
each of the landsat bands (except Band 8) -- recall their wavelengths:  [Landsat Bands](https://landsat.gsfc.nasa.gov/satellites/landsat-8/landsat-8-bands/)

There are also geotiffs for the 

- Solar Azimuth Angle (SAA) 
- Solar Zenith Angle (SZA)
- Sensor Azimuth Angle (VAA)
- Sensor Zenith Angle (VZA)

and a jpg image file called 'browse' which is a 1000 x 1000 pixel true color image for the scene.

```{code-cell} ipython3
june14_scene = items[1]
june14_scene.assets
```

### Download and display the true-color browse image

You can see the browse image by clicking on the asset href above. We can also use rioxarray to download the browse image from its url

```{code-cell} ipython3
june14_browse = rioxarray.open_rasterio(june14_scene.assets['browse'].href)
```

and we can plot it using imshow

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize=(10,10))
june14_browse.plot.imshow(ax=ax, origin = 'upper')
ax.set_title('June 14, 2015, Landsat 8');
```

## Saving the Band5 geotiff

Landsat Band5 in the near-infrared spans wavelengths between  0.845–0.885 $\mu m$.  This is a wavelength region where vegetation is very reflective,
because the leafs want to absorb red photons for photosynthesis and reflect slightly longer photons so they don't get absorbed and 
raise the leaf temperature.  This difference between red (Band4) and near-infrared (Band 5) is called the ["red edge"](https://agrio.app/Red-Edge-reflectance-monitoring-for-early-plant-stress-detection/).  

If you have managed to get your earthdata login into the `~/.netrc` file you should be able to download and save band 5 as shown below:

```{code-cell} ipython3
band_name="B05"
june14_scene.assets[band_name].href
```

### set the cookiefile

The nasa earthdata site will put an encrypted token into the file `cookies.txt` in the current directory

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

### Read the band 5 raster

The next cell reads in the raster.  By setting `masked=True` we are telling rasterio to look up the `_FillValue` tag in the
geotiff, and replace all pixels that have that value to `np.nan`.

```{code-cell} ipython3
the_band_href
```

```{code-cell} ipython3
the_band_href = june14_scene.assets[band_name].href
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
