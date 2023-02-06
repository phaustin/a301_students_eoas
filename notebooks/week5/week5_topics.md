# Week 5

## Learning goals

* Use cartopy and pyresample to regrid Modis data onto a uniform grid in a Lambert Aziumthal projection

* Map the 1 km and 5 km water vapor retrievals for your granule

* Week 5 topics for Monday

  * Go over the [assignment 1 solution](

  * 

  * Introduce [command line tutorial](https://realpython.com/python-command-line-arguments/)

  * Demonstrate how this works in the terminal with [hdf4_inspect]( https://github.com/phaustin/a301_2020/blob/master/sat_lib/bin/h5_list.py)

  * To list all geom hdf5 files and then print
    the contents of the myd03 file belonging to max:

         cd /home/jovyan/work/sat_data/h5_dir
         ls geom*h5
         ~/work/sat_lib/bin/h5_list.py geom*max*

   * Useful shell commands

         cd ..  (go up one directory)
         pwd    (print working directory)
         cd ~   (change to home directory)
         ls *    (list all files)
         ls -lRd *  (long listing all files, decending into directories recursively)

  * Go over {ref}`testing`

  * Introduce {ref}`assign3`

  * For Friday: Read [Stull Chapter 1 pages 8-11](https://www.eoas.ubc.ca/books/Practical_Meteorology/prmet102/Ch01-atmos-v102b.pdf) and my   {ref}`hydro` notes

* Topics for Friday

  * new data files in data_share/h5_files, written by
    [process_bands.py](https://github.com/phaustin/a301_2020/blob/master/sat_lib/process_bands.py)

  * Introduction to pandas: {ref}`pandas_intro`

  * Scale heights: {ref}`scale_heights`
