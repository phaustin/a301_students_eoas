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

# Week 11
## At the start of class

* `conda activate a301`

* fetch and reset

          git status
          git fetch
          git reset --hard origin/main
          

* Check to see whether your library version is up to date by comparing [the latest tag](https://github.com/phaustin/a301_students_eoas/tags) with the output of `hdf4_inspect --version`

  * If needed, update the libraries with `pip install -r requirements.txt`


## Learning goals

- Landsat: Finish Assignment 5, due Wednesday midnight, using the {ref}`assign5` notebook.


- Cloudsat: Understand how cloudsat calculates the heating rate of the atmosphere



## Week 11 topics for Monday

- Landsat: {ref}`assign5`  -- I've provided some extra code for working with files

- Heating rate calculation notes

  - {ref}`week11:cloudsat_heat`
  - {ref}`week11_flux_from_radianceII`
  - {ref}`week11_flux_schwartzchild`
  - {ref}`week11:diffuse_flux`
  - {ref}`week11_heating_rate`

## Week 11 topics for Wednesday

- Examples of how/why false color images are useful

  - {ref}`week11:false_color_examples`

- {ref}`assign5` due Saturday, April 1 midnight

## Week 11 topics for Friday

- Geosynchronous weather satellites - read [Stull chapter 8 pp. 227-234](https://www.eoas.ubc.ca/books/Practical_Meteorology/prmet102/Ch08-satellite_radar-v102b.pdf)
  - Notebook showing how to download and plot a GOES 16 true color image:

  - {ref}`week11:goes_true_color`


### Radar problems for assignment 6 -- due 9am Wednesday April 12

Q1: Suppose a Nexrad radar (Stull p.~246)  is
  receiving a signal with returned power Pr = -58 dBm.  Using the radar
  equation find the precipitation rate under the assumption that
  there is no attenuation and that it is a rainstorm (i.e. liquid water)
  100 km away from the radar.

Q2: Now keep everything the same, but make the mistake of guessing that it's a snowstorm,
    which means that $K^2$=0.208 and we use the snowfall Z-RR relation
    of Z=2000*RR**2.

Q3: Now assume it's rain, but make the mistake of guessing that there's a factor of La=2
    attenuation between the target and the rainstorm
 
 ### Cloudsat notebook for assignment 6
 
 - Posted tonight
 

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
- Mangkhut
- Omais
- Igor




