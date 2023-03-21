from .modischan_read import sd_open_file
import numpy as np
from xarray import DataArray,Dataset
import pyproj
from pathlib import Path
import datetime
import dateutil.tz as tz
from pyhdf.HDF import *
from pyhdf.V   import *
from pyhdf.VS  import *
from pyhdf.SD  import *
import pandas as pd

def read_attrs(filename):
    """
    Extract the data for non scientific data in V mode of hdf file
    """
    filename = Path(filename)
    filename = str(filename)
    hdf = HDF(filename, HC.READ)

    # Initialize the SD, V and VS interfaces on the file.
    sd = SD(filename)
    vs = hdf.vstart()
    v  = hdf.vgstart()
    ref = -1
    ref = v.getid(ref)
    vg = v.attach(ref)
    file_type = vg._name
    attr_dict = read_swath_attributes(v,vs)
    attr_dict['file_type']=file_type
    #print(f"{attr_dict=}")
    # Encontrar el puto id de las Geolocation Fields
    # Terminate V, VS and SD interfaces.
    v.end()
    vs.end()
    sd.end()
    # Close HDF file.
    hdf.close()
    return attr_dict


def read_swath_attributes(v,vs):
    ref = v.find('Swath Attributes')
    vg = v.attach(ref)
    members = vg.tagrefs()
    attr_dict = {}
    for tag, ref in members:
        if tag == HC.DFTAG_VH:
            vd = vs.attach(ref)
            nrecs, intmode, fields, size, name = vd.inquire()
            value = vd.read()
            attr_dict[name] = value
            vd.detach()
    vg.detach()
    return attr_dict

def get_geo(hdfname):
    """
    given the name of any hdf file from the Cloudsat data archive
    return lat,lon,time_vals,prof_times,dem_elevation
    for the cloudsat orbital swath

    Parameters
    ----------
    
    hdfname:  str or Path object
       full path to the hdf4 file  http://www.cloudsat.cira.colostate.edu/dataSpecs.php

    Returns
    -------

    the_data: xarray Datset with the following DataArrays

       lat  -- profile latitude in degrees east  (1-D vector)
       lon  -- profile longitude in degrees north (1-D vector)
       time_vals -- profile times in UTC  (1D vector)
       prof_times -- profile times in seconds since beginning of orbit (1D vector)
       dem_elevation -- surface elevation in meters
    """
    
    hdfname = Path(hdfname).resolve()
    hdfname=str(hdfname)
    the_attrs = read_attrs(hdfname)
    granule_id = int(the_attrs['granule_number'][0][0])
    file_type = the_attrs['file_type']
    hdffile=HDF(hdfname,HC.READ)
    vs = hdffile.vstart()
    out=vs.vdatainfo()
    #uncomment this line to see the variable names
    # print("VS variable names: ",out)
    old_variable_names=['Longitude','Latitude','Profile_time']
    new_variable_names=['longitude','latitude','profile_time']
    var_dict={}
    #
    # save the variables and conver names to lower case
    #
    for old_var_name,new_var_name in zip(old_variable_names,new_variable_names):
        the_var=vs.attach(old_var_name)
        nrecs=the_var._nrecs
        the_data=the_var.read(nRec=nrecs)
        the_data=np.array(the_data).squeeze()
        var_dict[new_var_name]=the_data
        the_var.detach()
    if file_type == 'ECMWF-AUX':
        the_var = vs.attach('EC_height')
        nrecs=the_var._nrecs
        the_data=the_var.read(nRec=nrecs)
        the_data=np.array(the_data).squeeze()
        var_dict['ec_height']=the_data
        the_var.detach()
    else: 
        the_var = vs.attach('DEM_elevation')
        nrecs=the_var._nrecs
        the_data=the_var.read(nRec=nrecs)
        the_data=np.array(the_data).squeeze()
        var_dict['dem_elevation']=the_data
        the_var.detach()
    tai_start=vs.attach('TAI_start')
    nrecs=tai_start._nrecs
    tai_start_value=tai_start.read(nRec=nrecs)
    tai_start.detach()
    hdffile.close()
    #
    #tai_start is the number of seconds since Jan 1, 1993 that the orbit
    # began
    #
    taiDelta=datetime.timedelta(seconds=tai_start_value[0][0])
    taiDayOne=datetime.datetime(1993,1,1,tzinfo=tz.tzutc())
    #this is the start time of the orbit in seconds since Jan 1, 1993
    orbitStart=taiDayOne + taiDelta
    time_vals=[]
    #now loop throught he radar profile times and convert them to 
    #python datetime objects in utc
    for the_time in var_dict['profile_time']:
        time_vals.append(orbitStart + datetime.timedelta(seconds=float(the_time)))
    time_vals = np.array(time_vals)
    day = time_vals[0].strftime("%Y-%m-%d")
    orbit_start_time = time_vals[0].isoformat()
    orbit_end_time = time_vals[-1].isoformat()
    time_vals = time_vals.astype("datetime64[ns]")
    var_dict['time_vals']=time_vals
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
    distance_km=np.array(distance)*meters2km
    var_dict['distance_km']=distance_km
    coord_names=['profile_time','distance_km','time_vals']
    variable_names=['latitude','longitude']
    variable_dict = {key:(['time'],var_dict[key]) for key in variable_names}
    coord_dict = {key:var_dict[key] for key in coord_names}
    #
    # get the height array if it exists
    #
    if file_type != 'ECMWF-AUX':
        hdf_SD = sd_open_file(hdfname)
        var_sd=hdf_SD.select('Height')
        var_attrs = var_sd.attributes()
        var_vals=var_sd.get()
        missing_vals = (var_vals == var_attrs['missing'])
        var_vals =var_vals.astype(np.float32)
        var_vals[missing_vals]=np.nan
        height_array =var_vals
        height = height_array[0,:]
        var_dict['full_heights'] = (['time','height'],height_array)
        #
        # y axis is first height column
        #
        coord_dict['height'] = height_array[0,:]
        coord_dict['full_heights'] = height_array[:,:]
        variable_dict['dem_elevation'] = (['time'], var_dict['dem_elevation'])
        hdf_SD.end()
    else:
        #
        # model only has vector height
        #
        coord_dict['height'] = var_dict['ec_height']
    coord_dict['height_km']= coord_dict['height']*meters2km
    # print(f"making new height_km, {coord_dict['height_km'][:5]=}")
    #
    # write the dataset
    # 
    attrs = dict(file_type=file_type,orbit_start_time = orbit_start_time,
                 orbit_end_time = orbit_end_time, granule_id=granule_id,
                 day = day)
    coords={'time':(['time'],coord_dict['time_vals']),
            'height':(['height'],coord_dict['height']),
            'height_km':(['height'],coord_dict['height_km']),
            'distance_km':(['time'],coord_dict['distance_km']),
            'profile_time':(['time'],coord_dict['profile_time'])
            }
    if attrs['file_type'] != "ECMWF-AUX":
        coords["full_heights"]=(['time','height'],coord_dict['full_heights'])

    # print(f"making distance_km: {coords['distance_km'][1][:5]=}")
    the_data = Dataset(data_vars=variable_dict, coords=coords,attrs=attrs)
    return the_data

