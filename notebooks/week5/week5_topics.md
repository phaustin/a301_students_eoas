# Week 5

## Learning goals

* Use cartopy and pyresample to regrid Modis data onto a uniform grid in a Lambert Aziumthal projection

* Map the 1 km and 5 km water vapor retrievals for your granule

## Week 5 topics for Monday

* Go over the {ref}`assign1_solution`

* Introduce new library routines: [readband_lw](https://phaustin.github.io/a301_web/_modules/sat_lib/modischan_read.html#readband_lw) and [read_plainvar](https://phaustin.github.io/a301_web/_modules/sat_lib/modischan_read.html#read_plainvar)

* To install these:  `pip install -r requirements.txt --upgrade`

* Start using error handling with [exceptions](https://pythonnumericalmethods.berkeley.edu/notebooks/chapter10.03-Try-Except.html) -- see the code in the [sd_open_file](https://phaustin.github.io/a301_web/_modules/sat_lib/modischan_read.html#read_plainvar) function.

* New command line program:  [hdf4_inspect](https://phaustin.github.io/a301_web/index.html)

* Introduce [command line tutorial](https://realpython.com/python-command-line-arguments/)

* Try hdf_inspect out on your MYD05 water vapor file

       cd /home/jovyan/sat_data/pha
       hdf_inspect MYD05*hdf

 * Useful shell commands

       cd ..  (go up one directory)
       pwd    (print working directory)
       cd ~   (change to home directory)
       ls *    (list all files)
       ls -lRd *  (long listing all files, decending into directories recursively)


 * Mapping and resampling:  {ref}`cartopy_resample_ch30}`

## For Wednesday

* Write a function like [readband_lw](https://github.com/phaustin/a301_students_eoas/blob/main/a301_libraries/sat_lib/src/sat_lib/modischan_read.py#L6) to extract either your 1 km near-infrared or 5 km infrared water vapor data into numpy arrays.  Useful links: [product description](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/MYD05_L2) and
[file specification](https://atmosphere-imager.gsfc.nasa.gov/sites/default/files/ModAtmo/MYD05_L2.C6.CDL.fs)

* Paper and pencil:  Write a program in pseudo-code (doesn't have to run) that would bin a list of lat/lon pairs into a regular lat/lon grid with 1 degree resolution from -180-180 degrees longitude and -90->90 degrees latitude.

## Wednesday

- Go over 
  - {ref}`assign2a_solution` 
  - {ref}`assign2b_solution`
 
- Introduce:
  - {ref}`assign3a`
  
## Friday

Continue with resampling -- how do we resample several images with different geometries onto
the same projection?  Demonstrate how to do this with channel 31 resampled onto the ir water vapor
grid.

- Interesting jupyter book:  [The Environmental Data Science book](https://the-environmental-ds-book.netlify.app/welcome.html)

- Set up Assignment 3b

  - New functions to read and write area_defs: [area_def_from_dict](https://phaustin.github.io/a301_web/full_listing.html#sat_lib.mapping.area_def_to_dict) and
[area_def_from_dict](https://phaustin.github.io/a301_web/full_listing.html#sat_lib.mapping.area_def_from_dict)

- Browse the source and note the use of [list expansion](https://note.nkmk.me/en/python-argument-expand/) and [dictionary comprehension](https://www.programiz.com/python-programming/dictionary-comprehension)

- Add cells in {ref}`week5:wv_resample` to save an `area_def` to a [json file](https://realpython.com/python-json/)

- New notebook that resamples the 1 km ch31 radiance to the 5 km ir water vapor grid: {ref}`week5:longwave_resample`

- Give a demo of [Modtran](http://climatemodels.uchicago.edu/modtran/) -- interactive version of 
  [Stull Figure 8.4.c](https://www.eoas.ubc.ca/books/Practical_Meteorology/prmet102/Ch08-satellite_radar-v102b.pdf)
  
  - Channel 31:  10.78-11.28 $\mu m$
  - Channel 32:  11.77-12.27 $\mu m$

  Increase the water vapor mixing ratio (water vapor scale) and note the change in the "dirty window".  Why is the brightness temperature decreasing with increasing H2O?

- For Monday: Read [Stull Chapter 1 pages 8-11](https://www.eoas.ubc.ca/books/Practical_Meteorology/prmet102/Ch01-atmos-v102b.pdf) and my   {ref}`hydro` notes

