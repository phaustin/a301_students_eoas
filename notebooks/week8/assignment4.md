---
jupytext:
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

(assign4)=
# Assignment 4 -- due midnight, march 15

+++ {"tags": [], "user_expressions": []}

## Q1) midterm question 2 revisit  

(6 points, for undergrads will replace your midterm Q2 mark)

Upload a notebook and a pdf scan of an analytic solution  solves {ref}`mid_2022t2_solutions` with this
change:

a) Instead of an constant temperature layer between 1 km and 6 km, use a temperature that
varies with linearly with height:

$$
T(z) = 270 - (z -  3.5) \Gamma_z
$$
where $z$ is the height in km and $\Gamma$ is a (negative) constant (K/km).

In a python notebook, make a plot of the blackbody radiance at 15 microns versus transmittance $t$
between z=1 and 6 km for three values of $\Gamma_z$: $\Gamma_z = 0$ (midterm case),  $\Gamma_z = -10\ K/km$
(dry atmosphere),$\Gamma_z = -6.5\ K/km$ (cloudy tropical atmosphere).

Use your plots to find values of $\Gamma_t = \frac{dB}{dt}$ that correspond to the three values of $\Gamma_z$
so that you can write an approximate linear function $B(t)$ that looks like:

$$
B(t) = B(t(1km)) - (t - t(3.5km))\Gamma_t
$$(eq:planck)

b) Given {eq}`eq:planck` derive an analytic solution for the radiance $L$ at 6 km coming from the air
between 1 km and 6 km.  That is, solve the Schwartzchild integral:

$$L(6km) = \int_{1km}^{6km} B(t^\prime) dt^\prime$$

as an equation.  You'll find [this page](https://en.wikipedia.org/wiki/List_of_integrals_of_exponential_functions) helpful.

+++ {"tags": [], "user_expressions": []}

In another cell in your notebook, calculate L(6km) for the three values of $\Gamma_z$.  How much do they vary, in percent, from each other?

+++ {"tags": [], "user_expressions": []}

## Question 2 ndvi
(6 points)

Use the function [get_landsat_scene](https://phaustin.github.io/a301_web/full_listing.html#sat_lib.landsat_read.get_landsat_scene) to read
in one of your landsat scenes and get back a dictionary containing the band4, band5 and Fmask channels.

Write a function called `calc_ndvi` that takes this dictionary and returns a new rioxarray DataArray
that contains the [normalized vegetation difference index](https://www.usgs.gov/landsat-missions/landsat-normalized-difference-vegetation-index) for each pixel in your scene.

Hand in a notebook produces the ndvi image and plots it in greyscale with a title that contains the image date.  Make sure you
multply your ndvi array by the cloud mask to set all cloudy/water pixels to np.nan, and in the last cell of the notebook write the ndvi
DataArray out as geotiff.

