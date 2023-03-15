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

* Work through {ref}`week9:cloudsat` which demonstrates how to read cloudsat data using
  [read_cloudsat_var](https://phaustin.github.io/a301_web/full_listing.html#sat_lib.cloudsat.read_cloudsat_var)

* Introduce datasets described in Table 3 of this [Cloudsat descriptive paper](https://cloudsat.atmos.colostate.edu/BAMS_CloudSat_CR.pdf)

* Focus on radar equation in Stull page 245 and my {ref}`week9:radar`

* Focus on Z-R relationship in Stull page 247 and my {ref}`week9:marshall`

* What is the bright band?  Why is it bright?

### Reserved hurricanes

- Nida - 2009/11/28
- Maria - 2017/09
- Flossie - 2008/7/14
- Mekkala
- Billy - 2008
- Mitchell


### Radar problem (part of assignment 5)

1) Integrate $Z=\int D^6 n(D) dD$ on paper, assuming a Marshall Palmer size distribution and show that it integrates to:

$$
Z \approx 300 RR^{1.5}
$$

with Z in $mm^6\,m^{-3}$ and RR in mm/hr.  It's helpful to know that:

$$
\int^\infty_0 x^n \exp( -a x) dx = n! / a^{n+1}
$$

2) Repeat using numerical integration in python (i.e. np.diff and np.sum) and show that the
   the result agrees.

