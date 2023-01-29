import a301_lib
import numpy as np
from matplotlib import pyplot as plt
from pyhdf.SD import SD
from pyhdf.SD import SDC
from pathlib import Path
import h5py
from contextlib import contextmanager
import os
from sat_lib.modismeta_read import get_core

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)

def readgeom(the_file):
    """
    read and calibrate a MODIS band from an open hdf4 SD dataset

    Parameters
    ----------

       the_file:pyhdf.SD object
           the dataset open for reading

    Returns
    -------
       lats,lons:  tuple
           two ndarrays containing lats and lons
    """
    lats = the_file.select("Latitude").get()
    lons = the_file.select("Longitude").get()
    return lats, lons


def write_geom(outname,latitude_array, longitude_array,core_metadata):
    """
    write MYD03 lats/lons to an h5 file

    Parameters
    ----------

       outname: str
           name of output hdf
       radiance_array: ndarray
           the pixel radiances in W/m^2/sr/micron

    Returns
    -------
       None-- the_file is closed by this function
    """
    with h5py.File(outname, "w") as f:
        group = f.create_group("geometry")
        dset = group.create_dataset("latitude", latitude_array.shape,
                                    dtype=latitude_array.dtype)
        dset[...] = latitude_array[...]
        dset = group.create_dataset("longitude", longitude_array.shape,
                                    dtype=longitude_array.dtype)
        dset[...] = longitude_array[...]
        dset.attrs['units'] = "degrees E"
        f.attrs["CoreMetadata.0"] = core_metadata
        f.attrs["history"] = 'written by process_geom.py'
        print(f"wrote {outname}")


if  __name__ == "__main__":
    import a301_lib
    the_dir = a301_lib.sat_data / "hdf4_files"
    with cd(the_dir):
        all_files = list(the_dir.glob("MYD03*2105*hdf"))
        all_files = [str(item) for item in all_files if (item.parent.name != "h5_dir"
                                                         and item.name.find('MYD03') == 0)]
        print(f"found these files: {all_files}")
        out_dir = the_dir / "h5_dir"
        out_dir.mkdir(parents=True, exist_ok=True)
        for a_file in all_files:
            str_file = Path(a_file).name
            core_metadata = get_core(a_file)
            out_file = out_dir  / f"geom_{str_file}"
            out_file = out_file.with_suffix('.h5')
            print(f"reading {a_file}, writing {out_file}")
            the_sd = SD(str_file, SDC.READ)
            the_band=30
            latitude_array, longitude_array = readgeom(the_sd)
            the_sd.end()
            write_geom(out_file,latitude_array, longitude_array, core_metadata)
