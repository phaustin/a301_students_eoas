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

+++ {"user_expressions": []}

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

from matplotlib import pyplot as plt
import numpy as np
from copy import copy

import rioxarray
from pystac_client import Client
from shapely.geometry import Point
import a301_lib
```

+++ {"user_expressions": []}

##  Doing an image search using pystac_client

STAC is an acronym for "Spatio-temporal asset catalog", which is a standard way of cataloging
GIS resources in the cloud.  A STAC catalog hold metadata, including web addresses, for geotiff
files like those uploaded by the [NASA harmonized landsat-sentinel project](https://www.earthdata.nasa.gov/learn/articles/hls-cloud-efforts) (HLS) to Amazon Web Services.

+++ {"user_expressions": []}

We get the url for the stac catalog from the [NASA CMR page](https://nasa-openscapes.github.io/2021-Cloud-Hackathon/tutorials/02_Data_Discovery_CMR-STAC_API.html). The HLS project catalog is called "LPCLOUD"  (for land processes cloud and is available at [https://cmr.earthdata.nasa.gov/stac/LPCLOUD](https://cmr.earthdata.nasa.gov/stac/LPCLOUD).  This is called a "stac endpoint" and will receive
and process requests sent to it by the pystac Client.

+++ {"user_expressions": []}

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

+++ {"user_expressions": []}

### setup the search

The client takes the search parameters as the following keywords:

```{code-cell} ipython3
search = client.search(
    collections=["HLSL30.v2.0"],
    intersects=vancouver,
    datetime= june_2015
) 
search
```

+++ {"user_expressions": []}

### get the metadata for search items

This search should find 4 scenes -- 2 of which have 4% cloud cover.

```{code-cell} ipython3
items = search.get_all_items()
for index, the_scene in enumerate(items):
    print(f"\n\n{index=}\nproperties: {the_scene.properties}")
```

+++ {"user_expressions": []}

### Get the assets for scene 1 (June 14, 2015)

Once we decide on the scene, we can access its assets.  It contains the href (url) for
each of the landsat bands (except Band 8) -- recall their wavelengths:  [Landsat Bands](https://landsat.gsfc.nasa.gov/satellites/landsat-8/landsat-8-bands/)

There are also geotiffs for the 

- Solar Azimuth Angle (SAA) 
- Solar Zenith Angle (SZA)
- Sensor Azimuth Angle (VAA)
- Sensor Zenith Angle (VZA)

and a jpg image file called 'browse' which is a 1000 x 1000 pixel true color image for the scene.

The June 14 scene was taken by Landsat -- Landsat filenames begin with HLS.L30, Sentinel with HLS.S30.

```{code-cell} ipython3
june14_scene = items[1]
june14_scene.assets
```

+++ {"user_expressions": []}

### Download and display the true-color browse image

You can see the browse image by clicking on the asset href above. We can also use rioxarray to download the browse image from its url

```{code-cell} ipython3
june14_browse = rioxarray.open_rasterio(june14_scene.assets['browse'].href)
```

+++ {"user_expressions": []}

and we can plot it using imshow

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize=(10,10))
june14_browse.plot.imshow(ax=ax, origin = 'upper')
ax.set_title('June 14, 2015, Landsat 8');
```

+++ {"user_expressions": []}

## Saving the Band5 geotiff

Landsat Band5 in the near-infrared spans wavelengths between  0.845???0.885 $\mu m$.  This is a wavelength region where vegetation is very reflective,
because the leaves want to absorb red photons for photosynthesis and reflect slightly longer photons so they don't get absorbed and 
raise the leaf temperature.  This difference between red (Band4) and near-infrared (Band 5) is called the ["red edge"](https://agrio.app/Red-Edge-reflectance-monitoring-for-early-plant-stress-detection/).  

If you have managed to get your earthdata login into the `~/.netrc` file you should be able to download and save band 5 as shown below:

```{code-cell} ipython3
band_name="B05"
june14_scene.assets[band_name].href
```

+++ {"user_expressions": []}

### set the cookiefile

The nasa earthdata site will put an encrypted token into the file `cookies.txt` in the current directory

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

+++ {"user_expressions": []}

### Read the band 5 raster

The next cell reads in the raster.  By setting `masked=True` we are telling rasterio to look up the `_FillValue` tag in the
geotiff, and replace all pixels that have that value to `np.nan`.

After we've got the masked image, we create the raster by multiplying by the `scale_factor`

```{code-cell} ipython3
june14_band5 = rioxarray.open_rasterio(june14_scene.assets['B05'].href, masked=True)
june14_raster = june14_band5.squeeze()
june14_raster = june14_raster*june14_band5.scale_factor
june14_raster
```

+++ {"user_expressions": []}

Note that scaling the image removed all the attributes from the xarray.
They are still there in the original, however

```{code-cell} ipython3
june14_band5
```

+++ {"user_expressions": []}

### Histogram the raster

Make sure the scaled band5 reflectance is in the range 0-1

```{code-cell} ipython3
june14_raster.plot.hist();
```

+++ {"user_expressions": []}

### Write out the raster as a geotiff

Save the original

```{code-cell} ipython3
writeit=True
if writeit:
   landsat_dir = a301_lib.data_share / "pha/landsat"
   landsat_dir.mkdir(exist_ok=True, parents=True)
   outfile = landsat_dir / f"vancouver_landsat8_{band_name}.tif"
   june14_band5.rio.to_raster(outfile)
```

+++ {"user_expressions": []}

### Plot it using a grey palette

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
june14_raster.plot(ax=ax, cmap=pal, norm = the_norm)
ax.set_title(f"Landsat band {band_name}");
```

+++ {"user_expressions": []}

## What's next

+++ {"user_expressions": []}

Now that we can get landsat and sentinel scenes, we need to be able to 
subset to a particular part of the image, apply the cloud mask to remove cloudy
pixels and use channel ratios to infer surface properties.  That's the topic for the
next few notebooks
