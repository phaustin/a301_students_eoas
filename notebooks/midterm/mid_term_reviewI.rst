.. default-role:: math

.. _mid_review1:

Sample mid-term questions I
===========================

Beers law
---------

Stull page 2.43 and the :ref:`week2_beerslaw` reading:

#. Prove that for a thin  non-reflecting layer the change in emissivity
   =  change in optical thickness, i.e. prove that:

   .. math::
      :label: thin
              
         \Delta e_\lambda \approx  \Delta \tau_\lambda

  


#. Repeat the problem above, but for a layer with an optical depth of `\tau_\lambda=1`.
   How does that change :eq:`thin` ?

  

#. Suppose you put ozone molecules in a 1 km long tunnel and measure an optical thickness of
   0.5 using an ultraviolet laser.  You know that the ozone mixing ratio is 1 g/kg and the air
   density is 1 kg/`m^3`.  What is the extinction coefficient `k` in `m^2/kg`?


#. Find the narrow beam transmission, absorption and emission for a series of
   stacked layers of equal transmissivities and temperatures in a direction perpendicular to the layers.

   
  
   
Solid angle and radiance
------------------------

From :ref:`radiance` reading:


#. Calculate the solid angle subtended by a cone with an angular width of
   `\Delta \theta` =20 degrees.

  


#. A laser pointer subtends the same solid angle as the sun: `7 \times 10^{-5}` sr.  You shine it at a wall that is 10 meters away.  What is the radius of the circular dot?


#.  What is the angle of the cone if `\omega = 7. \times 10^{-5}\ sr`?

    
#. A satellite orbits 800 km above the earth and has a telescope with a field of view
   that covers 1 `km^2` directly below (i.e. at nadir).  If that 1 `km^2` is ocean with
   an emissivity `e=1` at a temperature
   of 280 K, calculate the flux in `W\,m^2` reaching the satellite from all wavelengths
   from that pixel.
      
#. Suppose that a satellite's orbit changes from a height of 800 km to a height of 600 km
   above the surface.  If the telescope field of view stays the same, prove that
   the radiance stays constant.

      

Schwartzchild equation
----------------------

From Stull p. 224 and the :ref:`week4_schwartz` reading:

#.  Show that `e_\lambda` = `a_\lambda` for a gas that absorbs and transmits but doesn't reflect.
    (hint:  put the gas between two black plates, assume that the gas and the plates are at the
    same temperature and show that the 2nd law is violated if `e_\lambda \neq a_\lambda`


    
   
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

   **Hint:**

   See the section "Adding emission to Beers law" in the :ref:`week4_schwartz` notes.


From assignment 3a
------------------


4\. A satellite orbits 800 km above the earth and has a telescope with a field of view
   that covers 1 `km^2` directly below (i.e. at nadir).  If that 1 `km^2` is ocean with
   an emissivity $e=1$ at a temperature
   of 280 K, calculate the flux in $W\,m^2$ reaching the satellite from all wavelengths
   from that pixel.



5\. Suppose that a satellite's orbit changes from a height of 800 km to a height of 600 km
   above the surface.  If the telescope field of view stays the same, prove that
   the radiance stays constant.
