.. default-role:: math
   
.. _week2_flux_from_radiance:

Finding the flux given the radiance
###################################


Law of the cosine
*****************

Unless the sun is directly overhead, the flux  `E` on a level
surface is going to be less than the flux perpendicular to the
solar beam. The figure below shows the geometry:


.. figure:: ../figures/shadow.png
   :scale: 35
   :name: shadow

   `\cos \theta` effect           

Assuming that the y dimension (into and out of the screen) has unit
length, then if flux `E_1` `(W\,m^{-2})` is incident
on surface 1, power flowing through surface 1 is:

`P_1 = E_1 \times A_1` Watts

If we assume a direct beam of sunlight (so no inverse-square spreading),
then all of that power passes through surface 2, and so the flux
perpendicular to surface 2 is:

**Law of the cosine**

`E_2 = P_1/A_2 = P_1/(A_1 /cos \theta) = E_1 \cos \theta`

This is the main reason why it's cooler at sunset than at noon. It is
also the reason your shadow can be taller or smaller than you.

.. _moving:

Moving between flux and radiance
********************************

We saw in the :ref:`radiance` reading
that the
radiance and flux are related by:

.. math:: dE = L d\omega

.. math:: L = \frac{dE}{d\omega} \approx \frac{\Delta E}{\Delta \omega}

A good way to think about this to ask yourself how a satellite would
measure the radiance L in some direction. It would need to:

1) measure the power P reaching its sensor that has area A

2) Calculate the flux E= P/A

3) Divide that flux by the wavelength range of its filter (say
   `\Delta \lambda = 1\ \mu m`) to get the monochromatic
   flux:

.. math:: E_\lambda = \frac{E}{\Delta \lambda}

4) Divide the monochromatic radiance by the field of view of the
   telescope `\Delta \omega` to get the monochromatic radiance:

.. math:: L_\lambda = \frac{E_\lambda}{\Delta \omega}

The setup for this is shown in the following figure:

.. figure:: ../figures/L_E.png
   :scale: 50
   :name: L_E

   Relationship between L and E       

So how would you calculate the flux E crossing through the bottom
of this triangle if you knew the radiance L at every angle? Now you need
to use the law of the cosines to move from the perpendicular surface
with area `dA_1` to the surface you are interested in with larger
area `dA_2 = dA_1/\cos \theta`:


.. math::
   :label: cosflux

     dE_2 = \cos \theta dE_1 = \cos \theta L d\omega

To get the flux from every angle requires that you integrate over
a hemisphere. That means you need to integrate over all azimuths, so
`\phi = 0 \to 2\pi` and over 90 degrees of zenith, so that
`\theta = 0 \to \pi/2`
      
.. math::
   :label: fluxrel
   
     E_2 = \int dE_2 = \int_0^{2\pi} \int_0^{\pi/2} \cos \theta \, L \, d \omega =\int_0^{2\pi} \int_0^{\pi/2} L \cos \theta  \sin \theta \, d\theta \, d \phi 

.. _final_form:     
     
Final form: `E = \pi L`
***********************

The most common case for us is thermal emission, which is characterized
by photons coming isotropically from all directions. In that case the
surface emitted radiance `L^*` is independent of
`(\phi, \theta)` and can be taken outside of the integral. With
that simplification, we're down to trigonometric integrals from first
year:

.. math::
   :label: flux_final

    E_2 = E^* = \int_0^{2\pi}\int_0^{\pi/2} L^* \cos \theta  \sin \theta \, d\theta \, d \phi = 2 \pi L^*
         \int_0^{\pi/2} \cos \theta  \sin \theta\, d\theta = 2\pi L^* \left( \frac{1}{2} \right)  = \pi L^*

where we've continued to use an asterisk to denote that this is the
radiation coming from a black surface, immediately next to the surface.

More generally if we know `L` anywhere in space and know that it
is independent of direction, the the irriadiance at that point is going
to be:

.. math:: E = \pi L

**Question** What happened to the inverse square law for flux E?

