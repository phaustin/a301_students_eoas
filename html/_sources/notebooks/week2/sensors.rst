.. default-role:: math

.. _radiance:

Solid angle and radiance
########################

Some definitions
================

The *irradiance* or *radiant flux* **E** is defined as the energy
(Joules) crossing a unit surface (1 :math:`m^2`) in unit time (1 second)
so it has units of :math:`W\,m^{-2}`.

To measure it, you could use a photo diode to count the number of
photons per second hitting a sensor, recording the wavelength of each
photon. To get the photon energy use Stull eq. 2.12

.. math:: \nu = c/\lambda

where `\nu` is the frequency and c is the speed of light, and then use
Planck's constant (h) to convert frequency in Hz (:math:`s^{-1}`) to
energy in Joules

.. math:: energy = h \nu

where :math:`h=6.62607 \times 10^{-34}` :math:`J\,s`. Summing all
the photon energies and dividing by the sensor area would give you the
flux E.

Monochromatic Radiance vs. total flux
===========================================

In the real world, instruments only measure photons that arrive within a limited
field of view (i.e. the field of view of the telescope). The sensor also samples a limited 
range of wavelengths, both because the photo diode doesn't respond
equally to all wavelengths and because we are interested in particular
wavelength ranges.  The figure below shows the field of view for a typical
airborne scanning radiometer:


.. figure:: ../figures/c5_1.png
   :name: whisk

   Whiskbroom scanner

The photons reaching the sensor through the telescope are separated into
particular wavelength regions using a filter wheel or a beam splitter:

.. figure:: ../figures/c5_5.png
   :name: filters

   Waveband filters
      


Monochromatic flux
========================

Handling the fact that we are only receiving photons in a specific
wavelength range :math:`\Delta \lambda` is straight forward: we just
divide the measured flux by the wavelength range to get
:math:`E_\lambda`, the monochromatic flux:

.. math:: E_\lambda\ (W\,m^{-2}\,\mu m^{-1}) = \frac{ \Delta E}{\Delta \lambda}

and if I take :math:`\lim{\Delta \lambda \to 0}`

.. math::  dE = E_\lambda d \lambda 

so we can define :math:`\Delta E` as the portion of the flux that
is being transmitted by photons with wavelengths between
:math:`\lambda \to \lambda + \Delta \lambda`

Field of view
=============

**Planar angle**

Dealing with the fact that the telescope only sees photons coming from a
specific set of angles means that we need a way to define those angles.
In one dimension, we define an angle using radians:

.. math:: \phi = \frac{l}{r}

where :math:`l` is the arclength along a circle of radius :math:`r` that
defines the angle.

In the case that :math:`l`\ =\ :math:`r` the angle is 1 radian:

.. figure:: ../figures/Radian.png
   :name: radian

   Definition of planar angle


The differential version of this is:

.. math:: d\phi = \frac{dl}{r}

**solid angle**

A pixel has two dimensions, which makes things more complicated.
Consider the following spherical coordinate system:

.. figure:: ../figures/spherical.png
   :name: spherical

   Spherical coordinates          


:math:`\theta` is called the "zenith angle", and :math:`\phi` is called
the "azimuth angle". Image our sensor is looking up in the direction
given by :math:`\Omega`

Suppose the telescope has a field of view that's defined by a small
angle :math:`d\phi` in the azimuthal direction and :math:`d\theta` in
the zenith direction (these two angles would be equal if the field of
view was a circular cone). A distance :math:`r` away from the telescope,
the arclength in the zenith direction is :math:`r d\theta` by the
definition of the planar angle. For the azimuth direction though, the
planar angle is defined by the radius :math:`r \sin \theta`, which gives
the distance from the vertical axis to the surface of the sphere of
radius :math:`r`. That means that the area seen by the telescope at
radius r is:

.. math:: dA = width \times height = r \sin \theta d\phi \times r d\theta = r^2  \sin \theta d\theta d \phi


.. figure:: ../figures/solid_angle.png
   :name: solid_angle        

   Definition of solid angle       


Now that we know :math:`dA` we can define the solid angle
:math:`d\omega` (steradians) by analogy with the planar angle:

Planar angle:

.. math:: d\phi = \frac{dl}{r}

measured in radians

Solid angle:

.. math::
    :label: domegaA
           
    d\omega = \frac{dA}{r^2} = \frac{r^2 \sin \theta d\theta  d\phi}{r^2} = \sin \theta d\theta  d\phi

measured in steradians

Monochromatic radiance
======================

So if we know the monochromatic flux, and we know the
field of view :math:`\Delta \omega` of the telescope, then we can get
the monochromatic radiance :math:`L_\lambda` by:

.. math::
   :label: Llambda

   L_\lambda = \frac{\Delta E_\lambda}{\Delta \lambda \Delta \omega}

units: :math:`W\,m^{-2}\,\mu m^{-1}\,sr^{-1}`.

The monochromatic radiance :math:`L_\lambda` is the variable that the
Modis thermal sensors deliver.

Switching to differentials again, we've got:

.. math::
   :label: dE

   dE = L_\lambda d\lambda d\omega

Note that both :math:`dE` and :math:`L_\lambda` have a direction
associated with them -- their direction of propagation, which is
perpendicular to the surface the photons are passing through.

Note that :eq:`dE` assumes that all the energy is contained in the small solid
angle `d \omega`, which is true for satellites because they are using
a telescope to focus on a small pixel.  If we want to instead measure all the energy
crossing a surface from all directions, we need to integrate over all zenith and azimuth angles.




