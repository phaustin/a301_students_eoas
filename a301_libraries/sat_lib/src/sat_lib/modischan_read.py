"""
reading channels and variables
______________________________
"""
from pyhdf.SD import SD, SDC
import pyhdf
import numpy as np
from pathlib import Path

def readband_lw(the_file, the_band):
    """
    read and calibrate a MODIS L1B longwave band from the 
     path to the hdf4 file
    
    Parameters
    ----------
    
       the_file: str
           path to the hdf4 file
       the_band: int
           band number for MODIS (20-36)
           
    Returns
    -------
       the_chan_calibrated: ndarray
           the pixel radiances in W/m^2/sr/micron
    """
    sd_file = sd_open_file(the_file)
    longwave_data = sd_file.select("EV_1KM_Emissive")  # select sds
    longwave_bands = sd_file.select("Band_1KM_Emissive")
    band_nums = longwave_bands.get()
    thechan_index = int(np.searchsorted(band_nums, the_band))
    print(f"channel index for band {the_band} is {thechan_index}")
    thechan_data = longwave_data[thechan_index, :, :]
    scales = longwave_data.attributes()["radiance_scales"]
    offsets = longwave_data.attributes()["radiance_offsets"]
    thechan_scale = scales[thechan_index]
    thechan_offset = offsets[thechan_index]
    thechan_calibrated = (thechan_data - thechan_offset) * thechan_scale
    print(f"f{thechan_offset=}, {thechan_scale=}")
    sd_file.end()
    return thechan_calibrated


def readband_wv(the_file, band_name):
    """
    see: https://atmosphere-imager.gsfc.nasa.gov/sites/default/files/ModAtmo/MYD05_L2.C6.CDL.fs
       for file format
       
    read and calibrate a MODIS level 2 water vapor file
    
    Parameters
    ----------
    
       the_file: str
           path to the hdf file
       band_name: str
           either 'Water_Vapor_Near_Infrared` or `Water_Vapor_Infrared` 
           
    Returns
    -------
       the_chan_calibrated: ndarray
           column water vapor in cm
    """
    sd_file = sd_open_file(the_file)
    wv_data = sd_file.select(band_name)  # select sds
    wv_image = wv_data.get()
    #
    # convert from int16 to float64
    #
    wv_image = wv_image.astype('float64')
    wv_scale = wv_data.attributes()['scale_factor']
    wv_offset = wv_data.attributes()['add_offset']
    fill_value = wv_data.attributes()['_FillValue']
    #
    # convert fill values = -9999 to np.nan
    #
    wv_image[wv_image == fill_value] = np.nan
    wv_calibrated = (wv_image * wv_scale) + wv_offset
    sd_file.end()
    return wv_calibrated

def read_plainvar(the_file, the_var):
    """
    read a modis variable like latitude or longitude that doesn't require
    scaling or offset

    Parameters
    ----------
    
       the_file: Path or str for the hdf file

       the_var: str
           variable name to extract
           
    Returns
    -------
       var_array: ndarray
           the_variable as a numpy array
    """
    sd_file = sd_open_file(the_file)
    sd_var = sd_file.select(the_var)
    #
    # get the variable and convert to a ndarray
    # [...] gets all the data, no matter how many
    # dimensions
    #
    var_array = sd_var.get()[...]
    sd_file.end()
    return var_array
    
def sd_open_file(the_file):
    try:
        #
        # is the_file a str or Path?
        #
        hdf_path = Path(the_file)
        if not hdf_path.is_file():
            raise ValueError(f"can't find file {hdf_path}")
        sd_file = SD(str(the_file), SDC.READ)
        # print(f"sd_open -- file: {the_file}")
    except TypeError:
        raise ValueError(f"need a str or path got {the_file}")
    #
    # don't forget to close with sd_file.end() when finished
    #
    return sd_file




