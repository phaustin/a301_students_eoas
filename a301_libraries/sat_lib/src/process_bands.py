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
    print(f"reading ban {the_band}")
    print(thechan_index)
    thechan_data = longwave_data[thechan_index, :, :]
    scales = longwave_data.attributes()["radiance_scales"]
    offsets = longwave_data.attributes()["radiance_offsets"]
    thechan_scale = scales[thechan_index]
    thechan_offset = offsets[thechan_index]
    thechan_calibrated = (thechan_data - thechan_offset) * thechan_scale
    return thechan_calibrated

def write_bands(outname,chan_rads,core_metadata):
    """
    write a MODIS band 30 to an h5 file

    Parameters
    ----------

       outname: str
           name of output hdf
       chan_rads: dict
           the pixel radiances in W/m^2/sr/micron
           key: channel number (int)
           value: radiance (ndarray)

    Returns
    -------
       None-- the_file is closed by this function
    """
    with h5py.File(outname, "w") as f:
        group = f.create_group("channels")
        for key, value in chan_rads.items():
            chan_name = f"chan{key}"
            radiance_array = value
            radiance_array = radiance_array.astype(np.float32)
            dset = group.create_dataset(chan_name, radiance_array.shape,
                                    dtype=radiance_array.dtype)
            dset[...] = radiance_array[...]
            dset.attrs['units'] = "W/m^2/micron/ sr"
        f.attrs["history"] = 'written by process.py'
        f.attrs["CoreMetadata.0"] = core_metadata
        print(f"wrote {outname}")




if  __name__ == "__main__":
    import a301_lib
    sat_data = a301_lib.sat_data / "hdf4_files"
    with cd(sat_data):
        all_files = list(sat_data.glob("MYD021KM*2105*hdf"))
        all_files = [item for item in all_files if (item.parent.name != "h5_dir"
                                                         and item.name.find('MYD02') >= 0)]
        print(f"found {all_files}")
        out_dir = sat_data /"h5_dir"
        out_dir.mkdir(parents=True, exist_ok=True)
        for a_file in all_files[:]:
            core_metadata = get_core(a_file)
            out_file = out_dir  / f"oct9_{a_file.name}"
            out_file = out_file.with_suffix('.h5')
            print(f"reading {a_file}, writing {out_file}")
            the_sd = SD(str(a_file), SDC.READ)
            band_list = [30,31,32]
            rad_dict = {}
            for the_band in band_list:
                rad_dict[the_band] =  readband(the_sd,the_band)
            the_sd.end()
            write_bands(out_file,rad_dict,core_metadata)
