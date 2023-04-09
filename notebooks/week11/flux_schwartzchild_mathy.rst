.. default-role:: math

The diffusivity approximation
+++++++++++++++++++++++++++++

From the :ref:`heating` notes we have the heating rate equation :eq:`temprate` used by cloudsat:

.. math::

      \frac{dT}{dt} = \frac{1}{\rho c_p} \frac{dE_{net}}{dz}

But how do we get `E_{net}` if the satellites only measure radiance `L`?  Graphically, this is the
situation we know how to solve, from :ref:`schwartz` notes:

.. figure::  figures/schwartzchild.png
   :scale: 35
   :name: schwartzchild2

But this only works for photons that are going straight up or straight down.
For the flux, we need to count
every photon at going up at any zenith angle `\mu = \cos \theta`.  Our situation is more like this:

.. figure::  figures/diffuse_flux.png
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
           
    \hat{t}_f =  \int_0^1 \mu \exp \left ( \frac{(\tau - \tau^\prime)}{\mu} \right ) d\mu
       =  \exp \left (-1.66 (\tau - \tau^\prime) \right )

where `\hat{t_f}` is called the **flux transmissivity**.    


This gives a the upward flux version of :eq:`rep_constant`:

.. math::

   E_{\lambda \uparrow} = \pi L_{\lambda 0} \exp( -1.66 \tau_{\lambda T}  ) + \pi B_\lambda (T_{layer})(1- \exp( -1.66\tau_{\lambda T} ))

And if we then integrate this over all wavelengths we get the **broadband flux equation**:

.. math::

   E_{\lambda \uparrow} = \sigma T_0^4 \exp( -1.66 \overline{\tau}_{\lambda T}  ) + \sigma T_{layer}^4(1- \exp( -1.66 \overline{\tau}_{\lambda T} ))
   



This is called the "diffusivity approximation":  replace the vertical optical thickness `\tau` by
`\frac{5}{3} \tau` and multiply blackbody radiances by `\pi`.



