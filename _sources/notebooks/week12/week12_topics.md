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

# Week 12
## At the start of class

* `conda activate a301`

* fetch and reset

          git status
          git fetch
          git reset --hard origin/main
          

* Check to see whether your library version is up to date by comparing [the latest tag](https://github.com/phaustin/a301_students_eoas/tags) with the output of `hdf4_inspect --version`

  * If needed, update the libraries with `pip install -r requirements.txt`


## Topics for Monday

- {ref}`assign5_solution`

## Assignment 6

- Cloudsat: Assignment 6, due Wednesday April 12 9am 

  - Hurricane case study: use the {ref}`assign6` notebook.
  
  - Radar equation problems -- either a notebook or scanned pdf

    - Q1: Suppose a Nexrad radar (Stull p.~246)  is
     receiving a signal with returned power Pr = -58 dBm.  Using the radar
     equation find the precipitation rate under the assumption that
     there is no attenuation and that it is a rainstorm (i.e. liquid water)
     100 km away from the radar.

    - Q2: Now keep everything the same, but make the mistake of guessing that it's a snowstorm,
       which means that $K^2$=0.208 and we use the snowfall Z-RR relation
       of Z=2000*RR**2.

    - Q3: Now assume it's rain, but make the mistake of guessing that there's a factor of La=2
      attenuation between the target and the rainstorm
 
## Topics for Wednesday

* [global models and hurricanes](https://www.youtube.com/watch?v=n0mupl4FZsQ&list=PL8UshAqCEEvBPUtj6bThjh20bMhvNmeME&index=2)

* {ref}`week12:goes_review`

 
## Final exam 

* {ref}`week12:final-guide` -- added study questions

* [draft equation sheet](https://github.com/phaustin/a301_students_eoas/blob/main/notebooks/week12/docs/final_equations.pdf)

### Study questions



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




