import pyhdf.SD
from pyhdf import VS
import pyhdf
import pyhdf.HDF as HDF
from .modischan_read import sd_open_file
import numpy as np
from xarray import DataArray,Dataset
import pyproj
from pathlib import Path
import datetime
import dateutil.tz as tz

def get_geo(hdfname):
    """given the name of any hdf file from the Cloudsat data archive
       return lat,lon,time_vals,prof_times,dem_elevation
       for the cloudsat orbital swath
       usage:  lat,lon,height,time_vals,prof_times,dem_elevation=get_geo(hdffile)
       parameters:
         input:
           hdfname:  string with name of hdf file from http://www.cloudsat.cira.colostate.edu/dataSpecs.php
         output:  
           lat  -- profile latitude in degrees east  (1-D vector)
           lon  -- profile longitude in degrees north (1-D vector)
           time_vals -- profile times in UTC  (1D vector)
           prof_times -- profile times in seconds since beginning of orbit (1D vector)
           dem_elevation -- surface elevation in meters
    """
    hdfname = Path(hdfname).resolve()
    hdfname=str(hdfname)
    print(f"get_geo {hdfname=}")
    hdffile=HDF.HDF(hdfname,HDF.HC.READ)
    vs=hdffile.vstart()
    out=vs.vdatainfo()
    #uncomment this line to see the variable names
    # print("VS variable names: ",out)
    old_variable_names=['Longitude','Latitude','Profile_time','DEM_elevation']
    new_variable_names=['longitude','latitude','profile_time','dem_elevation']
    var_dict={}
    for old_var_name,new_var_name in zip(old_variable_names,new_variable_names):
        the_var=vs.attach(old_var_name)
        nrecs=the_var._nrecs
        the_data=the_var.read(nRec=nrecs)
        the_data=np.array(the_data).squeeze()
        var_dict[new_var_name]=the_data
        the_var.detach()
    tai_start=vs.attach('TAI_start')
    nrecs=tai_start._nrecs
    tai_start_value=tai_start.read(nRec=nrecs)
    tai_start.detach()
    hdffile.close()   
    #tai_start is the number of seconds since Jan 1, 1993 that the orbit
    #began
    taiDelta=datetime.timedelta(seconds=tai_start_value[0][0])
    taiDayOne=datetime.datetime(1993,1,1,tzinfo=tz.tzutc())
    #this is the start time of the orbit in seconds since Jan 1, 1993
    orbitStart=taiDayOne + taiDelta
    time_vals=[]
    #now loop throught he radar profile times and convert them to 
    #python datetime objects in utc
    for the_time in var_dict['profile_time']:
        time_vals.append(orbitStart + datetime.timedelta(seconds=float(the_time)))
    var_dict['time_vals']=time_vals
    neg_values=var_dict['dem_elevation'] < 0
    var_dict['dem_elevation'][neg_values]=0
    #
    # great circle distance
    #
    great_circle=pyproj.Geod(ellps='WGS84')
    distance=[0]
    lons, lats = var_dict['longitude'], var_dict['latitude']
    start=(lons[0],lats[0])
    meters2km = 1.e-3
    for index in np.arange(1,len(var_dict['longitude'])):
        azi12,azi21,step= \
            great_circle.inv(lons[index-1],lats[index-1],lons[index],lats[index])   
        distance.append(distance[index-1] + step)
    distance=np.array(distance)*meters2km
    var_dict['distance_km']=distance
    #
    # write the dataset
    # 
    x_dict={}
    variable_names=['latitude','longitude','profile_time','dem_elevation','distance_km']
    for var_name,var_data in var_dict.items():
        x_dict[var_name] = (['time'],var_data)
    #
    # get the height array if it exists
    #  
    hdf_SD = sd_open_file(hdfname)
    var_sd=hdf_SD.select('Height')
    var_vals=var_sd.get()
    height_array =var_vals.astype(np.float32)
    hdf_SD.end()
    x_dict['full_heights'] = (['time','height'],height_array)
    coords={'time':(['time'],var_dict['time_vals']),
            'height':(['height'],height_array[0,:])}
    the_data = Dataset(data_vars=x_dict, coords=coords)
    return the_data

def read_cloudsat_var(varname, filename):
    the_data = get_geo(filename)
    hdf_SD = sd_open_file(filename)
    print(f"in read_cloudsat_var, reading {varname=}")
    var_sd=hdf_SD.select(varname)
    var_vals=var_sd.get()
    try:
        fill_value=var_sd.attributes()["_FillValue"]
        missing_vals = var_vals == fill_value
        var_vals =var_vals.astype(np.float32)
        var_vals[missing_vals]=np.nan
    except:
        var_vals =var_vals.astype(np.float32)
    hdf_SD.end()
    scale_factor = 1
    new_name = varname
    if varname == 'Radar_Reflectivity':
        # https://www.cloudsat.cira.colostate.edu/data-products/2b-geoprof
        scale_factor = 0.001
        var_vals = var_vals*scale_factor
        var_array = DataArray(var_vals,dims=['time','height'])
    elif varname == 'LayerTop':
        var_vals[var_vals < 0]=np.nan
        #
        # 5 nray values, take the first 1
        #
        var_value = var_vals[:,0] 
        var_array = DataArray(var_value,dims=['time'])
    else:
        var_array = DataArray(var_vals,dims=['time'])
    the_data[varname] = var_array
    return the_data
    
    
