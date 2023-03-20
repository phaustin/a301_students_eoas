import copy
import numpy as np
from pystac_client import Client
from shapely.geometry import Point
from rasterio.windows import Window
from pyproj import CRS
import rioxarray
from xarray import Dataset

def get_clear_mask(fmask_ds):
    """
    return a DataArray copy of fmask_ds but with the pixel values set to
    1 where there is both no cloud and pixel is land, and np.nan where there is cloud
    or the pixel is water
    
    The bit patterns from the HSL QA mask are:
     
    Bits are listed from the MSB (bit 7) to the LSB (bit 0): 
    7-6    aerosol:
           00 - climatology
           01 - low
           10 - average
           11 - high
    5      water
    4      snow/ice
    3      cloud shadow
    2      adjacent to cloud
    1      cloud
    0      cirrus cloud
    
    so a bit mask of 0b00100011 when anded with a QA value
    will return non-zero when there is water, a cloud, or a cirrus cloud

    Parameters
    ----------

    fmask_ds: xarray DataArray
       landsat or sentinel hls scene create with rioxarray.open_rasterio

    Returns
    -------

    clearmask_ds: xarray DataArray
      new array with the clear sky mask for each pixel set to 1 if clear, np.nan if water or cloud
    """
    #
    # convert float32 to unsigned 8 bit integer
    #
    bit_mask = fmask_ds.data.astype(np.uint8)
    ref_mask = np.zeros_like(bit_mask)
    #
    # don't destroy original fmask DataArray
    #
    clearmask_ds = copy.deepcopy(fmask_ds)
    #
    # work with unsigned 8 bit values instead of
    # base 10 floats
    #
    bit_mask = fmask_ds.data.astype(np.uint8)
    #
    # create a reference mask that will select
    # bits 5, 1 and 0, which we want tocheck
    #
    ref_mask = np.zeros_like(bit_mask)
    ref_mask[...] = 0b00100011  #find water (bit 5), cloud (bit 1) , cirrus (bit 0)
    #
    # if all three of those bits are 0, then bitwise_and will return 0
    # otherwise it will return either a value greater than 0
    #
    cloudy_values = np.bitwise_and(bit_mask,ref_mask)
    cloudy_values[cloudy_values>0]=1  #cloud or water
    cloudy_values[cloudy_values==0]=0 #rest of scene
    #
    # now invert this, writing np.nan where there is 
    # cloud or water.  Go back to float32 so we can use np.nan
    #
    clear_mask = cloudy_values.astype(np.float32)
    clear_mask[cloudy_values == 1]=np.nan
    clear_mask[cloudy_values == 0]=1
    clearmask_ds.data = clear_mask
    return clearmask_ds


def get_landsat_scene(date, lon, lat, window):
    """
    retrieve windowed band4, band5 and Fmask for a given day and save
    the clipped geotiffs into three DataArrays, returned
    in a dictionary
    
    Parameters
    ----------
    
    date: str
       date in the form yyy-mm-yy
    lon: float
       longitude of point in the scene (degrees E)
    lat: 
        latitude of point in the scene (degrees N)
    window: rasterio.Window
        window for clipping the scene to a subscene
  
    Returns
    -------
    out_dict: dict
       dictionary with three rioxarray DataArrays: band4, band5, Fmask
    """
    #
    # set up the search -- we are looking for only 1 scene per date
    #
    the_point = Point(lon, lat)
    cmr_api_url = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD"
    client = Client.open(cmr_api_url)
    
    search = client.search(
        collections=["HLSL30.v2.0"],
        intersects=the_point,
        datetime= date
    )
    items = search.get_all_items()
    print(f"found {len(items)} item")
    #
    # get the metadata and add date, cloud_cover and band_name to the new DataArrays
    #
    props = items[0].properties
    out_dict = {}
    band_names = ['B04','B05','Fmask']
    array_names = ['b4_ds','b5_ds','fmask_ds']
    for band,array_name in zip(band_names, array_names):
        print(f"inside get_landsat_scene: reading {band} into {array_name}")
        href = items[0].assets[band].href
        lazy_ds = rioxarray.open_rasterio(href,mask_and_scale=True)
        #
        # now read the window
        #
        clipped_ds = lazy_ds.rio.isel_window(window)
        #
        # add some custom attributes
        #
        clipped_ds.attrs['date'] = props['datetime'] #date and time
        clipped_ds.attrs['cloud_cover'] = props['eo:cloud_cover']
        clipped_ds.attrs['band_name'] = band
        utm_zone = clipped_ds.attrs['HORIZONTAL_CS_NAME'][-3:].strip()
        if lat < 0:
            is_southern=True
        else:
            is_southern=False
        clipped_ds.attrs['cartopy_epsg_code'] = find_epsg_code(utm_zone,south=is_southern)
        clipped_ds.attrs['day']=props['datetime'][:10]  #yyyy-mm-dd
        out_dict[array_name] = clipped_ds
    #
    # convert the mask to 1=no cloud over land, np.nan=otherwise
    #
    out_dict['fmask_ds'] = get_clear_mask(out_dict['fmask_ds'])
    return out_dict

