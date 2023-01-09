.. _beers_law_answers:

Beers and inverse squared laws
++++++++++++++++++++++++++++++

Comments/derivations for the material in  Stull p. 38-39

.. _differences_answers:

Differences, differentials and derivatives
==========================================

1) What is a derivative?

-  According to
   `wikipedia <https://en.wikipedia.org/wiki/Derivative>`__, a
   derivative is defined as:

   The derivative of a function of a real variable measures the
   sensitivity to change of a quantity (a function value or dependent
   variable) which is determined by another quantity (the independent
   variable).

2) What is the derivative of :math:`E = \sigma T^4` with respect to T?

.. math:: \frac{dE}{dT} = \frac{d \sigma T^4}{dT} = 4 \sigma T^3 

Does that mean that you are free to treat dE/dT as a fraction, and
cancel dT in the denominator to write:

.. math:: dE = \frac{d \sigma T^4}{dT} dT = 4 \sigma T^3 dT

Scientists (and mathematicians) do this all the time, but that isn't how
derivatives work -- dE/dT is a function, not a fraction. So what is
really going on?

3) Instead, we need to treat the differentials dE and dT as limits, not
   numbers. We know that the following is true: given a small
   temperature difference :math:`\Delta T` the flux difference
   :math:`\Delta E` is aproximately:

.. math::  \Delta E \approx  \frac{dE}{dT} \Delta T =  4 \sigma T^3 \Delta T 

i.e. -- change in x times slope = change in y.

This equation in words is called a "first order Taylor series expansion"
of the function :math:`E = \sigma T^4`. It is not exact, but it gets
better as :math:`\Delta T` gets smaller. We can make it exact by writing
out the whole Taylor series expansion which is a power series with an
infinite number of terms. (See the Wikipedia entry
`here <https://en.wikipedia.org/wiki/Taylor_series>`__)

4) What is a differential?

Roughly, the differentials dE and dT represent limits that are evaluated
by integration:

:math:`dT = \lim{\  \Delta T \to 0}`, so that
:math:`\int dT = T` and

.. math::  dE = \lim_{ \Delta T \to 0} \Delta E

So if we take the :math:`\lim{\  \Delta T \to 0}` we can write

.. math:: dE = \frac{d \sigma T^4}{dT} dT = 4 \sigma T^3 dT

Note that this is just doing the steps in Stull p. 38 in the opposite
order. He starts with my last equation and winds up with 3). The
advantage of the alternative approach we're using here is that we don't
need to treat the function :math:`\frac{dE}{dT}` as if it can be ripped
apart to get :math:`dE` and :math:`dT`. If you really care, I recommend
reading `this
answer <http://math.stackexchange.com/questions/23902/what-is-the-practical-difference-between-a-differential-and-a-derivative>`__
to a question about differentials. This is also closely related to the
`chain rule <https://en.wikipedia.org/wiki/Chain_rule>`__ for
derivatives of functions.

By taking the limit as :math:`\Delta T` approaches 0 we've turned a
*difference equation* for the number :math:`\Delta E` (which we can
solve in python) into a *differential equation* for the differential
:math:`dE` (which we can integrate using calculus).

Beers law -- using differentials
================================

Both physics (Maxwell's equations) and observations show that when a
narrow beam of photons are travelling through a material (like air or
water) of constant composition, the flux obeys "Beer's law":

.. math::  E(s) = E_i \exp (-n b s) 

where :math:`s\ (m)` is the distance travelled (the path length),
:math:`n\ (\#/m^3)` is the number denstiy of reflecting/absorbing
particles and :math:`b\ (m^2)` is the extinction cross section due to
both absorption and scattering. You can think of :math:`b` as the
*target size* of the particles (molecules, smoke particles etc.) which
may be much different than the physical size of the particle because of
quantum mechanical and wave interference effects.

To get the differential version of Beers law, take the derivitive and
use the limit argument we went through above and get:

.. math:: dE = E_i (-nb) \exp(-nbs) ds =  (-nb) E ds

or

.. math:: \frac{dE}{E} = -n b ds

If we define the differential optical depth as:

.. math:: d\tau = n b ds

.. raw:: html
         
     <a name="diffbeers"></a>
          
Then we ge:


.. math:: \frac{dE^\prime}{E^\prime} = d \ln E^\prime = -d \tau^\prime
  :label: diffbeers_answer
          
and integrating from :math:`\tau^\prime=0,\ E^\prime=E_i` to
:math:`\tau^\prime = \tau,E^\prime = E` gives:

.. math:: \int_{E_i}^E  d \ln E^\prime = -\int_0^\tau d\tau^\prime

.. math:: \ln \left ( \frac{E}{E_i} \right ) = - \tau

.. math:: E = E_i \exp (-\tau) 

          
which is stull 2.31c. An important point is that the extinction cross
section :math:`b` can vary enormously over small wavlength ranges
(called "absorption bands") where the cross section can increase by a
factor of 100,000. This is why small concentrations of carbon dioxide
have such large impacts on climate.

Also note that now that we have the differential form of Beer's law, we
don't have to assume that :math:`n` or :math:`b` are constant, we can
make them depend on position and just do the (more complicated) integral
to get :math:`\tau`

.. _inverse_answers:

Inverse Square Law: In-class problem in energy conservation
===========================================================

On page 39, Stull asserts the inverse square law:

.. math:: E_2 = E_1^* \left ( \frac{R_1^2}{R_2^2} \right ) 

1) Prove this using conservation of energy (i.e. conservation of Joules)
n
**Answer: The power emitted from surface with radius** :math:`R_1` is:

