import cartopy.crs as ccrs
from pyresample import geometry

def get_proj_params(metadata):
    """
    given a metadata dictionary from parseMeta, return proj4 parameters
    for use by cartopy or pyresample, assuming a laea projection
    and WGS84 datum
    
    Parameters
    ----------
    
    metadata:  dictionary
       returned by parseMeta
    
    Returns
    -------
    (proj_params, globe): dict, cartopy.crs.Globe
        projection params plus datum created by cartopy crs
    
    """
    

    globe = ccrs.Globe(datum="WGS84", ellipse="WGS84")
    projection = ccrs.LambertAzimuthalEqualArea(
        central_latitude=metadata["lat_0"],
        central_longitude=metadata["lon_0"],
        globe=globe
    )
    
    return projection


def make_areadef_dict(lat_0,lon_0,ll_x,ll_y,pixel_size_x,pixel_size_y,
                 x_size, y_size,
                 proj="laea",area_id="laea_a301",proj_id="laea_a301",
                 name="human readable area def"):
    """
    construct a pyresample area_def from central lon/lat and raster
    characteristics

    Parameters
    ----------

    lat_0: float
      crs central latitude
    lon_0: float
      crs central longitude
    ll_x: float
      projection x coord of lower left pixel edge
    ll_y: float
      projection y coord of lower left pixel bottom
    pixel_x_size: float
      pixel horizontal size in projection coords
    pixel_y_size: float
      pixel vertical size in projection coords
    x_size: float
      number of columns in raster
    y_size: float
      number of rows in raster

    Returns
    -------

    area_dict: dict
       dictionary used as input to mapping.area_def_from_dict
    """
    
    proj_dict = {"proj": proj,
        "lat_0": lat_0,
        "lon_0": lon_0,
        "x_0": 0,
        "y_0": 0,
        "datum": "WGS84",
        "units": "m",
        "no_defs": None,
        "type": "crs"}
    #
    # find the ur corner by adding all rows
    # and columns to ll corner
    #
    ur_x = ll_x + x_size*pixel_size_x
    ur_y = ll_y + y_size*pixel_size_y
    area_extent = [ll_x,ll_y, ur_x, ur_y]
    area_dict = dict(area_id = area_id,
                     proj_id=proj_id,
                     name = name,
                     proj_dict = proj_dict,
                     x_size = x_size,
                     y_size = y_size,
                     area_extent = area_extent)
    return area_dict



def area_def_to_dict(area_def):
    """
    given an area_def, save it as a dictionary`

    introduced in week5/wv_resample.md

    Parameters
    ----------
    
    area_def: pyresample area_def object
         
    Returns
    -------
    
    area_dict: dict 
       area_def dictionary
         
    """
    keys = [
        "area_id",
        "proj_id",
        "name",
        "proj_dict",
        "x_size",
        "y_size",
        "area_extent",
        "pixel_size_x",
        "pixel_size_y"
    ]
    area_dict = {key: getattr(area_def, key) for key in keys}
    area_dict["proj_id"] = area_dict["area_id"]
    return area_dict

def area_def_from_dict(area_def_dict):
    """
    given an dictionary produced by area_def_to_dict
    return a pyresample area_def

    introduced in week5/longwave_resample.md
    
    Parameters
    ----------
    
    area_def_dict: dict
        dictionary containing area_def parameters
        
    Returns
    -------
    
    pyresample.area_def 

    """
    keys=['area_id','proj_id','name','proj_dict','x_size','y_size','area_extent']    
    arglist=[area_def_dict[key] for key in keys]
    area_def=geometry.AreaDefinition(*arglist)
    return area_def
