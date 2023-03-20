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

# Week 10
## At the start of class

* `conda activate a301`

* fetch and reset

          git status
          git fetch
          git reset --hard origin/main
          

* Check to see whether your library version is up to date by comparing [the latest tag](https://github.com/phaustin/a301_students_eoas/tags) with the output of `hdf4_inspect --version`

  * If needed, update the libraries with `pip install -r requirements.txt`


## Learning goals

- Landsat: download multiple windowed images, sort them by date and save them to disk
  using pandas and rioxarray

- Cloudsat: using xarray to clip a time series to specific times, and plot
  time-height cross sections with different coordinates


## Week 10 topics for Monday

- Cloudsat: plotting temperature pertubations and wind speed with {ref}`week10:temperature_perturb`

- Landsat: saving multiple windowed landsat scenes with {ref}`week10:write_geotiff`

- Current events

  - [radar tracking of Bird migration](https://cliffmass.blogspot.com/2023/03/massive-migration-occurring-aloft-and.html)
  
  - Using [chatgpt](https://chat.openai.com/chat) to understand python code

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



