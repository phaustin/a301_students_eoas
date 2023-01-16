# Week 2

* Learning objectives

  - Understand how to measure monochromatic radiance 
  
  - Begin image analysis of a Modis Channel 30 image

* Review from Week 1

  * Read Stull Chapter 2 through page 38
  
    - Main conceptual topic:  the definiton of radiative flux (section 2.2 plus {ref}`beerslaw`)

  * Intro to Jupyter

* Week 2 topics for Monday

   * make sure your image is working with {ref}`modis_level1b`

   * Review: Sections 4 and 5 of Kazarinoff:  Python REPL and datatypes

* Introduce: Stull Chapter 2 pages 36-42 on the Planck function (eq. 2.13), 
  Stefen-Boltzman (eq: 2.15), inverse square law 

* Week 2 topics for  Wednesday: 

    - Read my {ref}`radiance` notes.  -- key idea: how does a satellite camera
      actually make the measurement -- it uses a photon counter,
      wavelength filter, shutter timer, telescope.  You need to know 
      the area of the photon counter, the width of the  wavelength filter,
      the total exposure time of the shutter to
      turn photon counts into radiance with units of $W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$
    
* Week 2 topics for  Friday -- {ref}`flux_from_radiance`

  * Go over [Kazarinoff Chapter    8](https://atsc_web.eoas.ubc.ca/Functions-and-Modules/Introduction.html#functions-and-modules) on funtions and modules.

  * Read {ref}`flux_from_radiance`

  * Go over some notebooks:

    * {ref}`sec:debugging`  
    * {ref}`sec:numpy`  
    * {ref}`sec:planck`  

