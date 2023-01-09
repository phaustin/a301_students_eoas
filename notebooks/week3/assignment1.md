---
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0-dev
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(assign1)=
# Assignment 1 -- brightness temperatures

Upload this notebook to canvas by 10am Monday Sept. 28

+++

## Problem 1

In the cell below define a function that inverts the radiance (in MKS units) for the
brightness temperature in Kelvins.  Use the same format as the {ref}`sec:planck` notebook,
and use the %%file magic to output your function to a file called `planck_invert.py`

i.e. the top of the cell should look like:

```python
%%file planck_invert.py
def radiance_invert(wavelengths, Lstar):
   etc.
```

+++

## Problem 2

In the next cell import your `radiance_invert function` and use it to turn the calibrated
radiances you've written out in your `modis_data_analysis` notebook into brightness temperatures
in Kelvins.  Plot the temperatures as an image, using a colorbar as in Modis level1b notebook
