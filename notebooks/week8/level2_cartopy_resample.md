---
jupytext:
  formats: ipynb,md:myst,py:percent
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(level2_wv)=
# Water vapor retrieval using MYD05 data

+++

## Near IR vs. IR datasets

Modis provides two separate measurements on the column integrated water vapor.
The high level overview is given in the [modis water vapor products](https://atmosphere-imager.gsfc.nasa.gov/products/water-vapor).  Basically the reason for two separate retrievals is that they have different strengths and weaknesses.

* Near Infrared Retrieval

  * Uses reflected photons in two separate water vapor absorption bands

  * Strengths

    * 1 km spatial resolution at nadir

    * retrieval doesn't depend on temperature difference between vapor and surface

    * more accurate than longwave

  * Weaknesses

    * Doesn't work at night

    * Doesn't work over dark surfaces (can work over ocean
      as long as the pixel is reflecting direct sunlight ("sunglint")

    * Needs separate MYD03 file for lats/lons

* Infrared Retrieval

  * Uses the water absorption bands near 11 microns

  * Strengths

    * Works day/night, over dark surfaces

    * 5 km lat/lons included in file

  * Weaknesses

    * 5 km pixels at nadir

    * Doesn't work when most of the vapor is in the boundary layer and has about the same temperature
      as the surface

+++

### What this notebook does

1. Reads an MYD05 file named `MYD05*.hdf` located
   in `a301_lib.sat_data/hdf4_files` and grabs latitudes, longitudes and two arrays: `Water_Vapor_Near_Infrared` and
   `Water_Vapor_Infrared`

1. Scales the water vapar arrays by scale_factor and offset to produce the retrieved column water vapor
   in cm

1. Maps the two arrays onto the same 5km array for direct comparison

1. Maps the `near_ir` array onto a 1 km grid to show the full resolution.

1. Writes the three images with their area_def map information and metadata out to new folders in
   `./map_data/wv_maps` as npz files (for the images) and json files (for the metadata)

+++

## Setup

1. Download the MYD05 granule that corresponds to your 5 minute date/time.  It should look something like:

         MYD05_L2.A2013222.2105.061.2018048043105.hdf

1. Copy it into the google_drive `a301_data` folder

```{code-cell}
import json
import pdb
import pprint
from pathlib import Path

import numpy as np
from IPython.display import display
from IPython.display import Image
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from pyhdf.SD import SD
from pyhdf.SD import SDC

import a301_lib
from sat_lib.geometry import get_proj_params
from sat_lib.modismeta_read import parseMeta
## Image('figures/MYBRGB.A2016224.2100.006.2016237025650.jpg',width=600)
```

```{code-cell}
%matplotlib inline
```

## Read in the 1km and 5km water vapor files

+++

### Start with the lats/lons for 1km and 5km

```{code-cell}
m5_file= (a301_lib.sat_data / 'hdf4_files').glob("**/MYD05*2105*hdf")
m3_file = (a301_lib.sat_data / 'hdf4_files/myd03').glob("MYD03*2105*.hdf")
m5_file_str = str(list(m5_file)[0])
m3_file_str = str(list(m3_file)[0])
print(m5_file_str)
print(m3_file_str)

the_file = SD(m3_file_str, SDC.READ)
lats_1km = the_file.select("Latitude").get()
lons_1km = the_file.select("Longitude").get()
the_file.end()
print(lats_1km.shape)

the_file = SD(m5_file_str, SDC.READ)
lats_5km = the_file.select("Latitude").get()
lons_5km = the_file.select("Longitude").get()
the_file.end()
print(lats_5km.shape)
```

## Get the IR vapor plus 5 of its attributes

Store the data in a numpy array, and the attributes in a dictionary,
using a [dictionary comprehension](https://jakevdp.github.io/WhirlwindTourOfPython/11-list-comprehensions.html)
at line 4

```{code-cell}
the_file = SD(m5_file_str, SDC.READ)
wv_ir = the_file.select("Water_Vapor_Infrared")
attributes = ["units", "scale_factor", "add_offset", "valid_range", "_FillValue"]
attr_dict = wv_ir.attributes()
wv_ir_attrs = {k: attr_dict[k] for k in attributes}
print(f"wv_ir attributes: {pprint.pformat(wv_ir_attrs)}")
wv_ir_data = wv_ir.get()
the_file.end()
```

## Replace -9999 with np.nan

Note that this has to a happen before we scale the data by the scale_factor so the -9999 can be recognized

```{code-cell}
bad_data = wv_ir_data == wv_ir_attrs["_FillValue"]
#
# next line converts to floating point so we can use np.nan
#
wv_ir_data = wv_ir_data.astype(np.float32)
wv_ir_data[bad_data] = np.nan
```

## now scale the data and histogram it

```{code-cell}
wv_ir_scaled = wv_ir_data * attr_dict["scale_factor"] + attr_dict["add_offset"]
```

Note that we need to get rid of all nan values by taking ~ (not) np.isnan

```
plt.hist(wv_ir_scaled)
```
won't work

```{code-cell}
plt.hist(wv_ir_scaled[~np.isnan(wv_ir_scaled)])
ax = plt.gca()
ax.set_title("5 km wv data (cm)");
```

## Repeat for the 1 km near-ir data

Use a dictionary comprehension again to move the attributes in attrib_list into a dict at line 4

```{code-cell}
the_file = SD(m5_file_str, SDC.READ)
wv_nearir = the_file.select("Water_Vapor_Near_Infrared")
attrib_list = ["unit", "scale_factor", "add_offset", "valid_range", "_FillValue"]
attr_dict = wv_nearir.attributes()
wv_nearir_attrs = {k: attr_dict[k] for k in attrib_list}
print(f"wv_nearir attributes: {pprint.pformat(wv_nearir_attrs)}")
wv_nearir_data = wv_nearir.get()
the_file.end()
```

```{code-cell}
bad_data = wv_nearir_data == wv_nearir_attrs["_FillValue"]
wv_nearir_data = wv_nearir_data.astype(np.float32)
wv_nearir_data[bad_data] = np.nan
wv_nearir_scaled = wv_nearir_data * attr_dict["scale_factor"] + attr_dict["add_offset"]
```

## Note that the  scaled wv values are similar between near_ir and ir retrievals

```{code-cell}
plt.hist(wv_nearir_scaled[~np.isnan(wv_nearir_scaled)])
ax = plt.gca()
ax.set_title("1 km water vapor (cm)")
```

# Map the data

+++

### Resample the 5km IR retrieval onto a laea xy grid

Let swath_def.compute_optimal_bb_area choose the extent and dimensions for
the low resolution (lr) image.  The cell below let's pyresample create the
area_def object, which we will reuse for the 1 km watervapor retrieval to
get both onto the same grid.

The cell below produces:

* `image_wv_ir`  -- resampled 5 km infrared water vapor
* `area_def_lr`  -- area_def used for the resample

```{code-cell}
from pyresample import SwathDefinition, kd_tree, geometry

proj_params_5km = get_proj_params(m5_file_str)
proj_params_1km = get_proj_params(m3_file_str)
swath_def = SwathDefinition(lons_5km, lats_5km)
area_def_lr = swath_def.compute_optimal_bb_area(proj_dict=proj_params_5km)
#area_def_lr.name = "ir wv retrieval modis 5 km resolution (lr=low resolution)"
#area_def_lr.area_id = "modis_ir_wv"
#area_def_lr.job_id = area_def_lr.area_id
fill_value = -9999.0
image_wv_ir = kd_tree.resample_nearest(
    swath_def,
    wv_ir_scaled.ravel(),
    area_def_lr,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
image_wv_ir[image_wv_ir < -9000] = np.nan
print(f"\ndump area definition:\n{area_def_lr}\n")
print(
    (
        f"\nx and y pixel dimensions in meters:"
        f"\n{area_def_lr.pixel_size_x}\n{area_def_lr.pixel_size_y}\n"
    )
)
```

### Resample the 1km near-ir water vapor on the same grid

Reuse area_def_lr for the high resolution nearir image so we can compare directly with low resolution ir

The cell below produces:

* `image_wv_nearir_lr`  -- resampled using `area_def_lr`

```{code-cell}
swath_def = SwathDefinition(lons_1km, lats_1km)
fill_value = -9999.0
image_wv_nearir_lr = kd_tree.resample_nearest(
    swath_def,
    wv_nearir_scaled.ravel(),
    area_def_lr,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
image_wv_nearir_lr[image_wv_nearir_lr < -9000] = np.nan
```

```{code-cell}
plt.hist(image_wv_nearir_lr[~np.isnan(image_wv_nearir_lr)])
ax = plt.gca()
ax.set_title("1 km water vapor (cm), low resolution nearir scaled to 5km (lr)");
```

## now use the 1 km MYD03 lons and lats to get a full resolution xy grid

resample the neair wv onto that grid to show full resolution image.  Call this
area_def area_def_hr

The cell below produces:

* `image_wv_nearir_hr`  -- 1 km near-ir watervapor
* `area_def_hr`  -- the `area_def` file used to do the 1 k resample

```{code-cell}
### Resample the 1 km near-ir water vapor onto a 1 km grid

proj_params = get_proj_params(m3_file_str)
swath_def = SwathDefinition(lons_1km, lats_1km)
area_def_hr = swath_def.compute_optimal_bb_area(proj_dict=proj_params_1km)
# area_def_hr.name = "near ir wv retrieval modis 1 km resolution (hr=high resolution)"
# area_def_hr.area_id = "wv_nearir_hr"
# area_def_hr.job_id = area_def_hr.area_id
fill_value = -9999.0
image_wv_nearir_hr = kd_tree.resample_nearest(
    swath_def,
    wv_nearir_scaled.ravel(),
    area_def_hr,
    radius_of_influence=5000,
    nprocs=2,
    fill_value=fill_value,
)
image_wv_nearir_hr[image_wv_nearir_hr < -9000] = np.nan
```

# Save the mapped images
## Now save these three images plus their area_def's for future plotting

The function area_def_to_dict saves the pyresample area_def as a dict

At line 20 note that
```python
    a=getattr(area_def,key)
```
where key='my_attribute'  is the same as
```python
    a=area_def.my_attribute
```
but you don't have to hard-code in 'my_attribute'

```{code-cell}
import json


def area_def_to_dict(area_def):
    """
    given an area_def, save it as a dictionary`
    
    Parameters
    ----------
    
    area_def: pyresample area_def object
         
    Returns
    -------
    
    out_dict: dict containing
       area_def dictionary
         
    """
    keys = [
        "area_id",
        "proj_id",
        "name",
        "proj_dict",
        "x_size",
        "y_size",
        "area_extent",
    ]
    area_dict = {key: getattr(area_def, key) for key in keys}
    area_dict["proj_id"] = area_dict["area_id"]
    return area_dict
```

## Create a directory to hold the images and area_def dictionaries

```{code-cell}
map_dir = Path() / "map_data/wv_maps"
map_dir.mkdir(parents=True, exist_ok=True)
```

## Here's a function that writes the image plus metadata to npz and json files

We'll need to use area_def_to_dict when we create the metadata_dict

```{code-cell}
def dump_image(image_array, metadata_dict, foldername, image_array_name="image"):
    """
    write an image plus mmetadata to a folder
    
    Parameters
    ----------
    
    image_array: ndarray
        the 2-d image to be saved
    
    foldername:  Path object or string
        the path to the folder that holds the image files
        
    image_array_name:  str
        the root name for the npz and json files
        i.e. image.npz and image.json
        
    Returns: None
       side effect -- an npz and a json file are written
    """
    image_file = Path(foldername) / Path(image_array_name)
    out_dict = {image_array_name: image_array}
    np.savez(image_file, **out_dict)
    json_name = foldername / Path(image_array_name + ".json")
    with open(json_name, "w") as f:
        json.dump(metadata_dict, f, indent=4)
    print(f"\ndumping {image_file}\n and {json_name}\n")
```

## Write out images, putting useful metadeta in metadata_dict

We have three images:  

* `wv_ir` -- 5km ir retrieval
* `wv_nearir_hr`  -- 1 km nearir retrieval
* `wv_nearir_lr`  -- 1 km nearir retrieval resampled to 5 km grid

```{code-cell}
metadata_dict = dict(modismeta=parseMeta(m5_file_str))
map_dir.mkdir(parents=True, exist_ok=True)
map_dir = Path() / "map_data/wv_maps"

image_name = "wv_ir"
metadata_dict["area_def"] = area_def_to_dict(area_def_lr)
metadata_dict["image_name"] = image_name
metadata_dict["description"] = "modis ir water vapor (cm) sampled at 5 km resolution"
metadata_dict["history"] = "written by level2_cartopy_resample.ipynb"
dump_image(image_wv_ir, metadata_dict, map_dir, image_name)

image_name = "wv_nearir_hr"
metadata_dict["area_def"] = area_def_to_dict(area_def_hr)
metadata_dict["image_name"] = image_name
metadata_dict[
    "description"
] = "modis near ir water vapor (cm) sampled at 1 km resolution"
metadata_dict["history"] = "written by level2_cartopy_resample.ipynb"
dump_image(image_wv_nearir_hr, metadata_dict, map_dir, image_name)


image_name = "wv_nearir_lr"
metadata_dict["area_def"] = area_def_to_dict(area_def_lr)
metadata_dict["image_name"] = image_name
metadata_dict[
    "description"
] = "modis near ir water vapor (cm) sampled at 5 km resolution"
metadata_dict["history"] = "written by level2_cartopy_resample.ipynb"


dump_image(image_wv_nearir_lr, metadata_dict, map_dir, image_name)
```

```{code-cell}
area_def_lr
```

```{code-cell}
fig, ax = plt.subplots(1,1)
ax.imshow(image_wv_ir)
```

```{code-cell}
area_def_hr
```

```{code-cell}
fig, ax = plt.subplots(1,1)
ax.imshow(image_wv_nearir_lr)
```

```{code-cell}
fig, ax = plt.subplots(1,1)
ax.imshow(image_wv_nearir_hr)
```
