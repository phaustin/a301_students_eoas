import rioxarray
import xarray
import numpy as np
from pathlib import Path

lat = 49
lon=-120
size = 5

lat_range = np.array([size, -size]) + lat
lon_range = np.array([-size, size]) + lon

copern_tif  = list(Path().glob("*tif"))[0]
copern_xarray = rioxarray.open_rasterio(copern_tif)
copern_xarray = copern_xarray.sel(y=slice(lat_range[0], lat_range[1]), x=slice(lon_range[0], lon_range[1]))
copern_xarray
