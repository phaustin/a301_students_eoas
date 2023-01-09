# Week 5

* Week 5 topics for Monday

  * Review {ref}`schwartz`

  * Introduce [h5py](https://docs.h5py.org/en/latest/quick.html)

  * Move our files to hdf5 

    * {ref}`week4:resample`

    * For Wednesday

      * finish assignment 2

      * move your satellite images over to {ref}`week4:resample`

      * read the rest of {ref}`schwartz`


* Week 5 topics for Wednesday

  * Go over this [command line tutorial](https://realpython.com/python-command-line-arguments/)

  * Demonstrate how this works in the terminal with [h5_list]( https://github.com/phaustin/a301_2020/blob/master/sat_lib/bin/h5_list.py)

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
