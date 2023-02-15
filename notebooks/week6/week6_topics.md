# Week 6

## Learning goals

* Introduce/review pandas

* Apply the idea of scale height to compute atmospheric profiles of density, temperature and pressure

* Use the Schwartzchild equation (Stull 8.5) to retrieve temperaure and vapor profiles with height

* Understand how radiance profiles can be used to estimate flux with the diffusivity approximation

* Work with raster images using the affine transform

* Write out regridded files as geotifs

## At the start of class

* `conda activate a301`

* fetch and reset

          git status
          git fetch
          git reset --hard origin/main
          

* Check to see whether your library version is up to date by comparing [the latest tag](https://github.com/phaustin/a301_students_eoas/tags) with the output of `hdf4_inspect --version`

  * If needed, update the libraries with `pip install -r requirements.txt`

## Week 6 topics for Monday

* {ref}`week6:pandas_intro`
* {ref}`week6:pandas_cheatsheet`
* {ref}`sec:numpy`
* {ref}`week6:scale_heights`

## Week 6 topics for Wednesday

* new library module: sat_lib.thermo calculates pressure and density scale heights

* {ref}`assign3a_solution`
* {ref}`week6:weighting_funs`

## Week 6 topics for Friday

* new library function sat_lib.mapping.make_areadef_dict creates a pyresample areadef
  from projection and raster information

* Assignment 3b due Wednesday Feb. 22 at midnight
* Finish discussion of {ref}`week6:weighting_funs`
* Introduce geotiffs: {ref}`week6:geotiffs`
* [Standard representations for coordinate reference systems](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-vector-data-python/spatial-data-vector-shapefiles/epsg-proj4-coordinate-reference-system-formats-python/)
* [https://spatialreference.org/](https://spatialreference.org/)

