---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: -all
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
from xarray import DataArray
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
    variable_names=['Longitude','Latitude','Profile_time','DEM_elevation']
    var_dict={}
    for var_name in variable_names:
        the_var=vs.attach(var_name)
        nrecs=the_var._nrecs
        the_data=the_var.read(nRec=nrecs)
        the_data=np.array(the_data).squeeze()
        var_dict[var_name]=the_data
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
    for the_time in var_dict['Profile_time']:
        time_vals.append(orbitStart + datetime.timedelta(seconds=float(the_time)))
    var_dict['time_vals']=time_vals
    neg_values=var_dict['DEM_elevation'] < 0
    var_dict['DEM_elevation'][neg_values]=0
    variable_names=['Latitude','Longitude','time_vals','Profile_time','DEM_elevation']
    out_list=[var_dict[varname] for varname in variable_names]
    #test_array = DataArray(coords={'time':time_vals},dims=['time'])
    return tuple(out_list)
```

```{code-cell} ipython3
datetime.datetime.strptime('2008291', '%Y%j').date()
```

```{code-cell} ipython3
if __name__=="__main__":
    #radar reflectivity data see
    #http://www.cloudsat.cira.colostate.edu/dataSpecs.php?prodid=9
    radar_dir = a301_lib.data_share / "pha/cloudsat"
    radar_file = list(radar_dir.glob("2008291*2B-GEOPROF_GR*hdf"))[0].resolve()
    print(f"{radar_file=}")
    lidar_file = list(radar_dir.glob("2008291*2B-GEOPROF-LIDAR*GR*hdf"))[0].resolve()
    print(f"{lidar_file=}")
    lat,lon,time_vals,prof_seconds,dem_elevation=get_geo(radar_file)
    #
    # height values stored as an SD dataset
    #
    hdf_SD = sd_open_file(radar_file)
    height_sd=hdf_SD.select('Height')
    height_vals=height_sd.get()
    height=height_vals.astype(np.float32)
    refl=hdf_SD.select('Radar_Reflectivity')
    refl_vals=refl.get()
    fill_value=refl.attributes()["_FillValue"]
    missing_vals = refl_vals == fill_value
    #
    # https://www.cloudsat.cira.colostate.edu/data-products/2b-geoprof
    #
    scale_factor = 0.001
    refl_vals=refl_vals*scale_factor
    refl_vals[missing_vals] = np.nan
    hdf_SD.end()
    hdf_SD = sd_open_file(lidar_file)
    layerTop=hdf_SD.select('LayerTop')
    layerTop=layerTop.get()
    layerTop=layerTop.astype(np.float32)
    layerTop[layerTop < 0]=np.nan
    hdf_SD.end()
    
    fig1,axis1=plt.subplots(1,1)
    start=21000
    stop=22000
    im=axis1.pcolor(prof_seconds[start:stop],height[0,:]/1.e3,refl_vals[start:stop,:].T)
    axis1.set_xlabel('time after orbit start (seconds)')
    axis1.set_ylabel('height (km)')
    cb=fig1.colorbar(im)
    cb.set_label('reflectivity (dbZ)')
    fig1.savefig('reflectivity.png')
    
    fig2,axis2=plt.subplots(1,1)
    axis2.plot(prof_seconds,layerTop[:,0]/1.e3,'b')
    axis2.plot(prof_seconds,dem_elevation/1.e3,'r')
    axis2.set_xlabel('time after orbit start (seconds)')
    axis2.set_ylabel('height (km)')
    axis2.set_title('lidar cloud top (blue) and dem surface elevation (red)')
    fig2.savefig('lidar_height.png')
    plt.show()
```

```{code-cell} ipython3
    
```

```{code-cell} ipython3

```
