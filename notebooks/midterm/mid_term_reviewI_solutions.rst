.. default-role:: math

.. _mid_review1_sol:

Solutions: sample questions I
============================

Beers law
---------

Stull page 2.43 and the :ref:`beers_law` reading:

#. Prove that for a thin  non-reflecting layer the change in emissivity
   =  change in optical thickness, i.e. prove that:

   .. math::
      :label: thin
              
         \Delta e_\lambda \approx  \Delta \tau_\lambda

   **Answer:**
   
   Assuming no reflection, we know that the absorptivity is:

   `a_\lambda = 1 - t_\lambda = 1 - \exp(-\tau)`

   and from Kirchoff’s law:

   `e_\lambda = a_\lambda`

   so take the differential:

   `d e_\lambda = da_\lambda = \exp(-\tau) d\tau`

   but for a thin layer we are expanding about
   \(\tau=0,\ \exp(-\tau) = 1\) so

   `d e_\lambda \approx d\tau` or going to finite differences

   `\Delta e_\lambda \approx \Delta \tau`


#. Repeat the problem above, but for a layer with an optical depth of `\tau_\lambda=1`.
   How does that change :eq:`thin` ?

   **Answer:**

   Now the relationship has to be:

   `\Delta e_\lambda \approx \exp(-\tau) \Delta \tau`

   which makes sense because we are adding a thin layer `\Delta \tau` onto
   an existing layer of thickness `\tau`, so the amount of light reaching
   the thin layer is going to be reduced by the transmittance `\exp( -\tau )`

#. Suppose you put ozone molecules in a 1 km long tunnel and measure an optical thickness of
   0.5 using an ultraviolet laser.  You know that the ozone mixing ratio is 1 g/kg and the air
   density is 1 kg/`m^3`.  What is the extinction coefficient `k` in `m^2/kg`?

   **Answer:**
   
   .. math::

      \kappa_\lambda = \frac{\tau}{\rho_{air} r_{mix} \Delta z}

   Plugging in the numbers gives `k_\lambda = 0.5\ m^2/kg`

#. Find the narrow beam transmission, absorption and emission for a series of
   stacked layers of equal transmissivities and temperatures in a direction perpendicular to the layers:

   **Answer:**

   Consider 3 layers each with direct beam transmissivity
   `\hat{t} = \frac{E}{E_0} = \frac{L \Delta \omega}{L_0 \Delta \omega} = \frac{L}{L_0}`.
   The outgoing radiance from one layer is the
   incoming radiance from the next layer, so that

   .. math::

       L_3 = \hat{t} L_2 \\
       L_2 = \hat{t} L_1 \\
       L_1 = \hat{t} L_0


   and substituting in turn:

 
   .. math::
       
      L_3 = \hat{t}^3 L_0

   The amount absorbed is
     
   `(L_0 - L_3) = (1 - \hat{t^3}) L_0` so the absorptivity is
   `(1 - \hat{t}^3)` which by Kirchoff’s law is the emissivity. The
   emission is therefore:

   .. math::
      
    L = \left ( 1 - \hat{t}^3 \right ) \frac{\sigma}{\pi} T^4

   and the transmitted radiance is `\hat{t}^3 L_0`

   Note that this only works if all layers are the same temperature.  (Why?)

   **Answer:**

   We are solving the emission part of the Schwartzchild equation:

   .. math::
      
      L_{emitted} = \int B(T) d\hat{t}

   If `B(T)` is constant it can come out of the integral and we have:

   .. math::

      \begin{aligned}
      L_{emitted} &= B(T) \left . \hat{t} \right |_{t_{tot}}^1 \\
                  &= B(T)(1 - t_{tot})=B(T)(1 - \hat{t}^3)
      \end{aligned}

   which is the answer we got.  If B(T) changed with the layer, then we'd
   need that information in the integration to get the emitted radiance.


   Note also that this only works if the beam is going straight through the layers
   (i.e. not a slant path)  (Why? How would this change for a slant path?)

   **Answer:**

   For the slant path we would need to replace the vertical optical thickness:

   .. math::

      d \tau =  \kappa_\lambda \rho_g dz

   with the slant path optical thickness `\tau_s`:

   
   .. math::

      d \tau_s =  \kappa_\lambda \rho_g ds = \kappa_\lambda \rho_g dz/\cos \theta
      = \kappa_\lambda \rho_g dz/\mu

   Once we made that change, everything would work as before, just with a
   smaller transmittance due to the longer slant path for `\mu < 1`.
   
Solid angle and radiance
------------------------

From :ref:`radiance` reading:


#. Calculate the solid angle subtended by a cone with an angular width of
   `\Delta \theta` =20 degrees.

   **Answer**
   
   .. math::
      :label: solid
         
       \omega &= \int_0^{2\pi} \int_0^{10} \sin \theta d\theta d\phi = -2\pi (\cos(10) - \cos(0)) \\
        &= 2\pi (1 - \cos(10)) = 2\pi(1 - 0.985) = 0.0954\ sr


#. A laser pointer subtends the same solid angle as the sun: `7 \times 10^{-5}` sr.  You shine it at a wall that is 10 meters away.  What is the radius of the circular dot?

   **Answer:**

   .. math::

      \begin{aligned}
         r=10\ m \\
         A/r^2= 7 \times 10{-5}\ sr \\
         A=7 \times 10^{-3}\ m^2 = \pi R^2\\
         R=(.007/(\pi))^{0.5} \approx 5\ cm
      \end{aligned}

#.  What is the angle of the cone if `\omega = 7. \times 10^{-5}\ sr`?

    **Answer:**

    R= 0.05 m at 10 m, `\theta = \tan^{-1}(0.05/10) \approx 0.005` radians or about 0.3 degrees

