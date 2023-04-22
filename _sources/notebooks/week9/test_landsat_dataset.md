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

(week9:test_dataset)=
# Adding data to an image with xarray datasets

This is a copy of {ref}`week8:test_landsat` that uses [get_landsat_dataset](https://phaustin.github.io/a301_web/full_listing.html#sat_lib.landsat_read.get_landsat_dataset) and saves the scene to
a netcdf file for safekeeping.

We change the plot to band5, and set up the axis so we can add a point to the plot to make sure we know where we are

```{code-cell} ipython3
from matplotlib import pyplot as plt
from sat_lib.landsat_read import get_landsat_dataset
from rasterio.windows import Window
import cartopy.crs as ccrs
import rioxarray
import xarray
import a301_lib
```

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

+++ {"user_expressions": []}

## get three bands plus FMask and return as an xarray dataset

To fetch a new image that hasn't been saved and write it to disk,
set `doread=True`. Otherwise read the dataset from the netcdf file

```{code-cell} ipython3
date = "2015-06-14"
lon, lat  = -123.2460, 49.2606
ncfile = a301_lib.data_share / "pha/cloudsat/vancouver_ptgrey.nc"
#
# set to True first time through
#
doread=False
if doread:
    the_window = Window(col_off=2671, row_off=1352, width=234, height=301)
    scenes_data = get_landsat_dataset(date, lon, lat, the_window) 
    #
    # write out the file for reuse
    #
    scenes_data.to_netcdf(ncfile)
else:
    scenes_data = xarray.open_dataset(ncfile)
scenes_data
```

+++ {"user_expressions": []}

## Give the plotting routine the projection so we can add extra information in lon/lat coords

We want to set up the xarray plot so we can add points like we did in {ref}`week9:cloudsat`.  That means
creating the plotting axis with the map projection for the scene (which is saved as the xarray
attribute cartopy_epsg_code), and passing the Geodetic transform to the plot command, so it
knows that it needs to transform from lon/lat to map x,y

+++ {"user_expressions": []}

### Find the map projection using the epsg code for UTM Zone 10

```{code-cell} ipython3
band5 = scenes_data['B05']
code = band5.cartopy_epsg_code
projection = ccrs.epsg(code)
projection
```

+++ {"user_expressions": []}

### Create a plot axis with the projection and add a point for the EOAS building

```{code-cell} ipython3
from cartopy import feature as cfeature
kw_dict = dict(projection=projection)
#
# pass the landsat projection to the axis
#
fig, ax = plt.subplots(1,1,figsize=(10,8),subplot_kw = kw_dict);
band5.plot(ax=ax)
#
# tell the plot command that the points need to be transformed
# from lon/lat
#
transform = ccrs.Geodetic()
ax.plot(lon,lat,'bo',markersize=11,transform=transform)
ax.add_feature(cfeature.COASTLINE,color='black')
ax.set_title(f"landsat band 5 on {band5.day}");
```
