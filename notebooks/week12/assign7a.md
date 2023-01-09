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

(assign7a)=
# Assign 7a: Modis swath regridding

Skip to the bottom to see the assignment.  Below, I've shown how to regrid the Vancouver 1 km nearir water vapor data onto a reasonable grid that could be used, for example, to remap many different swaths for comparison.

```{code-cell} ipython3
import json
import pdb
import pprint
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from pyhdf.SD import SD
from pyhdf.SD import SDC
from pyproj import CRS, Transformer
from pyresample import SwathDefinition, kd_tree, geometry

import a301_lib
from sat_lib.geometry import get_proj_params
## Image('figures/MYBRGB.A2016224.2100.006.2016237025650.jpg',width=600)
```

## Read in the Vancouver level 2 water vapor and 1 km lat/lons

```{code-cell} ipython3
m5_file= (a301_lib.sat_data / 'hdf4_files').glob("**/MYD05*2105*hdf")
m3_file = (a301_lib.sat_data / 'hdf4_files').glob("MYD03*2105*.hdf")
m5_file_str = str(list(m5_file)[0])
m3_file_str = str(list(m3_file)[0])
print(m5_file_str)
print(m3_file_str)

the_file = SD(m3_file_str, SDC.READ)
lats_1km = the_file.select("Latitude").get()
lons_1km = the_file.select("Longitude").get()
the_file.end()
print(lats_1km.shape)
```

## Scale the data

```{code-cell} ipython3
the_file = SD(m5_file_str, SDC.READ)
wv_nearir = the_file.select("Water_Vapor_Near_Infrared")
attrib_list = ["unit", "scale_factor", "add_offset", "valid_range", "_FillValue"]
attr_dict = wv_nearir.attributes()
wv_nearir_attrs = {k: attr_dict[k] for k in attrib_list}
print(f"wv_nearir attributes: {pprint.pformat(wv_nearir_attrs)}")
wv_nearir_data = wv_nearir.get()
the_file.end()
```

```{code-cell} ipython3
bad_data = wv_nearir_data == wv_nearir_attrs["_FillValue"]
wv_nearir_data = wv_nearir_data.astype(np.float32)
wv_nearir_data[bad_data] = np.nan
wv_nearir_scaled = wv_nearir_data * attr_dict["scale_factor"] + attr_dict["add_offset"]
```

```{code-cell} ipython3
plt.hist(wv_nearir_scaled[~np.isnan(wv_nearir_scaled)])
ax = plt.gca()
ax.set_title("1 km water vapor (cm)");
```

## Get the optimum bounding box

+++

In order to get a feeling for the extent we want, we can make a first
pass as before with pyresample `swath_def.compute_optimal_bb_area` from resample and our own
[get_proj_params](https://github.com/phaustin/a301_2020/blob/2775d9249ebf43356232e05eabeb72182655758b/sat_lib/geometry.py#L12-L44)
We'll get a warning from pyproj because pyresample hasn't updated to the new wkt format yet, but
they are harmless.

```{code-cell} ipython3
proj_params = get_proj_params(m3_file_str)
print(f"here are the parameters from the sat_lib.geometry module:\n{proj_params=}")
swath_def = SwathDefinition(lons_1km, lats_1km)
area_def_hr = swath_def.compute_optimal_bb_area(proj_dict=proj_params)
fill_value = -9999.0
image_wv_nearir_hr = kd_tree.resample_nearest(
    swath_def,
    wv_nearir_scaled.ravel(),
    area_def_hr,
    radius_of_influence=5000,
     nprocs=2,
    fill_value=fill_value
)
image_wv_nearir_hr[image_wv_nearir_hr < -9000] = np.nan
print(f"here is the area_def_hr crs for cartopy\n{area_def_hr.to_cartopy_crs()}")
proj4_str = area_def_hr.proj_str
print(f"\nhere is the same crs as a proj4 string\n{proj4_str=}")
```

## Find our extent in lat/lon coords

To get a feeling for the lat/lon corners, use pyproj to transform
as we did in the week 10 {ref}`image_zoom` notebook.  Also see
the [pyproj docs](https://pyproj4.github.io/pyproj/stable/api/transformer.html)

```{code-cell} ipython3
#area_extent: (lower_left_x, lower_left_y, upper_right_x, upper_right_y)
ll_x,ll_y,ur_x,ur_y =area_def_hr.area_extent
print(f"lower left and upper right corners for the laea crs:\n{(ll_x,ll_y,ur_x,ur_y)=}")
```

```{code-cell} ipython3
p_latlon = CRS.from_proj4("+proj=latlon")
p_crs = CRS.from_proj4(proj4_str)
transform = Transformer.from_crs(p_crs, p_latlon)
ll_lon,ll_lat = transform.transform(ll_x,ll_y)
ur_lon, ur_lat =transform.transform(ur_x,ur_y)
print(f"same corners given in lon/lat:\n"
      f"{(ll_lon,ll_lat,ur_lon,ur_lat)=}")
```

### Double check by backward transforming to the laea crs

note we've a lost a tiny bit of accuracy in the round-trip, but we are just
using this to guide us on our lat/lon corner choices.

```{code-cell} ipython3
ll_x, ll_y = transform.transform(ll_lon,ll_lat,direction='INVERSE')
print(f"check the round-trip back to laea\n{(ll_x,ll_y)=}")
#help(transform.transform)
```

## Writing a new area_def

Now write a new area_def following the [pyresample example](https://pyresample.readthedocs.io/en/latest/geo_def.html).  Round the
central lon/lat to (-121,40), and the round the extent to nice round integer lon/lat values.
Once we have these rounded values, we need to map the extent back to laea using
the `INVERSE` keyword for the transform direction.

```{code-cell} ipython3
from pyresample.geometry import AreaDefinition
area_id = 'pnw'
description = 'Pacific NW grid'
proj_id = 'pnb'
proj_params['lon_0']= -121
proj_params['lat_0'] = 40
ll_lon,ll_lat,ur_lon,ur_lat=(-135, 27., -100., 50)
ll_x, ll_y = transform.transform(ll_lon,ll_lat,direction='INVERSE')
ur_x, ur_y = transform.transform(ur_lon,ur_lat,direction='INVERSE')
width = 500
height = 500
area_extent = (ll_x, ll_y, ur_x, ur_y)
area_def_lr = AreaDefinition(area_id, description, proj_id, proj_params,
                            width, height, area_extent)

print(f"the area_def: \n{area_def_lr=}")
```

## Now reproject the swath onto this new area_def_lr

```{code-cell} ipython3
fill_value = -9999.0
image_wv_nearir_lr = kd_tree.resample_nearest(
    swath_def,
    wv_nearir_scaled.ravel(),
    area_def_lr,
    radius_of_influence=5000,
     nprocs=2,
    fill_value=fill_value
)
image_wv_nearir_lr[image_wv_nearir_lr < -9000] = np.nan
```

```{code-cell} ipython3
plt.imshow(image_wv_nearir_lr)
print(f"new pixel x an y sizes (m):\n{area_def_lr.pixel_size_x}, {area_def_lr.pixel_size_y}")
area_def_lr
```

## Assignment 7a

Make the above code work for your image, and come up with an appropriate affine transform so that you write the geotiff and png files that contain the image in the laea crs with the following specfications:


    crs=laea, wgs84 datum
    lon_0 and lat_0  rounded to integer degree
    lower_left and upper_right corners in lat/lon crs rounded to nearest degree that doesn't
       clip the image
    500 x 500 pixels

Add date and contact tags with the date you wrote the geotiff, and your name

+++
