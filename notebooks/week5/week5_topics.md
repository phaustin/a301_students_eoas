# Week 5

## Learning goals

* Use cartopy and pyresample to regrid Modis data onto a uniform grid in a Lambert Aziumthal projection

* Map the 1 km and 5 km water vapor retrievals for your granule

## Week 5 topics for Monday

* Go over the {ref}`assign1_solution`

* Introduce new library routines: [readband_lw](https://phaustin.github.io/a301_web/_modules/sat_lib/modischan_read.html#readband_lw) and [read_plainvar](https://phaustin.github.io/a301_web/_modules/sat_lib/modischan_read.html#read_plainvar)

* New command line program:  [hdf_inspect](https://phaustin.github.io/a301_web/index.html)

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

