.. default-role:: math

.. _week11_flux_schwartzchild:
             
The Schwartzchild equation for flux
+++++++++++++++++++++++++++++++++++

How do we get `E_{net}` if the satellites only measure radiance `L`?  Graphically, this is the
situation we know how to solve, from :ref:`week4_schwartz` notes:

.. figure::  ./figures/schwartzchild.png
   :scale: 35
   :name: schwartzchild2

But this only works for photons that are going straight up or straight down.
For the flux, we need to count
every photon at going up at any zenith angle `\mu = \cos \theta`.  Our situation is more like this:

.. figure::  ./figures/diffuse_flux.png
   :scale: 55
   :name: diffuse

Where does that leave us?  Surprisingly, moving from radiance to flux is reasonably approximated by simply increasing the optical thickness of the layer, to take into account the fact
that almost all photons have further to travel through the layer than those that are
going straight up.  Specifically for a constant temperature layer we found :eq:`rad_constant`:

.. math::
   :label: rep_constant

   L_\lambda = L_{\lambda 0} \exp( -\tau_{\lambda T}  ) + B_\lambda (T_{layer})(1- \exp( -\tau_{\lambda T} ))

Accounting for slant paths
==========================

Nothing in the derivation of :eq:`rad_constant` prevents us from
setting the zenith angle for the photon paths
to something besides `\cos \theta = 0\ (\mu = 1)`.  Step 1 is to remember the relationship between
`L` and `E`.  For upward flux we integrate over the upward facing hemisphere:

.. math::
   :label: allangles2

           \begin{align}
           E&= \int_0^{2 \pi} \int_0^{\pi/2} \cos \theta\, L \sin \theta d\theta d\phi \\
           &\text{or changing variables $\mu=\cos \theta$ integrating over azimuth $\phi$}: \\
           E&= 2\pi\int_0^{1}  \mu  L d\mu 
   \end{align}

For :eq:`rad_constant` we took `L` out of the integral and got `E=\pi L`, but this isn't an option now, because the transmissivity depends on `\mu`.  Specifically, with `\mu \neq 1` we have new
definitions for the **slant transmissivity** `\hat{t}_s`:

.. math::
   :label: fluxtrans4

    \begin{align}
           \hat{t_s} &= \exp \left ( \frac{(\tau - \tau^\prime)}{\mu} \right ) \\
      d\hat{t_s} &=\frac{d \hat{t_s}(\tau^\prime,\tau)}{d\tau^\prime} d\tau^\prime = 
           \exp\left( -\frac{(\tau -
      \tau^\prime)}{\mu} \right ) \frac{1}{\mu} d\tau^\prime
    \end{align}

We can't integrate this transmission over `\mu` analytically, but the integrals are easy
to do numerically.  As you'll show in a separate notebook, the following "diffusivity"
approximation is quite good:

.. math::
   :label: diffusivity
           
    \hat{t}_f =  2 \int_0^1 \mu \exp \left (- \frac{(\tau - \tau^\prime)}{\mu} \right ) d\mu
       =  \exp \left (-1.66 (\tau - \tau^\prime) \right )

where `\hat{t_f}` is called the **flux transmissivity**.    


This gives a the upward flux version of :eq:`rep_constant`:

.. math::

   E_{\lambda \uparrow} = \pi L_{\lambda 0} \exp( -1.66 \tau_{\lambda T}  ) + \pi B_\lambda (T_{layer})(1- \exp( -1.66\tau_{\lambda T} ))

And if we then integrate this over all wavelengths we get the **broadband flux equation**:

.. math::
   :label: layer_flux

   E_{\uparrow} = \sigma T_0^4 \exp( -1.66 \overline{\tau}_{\lambda T}  ) + \sigma T_{layer}^4(1- \exp( -1.66 \overline{\tau}_{\lambda T} ))
   
where the overbar indicates that we've average `\tau_\lambda` over all thermal wavelengths.

.. _two-stream-approx:

The two stream approximation
============================

When we repeat this for the downward facing hemisphere (`\pi/2 \leq \theta \leq \pi`) and get
the downward flux `E_\downarrow`,
we've got the **two stream approximation**.  Next we'll show how Cloudsat uses this to get heating rates in the atmosphere.




