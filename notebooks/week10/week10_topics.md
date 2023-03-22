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

# Week 10
## At the start of class

* `conda activate a301`

* fetch and reset

          git status
          git fetch
          git reset --hard origin/main
          

* Check to see whether your library version is up to date by comparing [the latest tag](https://github.com/phaustin/a301_students_eoas/tags) with the output of `hdf4_inspect --version`

  * If needed, update the libraries with `pip install -r requirements.txt`


## Learning goals

- Landsat: download multiple windowed images, sort them by date and save them to disk
  using pandas and rioxarray

- Cloudsat: using xarray to clip a time series to specific times, and plot
  time-height cross sections with different coordinates


## Week 10 topics for Monday

- Cloudsat: plotting temperature pertubations and wind speed with {ref}`week10:temperature_perturb`

- Landsat: saving multiple windowed landsat scenes with {ref}`week10:write_geotiff`

- Current events

  - [radar tracking of Bird migration](https://cliffmass.blogspot.com/2023/03/massive-migration-occurring-aloft-and.html)
  
  - Using [chatgpt](https://chat.openai.com/chat) to understand python code

### Reserved hurricanes

- Nida - 2009/11/28
- Maria - 2017/09
- Flossie - 2008/7/14
- Mekkala
- Billy - 2008
- Mitchell
- Mirinae
- Iggy
- Amara
- Faxai
- Becky
- Gelane
- Bondo
- Maria
- Chebi
- Yagi
- Choi-wan
- Dolores
- Gonu


## For Wednesday

- Make sure your hurricane looks reasonable when run through the {ref}`week10:temperature_perturb` notebook

- Download all of your windowed landsat scenes to disk, and start making your ndvi timeseries plot for Assignment 5

## Week 10 topics for Monday

- Cloudsat: {ref}

## Assignment 5: Due midnight on Wednesday, March 29

### Radar problem

1) Integrate $Z=\int D^6 n(D) dD$ on paper, assuming a Marshall Palmer size distribution and show that it integrates to:

$$
Z \approx 300 RR^{1.5}
$$

with Z in $mm^6\,m^{-3}$ and RR in mm/hr.  It's helpful to know that:

$$
\int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}
$$

2) Repeat using numerical integration in python (i.e. np.diff and np.sum) and show that the
   the result agrees.


### Landsat problem 

Main objective: 

1) Download rioxarray datasets for 40 landsat windowed scenes for 10 years of seasonal data

2) For each dataset, add the new masked ndvi for that image as another rioxarray.

3) Loop through the 40 datasets, calculate the area-averaged ndvi for each scene, and
   make a simple x-y plot of average ndvi vs. time for the 40 scenes

Your notebook should have:

1)  a function that saves the date of the lowest cloud fraction for each scene, folllowing {ref}`week8:pandas_worksheet` as a python list.

2) a function that retrieves each scene from the list if it hasn't been downloaded and saves
   it to a netcdf dataset using code from {ref}`week10:write_geotiff`

3) a function that reads an image datset and adds the ndvi image as a new rioxarray
   
4) a function that reads and sorts the ndvi arrays by date, calculates the mean and makes the 
   x-y plot
   
Hand in:  pencil and paer for the radar problem with a notebook cell for the
verification, and a notebook that defines the functions and runs and makes the ndvi plot
for the landsat 


