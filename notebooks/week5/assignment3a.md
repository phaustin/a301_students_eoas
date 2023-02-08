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

(assign3a)=
# Assignment 3a -- Due Wednesday, Feb. 14 9am

Do these questions on paper and scan for upload a pdf created using one of these [scanning apps](https://help.gradescope.com/article/0chl25eed3-student-scan-mobile-device)

+++

## Q1: Flux from radiance  (6 points)

Suppose a satellite is looking at the surface with the following field of view:

<img src="cone.png" width="60%">

Where h = 800 km and r = 5 km

We know from  {ref}`flux_from_radiance` eq. 5 that the flux is given by:

$$
dE^\prime = L \cos \theta^\prime d \omega^\prime = L \cos \theta^\prime \sin \theta^\prime d \theta^\prime d\phi^\prime
$$ 

so that if we interate for all angles $\theta^\prime$ within the cone's field of view we would get the total flux reaching the sensor:

$$
E = \int dE = \int_0^{2\pi} \int_0^{\theta} \cos \theta^\prime \, L \, d \omega^\prime =\int_0^{2\pi} \int_0^{\theta} L \cos \theta^\prime  \sin \theta^\prime \, d\theta^\prime \, d \phi^\prime 
$$

### Q1a (2 points)

Use the change of variables $\mu^\prime = \cos \theta^\prime$ to change this integral into a integral with respect to $d\mu^\prime$ and $d\phi^\prime$

### Q1b (2 points)

Evaluate this intergral for the limit $\theta$ appropriate for the h=800 km and r=5 km case mentioned above.


### Q1c (2 points)

Compare the answer you get from Q2a with the following simple approximation for the flux:

$$
E = L \Delta \omega
$$

where

$$
\Delta \omega = \frac{Area}{h^2} = \frac{\pi r^2}{h^2}
$$

How accurate is this approximation compared to the exact integral?

### Q1d (2 points)

Suppose $L = L_\lambda \Delta_\lambda$  where $L_\lambda$ is the monochromatic planck blockbody radiance at a wavelength of 10 $\mu m$ and a temperature of 300 K.  If the filter width
$\Delta \lambda$ = 2 $\mu m$, what is the flux $E$ reaching the satellite for this problem?


## Q2 (3 points)  Kirchoff's law for a gas

In {ref}`schwartz` we used the 2nd law to prove by contradiction for that
absorptivity = emissivity for using two
surfaces at the same temperature.   Make the same argument for a gas between
two black plates -- i.e. show that if the emissivity and absorptivity of the
gas are not equal you violate the second law of thermodynamics.

## Q3 (5 points)  Histogramming lats/long

Write a program in pseudo-code (doesn't have to run) that would bin a list of lat/lon pairs into a regular lat/lon grid with 1 degree resolution from -180-180 degrees longitude and -90->90 degrees latitude.
