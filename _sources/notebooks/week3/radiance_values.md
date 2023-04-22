---
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info,-toc
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(week3:radiance_check)=
# Sanity checking radiance vaules

This notebook compares radiances from channel 30 (9.73 $\mu m$) and channel 31 (11.03 $\mu m$)

```{code-cell} ipython3
:trusted: true

import pprint
from pathlib import Path

import a301_lib
import numpy as np
from matplotlib import pyplot as plt
from pyhdf.SD import SD
from pyhdf.SD import SDC
from matplotlib.colors import Normalize
```

## two useful functions

Extra these from week2/radiation.py and week1/modis_level1b_read.md

```{code-cell} ipython3
:trusted: true

#
# get Stull's c_1 and c_2 from fundamental constants
#
# c=2.99792458e+08  #m/s -- speed of light in vacuum
# h=6.62606876e-34  #J s  -- Planck's constant
# k=1.3806503e-23  # J/K  -- Boltzman's constant

c, h, k = 299_792_458.0, 6.626_070_04e-34, 1.380_648_52e-23
c1 = 2.0 * h * c ** 2.0
c2 = h * c / k
sigma = 2.0 * np.pi ** 5.0 * k ** 4.0 / (15 * h ** 3.0 * c ** 2.0)



def Llambda(wavel, Temp):
    """
    Calculate the blackbody radiance starting with(Stull 2.13)

    Parameters
    ----------

      wavel: float or array
           wavelength (meters)

      Temp: float
           temperature (K)

    Returns
    -------

    Llambda:  float or arr
           monochromatic blackbody radiance (W/m^2/m/sr)
    """
    # Stull: Elambda_val = c1 * np.pi / (wavel ** 5.0 * (np.exp(c2 / (wavel * Temp)) - 1))
    Llambda_val = c1  / (wavel ** 5.0 * (np.exp(c2 / (wavel * Temp)) - 1))
    return Llambda_val

def readband(the_file,the_band):
    """
    read and calibrate a MODIS band from an open hdf4 SD dataset
    
    Parameters
    ----------
    
       the_file:pyhdf.SD object
           the dataset open for reading
       the_band: int
           band number for MODIS (1-36)
           
    Returns
    -------
       the_chan_calibrated: ndarray
           the pixel radiances in W/m^2/sr/micron
    """
    longwave_data = the_file.select("EV_1KM_Emissive")  # select sds
    longwave_bands = the_file.select("Band_1KM_Emissive")
    band_nums = longwave_bands.get()
    thechan_index = int(np.searchsorted(band_nums, the_band))
    print(f"channel index for band {the_band} is {thechan_index}")
    thechan_data = longwave_data[thechan_index, :, :]
    scales = longwave_data.attributes()["radiance_scales"]
    offsets = longwave_data.attributes()["radiance_offsets"]
    thechan_scale = scales[thechan_index]
    thechan_offset = offsets[thechan_index]
    thechan_calibrated = (thechan_data - thechan_offset) * thechan_scale
    return thechan_calibrated

```

## plot some channel 30/31 radiances

```{code-cell} ipython3
:trusted: true

hdf4_dir = a301_lib.sat_data / "pha"
all_files = list(hdf4_dir.glob("MYD021KM*2013222*hdf"))
print(all_files)
file_name = str(all_files[0])
print(f"reading {file_name}")
the_file = SD(file_name, SDC.READ)

the_band=30
ch30_radiance = readband(the_file,the_band)
from matplotlib import pyplot as plt
fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(8, 4))
ax1.hist(ch30_radiance.flat[0:5000])
ax1.set_ylabel('pixel count (unitless)')
ax1.set_title(f'Radiance for band {the_band}')
ax1.set_xlabel("radiance ($W\,m^{-2}\mu m^{-1}\,sr^{-1}$)")
the_band=31
ch31_radiance = readband(the_file,the_band)
ax2.hist(ch31_radiance.flat[0:5000])
ax2.set_ylabel('pixel count (unitless)')
ax2.set_title(f'Radiance for band {the_band}')
ax2.set_xlabel("radiance ($W\,m^{-2}\mu m^{-1}\,sr^{-1}$)")
the_file.end()
```

## Plot a planck function for a 280 K blackbody

Use code from week2/planck_function.md

```{code-cell} ipython3
:trusted: true

Temp = 280  # K
npoints=10000
wavelengths = np.linspace(0.1, 500.0, npoints) * 1.0e-6  # meters
Lstar = Llambda(wavelengths, Temp)  #W/m^2/m/sr
fig, ax = plt.subplots(1, 1, figsize=(5,5))
ax.plot(wavelengths * 1.0e6, Lstar * 1.0e-6)
ax.set(xlim=[0, 50])
ax.grid(True)
ax.set(
    xlabel="wavelength (m)",
    ylabel="$L_\lambda^*\ (W\,m^{-2}\,\mu^{-1}$)",
    title=f"Monochromatic blackbody radiance at Temp={Temp} K",
);
```

## close the file

```{code-cell} ipython3
:trusted: true


```
