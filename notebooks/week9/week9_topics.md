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

# Week 9
## At the start of class

* `conda activate a301`

* fetch and reset

          git status
          git fetch
          git reset --hard origin/main
          

* Check to see whether your library version is up to date by comparing [the latest tag](https://github.com/phaustin/a301_students_eoas/tags) with the output of `hdf4_inspect --version`

  * If needed, update the libraries with `pip install -r requirements.txt`


## Learning goals

- work with xarray datasets

- understand the Z-R relationship, Marshall Palmer distribution, bright bands

- download and analyze satellite radar and lidar data

## Week 9 topics for Monday

- Introduce xarray dataset with {ref}`week9:datasets`

- Finish {ref}`week8:pandas_worksheet`

- For cloudsat: 

  - choose a storm from [the 50 km storm track list](https://adelaide.cira.colostate.edu/tc/tcs-50km.txt) and let me know on slack (grads) or canvas (undergrads).  Storms with surface low surface pressures might be most interesting.

  - download data for the orbit containing your storm  
    from the [Cloudsat data center](https://cloudsat.atmos.colostate.edu/data).

  - Go over my notes on the [Radar equation] [Stull Chapter 8 pp. 240-248](https://www.eoas.ubc.ca/books/Practical_Meteorology/) on weather radar

  - Read this article on [Cloudsat](https://journals.ametsoc.org/view/journals/bams/96/4/bams-d-13-00282.1.xml)

- For Landsat

  - Introduce false color composites and band combinations
  
    - [NASA's choice of bands](https://earthobservatory.nasa.gov/features/FalseColor/page6.php)
    
    - [Explore different band combinations](https://gsp.humboldt.edu/olm/Courses/GSP_216/lessons/composites.html)


## Week 9 topics for Wednesday

### Reserved hurricanes

- Nida - 2009/11/28
- Maria - 2017/09
- Flossie - 2008/7/14
- Mekkala
- Billy - 2008
- Mitchell

