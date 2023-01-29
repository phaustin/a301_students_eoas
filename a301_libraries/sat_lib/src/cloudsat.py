"""
 these functions read a standard Cloudsat data file and return
 geolocation and time data for the orbit

 

"""
import h5py
import datetime
import numpy as np



def convert_field(tuple_field):
    """
    convert a numpy array of tuples from cloudsat int the form
       [(-9999,) (-9999,) (-9999,) ..., (111,) (110,) (107,)]
    into a regular numpy array of the same
    shape and dtype, by taking item[0] of each tuple

    Parameters
    ----------

    tuple_field: vector or matrix of tuples
       cloudsat vector/matrix of tuples of length 1

    Returns
    -------

    numpy vector or matrix: float
      same length, but with the tuple unpacked

    """
    save_shape=tuple_field.shape
    flat_test=tuple_field.ravel()
    out_flat=np.empty(len(flat_test),dtype=flat_test[0][0].dtype)
    for index,item in enumerate(flat_test):
        out_flat[index]=item[0]
    out=out_flat.reshape(save_shape)
    return out


def get_geo(hdfname, monotonic_lons=True,root_name=None):
    """
    given the name of any hdf file from the Cloudsat data archive
    return lat,lon,time_vals,prof_times,dem_elevation
    for the cloudsat orbital swath
    
    usage:  lat,lon,date_times,prof_times,dem_elevation=get_geo(filename)
    
    Parameters
    ----------
    
    hdfname:  str
          string with name of hdf file from http://www.cloudsat.cira.colostate.edu/dataSpecs.php
    monotonic_id: bool
           wrap the longitude by addint 360 degrees if it flips form 180 to -180 
    root_name: str
           optional name for root field name (like 2B-FLXHR_LIDAR) otherwise first key

    Returns
    -------
    
    lat: vector float
       profile latitude in degrees north  (1-D vector)
    
    lon: vector float
      profile longitude in degrees north (1-D vector)
    
    time_vals: vector datetimes
       profile times in UTC  (1D vector)
    
    prof_times: vector int
       profile times in seconds since beginning of orbit (1D vector)
    
    dem_elevation: vector float
       surface elevation in meters
    """
    
    with h5py.File(hdfname,'r') as f:
        if root_name is None:
            root_name=list(f.keys())[0]
        variable_names=['Longitude','Latitude','Profile_time','DEM_elevation']
        var_dict={}
        for var_name in variable_names:
            var_dict[var_name]=convert_field(f[root_name]['Geolocation Fields'][var_name][...])
        tai_start=f[root_name]['Geolocation Fields']['TAI_start'][0][0]
    #
    # the longitude can flip between +180 and -180 at the international dateline
    # detect if this happens, and shift it to make it in the range -360 to +720 degrees
    #
    # ===================================================================== #
    if monotonic_lons:
        lon=var_dict['Longitude'][:];
        for id in range(0, len(lon)-1):
            if lon[id+1] > lon[id]:
                lon[id+1] = lon[id+1]-360
        lonmin=np.amin(lon)
        #
        # basemap requires lons in the range -360 - 720 degrees
        #
        if lonmin < -360.:
            lon[:]=lon[:] + 360.
        var_dict['Longitude']=lon
    #
    #
    #tai_start is the number of seconds since Jan 1, 1993 for orbit start
    #
    #
    taiDelta=datetime.timedelta(seconds=tai_start)
    taiDayOne=datetime.datetime(1993,1,1,tzinfo=datetime.timezone.utc)
    #this is the start time of the orbit in seconds since Jan 1, 1993
    orbitStart=taiDayOne + taiDelta
    time_vals=[]
    #now loop throught he radar profile times and convert them to 
    #python datetime objects in utc
    for the_time in var_dict['Profile_time']:
        date_time=orbitStart + datetime.timedelta(seconds=float(the_time))
        time_vals.append(date_time)
    var_dict['date_day']=np.array(time_vals)
    neg_values=var_dict['DEM_elevation'] < 0
    var_dict['DEM_elevation'][neg_values]=0
    #
    # return a list with the five variables
    #
    variable_names=['Latitude','Longitude','date_day','Profile_time','DEM_elevation']
    out_list=[var_dict[varname] for varname in variable_names]  
    return out_list

if __name__ == "__main__":
    
    from a301utils.a301_readfile import download
    filename='2006303212128_02702_CS_2B-GEOPROF_GRANULE_P_R04_E02.h5'
    download(filename)
    lat,lon,date_times,prof_times,dem_elevation=get_geo(filename)
    minlat,maxlat = np.min(lat),np.max(lat)
    minlon,maxlon = np.min(lon),np.max(lon)
    maxheight = np.max(dem_elevation)
    print('\nlatitudes -- deg north: \nmin: {},  max: {}\n'.format(minlat,maxlat))
    print('\nlongitudes -- deg east: \nmin: {},max: {}\n'.format(minlon,maxlon))
    print('\nmax elev (m): {}\n'.format(maxheight))
    print('\norbit start/stop dates (UCT): \nstart: {}\nstop: {}\n'.format(date_times[0],date_times[-1]))
          