* Start with the equation for the upward radiance with `\mu=1` which we saw in :eq:`calc1`:

  .. math::

     L_\lambda(\tau)= B_\lambda(T_{skin})( \exp(-\tau) +    \int_0^{\tau} \exp\left(  - (\tau -\tau^\prime) \right ) 
     B_\lambda(T)\, d\tau^\prime 

* Add the fact that the photons that travel along a slant path have lower transmissivity.
  In fact:  they travel a distance `\Delta s = \Delta z/\cos \theta = \Delta z/\mu` which
  is Stull's `\Delta s` in his equation 2.31b

  .. math::
     :label: newslant

       L_\lambda(\tau,\mu)= B_\lambda(T_{skin})( \exp(-\tau/\mu) +    \int_0^{\tau} \exp\left(  - (\tau -\tau^\prime)/\mu \right ) 
       B_\lambda(T)\, \frac{d\tau^\prime}{\mu}
     
  
* So define a new transmission for the slant path:


* and use it to rewrite :eq:`newslant`:

  .. math::
     :label: newslant2

       L_\lambda(\tau,\mu)= B_\lambda(T_{skin}) \hat{t}_{stot}  +    \int_0^{\tau} B_\lambda(T)\,d\hat{t_s}

     
Integrating over `\mu=\cos \theta`
----------------------------------
  
* In the :ref:`week2_flux_from_radiance` notes we turned blackbody isotropic radiance
  into a flux by taking the normal component and integrating over the hemisphere, in :eq:`flux_final`:
  
  .. math::
     :label: allangles2

       \begin{align}
       E_\lambda&= \int_0^{2 \pi} \int_0^{\pi/2} \cos \theta\, I_\lambda \sin \theta d\theta d\phi \\
                &= 2 \pi  \int_0^1 \mu \, I_\lambda  d\mu
      \end{align}
  assuming no dependence on `\phi` and substituting `\mu= \cos \theta`

  .. math::
     :label: allangles2
          
      E_\lambda=  2 \pi L_\lambda \int_0^1 \mu  d\mu  = 2 \pi \frac{\mu^2}{2} \Bigg \rvert_0^1 = 2 \pi  I_\lambda \frac{ 1}{ 2} 
       = \pi L_\lambda



  

Radiance into flux
==================

So do this to :eq:`Luptrans`

.. math::
  :label: allanglesmu}

  \begin{gather}     
   E_\uparrow = \int_0^{2 \pi} \int_0^{\pi/2} \cos \theta\, 
   I_\lambda \sin \theta d\theta d\phi =  2\pi \int_0^1 \mu I_\lambda d \mu \notag\\ 
   = 2 \pi B_{\lambda 0}(T_s) \int_0^1 \mu  \exp(-\tau/\mu) d\mu \nonumber\\
   + 2 \pi \int_0^1  
   \int_0^{\tau} \exp\left( -\frac{(\tau - \tau^\prime)}{\mu} \right ) B_\lambda(T)\,d\tau^\prime d\mu
  \end{gather}

The difference
is that now our expression for  `L_\lambda(\tau,\mu, \phi)` depends on
the zenith angle `\theta`, so that the integral is more difficult (actually
it's impossible to do analytically).



Flux transmissivity
==================+

  
* To make progress, first swap the limits of integration (ok because the layers
    are plane parallel)

.. math::    
   :label: allanglesmuswapII

   \begin{gather}
         E_\uparrow =   \pi B_{\lambda 0}(T_s)\, 2 \int_0^1 \mu  \exp(-\tau/\mu) d\mu
         +      \nonumber\\
        \int_0^{\tau} \pi B_\lambda(T)\, 2 \int_0^1 \exp\left( -\frac{(\tau - \tau^\prime)}{\mu}
        \right ) \, d\mu\, d\tau^\prime
    \end{gather}

(Remember that `T` does depend on `z`, and therefore `B_\lambda(T)` has to stay inside the `\tau^\prime` integral.)


Flux transmissivity cont
========================
  
* Look what happens to this equation if we define `t_f`, the \textit{flux transmittance},
as:

.. math::
  :label: fluxtrans
          
   Tr_f=  2 \int_0^1 \mu  \exp(-(\tau - \tau^\prime)/\mu) d\mu 

and differentiating wrt `\tau^\prime`:

.. math::
  :label: fluxtransb
          
   dTr_f=  2 \int_0^1  \exp(-(\tau - \tau^\prime)/\mu) d\mu d\tau^\prime

Plug these into :eq:`allanglesmuswapII` and get:

.. math::
  :label: allangles2B
          
      E_\uparrow = \pi  B_{\lambda 0}(T_s) \, Tr_f(0,\tau)
      +  \int_0^{\tau}  \pi \, B_\lambda(T)\,d Tr_f(\tau^\prime,\tau) 

         
Exponential integrals
====================+
  
* But how do we get values for `Tr_f` and `dTr_f` if we can't do
the integration?  -- Use python to evaluate

.. math::
   :label: fluxtrans2

      Tr_f=  2 \int_0^1 \mu  \exp(-(\tau - \tau^\prime)/\mu) d\mu = 2 E_3(\tau)

exactly.

* We wouldn't be any further ahead except that, it turns out to
  a very good approximation:

.. math::
  :label: expapprox0
          
      Tr_f(\tau) = 2 E_3(\tau) \approx \exp \left (- \frac{5}{3} \tau \right )

In words, that means that the flux sees a layer that is effectively 5/3 times
thicker, compared with the layer faced by photons pointed at `\mu=1` (straight up).  
Be sure you understand why this make physical sense.


Repeat the Schwartzchild problem

* A 100 m thick nocturnal cloud layer with a temperature of 270 K floats
over a 300 K surface.  The volume absorption coefficient of the cloud
is `\beta_a=0.01\  (m^{-1})`, and the downward longwave flux density from the
air above the cloud is 100 \wm.  Assuming that there is no absorption between
the surface and the cloud base


*  Find the total flux transmission of the cloud


*  Find the upward and downward  monochromatic fluxes
     
`E_\lambda~ ( (W\,m^{-2}\mu m^{-1})`) 
at a height `z=75` m above cloud base and a wavelength of 10 \mu m, assuming that
the downward flux at cloud top is `E_{10\,\mu m}= 12\  (W\,m^{-2}\mu m^{-1})`
    
Python
======
  
* \href{/home/phil/public_html/courses/atsc301/repos/expint3.py}%
{expint3.py} plots 2 times the exact exponential integral calculated by
python and compares it to the approximation

.. math::
  :label: expapprox
          
   Tr_f(\tau) = 2 E_3(\tau) \approx \exp \left (- \frac{5}{3} \tau \right )


Not too shabby for such a simple approximation

Fluxes continued
================

.. math::
  :label: expapprox2
          
  \begin{gather}
     Tr_f(\tau) = 2 E_3(\tau) \approx \exp \left (- \frac{5}{3} \tau \right ) = \\
     \exp \left (- \tau/(3/5) \right ) 
     =\exp \left (- \tau/\cos 53^\circ \right ) \\
     = \exp \left (- \tau/ \overline{\mu} \right )
   \end{gather}

* So you if you like you can think of the flux as if it was a radiance
going through the layer at an angle of `53^\circ`.

or rewriting :eq:`allangles2B`

Or just think of it as passing though a layer that's 
1.66 times thicker than `\tau`.

.. math::
   :label: allangles3
           
      E_\uparrow = \pi  B_{\lambda 0}(T_s) \, Tr(0,1.66\tau)
      +  \int_0^{\tau}  \pi \, B_\lambda(T)\,d Tr(1.66\tau^\prime,1.66\tau) 

This is the approximation that we use for the day 17 problem.
