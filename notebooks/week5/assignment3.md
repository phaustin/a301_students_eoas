(assign3)=
# Assignment 3: Split window H2O retrieval

* Due Wednesday Oct. 14 10am

## Part 1 -- upload pdf or screenshot png

* Question 1.1: flux and radiance

  - We've got two definitions of E:

    * {ref}`radiance` eq. 2.4, which holds for a perpendicular beam where $\theta = 0$ so$\cos \theta = 1$

    * {ref}`flux_from_radiance` eq. 2.5, which holds for an $\theta$

   * How big can $\theta$ be before the difference between the two definitions
     reaches 1%?   Use the Taylor series for $\cos \theta$ to solve this, or
     just calculate the arccosine with python or a calculator.

   * If a satellite orbits at an altitude of 800 km above sea level and its pixel at
     nadir has an area of 1 $km^2$, find the solid angle of the satellite telescope
     field of view in steradians.

* Question 1.2:  Kirchoff's law for a gas

- In {ref}`schwartz` we used the 2nd law to prove by contradiction for that
    absorptivity = emissivity for using two
    surfaces at the same temperature.   Make the same argument for a gas between
    two black plates -- i.e. show that if the emissivity and absorptivity of the
    gas are not equal you violate the second law of thermodynamics.


## Part 2  -- Split window estimates of total precipitable water

   * Read this [explanation of split window retrievals](https://cimss.ssec.wisc.edu/satellite-blog/archives/23702)

   * Here's an actual map of [precipitable water](https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA12096)

   * Hand in a python notebook with a map of the brightness temperature difference for your Modis granule between the
     channel 31 "clean" channel - channel 32 "dirty" channel in degrees C, with a colorbar that
     use a normalized palette to hangle over and under temperature values, as in
     {ref}`week4:resample`
