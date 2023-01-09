.. _heating-rate:

Finding the heating rate of the atmosphere
++++++++++++++++++++++++++++++++++++++++++

Review
======

Now that we have  the diffusivity approximation from :ref:`assign6a`, we can solve the Schwartzchild equation for fluxes.  First remember what it looks like for radiance:

.. math::
   :label: main

      L_\lambda(\tau_T)= B_\lambda(T_{skin}) \exp(-\tau_T) +    \int_0^{\tau_T} B_\lambda(T)\, d\hat{t}

where :math:`\exp(-\tau_T)` is the total transmissivity of an atmosphere with optical thickness :math:`\tau_T` and :math:`\hat{t}` is the transmissivity of the atmosphere from the top of the atmosphere (where the optical depth=0, to a height at which the optical depth= :math:`\tau`.

Here's the picture:

.. figure::  figures/schwartzchild.png
   :scale: 40
   :name: schwartzchild_rep


If :math:`T` is constant with height then integrating :eq:`main` is simple:


.. math::
   :label: main2

     \begin{aligned}
         L_\lambda(\tau_T) &= B_\lambda(T_{skin}) \exp(-\tau_T) +    B_\lambda(T) \int_0^{\tau_T} \, d\hat{t}\\
           &= B_\lambda(T_{skin}) \exp(-\tau_T) +    B_\lambda(T)(\hat{t}(\tau_T) - \hat{t}(0) ) \\
           &= B_\lambda(T_{skin}) \exp(-\tau_T) +    B_\lambda(T)(1 - \exp(-\tau_T) )
     \end{aligned}

For fluxes, we have a new flux transmission, `\hat{t}_f` = `\exp(-1.666 \tau)`  So using that:


.. math::
   :label: main3

     \begin{aligned}
         E_\lambda(\tau_T) &= E_{bb \lambda}(T_{skin}) \exp(-1.66 \tau_T) +    E_\lambda(T) \int_0^{\tau_T} \, d\hat{t}\\
           &= E_\lambda(T_{skin}) \exp(-1.66 \tau_T) +    E_\lambda(T)(\hat{t}_f(\tau_T) - \hat{t}(0) ) \\
           &= E_\lambda(T_{skin}) \exp(-1.666 \tau_T) +    E_\lambda(T)(1 - \exp(-1.666\tau_T) )
     \end{aligned}



Net flux
========

If we want to know whether the atmosphere is heating or cooling at a particular place, however, we need
to convert the monochromatic radiance :math:`L_\lambda` into the corresponding broadband flux :math:`E` by:

1) Integrating :math:`\cos \theta L_\lambda d\omega` over a hemisphere to get the monochromatic flux :math:`E_\lambda`
   as in :ref:`moving` equation (1):

   .. math::
     :label: fluxrel

     \begin{aligned}
     E_{\lambda \uparrow} &= \int dE_\lambda = \int_0^{2\pi} \int_0^{\pi/2} \cos \theta \, L_\lambda \, d \omega =\int_0^{2\pi} \int_0^{\pi/2} L_\lambda \cos \theta  \sin \theta \, d\theta \ \, d \phi  \\
     &= \int_0^{2\pi} \int_0^1 L_\lambda  \mu d \mu\ \, d \phi
     \end{aligned}

   where the arrow :math:`\uparrow` reminds us we have integrated over all upward pointing radiances

2) Integrating :math:`E_\lambda` over all wavelengths to get :math:`E`.   If we can do that, then we can get
   an energy budget for a layer that looks like this:

   .. figure:: figures/layer_budget.png
      :scale: 110


To get the heating rate in :math:`W\,m^{-2}` for the layer above, use the following convention:

1) Downward fluxes are positive (heating), upward fluxes are negative (cooling)

2) The net flux :math:`E_n = E_\uparrow + E_\downarrow`

3) The heating rate is then defined as:

   .. math::

      \Delta E_n = E_{nTop} - E_{nBot} = (60 - 20) - (80 - 25) = 40 - 55 = -15\ W\,m^{-2}

In other words, the layer is cooling at a rate of -15 :math:`W\,m^{-2}`, because more energy is
exiting from top of the layer than is entering from below.

Temperature change
==================

To turn the radiative heating rate into a rate of temperature change, we need to use the first law of thermodynamics
(see Stull equation 3.4a):

.. math::

    \frac{dH}{dt} = \Delta E_n

where :math:`H` (units: :math:`Joules/m^2`)  is called the *enthalpy* (note that the units work out to :math:`W/m^2`).  The enthalpy of
a 1 :math:`m^2` column of thickness :math:`\Delta z` is related to the temperature T via the **heat capacity at constant pressure** :math:`c_p`
(units: :math:`J\,kg^{-1}\,K^{-1}`  and the density :math:`\rho` (:math:`kg\,m^{-3}`):

.. math::

   H=\rho\, c_p\, \Delta z\, T

We define the **specific enthalpy** *h* as the enthalpy/unit mass = :math:`h=H/(\rho \Delta z)` where we are implicitly assuming that
our column is 1 :math:`m^2`

Putting these two equations together gives the heating rate, :math:`Q_r` (units: K/second):

.. math::

   \begin{aligned}

   \rho c_p \Delta z \frac{dT}{dt} &= \Delta E_n\\

   Q_r = \frac{dT}{dt} &= \frac{1}{\rho c_p} \frac{\Delta E_n}{\Delta z} = \frac{1}{\rho c_p} \frac{dE_n}{dz}
   \end{aligned}
