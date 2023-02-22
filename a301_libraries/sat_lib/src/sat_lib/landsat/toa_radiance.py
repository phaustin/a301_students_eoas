"""
ported from https://github.com/NASA-DEVELOP/dnppy/tree/master/dnppy/landsat
"""

# standard imports
from .landsat_metadata import landsat_metadata
from . import core
import os
from pathlib import Path
import numpy as np
import rasterio

__all__ = ['toa_radiance_8',          # complete
           'toa_radiance_457',
           'calc_radiance_8',
           'calc_radiance_457'
          ] 

def calc_radiance_457(np_image,band_num,meta_path):
    """
    Calculate the radiance for a landsat 4,5,7 band

    Parameters
    ----------

    np_image: ndarray, 2-D, uint16
          landsat scene counts

    band_num:  str
        landsat ban

    meta_path: Path object
       path to MTL.txt file for scene

    Returns
    -------

    TOA_rad: ndarray, 2-d, float32
       radiance for the scene (W/m^2/micron/sr
    """

    #the presence of a PRODUCT_CREATION_TIME category is used to identify old metadata
    #if this is not present, the meta data is considered new.
    #Band6length refers to the length of the Band 6 name string. In the new metadata this string is longer

    #metadata format was changed August 29, 2012. This tool can process either the new or old format
    with open(meta_path) as f:
        MText = f.read()

    metadata = landsat_metadata(meta_path)

    if "PRODUCT_CREATION_TIME" in MText:
        Meta = "oldMeta"
        Band6length = 2
    else:
        Meta = "newMeta"
        Band6length = 8

    #The tilename is located using the newMeta/oldMeta indixes and the date of capture is recorded
    if Meta == "newMeta":
        TileName    = getattr(metadata, "LANDSAT_SCENE_ID")
        year        = TileName[9:13]
        jday        = TileName[13:16]
        date        = getattr(metadata, "DATE_ACQUIRED")

    elif Meta == "oldMeta":
        TileName    = getattr(metadata, "BAND1_FILE_NAME")
        year        = TileName[13:17]
        jday        = TileName[17:20]
        date        = getattr(metadata, "ACQUISITION_DATE")

    #the spacecraft from which the imagery was capture is identified
    #this info determines the solar exoatmospheric irradiance (ESun) for each band
    spacecraft = getattr(metadata, "SPACECRAFT_ID")

    if "7" in spacecraft:
        TM_ETM_bands = ['1','2','3','4','5','7','8','6_VCID_1','6_VCID_2']

    elif "5" in spacecraft:
        TM_ETM_bands = ['1','2','3','4','5','7']

    elif "4" in spacecraft:
        TM_ETM_bands = ['1','2','3','4','5','7']

    else:
        raise ValueError("Landsat 4, 5, or 7")
        #arcpy.AddError("This tool only works for Landsat 4, 5, or 7")
        #raise arcpy.ExecuteError()

    if band_num not in TM_ETM_bands:
        errmsg=f"""Can only perform reflectance conversion on OLI sensor bands")
                  Skipping band {band_num}
               """
        raise ValueError(errmsg)
    
    # print(f"Processing radiance for band {band_num}")
    # str_path = str(meta_path)
    # band_path  = Path(str_path.replace("MTL.txt",f"B{band_num}.TIF"))

    # with rasterio.open(str(band_path)) as raster:
    #     Qcal = raster.read(1)

    #using the oldMeta/newMeta indixes to pull the min/max for radiance/Digital numbers
    if Meta == "newMeta":
        LMax    = getattr(metadata, "RADIANCE_MAXIMUM_BAND_{0}".format(band_num))
        LMin    = getattr(metadata, "RADIANCE_MINIMUM_BAND_{0}".format(band_num))  
        QCalMax = getattr(metadata, "QUANTIZE_CAL_MAX_BAND_{0}".format(band_num))
        QCalMin = getattr(metadata, "QUANTIZE_CAL_MIN_BAND_{0}".format(band_num))

    elif Meta == "oldMeta":
        LMax    = getattr(metadata, "LMAX_BAND{0}".format(band_num))
        LMin    = getattr(metadata, "LMIN_BAND{0}".format(band_num))  
        QCalMax = getattr(metadata, "QCALMAX_BAND{0}".format(band_num))
        QCalMin = getattr(metadata, "QCALMIN_BAND{0}".format(band_num))

    TOA_rad = (((LMax - LMin)/(QCalMax-QCalMin)) * (np_image - QCalMin)) + LMin
    return TOA_rad


