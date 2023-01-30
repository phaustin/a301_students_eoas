"""
  satellite utilities
  ___________________

  parses a Modis Level1b CoreMetata.0 string and extracts
  a dictionary.

  Usage:

      from sat_lib.modismeta_read import parseMeta
      parseMeta(file_path)
"""

import click
import pdb
import pprint
import sys
import types
from pathlib import Path

import numpy as np
from pyhdf.SD import SD
from pyhdf.SD import SDC

def get_core(filename):
    """
    given the path to a Modis hdf4 file with a "CoreMetadata.0" attribute
    return that value as a string
    """
    filename = str(filename)
    the_file = SD(filename, SDC.READ)
    metaDat = the_file.attributes()["CoreMetadata.0"]
    core_meta = str(metaDat).rstrip(" \t\r\n\0")
    the_file.end()
    return core_meta


# from https://github.com/pytroll/satpy/blob/master/satpy/readers/modis_l1b.py
def read_mda(attribute):
    lines = attribute.split("\n")
    mda = {}
    current_dict = mda
    path = []
    for line in lines:
        if not line:
            continue
        if line.strip() == "END":
            break
        try:
            key, val = line.split("=")
        except ValueError:
            continue
        key = key.strip()
        val = val.strip()
        try:
            val = eval(val)
        except (NameError, SyntaxError, ValueError) as e:
            pass
        if key in ["GROUP", "OBJECT"]:
            new_dict = {}
            path.append(val)
            current_dict[val] = new_dict
            current_dict = new_dict
        elif key in ["END_GROUP", "END_OBJECT"]:
            if val != path[-1]:
                raise SyntaxError
            path = path[:-1]
            current_dict = mda
            for item in path:
                current_dict = current_dict[item]
        elif key in ["CLASS", "NUM_VAL"]:
            pass
        else:
            current_dict[key] = val
    return mda


class metaParse:
    def __init__(self, metaDat):
        import re
        self.metaDat = str(metaDat).rstrip(" \t\r\n\0")
        self.meta_dict = read_mda(self.metaDat)
        the_dict = self.meta_dict["INVENTORYMETADATA"]
        product = the_dict["COLLECTIONDESCRIPTIONCLASS"]["SHORTNAME"]["VALUE"]
        L2 = product.find("L2") > -1
        if L2:
            rectangle = the_dict["SPATIALDOMAINCONTAINER"][
                "HORIZONTALSPATIALDOMAINCONTAINER"
            ]["BOUNDINGRECTANGLE"]
            left_lon = rectangle["WESTBOUNDINGCOORDINATE"]["VALUE"]
            right_lon = rectangle["EASTBOUNDINGCOORDINATE"]["VALUE"]
            top_lat = rectangle["NORTHBOUNDINGCOORDINATE"]["VALUE"]
            bot_lat = rectangle["SOUTHBOUNDINGCOORDINATE"]["VALUE"]
            theLongs = [right_lon, left_lon, left_lon, right_lon]
            theLats = [bot_lat, bot_lat, top_lat, top_lat]  # ccw from lower right
        else:
            # pdb.set_trace()
            theLongs = self.meta_dict["INVENTORYMETADATA"]["SPATIALDOMAINCONTAINER"][
                "HORIZONTALSPATIALDOMAINCONTAINER"
            ]["GPOLYGON"]["GPOLYGONCONTAINER"]["GRINGPOINT"]["GRINGPOINTLONGITUDE"][
                "VALUE"
            ]
            theLats = self.meta_dict["INVENTORYMETADATA"]["SPATIALDOMAINCONTAINER"][
                "HORIZONTALSPATIALDOMAINCONTAINER"
            ]["GPOLYGON"]["GPOLYGONCONTAINER"]["GRINGPOINT"]["GRINGPOINTLATITUDE"][
                "VALUE"
            ]
        lon_list, lat_list = np.array(theLongs), np.array(theLats)
        min_lat, max_lat = np.min(lat_list), np.max(lat_list)
        min_lon, max_lon = np.min(lon_list), np.max(lon_list)
        lon_0 = (max_lon + min_lon) / 2.0
        lat_0 = (max_lat + min_lat) / 2.0
        lon_list, lat_list = list(lon_list), list(lat_list)
        corner_dict = dict(
            lon_list=lon_list,
            lat_list=lat_list,
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            lon_0=lon_0,
            lat_0=lat_0,
        )
        self.value1 = corner_dict
        self.value2 = self.meta_dict["INVENTORYMETADATA"][
            "ORBITCALCULATEDSPATIALDOMAIN"
        ]["ORBITCALCULATEDSPATIALDOMAINCONTAINER"]
        self.value3 = self.meta_dict["INVENTORYMETADATA"]["ECSDATAGRANULE"]
        self.value4 = self.meta_dict["INVENTORYMETADATA"]["RANGEDATETIME"]
        self.value5 = self.meta_dict["INVENTORYMETADATA"]["COLLECTIONDESCRIPTIONCLASS"]
        self.value6 = self.meta_dict["INVENTORYMETADATA"][
            "ASSOCIATEDPLATFORMINSTRUMENTSENSOR"
        ]["ASSOCIATEDPLATFORMINSTRUMENTSENSORCONTAINER"]


