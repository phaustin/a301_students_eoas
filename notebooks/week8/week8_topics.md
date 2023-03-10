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

# Week 8

## Learning goals

- Review midterm solution

- Learn how to subset regions of Landsat images

- Use pandas to sort and to analysis on a large number of landsat scenes

- Use the normalized vegetation difference index to track changes in vegetation from 2013-2022

## At the start of class

* `conda activate a301`

* fetch and reset

          git status
          git fetch
          git reset --hard origin/main
          

* Check to see whether your library version is up to date by comparing [the latest tag](https://github.com/phaustin/a301_students_eoas/tags) with the output of `hdf4_inspect --version`

  * If needed, update the libraries with `pip install -r requirements.txt`

## Week 8 topics for Monday

### Midterm solution

* {ref}`mid_2022t2_solutions`

### Zooming a landsat image

* {ref}`week8:zoom_landsat`

### Using `pystac` to fetch 9 years of landsat images

* {ref}`week6:pandas_intro`
* {ref}`week6:pandas_cheatsheet`
* {ref}`week8:fetch`

## Week 8 topics for Wednesday

* Midterm handback/midterm takehome problem
* {ref}`assign4`
* fetching a windowed landsat scene with {ref}`week8:windowed`
* test the library code with {ref}`week8:test_landsat`

## Week 8 topics for Friday

* Do the {ref}`week8:pandas_worksheet`

## For Monday

* Read [Stull Chapter 8 pp. 240-248](https://www.eoas.ubc.ca/books/Practical_Meteorology/) on weather radar
* Read this article on [Cloudsat](https://journals.ametsoc.org/view/journals/bams/96/4/bams-d-13-00282.1.xml) to get ready for our next set of satellite data
