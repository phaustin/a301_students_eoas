---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
""" modified 2012/11/24 to add cast for LayerTop"""
import matplotlib
import datetime
import dateutil.tz as tz
import numpy as np
import matplotlib.pyplot as plt
import pyhdf.SD
from pyhdf import VS
import pyhdf
import pyhdf.HDF as HDF
from pathlib import Path
from sat_lib.modischan_read import sd_open_file
import a301_lib
from xarray import DataArray,Dataset
import pyproj
```

```{code-cell} ipython3
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
```

```{code-cell} ipython3
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
    
    
```

```{code-cell} ipython3
datetime.datetime.strptime('2008291', '%Y%j').date()
```

```{code-cell} ipython3
#read_cloudsat_var('Radar_Reflectivity',radar_file)
lidar_ds = read_cloudsat_var('LayerTop',lidar_file)
lidar_ds
```

```{code-cell} ipython3
#radar reflectivity data see
#http://www.cloudsat.cira.colostate.edu/dataSpecs.php?prodid=9
radar_dir = a301_lib.data_share / "pha/cloudsat"
radar_file = list(radar_dir.glob("2008291*2B-GEOPROF_GR*hdf"))[0].resolve()
print(f"{radar_file=}")
lidar_file = list(radar_dir.glob("2008291*2B-GEOPROF-LIDAR*GR*hdf"))[0].resolve()
print(f"{lidar_file=}")
```

```{code-cell} ipython3
refl_ds = read_cloudsat_var('Radar_Reflectivity',radar_file)
refl_array = refl_ds['Radar_Reflectivity']
dem_elevation = refl_ds['dem_elevation']
height = refl_ds.coords['height']
lidar_ds = read_cloudsat_var('LayerTop',lidar_file)
layer_top = lidar_ds['LayerTop']

fig1,axis1=plt.subplots(1,1)
start=21000
stop=22000
meters2km = 1.e-3
storm_distance = distance_km[start:stop]
storm_distance = storm_distance - storm_distance[0]
im=axis1.pcolor(storm_distance,height*meters2km,refl_array[start:stop,:].T)
axis1.set_xlabel('storm distance (km)')
axis1.set_ylabel('height (km)')
cb=fig1.colorbar(im)
cb.set_label('reflectivity (dbZ)')
fig1.savefig('reflectivity.png')

fig2,axis2=plt.subplots(1,1)
axis2.plot(distance_km,layer_top*meters2km,'b')
axis2.plot(distance_km,dem_elevation*meters2km,'r')
axis2.set_xlabel('track distance (km)')
axis2.set_ylabel('height (km)')
axis2.set_title('whole orbit: lidar cloud top (blue) and dem surface elevation (red)')
fig2.savefig('lidar_height.png')
plt.show()
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