def parseMeta(meta_source):
    """
    Read useful information from a CoreMetata.0 attribute

    Parameters
    ----------

    meta_source: str or Path object to file or string with metadata

    Returns
    -------
    
    outDict: dict
        key, value:

    lat_list: np.array
        4 corner latitudes
    lon_list: np.array
        4 corner longitudes
    max_lat: float
        largest corner latitude
    min_lat: float
        smallest corner latitude
    max_lon: float
        largest corner longitude
    min_lon: float
        smallest corner longitude
    lon_0: float
        center longitude
    lat_0: float
        center latitude
    daynight: str
        'Day' or 'Night'
    starttime: str
        swath start time in UCT
    stoptime: str
        swath stop time in UCT
    startdate: str
        swath start datein UCT
    orbit: str
        orbit number
    equatordate: str
        equator crossing date in UCT
    equatortime: str
        equator crossing time in UCT
    nasaProductionDate: str
        date file was produced, in UCT
    """
    #
    # meta_source can be either the path to an
    # hdf4 file or the "CoreMetadata.0" string itself
    #
    try:
        filename = Path(meta_source).resolve()
        if filename.is_file():
            the_file = SD(str(filename), SDC.READ)
            metaDat = the_file.attributes()["CoreMetadata.0"]
            the_file.end()
        else:
            raise ValueError(f"could not open {filename}")
    except OSError:
        #
        # filename too long, assume it's the metadata string
        #
        metaDat = meta_source
    parseIt = metaParse(metaDat)
    outDict = {}
    outDict["orbit"] = parseIt.value2["ORBITNUMBER"]["VALUE"]
    outDict["daynight"] = parseIt.value3["DAYNIGHTFLAG"]["VALUE"]
    outDict["filename"] = parseIt.value3["LOCALGRANULEID"]["VALUE"]
    outDict["stopdate"] = parseIt.value4["RANGEENDINGDATE"]["VALUE"]
    outDict["startdate"] = parseIt.value4["RANGEBEGINNINGDATE"]["VALUE"]
    outDict["starttime"] = parseIt.value4["RANGEBEGINNINGTIME"]["VALUE"]
    outDict["stoptime"] = parseIt.value4["RANGEENDINGTIME"]["VALUE"]
    outDict["equatortime"] = parseIt.value2["EQUATORCROSSINGTIME"]["VALUE"]
    outDict["equatordate"] = parseIt.value2["EQUATORCROSSINGDATE"]["VALUE"]
    outDict["nasaProductionDate"] = parseIt.value3["PRODUCTIONDATETIME"]["VALUE"]
    outDict["type"] = parseIt.value5
    outDict["sensor"] = parseIt.value6
    outDict.update(parseIt.value1)
    return outDict


@click.command()
@click.argument('hdf_file',type=str,nargs=1)
def main(hdf_file):
    """
    print the metadata dict
    """
    hdf_path = Path(hdf_file).resolve()
    out = parseMeta(hdf_path)
    print(f"core metadata for {hdf_path}")
    pprint.pprint(out)

