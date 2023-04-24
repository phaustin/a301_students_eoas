---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: -all
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(week12:final-guide)=
# Study guide for final exam -- 

## Format

- 2 hours in-class + 30 minute group with 1 question take home
- Take-home question: 3 day window, should take 1-2 hours
- Equation sheet provided (will post)

## Topic focus

1. Calculating radiative fluxes from atmospheric conditions:

   1. Find optical depth and transmisson profiles given a hydrostatic atmosphere with
      a specified scale height
   2. Calculate broadband (\$sigma T^4/pi\$) and monochromatic radiances and fluxes
   3. Calculate the flux observed by a satellite through an atmosphere of known properties
   4. Convert between radiance and brightness temperature
   5. Calculate heating/cooling rates given atmospheric fluxes
   6. Explain how weighting functions are used for temperature retrieval

2. Calcuate atmospheric/solar properties from radiation measurements

   1. Use Beer's law to estimate the solar flux as a function of optical depth
   2. Use brightness temperature differences and/or
      weighting functions/transmissions at multiple wavelengths to show how
      column water vapor amounts can be inferred from satellite data

3. Radar:

   1. Find the rain rate from a Z-R relationship
   2. Find Z from a cloud droplet size distribution
   3. Explain the terms in the radar equation

4. Derivations/equations

   1. Integrate the hydrostatic equation to find the pressure as a function of height
   2. Integrate the Schwartzchild equation with a constant temperature profile to find the
      radiance or the flux for a  layer
   3. Derive the heating rate equation
   4. Use change of variables to solve an integral
   5. Estimate the heating rate in a layer given fluxes

5. Definitions, paragraph answers/pseudo code

   - Trace a pixel from its photon count at the satellite to a physical property on a map (ndvi, temperature)  -- what's the workflow from data download to presentation at a meeting?  What routines do you need to call, and what do they do?
   - WGS94, UTM, Lambert azimuthal projection  -- definition, when to use and for what
   - Affine transform, crs, how are they used to zoom an image to a specific lon/lat box?
   - tradeoffs -- choices about pixel size, orbit altitude, etc. depending on the target and technology -- i.e. what a real sensor is capable of measuring.   I give you the sensor limitations (how many photons it needs per second to make a reliable observation), you give me a combination of target, orbit, pixel size that would be possible with that sensor.

5) Python programming

   - Be able to explain and use the following functions or a program that includes them (i.e. relate the code to equations and/or explain the programming logic).

     - imshow
     - pcolormesh
     - hist
     - np.sum, np.diff
     - pyresample
     - cartopy coordinate transforms
     - rasterio.windows.Window
     - cartopy mapping
     - pandas  (indexing and searching rows, using groupby)
     - finding and replacing values using logical indexing (i.e. chan1[hit]=np.nan)
     - loop comprehensions (i.e. newlist=[f(item) for item in list]
     - iterating over keys and values in a dictionary
     - finding files with Path().glob()
     - reading and writing netcdf and geotiff
     - histogram equalization using scikit image
     - creating false color composites
     - clipping an xarray dataset
     - changing the crs and affine transform for an image to a new projection and clipped size

+++

## Study questions

### Midterm questions

* the final is comprehensive so be sure you understand the midterm solutions

+++

### Heating rate

1) Derive the heating rate equation 

see [the heating rate notes](https://eoasubc.xyz/a301_2022/notebooks/week11/heating_rate.html#temperature-change)

2) A 150 m thick nocturnal cloud layer with a temperature of 275 K floats
over a 300 K surface.

Given: 

(i) mass absorption coefficient of the cloud liquid water
is $k=0.004\ $m^2/kg$

(ii) $\rho_{air}$ = 1 $kg/m^3$

(ii) downward longwave flux density from the
air above the cloud of $E_\downarrow(z_T)$=75 $W\,m^{-2}$. (where $z_T=150$ m is the height of 
cloud top above cloud base) 

(iii)  No atmospheric absorption

- Find the total vertical optical depth of the cloud


For constant density, this is 

$$\tau = \rho_{air} k \Delta z = 0.004*150 = 0.6$$


-  Write down expressions for the flux transmission $\hat{t}_f$
   between $z$ and $z_T$ and between 0 and $z$ as functions
   of $z,\,z_T,\,k$ assuming  $z$  is inside the cloud, i.e.~$0 < z < z_T$.
   
Since $t_{f} = \exp(-1.66 \tau)$, the transmission from 0 to z is $t_{f}(z) = \exp(-1.66 \rho\,k\,z)$ and the
transmission from z to $z_T$ is 

$$t_f(z) = \exp(-1.66 \rho\,k\,(z_T - z))$$

- Find the heating rate of the cloud $dT/dt$ in K/hour


The total transmission is 

$$t_{ftot} = \exp(-1.66*\tau_{ftot}) = \exp(-1.66*0.6)= 0.37$$

Upwelling flux passing through the top of the cloud is 

$$
E_\uparrow(z_{top}) = E_{sfc} t_{ftot} + E_{cld} (1 - t_{ftot})
$$

Downwelling flux passing through the bottom of the cloud is

$$
E_\downarrow(0) = E_{top} t_{ftot} + E_{cld} (1 - t_{ftot})
$$


To get the heating rate, we need use the equations from the heating rate notes with 

$$
E_{sfc} = \sigma 300^4
$$

and 

$$
E_{cld} = \sigma 275^4
$$

+++

### Radiance looking up  