def read_var(varname, hdfname):
    hdfname = Path(hdfname).resolve()
    hdfname=str(hdfname)
    sd = sd_open_file(hdfname)
    hdf = HDF(hdfname, HC.READ)
    vs = hdf.vstart()
    v  = hdf.vgstart()
    ref = v.find('Data Fields')
    vg = v.attach(ref)
    members = vg.tagrefs()
    var_dict = dict()
    #
    # build a dictionary with all variable names
    #
    for tag, ref in members:
        # Vdata tag
        if tag == HC.DFTAG_VH:
            vd = vs.attach(ref)
            nrecs, intmode, fields, size, name = vd.inquire()
            # nrecs, intmode, fields, size, name = vd.inquire()
            # nrecs.append(vd.inquire()[0]) # number of records of the Vdata
            # names.append(vd.inquire()[-1])# name of the Vdata
            vd.detach()
            row_dict = dict(ref=ref,nrecs=nrecs,intmod=intmode,fields=fields,size=size)
            var_dict[name] = row_dict
        elif tag == HC.DFTAG_NDG:
            sds = sd.select(sd.reftoindex(ref))
            name, rank, dims, the_type, nattrs = sds.info()
            row_dict = dict(ref=ref,rank=rank,dims=dims,the_type=the_type,nattrs=nattrs)
            var_dict[name] = row_dict
            sds.endaccess()
    if varname not in var_dict:
        raise KeyError(f"can't fine {varname} in {hdfname}")
    else:
        if 'rank' in var_dict[varname]:
            print(f"in read_cloudsat_var: reading {varname=}")
            var_sd=sd.select(varname)
            var_vals=var_sd.get()
            var_attrs = var_sd.attributes()
            print(f"sd variable type before scaling: {var_vals.dtype=}")
        else:
            nrecs = var_dict[varname]['nrecs']
            ref = var_dict[varname]['ref']
            var = vs.attach(ref)
            var_vals   = var.read(nrecs)
            var_vals=np.array(var_vals).squeeze()
            var_attrs = None
            print(f"vdata variable type before scaling: {var_vals.dtype=}")
            var.detach()
    v.end()
    vs.end()
    hdf.close()
    return var_vals, var_attrs

def read_cloudsat_var(varname, filename):
    """
    Given a variable name and a file name, return a cloudsat dataset

    Parameters
    ----------

    varname: str
       name of cloudsat variable

    filename: str or Path object
       path to the cloudsat haf file
    """
    the_data = get_geo(filename)
    swath_attrs = read_attrs(filename)
    var_vals, var_attrs = read_var(varname, filename)
    #
    # mask on the integer fill_value
    #
    fill_value = np.nan
    if (var_attrs is not None) and "_FillValue" in var_attrs:
        fill_value = var_attrs["_FillValue"]
    elif (var_attrs is not None) and "missing" in var_attrs:
        fill_value = var_attrs["missing"]
    print(f"using {fill_value=}")
    missing_vals = (var_vals == fill_value)
    var_vals =var_vals.astype(np.float32)
    var_vals[missing_vals]=np.nan
    if var_attrs is not None:
        try:
            scale_factor = var_attrs['factor']
        except KeyError:
            #print(f"{swath_attrs=}")
            if varname == "Radar_Reflectivity":
                scale_factor = swath_attrs['Radar_Reflectivity.factor']
            else:
                scale_factor = 1
    else:
        scale_factor = 1
    if var_vals.ndim == 2 and varname != "LayerTop":
        # https://www.cloudsat.cira.colostate.edu/data-products/2b-geoprof
        var_vals = var_vals/scale_factor
        var_array = DataArray(var_vals,dims=['time','height'],attrs=var_attrs)
    elif varname == 'LayerTop':
        var_vals[var_vals < 0]=np.nan
        #
        # 5 nray values, take the first 1
        #
        var_value = var_vals[:,0] 
        var_array = DataArray(var_value,dims=['time'],attrs=var_attrs)
    elif var_vals.ndim == 1:
        var_array = DataArray(var_vals,dims=['time'],attrs=var_attrs)
    else:
        raise ValueError(f"problem reading {varname} from {filename}")
    the_data[varname] = var_array
    return the_data
    
    