.. math:: P_1 = 4 \pi R_1^2 E_1^*\ Watts

That power is conserved and spreads out over a sphere of radius
:math:`R_2`, so that:

.. math:: E_2 = \frac{P_1}{4 \pi R_2^2} = \frac{4 \pi R_1^2 E_1^*}{4 \pi R_2^2} =  E_1^* \left ( \frac{R_1^2}{R_2^2} \right ) 

2) Suppose a 10 cm x 10 cm piece of white paper with a visible
   reflectivity of 80% is pinned to a wall and illuminated by visible
   light with a flux of 100 :math:`W\,m^{-2}`. If the paper reflects
   evenly in all directions (isotropic, not glossy), what is the flux
   from the paper 3 meters from the wall? What about 6 meters from the
   wall?

**Answer: if the photons spread out over a hemisphere, then 3 meters
from the wall the Watts will be spread over a hemisphere of area:**

:math:`2\pi 3^2\ m^2`.

The total watts: :math:`100 \times 0.1 \times 0.1 \times0.8=0.8\ W`

Flux at 3 meters:

.. math:: F =\frac{0.8}{2 \pi 9}=0.014\ W\,m^{-2}

.. code:: python

    0.8/(2.*np.pi*9)




.. parsed-literal::

    0.01414710605261292



**Answer**: At 6 meters the flux will be lower by a factor of 4 because
of inverse square.

(Try this experiment in the classroom. Is the paper visibly dimmer at
   6 meters than 3 meters? Why or why not?)

**Answer: The brightness looks the same, because the "pixel" seen by
your eye gets bigger as the distance between the wall and your eye
increase. This extra area provides exactly enough extra photons to
compensate for the larger hemisphere.**


3) Stull defines the direct beam transmissivity as:

.. math:: t = \frac{E}{E_{i}} = \exp(-\tau)

Suppose I have two pieces of translucent glass that absorb but don't
reflect light, and their indvidual transmissivities are :math:`t_1` and
:math:`t_2`. Use conservation of energy to prove that if we stack the
two pieces, the combined transmissivity will be :math:`t_1 \times t_2`,
which means that the combined optical depth will be
:math:`\tau_1 + \tau_2` (i.e. optical depths add). Note that I had to
assume no reflection so that photons wouldn't bounce back and forth
between the two plates.

**Answer**: let :math:`E_a` be be the flux exiting from plate 1, and
:math:`E_b` be the flux exiting from plate 2. Since the energy decrease
only because of absorption by the plates, we know that what exits plate
1 must enter plate 2:

.. math:: E_a = E_{in}\exp ( -\tau_1)

.. math::

   E_b = E_a \exp (-\tau_2) = E_{in} \exp( -\tau_1) \exp(-\tau_2) = E_{in} t_1 t_2 =
     E_{in} \exp(- (\tau_1 + \tau_2 ))

2) Find an expression for :math:`\Delta E_2^*` in terms of
   :math:`\Delta R_2`.

   **Answer:**

   .. math::

     \Delta E^*_2 =  \frac{d}{dR_2} \left ( E_1^* \left ( \frac{R_1^2}{R_2^2} \right ) \right ) \Delta R_2=  \frac{d}{dR_2} \left ( E_1^* R_1^2\,{R_2^{-2}} \right ) \Delta R_2= -2 E_1^* R_1^2\,R_2^{-3} \Delta R_2

   Divide both sides by :math:`E_2`

   .. math:: \frac{\Delta E_2}{E_2} = -2 \frac{\Delta R_2}{R_2}


             
