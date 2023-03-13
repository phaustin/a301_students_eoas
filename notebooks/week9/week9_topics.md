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

## Learning goals

## Week 9 topics for Monday

- Introduce xarray dataset with {ref}`week9:datasets`

- Finish {ref}`week8:pandas_worksheet`

- For cloudsat: 

  - choose a storm from [the 50 km storm track list](https://adelaide.cira.colostate.edu/tc/tcs-50km.txt) and let me know on slack (grads) or canvas (undergrads).

  - download data for the orbit containing your storm  
    from the [Cloudsat data center](https://cloudsat.atmos.colostate.edu/data).

  - My notes on the [Radar equation] [Stull Chapter 8 pp. 240-248](https://www.eoas.ubc.ca/books/Practical_Meteorology/) on weather radar
* Read this article on [Cloudsat](https://journals.ametsoc.org/view/journals/bams/96/4/bams-d-13-00282.1.xml) to get ready for our next set of satellite data



## At the start of class

* `conda activate a301`

* fetch and reset

          git status
          git fetch
          git reset --hard origin/main
          

* Check to see whether your library version is up to date by comparing [the latest tag](https://github.com/phaustin/a301_students_eoas/tags) with the output of `hdf4_inspect --version`

  * If needed, update the libraries with `pip install -r requirements.txt`

## For Monday

