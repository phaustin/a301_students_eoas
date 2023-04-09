.. _week9:radar:

Notes on the radar equation
+++++++++++++++++++++++++++

Stull Chapter 8 page 246 has an excellent discussion of the **radar equation**,
which relates the power :math:`P_r` returning to the receiving antenna to radar and atmospheric variables

.. math::

   P_r = \underbrace{\frac{c \pi^3}{1025 \ln(2)}}_{\text{Gaussian beam factor + constants}} \times
          \overbrace{\frac{P_t G^2 (\Delta \beta)^2 \Delta t}{\lambda^2}}^{\text{radar characteristics}} \times
          \underbrace{\left ( \frac{|K|}{L_a R} \right )^2 Z}_{\text{atmospheric target characteristics}}


where

* :math:`P_t` = transmitter power
* G = gain of the transmitting antenna
* :math:`\Delta \beta` = beam width in radians
* :math:`\Delta t` = radar pulse with in seconds
* :math:`\lambda` = radar wavelength
* :math:`K` = complex index of refraction for water/ice
* R=distance to target
* :math:`L_a` = attenuation factor :math:`\geq` 1
* Z= :math:`\int D^6 n(D) dD` where D is the drop diameter and n(D) is the drop size distribution

As Stull points out, if you divide and multiply this equation by :math:`Z_1= 1\ mm^6\,m^{-3}` the equation becomes:

.. math::

   \frac{P_r}{P_t}=\underbrace{\frac{\pi^3 G^2 (\Delta \beta)^2}{1024 \ln(2)}}_{b=10^{4.55}\ for\ Nexrad} \times
          \overbrace{Z_1 c  \Delta t/\lambda^2}^{R_1^2 = (2.17 \times 10^{-10}\ km)^2\ for\ Nexrad} \times
          \underbrace{\left ( \frac{|K|}{L_a R} \right )^2 \frac{Z}{Z_1}}_{\text{atmospheric target characteristics}}

and taking :math:`10 \log_{10}` of both sides:

.. math::

  10 \log_{10} \left ( \frac{P_r}{P_t} \right ) = 10 \log_{10}(b) + 20 \log_{10} (R_1) + 20 \log_{10} \left | \frac{K}{L_a} \right |
          - 20 \log_{10} (R) + 10 \log_{10} \frac{Z}{Z_1}

Rearranging:

.. math::

   10 \log_{10} \frac{Z}{Z_1} =  10 \log_{10} \left ( \frac{P_r}{P_t} \right ) - 10 \log_{10}(b)  - 20 \log_{10} \left | \frac{K}{L_a} \right |
         +  20 \log_{10} \left ( \frac{R}{R_1} \right )

where all the terms are now unitless.

Questions/Comments
==================


1) Why does the returned power decrease as :math:`1/R^2` and not the roundtrip spreading of :math:`1/R^4` ?

2) We have "hardwired" in a wavelength of 10 cm, a beam width of 0.95 deg, etc. which is specific to the WSR-88D radar.  We
   are also assuming that we are using the same antenna to receive and to transmit

3) Transmitted power is 750,000 Watts, Received power can be as low as :math:`10^{-15}` Watts

4) Suppose you are given :math:`Z_1` in :math:`mm^6\,m^{-3}`, c in m/s, :math:`\Delta t` in s and :math:`\lambda` in cm.  How do you convert
   :math:`Z_1 c  \Delta t/\lambda^2` to :math:`km^2`?

5) The reflectivity goes down as b and K increase and goes up as :math:`L_a` and R increase -- explain.

6) Why is the width of the radar sample volume proportional to :math:`\Delta t/2` instead of :math:`\Delta t` ?
