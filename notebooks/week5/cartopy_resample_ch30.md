---
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
toc-autonumbering: true
toc-showmarkdowntxt: false
toc-showtags: true
---

(week5:resample)=
# Use pyresample and cartopy to plot channel 30 radiances

This notebook uses two hdf files: the MYD03 geom file containing pixel lats and lons at 1 km resolution
and the Level 1B Modis MYD02 readiance file with the 36 channel radiances.

The work is split into 5 sections:

* **Section 1.1**:  Read the lats, lons, metadata and radiances into variables

* **Section 1.2**: Set up the parameters for Lambert Azimuthal map projection centered on the scene center.  Using this projection
  create a an instance of a [pyresample SwathDefinition](https://pyresample.readthedocs.io/en/latest/api/pyresample.html#pyresample.geometry.SwathDefinition)
  which contains the pixel lats and lons.  With that information, create an [Area Definition](https://pyresample.readthedocs.io/en/latest/geometry_utils.html#areadefinition-creation) that
specifies the resampled grid for the new resampled image.

* **Section 1.3**: Resample the Channel 30 radiances into the pyresample `area_def`

* **Section 1.4**: Plot the image using cartopy

* **Section 1.5**: Write the image and the metadata out to disk

```{code-cell} ipython3
:trusted: true

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

## Read in the data

### Find the files in the sat_data/pha folder

```{code-cell} ipython3
:trusted: true

geom_filelist = list(a301_lib.sat_data.glob("pha/MYD03*2105*hdf"))
ch30_filelist = list(a301_lib.sat_data.glob("pha/MYD02*2105*hdf"))
```

```{code-cell} ipython3
:trusted: true

geom_file_name = geom_filelist[0]
print(geom_file_name)
ch30_file_name = ch30_filelist[0]
print(ch30_file_name)
```

### Read the 1 km latitudes and longitudes

Use the new `sat_lib` functions to get the data

```{code-cell} ipython3
:trusted: true

lat_1km = read_plainvar(geom_file_name,'Latitude')
lon_1km = read_plainvar(geom_file_name,'Longitude')
print(f"{lat_1km.shape=},{lon_1km.shape=}")
```

### Read the channel 30 radiances

```{code-cell} ipython3
:trusted: true


ch30= readband_lw(ch30_file_name,30)
ch30.shape
```

### Read the metadata

```{code-cell} ipython3
:trusted: true

metadata = parseMeta(ch30_file_name)
```

## Create the SwathDefinition using a map projection and the lats and lons

### Make a Lambert Azimuthal projection with the WGS84 datum

pyresample needs proj4 map parameters to put together its grid.  These are
returned by the get_proj_params file below.

```{code-cell} ipython3
:trusted: true

def get_proj_params(metadata):
    """
    given a metadata dictionary from parseMeta, return proj4 parameters
    for use by cartopy or pyresample, assuming a laea projection
    and WGS84 datum
    
    Parameters
    ----------
    
    metadata:  dictionary
       returned by parseMeta
    
    Returns
    -------
    (proj_params, globe): dict, cartopy.crs.Globe
        projection params plus datum created by cartopy crs
    
    """
    

    globe = ccrs.Globe(datum="WGS84", ellipse="WGS84")
    projection = ccrs.LambertAzimuthalEqualArea(
        central_latitude=metadata["lat_0"],
        central_longitude=metadata["lon_0"],
        globe=globe,
    )
    
    return projection
```

### What is the `projection`?

```{code-cell} ipython3
:trusted: true

projection = get_proj_params(metadata)
print(type(projection))
```

Source code for the [Lambert projection](https://scitools.org.uk/cartopy/docs/v0.15/_modules/cartopy/crs.html#LambertAzimuthalEqualArea)

Use python's `dir` function to print the methods and attributes

```{code-cell} ipython3
:trusted: true

print(dir(projection))
```

```{code-cell} ipython3
:trusted: true

print(projection.to_dict())
```

### What is the `globe`

```{code-cell} ipython3
:trusted: true

print(type(projection.globe))
```

Man page for [cartopy.crs.Globe](https://scitools.org.uk/cartopy/docs/latest/reference/generated/cartopy.crs.Globe.html)

```{code-cell} ipython3
:trusted: true

print(projection.globe.to_proj4_params())
```

```{code-cell} ipython3
:trusted: true

proj_params =  projection.proj4_params
print(proj_params)
```

### Create the SwathDefinition and make the `area_def`

The SwathDefinition holds the original lat/lons, while the
`area_def` holds the resampled grid, with its bounding box
and the specification for the number of rows and columns,
and the size of the resampled pixels.

```{code-cell} ipython3
:trusted: true

swath_def = SwathDefinition(lon_1km, lat_1km)
area_def = swath_def.compute_optimal_bb_area(proj_dict=proj_params)
```

Here is the `area_def` we will be resampling into:

```{code-cell} ipython3
:trusted: true

out = area_def.to_cartopy_crs()
display(out);
```

### What is a `SwathDefinition`?

```{code-cell} ipython3
:trusted: true

print(type(swath_def))
```

Man page for [SwathDefinition](https://pyresample.readthedocs.io/en/latest/geo_def.html#swathdefinition)

```{code-cell} ipython3
:trusted: true

print(dir(swath_def))
```

```{code-cell} ipython3
:trusted: true

print(help(swath_def.compute_optimal_bb_area))
```

### What is an `AreaDefiniton`?

```{code-cell} ipython3
:trusted: true

print(type(area_def))
```

Man page for [AreaDefinition](https://pyresample.readthedocs.io/en/latest/geo_def.html#areadefinition)

```{code-cell} ipython3
:trusted: true

print(dir(area_def))
```

### Get the number of rows and columns in the regridded image

Below we dump imformation about the `area_def` -- in particular `area_def.width, area_def.height, area_def.pixel_size_x, area_def.pixel_size_y`  Note that pyresample has increase the image size from the original 2040 x 1354 to the new 2244 x 2534.  This produces resampled pixels that are "downscaled" to higher resolution in the row direction, so that the new pixels are approximately square (1105 meters wide by 1088 meters high( 


```{code-cell} ipython3
:trusted: true

print(f"\ndump area definition:\n{area_def}\n")
print(
    (
        f"\nx and y pixel dimensions in meters:"
        f"\n{area_def.pixel_size_x}\n{area_def.pixel_size_y}\n"
    )
)
```

## resample ch30 on the `area_def` grid

The `pyresample.kd_tree` samples data that is defined on the `swath_def` grid onto the new grid defined by the `area_def`.  It uses a [k-dimensional tree](https://en.wikipedia.org/wiki/K-d_tree) to organize the pixels so
that a pixel's nearest neighbors can be rapidily found, and data from neighbors can be used to fill in any
holes that appear when mapping to the new grid.  It uses a 5 km "radius of influence" to determine which pixels
to use for hole filling.


```{code-cell} ipython3
:trusted: true

fill_value = -9999.0
area_name = "modis swath 5min granule"
image_30 = kd_tree.resample_nearest(
    swath_def,
    ch30.ravel(),
    area_def,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
```

### What is `image_30`

```{code-cell} ipython3
:trusted: true

print(type(image_30))
print(image_30.shape)
print(image_30.dtype)
```

### replace missing values = -9999. with floating point nan for mapping

```{code-cell} ipython3
:trusted: true

image_30[image_30 < -9000] = np.nan
```

## Plot the image using cartopy

### Create a palette

We want to spread the colors over a limited range of values between 0.1 and 7 $W/m^2\, \mu m^{-1}\,sr^{-1}$ so we
will set over and under colors and normalize the data to this range

```{code-cell} ipython3
:trusted: true

pal = plt.get_cmap("plasma")
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("r")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
vmin = 0.1  #anything under this is colored black
vmax = 7.0  #anything over this is colored red
from matplotlib.colors import Normalize

the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
```

### use the palette on the image_30 array

```{code-cell} ipython3
:trusted: true

crs = area_def.to_cartopy_crs()
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": crs})
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
ax.set_extent(crs.bounds, crs)
cs = ax.imshow(
    image_30,
    transform=crs,
    extent=crs.bounds,
    origin="upper",
    alpha=0.8,
    cmap=pal,
    norm=the_norm,
)
fig.colorbar(cs, extend="both");
```

## write out all the projection information as a json file

Make a new folder to hold the metadata and the npz file with the the resampled image.

```{code-cell} ipython3
:trusted: true

do_write = True
if do_write:
    out_dict = {}
    hdf_file = ch30_file_name
    geom_file = geom_file_name
    out_dict["extent"] = crs.bounds
    globe = projection.globe.to_proj4_params()
    out_dict["globe"] = dict(globe)
    out_dict["area_def"] = proj_params
    out_dict["field_name"] = "ch30"
    out_dict["units"] = "W/m^2/sr/micron"
    out_dict["variable_description"] = "channel 30 radiance"
    out_dict["x_size"] = area_def.x_size
    out_dict["y_size"] = area_def.y_size
    out_dir_name = "ch30_resample"
    out_dict["out_dir"] = out_dir_name
    out_dir = a301_lib.data_share / Path("test_data") / Path(out_dir_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    image_name = out_dir / Path(f"{out_dir_name}.npz")
    json_name = out_dir / Path(f"{out_dir_name}.json")
    np.savez(image_name, ch30_resample=image_30)
    with open(json_name, "w") as f:
        json.dump(out_dict, f, indent=4)
```
