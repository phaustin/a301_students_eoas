---
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info,-toc
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

(week3:modis_geom)=
# Reading modis level1b data

## Background

[Modis geolocation data](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/MYD03#overview)

```{code-cell} ipython3
:trusted: true

import pprint
from pathlib import Path

import a301_lib
import numpy as np
from matplotlib import pyplot as plt
from pyhdf.SD import SD
from pyhdf.SD import SDC
```

```{code-cell} ipython3
:trusted: true

print(a301_lib.sat_data)
type(a301_lib.sat_data)
```

```{code-cell} ipython3
:tags: []
:trusted: true

dir(a301_lib)
```

## get the geom file in the `sat_data` pha flder

a301_lib.sat_data is a `PosixPath` object, which is the way that python is able to treat all folder paths the same, whether they look like `C:\Users\phil` or `/Users/home/phil`

```{code-cell} ipython3
:trusted: true

hdf4_dir = a301_lib.data_share / "pha/cloudsat"
all_files = list(hdf4_dir.glob("*hdf"))
test = all_files[0]
test
```

Now read that file (converting PosixPath into a string since the pyhdf library is
expecting a string).  Use the `.info` method to get the number of datasets and attributes

```{code-cell} ipython3
:scrolled: true
:trusted: true

file_name = str(all_files[0])
print(f"reading {file_name}")
the_file = SD(file_name, SDC.READ)
stars = "*" * 50
print(
    (
        f"\n{stars}\n"
        f"number of datasets, number of attributes\n"
        f"={the_file.info()}\n"
        f"{stars}\n"
    )
)
```

```{code-cell} ipython3
:tags: []
:trusted: true

the_file.attributes()
```

## Find the datasets and print their indices

We know we've got 46 datasets in the file -- what are their names?

```{code-cell} ipython3
:trusted: true

datasets_dict = the_file.datasets()

for idx, sds in enumerate(datasets_dict.keys()):
    print(idx, sds)

#breakpoint()
```

```{code-cell} ipython3
:tags: []
:trusted: true

out=the_file.select('precip_liquid_water')
out.dimensions()
```

 ## open the latitude and longitude dataset

+++

## read the latlon data, save and plot it

```{code-cell} ipython3
:trusted: true

latitude_data = the_file.select("Latitude")
longitude_data = the_file.select("Longitude")
longitude = longitude_data[:50,:50]
latitude = latitude_data[:50,:50]
print("shapes: ",longitude.shape,latitude.shape)
np.savez('pha_2013222.2105.npz',longitude=longitude,latitude=latitude)
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
ax.plot(longitude,latitude,'k+')
ax.set(title="lat/lons for first 50 rows and columns",
       xlabel = "longitude (degrees east)",ylabel="latitude (degrees north)")
fig.savefig("first_50.png")
```

## close the file

```{code-cell} ipython3
:trusted: true

the_file.end()
```
