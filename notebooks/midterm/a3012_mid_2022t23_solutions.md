---
jupytext:
  cell_metadata_filter: -all
  encoding: '# -*- coding: utf-8 -*-'
  formats: ipynb,md:myst,py:percent
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

(mid_2020)=
# A301 midterm -- solutions

Q1) (12) A satellite orbiting at an altitude of 36000 km observes the
    surface in the $CO_2$ absorption band with a wavelength
    range of 14 μm  $< λ < 16$ μm.

-   Q1a) (4 points) The atmosphere is 20 km thick, and has a density scale height of
    $H_\rho$ = 9 km and a surface air density of
    $\rho_{air}$ = 1.1 $kg\,m^{-3}$. The $CO_2$ mass
    absorption coefficient is
    $k_λ$ = 0.15 $m^2\,kg^{-1}$ at
    λ = 15 μm and its mixing ratio is $4 \times 10^{−4}\,kg\,kg^{-1}$.
    Find the:

    - the atmosphere’s vertical optical thickness
        $τ_λ$ in the $CO_2$ band

    - the atmosphere’s transmittance $t_\lambda$ in the $CO_2$
        band

    for a pixel directly beneath the satellite.
    
    - **Q1a answer**: From the definition of optical depth we've got
    
    

-  Q1b) (4 points) If the surface is a blackbody with a temperature of 290 K, and
        the atmosphere has an constant temperature of 270 K, find the

    -   monochromatic radiance observed by the satellite at 15
        μm in ($W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$)

    -   the brightness temperature of the pixel in Kelvins for that
        radiance

-  Q1c) (4 points) Given a pixel size $10\ km^2$, find:

    -   the imager field of view in steradians

    -   the flux, in $W\,m^{-2}$ at the satellite for the wavelength range between
        14-16 $\mu m$
        
Q2) (6 points) For the same atmosphere as in Q1) (i.e. scale height of 9 km and isothermal temperature of 270 K) find the flux between 14-16 $\mu m$ reaching the satellite that originates from the atmospheric layer between heights $z=1\ km$ and $z=6\ km$ in $W\,m^{-2}$


Q3) (3 points) A cone has a spreading angle of 35 degrees between its center
    and its side. What is its subtended solid angle?

+++

## Draw a nice planck function

```{code-cell} ipython3
import a301_lib
from rad_lib import radiation
import sys
from rad_lib.radiation import calc_radiance, radiance_invert
import matplotlib.pyplot as plt
import numpy as np
import math as m
```

```{code-cell} ipython3

```

## Problem 1

### Problem 1a

+++

-   The atmosphere is 20 km thick, and has a density scale height of
    *H*<sub>*ρ*</sub> = 9 km and a surface air density of
    *ρ*<sub>*a**i**r*</sub> = 1.1 kg/m3. The CO<sub>2</sub> mass
    absorption coefficient is
    k<sub>λ</sub> = 0.15 m<sup>2</sup>/kg at
    λ = 15 μm and its mixing ratio is 4 × 10<sup> − 4</sup>
    kg/kg. Find the

    -   the atmosphere’s vertical optical thickness
        τ<sub>λ</sub> in the CO<sub>2</sub> band

    -   the atmosphere’s transmittance *t* in the CO<sub>2</sub>
        band

    directly beneath the satellite.

```{code-cell} ipython3
Hrho=9000.
ztop = 20.e3
k=0.15
rho_air = 1.1
rmix=4.e-4
tau=k*rmix*rho_air*Hrho*(1 - np.exp(-(ztop/Hrho)))
print(f"tau: {tau:5.2f}")
Tr=np.exp(-tau)
print(f"Tr: {Tr:5.2f}")
```

### Problem 1b

-   If the surface is a blackbody with a temperature of 290 K, and
    the atmosphere has an constant temperature of 270 K, find the

    -   monochromatic radiance observed by the satellite in at 15
        μm

    -   the brightness temperature of the pixel in Kelvin for that
        radiance

```{code-cell} ipython3
Bsfc=calc_radiance(15.e-6,290.)*1.e-6  #convert to W/m^2/micron
Batm=calc_radiance(15.e-6,270.)*1.e-6
print(f'Bsfc={Bsfc:5.2f} W/m^2/micron/sr, Batm={Batm:5.2f} W/m^2/micron/sr')
TOA=Bsfc*Tr + (1 - Tr)*Batm
print(f'TOA monochromatic radiance = {TOA:5.2f} W/M^2/micron/sr')
print(f'corresponding monochromatic flux for blackbody = {TOA*m.pi:5.2f} W/M^2/micron')
Tb=radiance_invert(15.e-6,TOA*1.e6)
print(f"Brightness temperature {Tb:5.2f}")
```

### Problem 1c

 -   Given a pixel size 4 km<sup>2</sup>, find:

    -   the field of view in steradians, of the pixel

    -   the flux, in *W*/*m*<sup> − 2</sup> at the satellite between
        $14-16 \mu m$

```{code-cell} ipython3
delta_omega = delta_omega=10/36000.**2.
print(f'delta_omega: {delta_omega:8.3g} sr')
```

```{code-cell} ipython3
channel_width = 2
TOA_flux = TOA*delta_omega*channel_width
print(f'TOA flux from 14-16 microns: {TOA_flux:8.3g} W/m^2')
```

## Problem 2

```{code-cell} ipython3
tau4km =k*rmix*rho_air*Hrho*(1 - np.exp(-(6000/Hrho)))
tau3km = k*rmix*rho_air*Hrho*(1 - np.exp(-(1000/Hrho)))
tr3km = np.exp(-(Tr - tau3km))
tr4km = np.exp(-(Tr - tau4km))
emission = Batm*(tr4km - tr3km)
tr4km - tr3km
emission*tr4km
```

## Problem 3

- (3) A cone has a spreading angle of 23 degrees between its center
    and its side. What is its subtended solid angle?
  
Use [Problem 7.2.2](https://a301_web.eoas.ubc.ca/week6/answers/sols_mid_revI.html#solid-angle-and-radiance)

$$
\begin{align}
\omega &= \int_0^{2\pi} \int_0^{23} \sin \theta d\theta d\phi \\
       &= -2\pi (\cos(23) - \cos(0)) \\
       &= 2\pi (1 - \cos(23)) = 2\pi(1 - 0.92) = 0.5\ sr \\
\end{align}
$$

```{code-cell} ipython3
cos23 = np.cos(35*np.pi/180.)
print(f'cos23: {cos23:5.2f}')
print(f'omega: {2*np.pi*(1. - cos23):5.2f} sr')
```