#. A satellite orbits 800 km above the earth and has a telescope with a field of view
   that covers 1 `km^2` directly below (i.e. at nadir).  If that 1 `km^2` is ocean with
   an emissivity `e=1` at a temperature
   of 280 K, calculate the flux in `W\,m^2` reaching the satellite from all wavelengths
   from that pixel.


   .. math::

      \Delta \omega \approx \frac{A}{R^2} = \frac{1}{800^2} = 1.562 \times 10^{-6}\ sr

   For small angles we can take `L` out of the flux integral and approximate `cos \theta \approx 1`:

   .. math::

      E = \int \cos \theta L(\theta, \phi) d\omega \approx L \Delta \omega
      
      L = \frac{\sigma}{\pi} T^4 = 111\ W/m^2/sr

      E = L \Delta \omega = 111 \times 1.562 \times 10^{-6} = 0.17\ milliWatts/m^2
      
Flux from radiance
------------------

From :ref:`flux_from_radiance`:
   

#. Calculate the flux arriving at a sensor assuming a constant radiance and a field of view
   that is a cone with an angular width of `\Delta \theta` =20 degrees.

   **Answer:**

   This is the same geometry as :eq:`solid`, but now we need to include `\mu=\cos \theta` in the
   integral.  The half-angle is 10 degrees or 0.174 radians

   .. math::

      \begin{align}
      E &= L \int_0^{2\pi} \int \,cos \theta \, sin \theta \, d \theta \, d \phi \\
      &= 2 \pi L \int_{\cos(0.174)}^1 \mu d \mu = 2 \pi  L \times \left . \frac{\mu^2}{2} \right |_{\cos(0.174)}^1 \\
      &= 2 \pi L (0.5 - 0.485) = 0.09 L\ W/m^2
      \end{align}

   i.e., for this big a solid angle, taking account of the variation in `cos \theta`
   does make the difference between 0.0954L (for :eq:`solid`) and 0.09L (for this
   calculation).
      
#. Prove that for an infinite flat surface the emitted radiance and flux are related by:

   .. math::

      E_\lambda = \pi L_\lambda

   **Answer**:


   See the section at the end of the :ref:`flux_from_radiance` notes.
      
#. Suppose that a satellite's orbit changes from a height of 800 km to a height of 600 km
   above the surface.  If the telescope field of view stays the same, prove that
   the radiance stays constant.
   

   **Answer**:

   Suppose that at a height of 800 km the satellite sees a circular area of 1 `km^2` in a single
   pixel.  If the surface is emitting a flux of `E_{fsc}\ W/m^2` then the those photons will
   be emitted into a hemisphere of radius `h=800\ km`, and the flux at the satellite
   will be power/area = `E_{sfc} \times 1\ km^2\ Watts/(2 \pi h^2\ meters^2)`.  
   
   Note that the flux
   will increase the altitude `h` decreases, because of the `1/h^2` factor.

   Now suppose the satellite descends to h=600 km. Again, if the power emitted by the surface stayed the same, 
   then the flux reaching the satellite would
   increase by a factor `(800/600)^2` because the same Watts are being distributed over a smaller
   hemisphere.  The power emitted by the surface is reduced however, because the pixel is smaller.  
   The pixel radius before was `R=800 \tan(\theta)\ km`, where `\theta` is the half-angle of the cone
   field of view of the telescope.  At 600 km altitude, `R=600\,\tan(\theta)`, and since the pixel
   area is `\pi R^2= \pi h^2 (\tan\theta)^2` and `E_{sfc}` hasn't changed, the emitted power is lower by `(600/800)^2`, exactly
   counteracting the inverse squared increase in the flux due to bringing the satellite closer to the surface.  Since the flux at the
   satellite is the same, and the field of view is the same, the radiance hasn't changed.
   

Schwartzchild equation
----------------------

From Stull p. 224 and the :ref:`schwartz` reading:

#.  Show that `e_\lambda` = `a_\lambda` for a gas that absorbs and transmits but doesn't reflect.
    (hint:  put the gas between two black plates, assume that the gas and the plates are at the
    same temperature and show that the 2nd law is violated if `e_\lambda \neq a_\lambda`


    Suppose the gas has absorptivity a and emissivity ε and they are new equal to each other.
    The it will be transmitting `(1 - a)\sigma T^4` from the right wall to the left wall,
    and emitting `\epsilon \sigma T^4` to the left wall, while the (black) left wall will
    be emitting `\sigma T^4`.  The temperature of the wall will change because the balance
    will be:

    .. math::

       \begin{aligned}
       \sigma T^4 &= \epsilon \sigma T^4 + (1 - a) \sigma T^4 \\
       & \text{so:}\\
       1 &= 1 + (\epsilon - a)
       \end{aligned}

    i.e. the flux at the wall will be unbalanced, and the temperature
    will change in violation of the 2nd law, unless ε=a for the gas.
   
#. Integrate the Schwartzchild equation
   
   .. math::

      \begin{gathered}
          \label{eq:sch1}
           dL_{\lambda,absorption} + dL_{\lambda,emission}  = -L_\lambda\, d\tau_\lambda + B_\lambda (T_{layer})\, d\tau_\lambda
        \end{gathered}

   across a constant temperature layer of thickness `\Delta \tau_\lambda` over a surface
   emitting radiance `L_{\lambda 0}`
   and show that the radiance at the top of a constant temperature layer is given by:        

   .. math::

      \begin{gathered}
      L_\lambda = L_{\lambda 0} \exp( -\Delta \tau_\lambda  ) + B_\lambda (1- \exp( -\Delta \tau_\lambda))\end{gathered}

   **Answer:**

   See the section "Adding emission to Beers law" in the :ref:`schwartz` notes.
