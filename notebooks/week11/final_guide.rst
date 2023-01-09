.. include:: refs.txt
.. include:: coursebuild/index_notebooks.txt

.. _final_guide:

Study guide for final exam
++++++++++++++++++++++++++

Format
======

* Take home, timed for about 90 minutes on written component, 4-6 hours on notebook

* 7 day window, starting December 4, ending December 11

* 15-20 minute oral runthrough -- December 14/15.


Topic focus
===========

A) Calculating radiative fluxes from atmospheric conditions:

   1) Find optical depth and transmisson profiles given a hydrostatic atmosphere with
      a specified scale height

   2) Calculate the equilibrium temperature profile of a multilayer atmosphere with known
      transmission

   3) Calculate the flux observed by a satellite through an atmosphere of know properties

   4) Convert between radiance and brightness temperature

   5) Calculate heating/cooling rates given atmospheric fluxes

B) Calcuate atmospheric/solar properties from radiation measurements

   1)  Use Beer's law to estimate the solar flux as a function of optical depth


   2)  Use brightness temperature differences and/or
       weighting functions/transmissions at multiple wavelengths to show how
       column water vapor amounts can be inferred from satellite data

C) Radar:

   1) Find the rain rate from a Z-R relationship

   2) Find Z from a cloud droplet size distribution

   3) Locate and plot cloudsat atmopsheric profiles from data


D) Derivations/equations

   1) Integrate the hydrostatic equation to find the pressure as a function of height

   2) Integrate the Schwartzchild equation with a constant temperature profile to find the
      radiance or the flux for a  layer

   3) Integrate the Schwartzchild equation with a varying temperature profile

   4) Derive the heating rate equation

   5) Use change of variables to solve an integral

   6) Use differentials to estimate small changes to a function

   7) Estimate the heating rate in a layer given fluxes


E) Python programming

   -  Be able to explain and use the following functions or programs does (i.e. relate the code to
      equations and/or explain the programming logic).

      - searchsorted
      - imshow
      - hist
      - np.sum, np.diff
      - pyresample
      - pyproj
      - rasterio.windows.Window
      - rasterio.mask
      - cartopy
      - pandas and geopandas (indexing and searching rows)
      - finding and replacing values using logical indexing (i.e. chan1[hit]=np.nan)
      - loop comprehensions (i.e. newlist=[f(item) for item in list]
      - reading hdf and writing hdf, h5 and tiff and png files
      - histogram equalization using scikit image
      - creating false color composites


F) Longer answer

   - Trace a pixel from it's photon count at the satellite to a physical property on a map (ndvi, temperature)  -- what's the workflow from data download to presentation at a meeting?  What routines do you need to call, and what do they do?

   - WGS94, UTM, Lambert azimuthal projection  -- definition, when to use and for what

   - tradeoffs -- choices about pixel size, orbit altitude, etc. depending on the target and technology -- i.e. what a real sensor is capable of measuring.   I give you the sensor limitations (how many photons it needs per second to make a reliable observation), you give me a combination of target, orbit, pixel size that would be possible with that sensor.
