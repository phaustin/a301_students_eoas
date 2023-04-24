---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: -all
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

# Midterm backpages

The following equation sheet and blackbody plot will be stapled to the
back of the midterm

## Useful Equations

$$
  \nu &=& c / \lambda\\
   E &=& h \nu
$$

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

- Transmission function for upwelling radiation

$$t &=& \exp ( - (\tau - \tau^\prime) ) $$


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
\begin{gathered}
L_\lambda(\tau_{\lambda T})= B_\lambda(T_{skin}) \exp(-\tau_{\lambda T}) +    \int_0^{\tau_{\lambda T}} B_\lambda(T)\, d\hat{t}
\end{gathered}
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

## Planck curves

```{figure} ./a301_planck.png
---
width: 60%
name: fig:planck
---
Planck function
```
