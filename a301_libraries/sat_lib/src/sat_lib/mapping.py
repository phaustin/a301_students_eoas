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
