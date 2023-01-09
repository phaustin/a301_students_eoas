---
jupytext:
  cell_metadata_filter: all
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

(week4:resample)=
# Use pyresample to plot channel 30 radiances

This notebook uses to hdf5 files: a geom file containing lats and lons copied
from the original MYD03 and a ch30 file containing channel 30 radiances
copied and scaled from a MYD031KM file

```{code-cell} ipython3
import json
import pdb
import pprint
import shutil
from pathlib import Path

import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import h5py
import a301_lib
import sys
from pyresample import kd_tree
from sat_lib.modismeta_read import get_core, parseMeta
```

## Find the files in the sat_data.h5_dir

```{code-cell} ipython3
geom_filelist = list(a301_lib.sat_data.glob("h5_dir/geom*2105*h5"))
ch30_filelist = list(a301_lib.sat_data.glob("h5_dir/ch30*2105*h5"))
```

```{code-cell} ipython3
geom_file_name = geom_filelist[0]
print(geom_file_name)
ch30_file_name = ch30_filelist[0]
print(ch30_file_name)
```

## Read the latitudes and longitudes

Also read the core metadata to get the swath corners

```{code-cell} ipython3
with h5py.File(geom_file_name,'r') as f:
    print(list(f.keys()))
    geom_group = f['geometry']
    print(list(geom_group.keys()))
    lats = geom_group['latitude'][...]
    print(lats.shape)
    lons = geom_group['longitude'][...]
    print(lons.shape)
    print(f.attrs.keys())
    core_metadata = f.attrs["CoreMetadata.0"]
    swath_info = parseMeta(core_metadata)
```

## Read the channel 30 radiances

```{code-cell} ipython3
with h5py.File(ch30_file_name,'r') as f:
    print(list(f.keys()))
    channel_group = f['channels']
    print(list(channel_group.keys()))
    ch30 = channel_group['chan30'][...]
    print(ch30.shape)
```

## Now resample

pyresample needs proj4 map parameters to put together its grid.  These are
returned by the get_proj_params file below.

```{code-cell} ipython3
def get_proj_params(swath_info):
    """
    given a swath_info dictionary return proj4 parameters
    for use by cartopy or pyresample, assuming a laea projection
    and WGS84 datum
    
    Parameters
    ----------
    
    swath_info:  dictionary
       returned by modismeta_read
    
    Returns
    -------
    
    proj_params: dict
        dict with parameters for proj4
        
    """
    import cartopy.crs as ccrs

    globe_w = ccrs.Globe(datum="WGS84", ellipse="WGS84")
    projection_w = ccrs.LambertAzimuthalEqualArea(
        central_latitude=swath_info["lat_0"],
        central_longitude=swath_info["lon_0"],
        globe=globe_w,
    )
    proj_params = projection_w.proj4_params
    return proj_params
```

```{code-cell} ipython3
proj_params =get_proj_params(swath_info)
print(f"proj_params: {proj_params}")
```

* Use pyresample to define a new grid in this projection

```{code-cell} ipython3
from pyresample import load_area, save_quicklook, SwathDefinition

proj_params = get_proj_params(swath_info)
swath_def = SwathDefinition(lons, lats)
area_def = swath_def.compute_optimal_bb_area(proj_dict=proj_params)
```

```{code-cell} ipython3
print(area_def)
```

* resample ch30 on this grid

```{code-cell} ipython3
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
print(f"\ndump area definition:\n{area_def}\n")
print(
    (
        f"\nx and y pixel dimensions in meters:"
        f"\n{area_def.pixel_size_x}\n{area_def.pixel_size_y}\n"
    )
)
```

* replace missing values with floating point nan

```{code-cell} ipython3
nan_value = np.array([np.nan], dtype=np.float32)[0]
image_30[image_30 < -9000] = nan_value
```

## Plot the image using cartopy

* Create a palette

We want to spread the colors over a limited range of values between 0.1 and 7 W/m^2/microns/sr so we
will set over and under colors and normalize the data to this range

 Some links about colors:

* [rods, cones and rgb](https://theneurosphere.com/2015/12/17/the-mystery-of-tetrachromacy-if-12-of-women-have-four-cone-types-in-their-eyes-why-do-so-few-of-them-actually-see-more-colours/)

* [matplotlib palettes](https://matplotlib.org/examples/color/colormaps_reference.html)

* [xkcd color survey](https://blog.xkcd.com/2010/05/03/color-survey-results/)

* [xkcd colors from matplotlib](https://seaborn.pydata.org/generated/seaborn.xkcd_palette.html)

* [wikipedia article on RGB colors](https://en.wikipedia.org/wiki/RGB_color_model)

```{code-cell} ipython3
pal = plt.get_cmap("plasma")
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("r")  # color cells > vmax red
pal.set_under("k")  # color cells < vmin black
vmin = 0.1
vmax = 7.0
from matplotlib.colors import Normalize

the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
```

* use the palette on the image_30 array

```{code-cell} ipython3
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
fig.colorbar(cs, extend="both")
```

* write out all the projection information as a json file

Make a new folder to hold this, along with the resampled image written as
a [numpy npz file](https://docs.scipy.org/doc/numpy/reference/generated/numpy.savez.html)

In that folder, also write out a json file with all the metadata

```{code-cell} ipython3
out_dict = {}
out_dict["proj_params"] = crs.proj4_params
out_dict["extent"] = crs.bounds
globe = crs.globe.to_proj4_params()
out_dict["globe"] = dict(globe)
out_dict["metadata"] = swath_info
out_dict["field_name"] = "ch30"
out_dict["units"] = "W/m^2/sr/micron"
out_dict["variable_description"] = "channel 30 radiance"
out_dict["x_size"] = area_def.x_size
out_dict["y_size"] = area_def.y_size
out_dir_name = "ch30_resample"
out_dict["out_dir"] = out_dir_name
out_dir = a301_lib.data_share.parent / Path("test_data") / Path(out_dir_name)
out_dir.mkdir(parents=True, exist_ok=True)
image_name = out_dir / Path(f"{out_dir_name}.npz")
json_name = out_dir / Path(f"{out_dir_name}.json")
np.savez(image_name, ch30_resample=image_30)
with open(json_name, "w") as f:
    json.dump(out_dict, f, indent=4)
```
