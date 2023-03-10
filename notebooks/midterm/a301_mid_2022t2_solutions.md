---
jupytext:
  cell_metadata_filter: -all
  encoding: '# -*- coding: utf-8 -*-'
  formats: ipynb,md:myst,py:percent
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(mid_2022t2_solutions)=
# A301 midterm -- solutions

**March 10, 2023**: Note that Q2 had a error for the question 2 python code.  The original (incorrect) function had this typo:  `tr_1km = np.exp(-(tr_tot - tau_1km))` 

Below I've fixed that so that it now is:


`tr_1km = np.exp(-(tau_tot - tau_1km))`


## Q1


Q1) (12) A satellite orbiting at an altitude of 36000 km observes the
    surface in the $CO_2$ absorption band with a wavelength
    range of 14 μm  $< λ < 16$ μm.
    
## Q1a

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
    
### Q1a Answer
    
From the definition of optical depth we've got
          
$$
 \begin{aligned}
 \rho(z) &= \rho_0 r_{mix} \exp( -z/H_\rho) \\
 \tau_T &= \int_0^{20} \rho_0 r_{mix} \exp(-z/H) k_\lambda dz = - H \rho_0 r_{mix} k_\lambda (\exp(-20/9)-1)\\
 \tau_T &= 9000 \times 4 \times 10^{-4} *0.15 * (1 - 0.108) = 0.53\\
 t_T &= \exp(-\tau_T) = 0.589
 \end{aligned}
$$

+++

### python for Q1a

```{code-cell} ipython3
import numpy as np
Hrho=9000.
ztop = 20.e3
k=0.15
rho_air = 1.1
rmix=4.e-4
tau_tot=k*rmix*rho_air*Hrho*(1 - np.exp(-(ztop/Hrho)))
print(f"tau_tot: {tau_tot:5.2f}")
tr_tot=np.exp(-tau_tot)
print(f"tr_tot: {tr_tot:5.3f}")
```

 ## Q1b
 
 Q1b) (4 points) If the surface is a blackbody with a temperature of 290 K, and
        the atmosphere has an constant temperature of 270 K, find the

-   monochromatic radiance observed by the satellite at 15
        μm in ($W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$)

-   the brightness temperature of the pixel in Kelvins for that
        radiance

+++

### Q1b answer

  The temperature is constant, so you can pull the Planck function out of the Schwartzchild equation:

  - Schwartzchild equation for surface plus full atmosphere:

 $$ L^\uparrow (\tau_T) = L_0 \, t_{tot} + \int_{t_{tot}}^1  B(T^\prime)\, d\,t^\prime$$



  $$L_\uparrow(\tau_T) = L_0 \exp( - \tau_T /\mu) + (1 - \exp( - \tau_T)) B_\lambda(T)$$
  
   $$L_\uparrow(\tau_T) = L_0 t_T + (1 - t_T) B_\lambda(T)$$

  From the Planck diagram, at $\lambda=15\ \mu m$ I get:
  
  - $L_0 \approx 6\ W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$
  - $B_\lambda \approx 4.6\ W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$
  
  $$L_\uparrow(\tau_T) = 6 \times 0.589   + (1 - 0.589) \times 4.6 = 5.41\ W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$$
  
  From the Planck diagram 5.41 $W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$ at 15 $\mu m$ is a brightness temperature of about 282 K.

+++

### Python for Q1b

```{code-cell} ipython3
from rad_lib.radiation import calc_radiance, radiance_invert
L0=calc_radiance(15.e-6,290.)*1.e-6  #convert to W/m^2/micron
Batm=calc_radiance(15.e-6,270.)*1.e-6
print(f'L0={L0:5.2f} W/m^2/micron/sr, \nBatm={Batm:5.2f} W/m^2/micron/sr')
TOA=L0*tr_tot + (1 - tr_tot)*Batm
print(f'TOA monochromatic radiance = {TOA:5.2f} W/M^2/micron/sr')
wavelength = 15e-6  #meters
Tb=radiance_invert(wavelength,TOA*1.e6)
print(f"Brightness temperature {Tb:5.2f} K")
```

## Q1c

-  Q1c) (4 points) Given a pixel size $10\ km^2$, find:

    -   the imager field of view in steradians

    -   the flux, in $W\,m^{-2}$ at the satellite for the wavelength range between
        14-16 $\mu m$
        
### Q1c answer