(note that this would be a takehome problem, since it's too long for an exam)

```{figure} figures/two_layers_2016.png
:width: 30%
:name: two_layer

Two layer atmosphere at night
```

(Hint -- remember from the hydrostatic equation that $\Delta p = -\rho g \Delta z$ if $\rho$ is approximately constant.)

+++

* For the figure above, suppose you were looking upward from the surface with an infrared instrument at an angle of 30 degrees off vertical.  Assuming that
the mass absorption coefficient is $k = 0.001\ m^{2}/kg$ for longwave photons, the telescope measures all wavelengths of interest
and  the telescope's field of view is 0.01 sr find:

### The radiance observed by the telescope

+++

#### Radiance Answer

First find the slant transmissivity of each layer. 
For layer 1 the vertical optical depth is 

$$\tau_1 = \rho k \Delta z = \frac{-\Delta p_1}{g} k$$

with  slant transmissivity at $\mu = \cos (30)$ of:


$$t_1 = \exp(-\tau_1/\mu)$$

and for layer 2

For layer 2 the vertical optical depth is 

$$\tau_2 = \rho k \Delta z = \frac{-\Delta p_2}{g} k$$

with slant transmissivity:


$$t_2 = \exp(-\tau_2/\mu)$$

+++

The telescope is seeing a radiance of  $100/\pi$ $W\,m^{-2}\,sr^{-1}$ transmitted through 2 layers, so that
the radiance reaching the surface at 100 kPa from above both layers is:

$$L_{top}(100\ kPa) = \frac{100}{\pi} t_1\,t_2$$

From Layer 2, we need to calculate the amount emitted by layer 2 that reaches the surface after going through layer 1.


The blackbody radiance from layer 2 is:

$$L_{2BB} = \frac{\sigma 270^4}{\pi}$$

And from equation 26 on the equation sheet we know that the emissivity of layer 2 is (since absorptivity + transmissivity = 1):

$$\epsilon_2 = (1 - t_2)$$

and the amount that reaches the surface is reduced by transmission through layer 1:

$$L_2(100\ kPa) = (1 - t_2)L_{2BB}t_1$$

Finally the third term is the amount emitted from layer 1, with 

$$L_{1BB} = \frac{\sigma 290^4}{\pi} $$

with 

$$\epsilon_1 = (1 - t_1)$$

So the third term is:

$$
L_{1}(100\ kPa) = (1 - t_1) L_{1BB}
$$

and the answer is:

$$
L_{telescope} = L_{top}(100\ kPa) + L_2(100\ kPa) + L_1(100\ kPa) 
$$

+++

### The flux observed by the telescope

+++

#### Flux answer

+++

Using equation 5 from the equation sheet:

$$ E_{telescope} = L_{telescope} \Delta \omega$$

+++

### The brightness temperature observed by the telescope

+++

#### Brightness temperature answer

From the definition of brightness temperature over all wavelengths:

$$
L_{telescope} = \frac{\sigma T_{bright}^4}{\pi}
$$

+++

### Pixel area

Suppose you put this instrument into orbit 800 km above the ocean.  
Approximately what is the area of pixel you see at nadir (i.e. directly below) with this field of view? 
Roughly how big is the pixel looking 60 degrees off nadir?

#### Pixel area answer

$$
    \Delta \omega = 0.01\ sr = \frac{area}{800^2\ km^2}
$$

Looking off to the side at an angle of 60 degrees, the pixel area would be bigger by $area/\cos(60)$.

+++

### Short answer

*  Starting with the fact that radiance is conserved in a vacuum, show that over a uniform
   black surface emitting radiance $L_s$ that extends infinitely in the horizontal, the flux at
   any height above the surface is given by:

$$
  E = \pi L_s
$$

* How would you do the following integral using numpy?

$$
  \int_2^5 \exp(-x^2) dx
$$


* The Landsat geotiffs we worked with stored pieces of metadata called a crs (a coordinated reference system) and an ``affine transform''.  Explain briefly what these are and how they are used in mapping a satellite image.

```{code-cell} ipython3
import numpy as np
np.exp(-1.66*0.6)
```

### Radar


*  What is the bright band?   Why is it bright?


* The radar equation says that:

    $$
      \mathrm{Returned\ power} \propto |k^2| \frac{Z}{R^2}
    $$

  * Define each of the terms in this equation and explain qualitatively why we expect this
    dependence on $Z$ and $r$.

  * Explain how you can use this equation to find the rain rate in mm/hour 50 km
    from the radar

#### From {ref}`week9:radar`

1) Why does the returned power decrease as $1/R^2$` and not the roundtrip spreading of $1/R^4$ ?

2) Suppose you are given $Z_1$ in $mm^6\,m^{-3}$, c in m/s,$\Delta t$ in s and $\lambda$ in cm.  How do you convert $Z_1 c  \Delta t/\lambda^2$` to $km^2$?

3) The reflectivity goes down as b and K increase and goes up as $L_a$ and R increase -- explain.

4) Why is the width of the radar sample volume proportional to $\Delta t/2$ instead of $\Delta t$ ?

#### More radar

1) What is the maximum unambiguous range for cloudsat?

### Take home question

#### from {ref}`week11:goes_true_color`

1) Use a seaborn jointplot to compare the channel 1 (blue) histogram before and after the gamma correction

1) Use xarray.isel to clip just the portion of the abi scene that's in the [-114.75, -108.25, 36, 43] lon/lat bounding
box and save it to disk as a netcdf file with the correct affine transform and crs

1) Change the map projection from lambert to azimuthal equal area -- does it look less weird?

#### from {ref}`week12:goes_review`

1) Use the affine transform to find the point at which cloudsat first enters the image, and denote it by a green dot

2) Find the  GOES band01 reflectance (or cloudtop temperature, etc.) directly below the cloudsat track
