.. default-role:: math

Midterm backpages
=================

The following equation sheet and blackbody plot
will be stapled to the back of the midterm
                  
Useful Equations
----------------

.. math::
  :label: nu

   \begin{aligned}
     \nu &=& c / \lambda\\
      E &=& h \nu
   \end{aligned}

.. math::
   :label: omega

    $$d \omega = \sin \theta d\theta d\phi = -d\mu d\phi \approx \frac{ A}{r^2}$$

.. math::
   :label: cos
           
     $$S = S_0 \cos(\theta)$$

.. math::
   :label: conservation
           
     $$a_\lambda + r_\lambda + t_\lambda = 1$$

.. math::
   :label: intensity
           
     $$L_\lambda = \frac{\Delta E}{\Delta \omega \Delta \lambda}$$

.. math::
   :label: flux_int
           
     $$E = \int_{2 \pi} L \cos \theta \sin \theta d \theta d \phi$$

.. math::
   :label: planck
           
   $$B_\lambda(T)  = \frac{h c^2}{\lambda^5 \left [ \exp (h c/(\lambda k_B T )) -1 \right ] }$$

.. math::
   :label: pi
           
     $$E_{\lambda\,BB} = \pi B_\lambda$$

.. math::
   :label: stefan
           
     $$E^* =\sigma T^4$$

.. math::
   :label: taylor
           
     $$E_\lambda(T) \approx E_{\lambda\, 0} + \left .\frac{dE_\lambda}{dT}  \right |_{T_0,\lambda} \!\!\! (T - T_0) + \ldots$$

.. math::
   :label: exp
           
     $$\exp(x) = 1 + x +  \frac{x^2}{2} + \frac{x^3}{3!} + \ldots$$

.. raw:: latex

   \vspace{0.5in}



Beer’s law for absorption:

.. math::
  :label: extinct
   $$       
   \begin{aligned}
   \frac{dL_\lambda}{L_\lambda}  & = &   -\kappa_{\lambda } \rho_{g} ds \nonumber\\
           &=& -\kappa_{\lambda} \rho_{g} dz/\mu
   \end{aligned}
   $$
   
Beer’s law integrated (either direct beam `E` or radiance `L`):

.. math::
   :label: binteg

     E= E_0 \exp (- \tau/\mu)



Hydrostatic equation for pressure:

.. math::
   :label: hydro
           
     $$dp = -\rho_{air}\, g\, dz$$



Hydrostatic pressure equation integrated:

.. math::
   :label: hydroint
           
   $$p = p_0 \exp(-z/H)$$

Equation of state:

.. math::
   :label: state
           
     $$p = R_d \rho_{air} T$$


vertical optical thickness:

.. math::
   :label: tauThick
           
     d \tau =  \kappa_\lambda \rho_g dz = \kappa_\lambda r_{mix} \rho_{air} dz = \beta_a dz

integrate vertical optical thickness:

.. math::
   :label: tauup
           
     \tau(z_1, z_2 ) = \int_{z_1}^{z_{2}} k_\lambda r_{mix} \rho_{air}\, dz^\prime

Transmission function for upwelling radiation

.. math::
   
   \begin{aligned}
   t &=& \exp ( - (\tau - \tau^\prime) ) \nonumber\\
   \end{aligned}



Schwarzchild’s equation for an absorbing/emitting gas

.. math::
   :label: schwarz
           
     dL = -L\, d\tau + B_{\lambda}(T(z)) d \tau

Radiance an isothermal layer:

.. math::
   :label: isothermal
           
   L_\uparrow(\tau_T) = L_0 \exp( - \tau_T /\mu) + (1 - \exp( - \tau_T)) B_\lambda(T)

--------------

`~`

Useful constants:

`~`

`c_{pd}=1004` ,

`\sigma=5.67 \times  10^{-8}`

`k_b = 1.381  \times 10^{-23}`

`c=3 \times 10^{8}`

`h=6.626 \times 10^{-34}`

`\pi \approx 3.14159`

`R_d=287 {J\,kg^{-1}\,K^{-1}}`

Solar radius=`7 \times 10^8` m

Earth-sun distance = `1.5 \times 10^{11}` m

Planck curves
-------------

.. image:: midterm/a301_planck.png
   :scale: 65
