import cartopy.crs as ccrs

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

