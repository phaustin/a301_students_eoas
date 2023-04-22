# Week 7

## Learning goals

- Review Assignment 3b solution

- Review Friday midterm practice solutions

- Introduction to using rasterio and xarray to manage geotiff data

- Wednesday: Introduction to Landsat and Sentinel data

## At the start of class

* `conda activate a301`

* fetch and reset

          git status
          git fetch
          git reset --hard origin/main
          

* Check to see whether your library version is up to date by comparing [the latest tag](https://github.com/phaustin/a301_students_eoas/tags) with the output of `hdf4_inspect --version`

  * If needed, update the libraries with `pip install -r requirements.txt`

## Week 7 topics for Monday

### Midterm coverage

* Schwartzchild equation
* Beers law, absorptivity, emissivity, transmissivity
* calculating optical depth
* solid angle
* Calculating flux, radiance, power at satellite
* [Midterm planck diagram](https://www.dropbox.com/s/kt9jx98b6p3pw94/planck_midterm.pdf?dl=0)

* {ref}`mid_review1_sol`
* {ref}`assign3b_solution`
* {ref}`week7:geotiff_xarray`

### Week 7 topics for Wednesday

* {ref}`mid_review2_sols`
* [Equation sheet from previous midterm](https://drive.google.com/file/d/1vzFhERy1thQ80gpiInWQJFs2ipFKYvoZ/view?)

* Read these links about Landsat and Sentinel
  - [landsat program](https://en.wikipedia.org/wiki/Landsat_program)
  - [sentinel program](https://en.wikipedia.org/wiki/Sentinel-2)
  - [landsat bands](https://landsat.gsfc.nasa.gov/satellites/landsat-8/landsat-8-bands/)
  - [NASA hls program](https://earthobservatory.nasa.gov/blogs/earthmatters/2021/05/17/data-in-harmony/)
  
* Go over {ref}`week7:hls` with your own landsat image.

### Week 7 topics for Friday

* Midterm
* For Monday -- review {ref}`week6:pandas_intro` and make sure {ref}`week8:fetch` works
  for your Landsat location
  
  

