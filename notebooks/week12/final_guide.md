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
     - pandas  (indexing and searching rows)
     - finding and replacing values using logical indexing (i.e. chan1[hit]=np.nan)
     - loop comprehensions (i.e. newlist=[f(item) for item in list]
     - reading hdf and writing hdf
     - histogram equalization using scikit image
     - creating false color composites
     - clipping an xarray dataset
