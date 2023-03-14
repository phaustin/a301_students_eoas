---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
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

```{code-cell} ipython3
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sat_lib.cloudsat import read_cloudsat_var

import a301_lib
```

```{code-cell} ipython3
#radar reflectivity data see
#http://www.cloudsat.cira.colostate.edu/dataSpecs.php?prodid=9
radar_dir = a301_lib.data_share / "pha/cloudsat"
radar_file = list(radar_dir.glob("2008291*2B-GEOPROF_GR*hdf"))[0].resolve()
print(f"{radar_file=}")
lidar_file = list(radar_dir.glob("2008291*2B-GEOPROF-LIDAR*GR*hdf"))[0].resolve()
print(f"{lidar_file=}")
```

```{code-cell} ipython3
refl_ds = read_cloudsat_var('Radar_Reflectivity',radar_file)
refl_array = refl_ds['Radar_Reflectivity']
dem_elevation = refl_ds['dem_elevation']
distance_km = refl_ds['distance_km']
longitude = refl_ds['longitude']
latitude = refl_ds['latitude']
western = np.logical_and(longitude > -180, longitude < 0)
eastern = np.logical_not(western)
height = refl_ds.coords['height']
lidar_ds = read_cloudsat_var('LayerTop',lidar_file)
layer_top = lidar_ds['LayerTop']

fig, axes =plt.subplots(2,2,figsize=(11,11))
axis1,axis2,axis3,axis4 = axes.ravel()
start=21000  #seconds in orbit
stop=22000
meters2km = 1.e-3
storm_distance = distance_km[start:stop]
storm_distance = storm_distance - storm_distance[0]
im=axis1.pcolor(storm_distance,height*meters2km,refl_array[start:stop,:].T)
axis1.set_xlabel('storm distance (km)')
axis1.set_ylabel('height (km)')
cb=fig.colorbar(im)
cb.set_label('reflectivity (dbZ)')

axis2.plot(distance_km,layer_top*meters2km,'b')
axis2.plot(distance_km,dem_elevation*meters2km,'r')
axis2.set_xlabel('track distance (km)')
axis2.set_ylabel('height (km)')
axis2.set_title('whole orbit: lidar cloud top (blue) and dem surface elevation (red)')


axis3.plot(latitude[western],layer_top.data[western]*meters2km,'b')
axis3.plot(latitude.data[western],dem_elevation.data[western]*meters2km,'r')
axis3.set_xlabel('latitude (deg N)')
axis3.set_ylabel('height (km)')
axis3.set_title('western hem: lidar cloud top (blue) and dem surface elevation (red)')


axis4.plot(latitude[eastern],layer_top.data[eastern]*meters2km,'b')
axis4.plot(latitude.data[eastern],dem_elevation.data[eastern]*meters2km,'r')
axis4.set_xlabel('latitude (deg N)')
axis4.set_ylabel('height (km)')
axis4.set_title('eastern hem: lidar cloud top (blue) and dem surface elevation (red)')


```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
