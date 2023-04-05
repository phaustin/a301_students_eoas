---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: -all
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
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
     
## Study questions

### Midterm questions

* the final is comprehensive so be sure you understand the midterm solutions

### Heating rate

1) Derive the heating rate equation 

2) A 150 m thick nocturnal cloud layer with a temperature of 275 K floats
over a 300 K surface.

Given: 

(i) mass absorption coefficient of the cloud liquid water
is $k=0.004\ $m^2/kg$

(ii) $\rho_{air}$ = 1 $kg/m^3$

(ii) downward longwave flux density from the
air above the cloud of $E_\downarrow(z_T)$=75 \wm. (where $z_T=150$ m is the height of 
cloud top above cloud base) 

(iii)  No atmospheric absorption

- Find the total vertical optical depth of the cloud
-  Write down expressions for the flux transmission $\hat{t}_f$
   between $z$ and $z_T$ and between 0 and $z$ as functions
   of $z,\,z_T,\,k$ assuming  $z$  is inside the cloud, i.e.~$0 < z < z_T$.

- Find the heating rate of the cloud $dT/dt$ in K/hour

### Radar

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