- $\Delta \omega$ = $\frac{area}{R^2}$ = $\frac{10}{36000^2}$ = $7.7 \times 10^{-9}\ sr$
    
- $E = L_\uparrow(\tau_T) \Delta \lambda \,\Delta \omega = 5.41 \times 2 \times 7.7\times 10^{-9} = 8.4\times 10^{-8}\ W\,m^{-2}$

+++

### python for q1c

```{code-cell} ipython3
delta_omega = delta_omega=10/36000.**2.
print(f'delta_omega: {delta_omega:8.3g} sr')
delta_lambda = 2
flux = TOA*delta_lambda*delta_omega
print(f'flux in channel = {flux:7.2g} W/m^2')
```

## Q2

+++

Q2) (6 points) For the same atmosphere as in Q1) (i.e. scale height of 9 km and isothermal temperature of 270 K) find the flux between 14-16 $\mu m$ reaching the satellite that originates from the atmospheric layer between heights $z=1\ km$ and $z=6\ km$ in $W\,m^{-2}$

### Q2 answer 

Recall this picture from {ref}`mid_review2_sols`


```{figure} figures/midII_layers.png
---
width: 60%
name: fig:layers
---
Schwartzchild layers
```

As in Question 1 above, we want to find the atmopsheric contribution, which has the form

$$
\int_{t_{bot}}^{t_{top}}\,B(T(z)) dt^\prime
$$
but now the bottom and top levels have changed from the $z_T$ (where $t^\prime=1$) and z=0 (where $t^\prime$ = 0.59) to z=6 km at the top and z=1 km at the bottom.  The two optical thicknesses we need for those 
transmissivities are:

\begin{align}
\tau_{1km} &= \int_0^{1} \rho_0 r_{mix} \exp(-z/H) k_\lambda dz =  H \rho_0 r_{mix} k_\lambda (1 - \exp(-1/9)) = 0.06 \\
\tau_{6km} &= \int_0^{6} \rho_0 r_{mix} \exp(-z/H) k_\lambda dz =  H \rho_0 r_{mix} k_\lambda (1 - \exp(-6/9))=0.29
\end{align}

and the corresponding transmissivities are:

$$t_{6km} = \exp(-(\tau_T - 0.29)) = 0.79$$

$$t_{1km} = \exp(-(\tau_T - 0.06)) = 0.63$$

and the Schwartzchild integral becomes:

$$L_{6km} = \int_{0.591}^{0.74} B_{\lambda} dt^\prime = (0.79 - 0.63) \times 4.6 = 0.74\  W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$$

Finally -- how much of the $0.74\  W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$ makes it out through the atmosphere to 20 km?
From the picture, we just need to multiply the radiance leaving 6 km with the transmissivity from 6 km to the top of the atmosphere:

$$L_{top} = L_{6km} \times t_{6km} = 0.74 \times 0.79 = 0.58\ W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$$

+++

### python for q2

```{code-cell} ipython3
tau_6km =k*rmix*rho_air*Hrho*(1 - np.exp(-(6000/Hrho)))
tau_1km = k*rmix*rho_air*Hrho*(1 - np.exp(-(1000/Hrho)))
print(f"{tau_6km=:5.2f},{tau_1km=:5.2f}")
tr_1km = np.exp(-(tau_tot - tau_1km))
tr_6km = np.exp(-(tau_tot - tau_6km))
print(f"{tr_6km=:5.2f}\n{tr_1km=:5.3f}")
L_6km = Batm*(tr_6km - tr_1km)
print(f"{L_6km=:5.2f} W/(m^2 um sr)")
L_top = L_6km*tr_6km
print(f"{L_top=:5.2f} W/m^2/um/sr")
```

## Q3

Q3) (3 points) A cone has a spreading angle of 35 degrees between its center
    and its side. What is its subtended solid angle?

+++

### Q3 answer

The definition of solid angle:

$$
\begin{align}
\Delta \omega &= \int_0^{2pi} \int_0^\theta \sin \theta^\prime\, d \theta^\prime\, d\phi^\prime\\
 &= -2\pi (\cos(35) - \cos(0)) \\
 &= 2\pi (1 - \cos(35)) = 2\pi(1 - 0.82) = 1.14\ sr \\
\end{align}
$$

+++

### python for q3

```{code-cell} ipython3
cos35 = np.cos(35*np.pi/180.)
print(f'cos35: {cos35:5.2f}')
print(f'omega: {2*np.pi*(1. - cos35):5.2f} sr')
```

