
(assign4)=
# Assignment 4: water vapor path

## Column water vapor

Add cells to {ref}`scale_heights`

1\.  Print out the density and pressure scale heights for each of the five soundings

2\.  Define a function that takes a sounding dataframe and returns the "total precipitable water", which is defined as:

$$W = \int_0^{z_{top}} \rho_v dz $$

Do a change of units to convert $kg\,m^{-2}$ to $cm\,m^{-2}$ using the density of liquid water (1000 $kg\,m^{-3}$) -- that is, turn the kg of water in the 1 square meter column into cubic meters and turn that into $cm/m^{-2}$

3\.  Use your function to print out W for all five soundings

+++

## Pencil and paper problems

+++

4\. A satellite orbits 800 km above the earth and has a telescope with a field of view
   that covers 1 $km^2$ directly below (i.e. at nadir).  If that 1 $km^2$ is ocean with
   an emissivity $e=1$ at a temperature
   of 280 K, calculate the flux in $W\,m^2$ reaching the satellite from all wavelengths
   from that pixel.

+++

5\. Suppose that a satellite's orbit changes from a height of 800 km to a height of 600 km
   above the surface.  If the telescope field of view stays the same, prove that
   the radiance stays constant.