def calc_radiance_8(np_image,band_num,meta_path):
    """
    Calculate the radiance for a landsat 8 band

    Parameters
    ----------

    np_image: ndarray, 2-D, float
          landsat scene counts

    band_num:  str
        landsat ban

    meta_path: Path object
       path to MTL.txt file for scene

    Returns
    -------

    TOA_rad: ndarray, 2-d, float32
       radiance for the scene (W/m^2/micron/sr
    """

    meta = landsat_metadata(meta_path)
    #scrape the attribute data
    Ml   = getattr(meta,"RADIANCE_MULT_BAND_{0}".format(band_num)) # multiplicative scaling factor
    Al   = getattr(meta,"RADIANCE_ADD_BAND_{0}".format(band_num))  # additive rescaling factor

    #calculate Top-of-Atmosphere radiance
    TOA_rad = (np_image * Ml) + Al
    return TOA_rad


def toa_radiance_8(band_nums, meta_path):
    """
    Top of Atmosphere radiance (in Watts/(square meter x steradians x micrometers))
    conversion for landsat 8 data. To be performed on raw Landsat 8
    level 1 data. See link below for details:
    see here http://landsat.usgs.gov/Landsat8_Using_Product.php

    Parameters
    ----------

    band_nums: list
           A list of desired band numbers such as [3, 4, 5]

    meta_path: str or Path object
             The full filepath to the MTL.txt metadata file for those bands


    Returns
    -------

    out_dict: dict
        dictionary with band_num as keys and TOA radiance (W/m2/sr/um) as values
    """

    meta_path = Path(meta_path).resolve()

    #enforce list of band numbers and grab the metadata from the MTL file
    band_nums = core.enf_list(band_nums)
    band_nums = map(str, band_nums)
    
    OLI_bands = ['1','2','3','4','5','6','7','8','9','10','11']
    
    #loop through each band
    out_dict=dict()
    
    for band_num in band_nums:
        print(f'working on band {band_num}')
        if band_num not in OLI_bands:
            print("Can only perform radiance conversion on OLI sensor bands")
            print("Skipping band {0}".format(band_num))
            continue
        
        #create the band name
        str_path = str(meta_path)
        band_path  = Path(str_path.replace("MTL.txt",f"B{band_num}.TIF"))
        with rasterio.open(str(band_path)) as raster:
            Qcal = raster.read(1)

        hit = (Qcal == 0)
        Qcal=Qcal.astype(np.float32)
        Qcal[hit]=np.nan
        out_dict[int(band_num)]=calc_radiance_8(Qcal,band_num,meta_path)
    return out_dict

def toa_radiance_457(band_nums, meta_path, outdir = None):
    """
    Top of Atmosphere radiance (in Watts/(square meter x steradians x micrometers))
    conversion for Landsat 4, 5, or 7 level 1 data.
    See link below for details:
    see here http://landsat.usgs.gov/Landsat8_Using_Product.php

    Parameters
    ----------

    band_nums: list
           A list of desired band numbers such as [3, 4, 5]

    meta_path: str or Path object
             The full filepath to the MTL.txt metadata file for those bands


    Returns
    -------

    out_dict: dict
        dictionary with band_num as keys and TOA radiance (W/m2/sr/um) as values
    """
    
    
    meta_path = Path(meta_path).resolve()

    band_nums = core.enf_list(band_nums)
    band_nums = map(str, band_nums)
    TM_ETM_bands = ['1','2','3','4','5','7','8','6_VCID_1','6_VCID_2']

    #Calculating values for each band
    out_dict={}
    for band_num in band_nums:
        if band_num not in TM_ETM_bands:
            print("Can only perform radiance conversion on ETM sensor bands")
            print("Skipping band {0}".format(band_num))
            continue
        str_path = str(meta_path)
        band_path  = Path(str_path.replace("MTL.txt",f"B{band_num}.TIF"))
        with rasterio.open(str(band_path)) as raster:
            Qcal = raster.read(1)
        hit = (Qcal == 0)
        Qcal=Qcal.astype(np.float32)
        Qcal[hit]=np.nan
        out_dict[int(band_num)]=calc_radiance_457(Qcal,band_num,meta_path)
    return out_dict