## Planck curves

```{figure} figures/a301_radiance_planck.png
---
width: 60%
---
Planck function
```


## Useful Equations

$$
  \nu &=& c / \lambda\\
   E &=& h \nu
$$

Solid angle

$$d \omega = \sin \theta d\theta d\phi = -d\mu d\phi \approx \frac{ A}{r^2}$$

+++

$$
S = S_0 \cos(\theta)
$$

- conservation of energy

$$
a_\lambda + r_\lambda + t_\lambda = 1
$$

- Monochromatic radiance

$$
L_\lambda = \frac{\Delta E}{\Delta \omega \Delta \lambda}
$$

- Flux from radiance

$$
E = \int_{2 \pi} L \cos \theta \sin \theta d \theta d \phi
$$

- Planck function

$$
B_\lambda(T)  = \frac{h c^2}{\lambda^5 \left [ \exp (h c/(\lambda k_B T )) -1 \right ] }
$$

- Blackbody flux

$$E_{\lambda\,BB} = \pi B_\lambda$$

- Stefan-Boltzman

$$E^* =\sigma T^4$$

- Taylor series

$$ E_\lambda(T) \approx E_{\lambda\, 0} + \left .\frac{dE_\lambda}{dT}  \right |_{T_0,\lambda} \!\!\! (T - T_0) + \ldots$$

- Exponential series

$$\exp(x) = 1 + x +  \frac{x^2}{2} + \frac{x^3}{3!} + \ldots$$

Beer’s law for absorption:


$$
\begin{align}
\frac{dL_\lambda}{L_\lambda}  & =    -\kappa_{\lambda } \rho_{g} ds \nonumber\\
 &= -\kappa_{\lambda} \rho_{g} dz/\mu
\end{align}
$$

- Beer’s law integrated (either direct beam $E$ or radiance $L$):

$$E= E_0 \exp (- \tau/\mu)$$

- Hydrostatic pressure equation:


$$dp = -\rho_{air}\, g\, dz$$

- Hydrostatic pressure equation integrated

$$p = p_0 \exp(-z/H)$$

- Equation of state

$$p = R_d \rho_{air} T$$

- differential optical thickness


$$ d \tau =  \kappa_\lambda \rho_g dz = \kappa_\lambda r_{mix} \rho_{air} dz = \beta_a dz$$

integrate vertical optical thickness:

- integrated optical thickness

$$ \tau(z_1, z_2 ) = \int_{z_1}^{z_{2}} k_\lambda r_{mix} \rho_{air}\, dz^\prime$$

- Transmission function for upwelling radiation ($\tau$ increasing with height)

$$t = \exp ( - (\tau - \tau^\prime) ) $$


- Schwarzchild’s equation for an absorbing/emitting gas

$$dL = -L\, d\tau + B_{\lambda}(T(z)) d \tau $$

- Integration for temperature constant with height



$$L_\uparrow(\tau_T) = L_0 \exp( - \tau_T /\mu) + (1 - \exp( - \tau_T)) B_\lambda(T)$$

- Integration for temperature changing with height

$$
     L_\lambda(\tau_{\lambda T})= B_\lambda(T_{skin})( \exp(-\tau_{\lambda T}) +    \int_0^{\tau} \exp\left(  - (\tau_{\lambda T} -\tau^\prime) \right ) 
     B_\lambda(T)\, d\tau^\prime 
$$

- Change of variables to tranmissivity

$$
\begin{gathered}
 L_\lambda = B_\lambda(T_{skin} ) \hat{t}_{tot} + \sum_{j=1}^n e_\lambda B_\lambda(T_j)
   \hat{t}_{\lambda,j}
\end{gathered}
$$

or

$$
L_\lambda(\tau_{\lambda T})= B_\lambda(T_{skin}) \exp(-\tau_{\lambda T}) +    \int_0^{\tau_{\lambda T}} B_\lambda(T)\,dt^\prime
$$
------------------------------------------------------------------------

$~$

Useful constants:

$~$

$c_{pd}=1004$ ,

$\sigma=5.67 \times  10^{-8}$

$k_b = 1.381  \times 10^{-23}$

$c=3 \times 10^{8}$

$h=6.626 \times 10^{-34}$

$\pi \approx 3.14159$

$R_d=287 {J\,kg^{-1}\,K^{-1}}$

Solar radius= $7 \times 10^8\,m$

Earth-sun distance = $1.5 \times 10^{11}$ m