def get_landsat_dataset(date, lon, lat, window, bands=None):
    """
    retrieve windowed bands specified in the bands variable.
    Save the clipped geotiffs as xarray.DattArrays, returned
    in an xarray Dataset
    
    Parameters
    ----------
    
    date: str
       date in the form yyy-mm-yy
    lon: float
       longitude of point in the scene (degrees E)
    lat: 
        latitude of point in the scene (degrees N)
    window: rasterio.Window
        window for clipping the scene to a subscene
    bands: list
        list of bands in the form ['B01','B02',...]
        the default is ['B04','B05','B06']
  
    Returns
    -------
    the_dataset: xarray.Dataset
       dataset with rioxarrays of requested bands plus Fmask
    """
    if bands is None:
        bands = ['B04','B05','B06']
    #
    # set up the search -- we are looking for only 1 scene per date
    #
    the_point = Point(lon, lat)
    cmr_api_url = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD"
    client = Client.open(cmr_api_url)
    
    search = client.search(
        collections=["HLSL30.v2.0"],
        intersects=the_point,
        datetime= date
    )
    items = search.get_all_items()
    print(f"found {len(items)} item")
    #
    # get the metadata and add date, cloud_cover and band_name to the new DataArrays
    #
    props = items[0].properties
    out_dict = {}
    bands.extend(['Fmask'])
    for the_band in bands:
        print(f"inside get_landsat_scene: reading {the_band}")
        href = items[0].assets[the_band].href
        lazy_ds = rioxarray.open_rasterio(href,mask_and_scale=True)
        #
        # now read the window
        #
        clipped_ds = lazy_ds.rio.isel_window(window)
        #
        # add some custom attributes
        #
        clipped_ds.attrs['date'] = props['datetime'] #date and time
        clipped_ds.attrs['cloud_cover'] = props['eo:cloud_cover']
        clipped_ds.attrs['band_name'] = the_band
        clipped_ds.attrs['target_lat']= lat
        clipped_ds.attrs['target_lon']= lon
        utm_zone = clipped_ds.attrs['HORIZONTAL_CS_NAME'][-3:].strip()
        if lat < 0:
            is_southern=True
        else:
            is_southern=False
        clipped_ds.attrs['cartopy_epsg_code'] = find_epsg_code(utm_zone,south=is_southern)
        clipped_ds.attrs['day']=props['datetime'][:10]  #yyyy-mm-dd
        out_dict[the_band] = clipped_ds
    #
    # convert the mask to 1=no cloud over land, np.nan=otherwise
    #
    out_dict['Fmask'] = get_clear_mask(out_dict['Fmask'])
    coords = out_dict['Fmask'].coords
    attrs = out_dict['Fmask'].attrs
    dataset = Dataset(data_vars = out_dict, coords = coords, attrs = attrs )
    return dataset


def find_epsg_code(utm_zone, south=False):
    """
    https://gis.stackexchange.com/questions/365584/convert-utm-zone-into-epsg-code
    
    cartopy wants crs names as epsg codes, i.e. UTM zone 10N is EPSG:32610, 10S is EPSG:32710
    """
    crs = CRS.from_dict({'proj': 'utm', 'zone': utm_zone, 'south': south})
    epsg, code = crs.to_authority()
    cartopy_epsg_code = code
    return cartopy_epsg_code

