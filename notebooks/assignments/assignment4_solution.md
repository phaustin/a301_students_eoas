---
jupytext:
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

+++ {"tags": [], "user_expressions": []}

(assign4_solution)=
# Assignment 4 -- solutions

+++ {"tags": [], "user_expressions": []}

## Q1) midterm question 2 revisit  

(6 points, for undergrads this will replace your midterm Q2 mark)

Upload a notebook and a pdf scan of an analytic solution that solves Q2 in the {ref}`mid_2022t2_solutions` with this
change:

a) Instead of a constant temperature layer between 1 km and 6 km, use a temperature that
varies  linearly with height:

$$
T(z) = 270 + (z -  3.5) \Gamma_z
$$
where $z$ is the height in km and $\Gamma$ is a (negative) constant (K/km).

In a python notebook, make a plot of the blackbody monchromatic radiance $B_\lambda$ at $\lambda = 15\ \mu m$ versus transmittance $t$
between z=1 and 6 km for three values of $\Gamma_z$: $\Gamma_z = 0$ (midterm case),  $\Gamma_z = -10\ K/km$
(dry atmosphere),$\Gamma_z = -6.5\ K/km$ (cloudy tropical atmosphere).

+++ {"tags": [], "user_expressions": []}

### Q1a solution

Approach -- use the [calc_radiance](https://phaustin.github.io/a301_web/full_listing.html#rad_lib.radiation.calc_radiance) to
get the brightness temperature at 15 $\mu m$ for a vector of temperatures.

#### step 1: Blackbody profiles

from the assignment I get the temperature profile and calculate the blackbody radiance for $\Gamma_z$ = -6.5 K/km, -10 K/km and 0 K/km

 I'll call my 3 blackbody profiles for dT/dz = 0, -6.5 and =10 K/km: B_0, B_65, and B_10

```{code-cell} ipython3
import numpy as np
from copy import copy
from matplotlib import pyplot as plt
from rad_lib.radiation import calc_radiance

#
# simple function for the temperature profile
#
def temperature_profile(z, gamma_z):
    temp = 270 + (z - 3500)*gamma_z
    return temp

#
# I'll make two different z ranges from 1 to 6 km, one in meters
# and one in km
#
z_layer_m = np.arange(1,6,0.0001)*1.e3
#
# calculate 3 different temperature profiles for the 3 slopes
#
gamma_z = -6.5e-3
temp_z_layer_65 = temperature_profile(z_layer_m,gamma_z)
gamma_z = -10e-3
temp_z_layer_10 = temperature_profile(z_layer_m,gamma_z)
gamma_z = 0
temp_z_layer_0 = temperature_profile(z_layer_m,gamma_z)
#
# calculate 3 different blackbody radiance profiles
#
wavel=15.e-6
B_65 = calc_radiance(wavel,temp_z_layer_65)
B_10 = calc_radiance(wavel,temp_z_layer_10)
B_0 = calc_radiance(wavel,temp_z_layer_0)
```

+++ {"tags": [], "user_expressions": []}

#### Good idea to plot vs. height to check

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
m2km = 1.e-3  #meters to km
ax.plot(temp_z_layer_65,z_layer_m*m2km,label="-6.5 K/km")
ax.plot(temp_z_layer_10,z_layer_m*m2km,label="-10 K/km")
ax.plot(temp_z_layer_0,z_layer_m*m2km,label="constant")
ax.grid(True)
ax.set_title("Q1a solution:  Temp (K) vs. z (km))")
ax.legend();
```

+++ {"tags": [], "user_expressions": []}

#### step 2:  From the solution, get the functions for optical depth and transmissivity and calculate the transmissivity profile

The next cell borrows the equations from the midterm solution to calculate
$\tau_T$, $\tau$ and the transmisivity $t$

```{code-cell} ipython3
Hrho=9000.  # m
ztop = 20.e3 # m
k=0.15 # m^2/kg
rho_air = 1.1 # kg/m^3
rmix=4.e-4  #unitless

def calc_tau(k,rmix,rho_air,Hrho,z):
    """
    all units mks
    """
    tau_z = k*rmix*rho_air*Hrho*(1 - np.exp(-(z/Hrho)))
    return tau_z

def calc_trans(k,rmix,rho_air,Hrho,z,ztop):
    tau_tot = calc_tau(k,rmix,rho_air,Hrho,ztop)
    tau_z = calc_tau(k,rmix,rho_air,Hrho,z)
    trans_z = np.exp(-(tau_tot - tau_z))
    return trans_z

#
# transmissivity from 1 - 6 km
#
trans_z_layer = calc_trans(k,rmix,rho_air,Hrho,z_layer_m,ztop)
```

+++ {"tags": [], "user_expressions": []}

From the midterm solution I know that the transmissivity should increase from 0-.63 to 0.79,
which it does

```{code-cell} ipython3
fig,ax=plt.subplots(1,1)
ax.plot(trans_z_layer,z_layer_m*m2km)
ax.grid(True)
ax.set_title("transmissivity vs height (km)");
```

+++ {"tags": [], "user_expressions": []}

#### Q1a answer plot: plot the blackbody radiance vs transmissivity for the three slopes

So puth this together to get the profile plot

```{code-cell} ipython3
fig, ax = plt.subplots(1,1)
ax.plot(B_65,trans_z_layer,label="-6.5 K/km")
ax.plot(B_10,trans_z_layer,label="-10 K/km")
ax.plot(B_0,trans_z_layer,label="constant")
ax.grid(True)
ax.set_title("Q1a solution:  B(t) ($W\,m^{-2}\,m^{-1}\,sr^{-1}$) vs. t)")
ax.set_xlabel("blackbody radiance B ($W\,m^{-2}\,m^{-1}\,sr^{-1}$)")
ax.set_ylabel("15 $\mu m$ transmittance to top of atmosphere")
ax.legend();
```

+++ {"tags": [], "user_expressions": []}

Use your plots to find values of $\Gamma_t = \frac{dB}{dt}$ that correspond to the three values of $\Gamma_z$
so that you can write an approximate linear function $B(t)$ that looks like:

$$
B(t) = B(t(3.5km)) + (t - t(3.5km))\Gamma_t
$$ (eq:planck)

+++ {"tags": [], "user_expressions": []}

#### Q1a answer for slope: slope_65=-13, slope_10=-20: units: $W\,m^{-2}\,sr^{-1}\,\mu m^{-1}$

To find the slopes I need to calculate "rise over run"  for $\Delta B$ and $\Delta t$  between 1 km and 6 km

Change the radiance units to $W\,m^{-2}\,sr^{-1}\,\mu m^{-1}$ to make it easier to write

```{code-cell} ipython3
def find_slope(t,B):
    #
    # find the delta values last - first
    #
    delta_t = t[-1] - t[0]
    delta_B = B[-1] - B[0]
    slope = delta_B/delta_t
    return slope

meter2micron = 1.e-6
slope_65 = find_slope(trans_z_layer,B_65*meter2micron)
slope_10 = find_slope(trans_z_layer,B_10*meter2micron)
print(f"Slope Answer: {slope_65=:.0f} W/m2/sr/mum, {slope_10=:.0f} W/m^2/sr/micron")
```

+++ {"tags": [], "user_expressions": []}

## Q1b numerical solution

Since we have profiles for $t$ and $B$, we can use the approach of {ref}`week2:numint` to get the numerical integral as a check
on our analytic answer

The answer below for the three slopes:  B10integ=0.757, B65integ=0.748, B0integ=0.736 $W\,m^{-2}\,sr^{-1}\,\mu m^{-1}$

```{code-cell} ipython3
B10centers = (B_10[1:] + B_10[0:-1])/2.
B65centers = (B_65[1:] + B_65[0:-1])/2
B0centers = (B_0[1:] + B_0[0:-1])/2
dt = np.diff(trans_z_layer)
#
# integrage and convert to W/m^2/sr/micron
#
B0integ = np.sum(B0centers*dt)*1.e-6
B10integ = np.sum(B10centers*dt)*1.e-6
B65integ = np.sum(B65centers*dt)*1.e-6
print(f"{B10integ=:.3f}, {B65integ=:.3f}, {B0integ=:.3f} W/m^2/micron/sr")
```

+++ {"tags": [], "user_expressions": []}

## Q1b -- analytic solution

+++ {"tags": [], "user_expressions": []}

b) Given {eq}`eq:planck` derive an analytic solution for the radiance $L$ at 6 km coming from the air
between 1 km and 6 km.  That is, solve the Schwartzchild integral:

$$
L(6km) = \int_{1km}^{6km} B(t^\prime) dt^\prime
$$ (eq:schwartz)

as an equation.

+++ {"tags": [], "user_expressions": []}

### Q1b solution -- equations

Integrate {eq}`eq:schwartz` and get:

$$
\begin{align}
&\int_{1km}^{6km} \left ( B_0+\Gamma_t t^\prime \right )dt^\prime = \\
&B_0(t_{6km} - t_{1km}) + \left ( \frac{t_{6km}^2}{2} - \frac{t_{1km}^2}{2} \right ) \Gamma_t
\end{align}
$$ (eq:solution)

where $B_0$ is given by:

+++ {"tags": [], "user_expressions": []}

$$
\begin{aligned}
& B=B_{3.5 \mathrm{~km}}+\left(t-t_{3.5}\right) \Gamma_t \\
& B=\left(B_{3.5 \mathrm{~km}}+\Gamma_t\left(-t_{3.5}\right)\right)+\Gamma_t t \\
& \text{therefore} \\
& B_0=B_{3.5 \mathrm{~km}}-t_{3.5} \Gamma_t
\end{aligned}
$$ (eq:deriv2)

+++ {"user_expressions": []}

In another cell in your notebook, calculate L(6km) for the three values of $\Gamma_z$ using your solution to {eq}`eq:schwartz`.
How much do they vary, in percent, from each other?

+++ {"tags": [], "user_expressions": []}

### Q1b calculate $t_{3.5km}$ and $B(270 K)$

To get numbers for {eq}`eq:solution`, I need to find $B_{3.5km}$ and $t_{3.5km}$

```{code-cell} ipython3
trans35 = calc_trans(k,rmix,rho_air,Hrho,3.5e3,ztop)
B35 = calc_radiance(wavel,270)
B35, trans35
```

```{code-cell} ipython3
def calc_B0(B35,trans35,gamma_t):
    B0 = B35 - trans35*gamma_t
    return B0
    
def calc_L6km(B35,trans35, trans_z_layer ,gamma_t):
    """
    all units are mks
    """
    trans6km = trans_z_layer[-1]
    trans1km = trans_z_layer[0]
    delta_trans = trans6km - trans1km
    B0 = calc_B0(B35,trans35,gamma_t)
    term1 = B0*delta_trans
    term2 = (trans6km**2.- trans1km**2.)/2.*gamma_t
    answer = term1 + term2
    return answer
```

+++ {"tags": [], "user_expressions": []}

## Q1b: answer: L6km for 3 slopes

Looks like the numerical solution is slightly off, but  within a couple tenths of a percent

L6km_10=0.758, L6km_65=0.751, L6km_0=0.737 $W\,m^{-2}\,sr^{-1}\,\mu m^{-1}$ 

```{code-cell} ipython3
L6km_65 = calc_L6km(B35,trans35,trans_z_layer,slope_65*1.e6)*meter2micron
L6km_10 = calc_L6km(B35,trans35,trans_z_layer,slope_10*1.e6)*meter2micron
L6km_0 = calc_L6km(B35,trans35,trans_z_layer,0.)*meter2micron
print(f"radiance at 6 km in W/m^2/micron/sr: {L6km_10=:0.3f}, {L6km_65=:0.3f}, {L6km_0=:0.3f}")
```

+++ {"tags": [], "user_expressions": []}

## Fractional radiance change

The radiance change between lapse rates of  -10 K/km to -6.5 K/km (0.758 - 0.737)/0.737 $\approx$ 3%, so not much of a signal
to work with for atmospheric sounding

+++ {"tags": [], "user_expressions": []}

## Question 2 ndvi
(6 points)

Use the function [get_landsat_scene](https://phaustin.github.io/a301_web/full_listing.html#sat_lib.landsat_read.get_landsat_scene) to read
in one of your landsat scenes and get back a dictionary containing the band4, band5 and Fmask channels.

Write a function called `calc_ndvi` that takes this dictionary and returns a new rioxarray DataArray
that contains the [normalized vegetation difference index](https://www.usgs.gov/landsat-missions/landsat-normalized-difference-vegetation-index) for each pixel in your scene.

Hand in a notebook that:

* calculates the ndvi index
  (Make sure you
  multply your ndvi array by the cloud mask to set all cloudy/water pixels to np.nan)
* plots it in greyscale with a title that contains the image date.
* writes the ndvi DataArray out as geotiff

```{code-cell} ipython3
import os
os.environ["GDAL_HTTP_COOKIEFILE"] = "./cookies.txt"
os.environ["GDAL_HTTP_COOKIEJAR"] = "./cookies.txt"
```

```{code-cell} ipython3
import rioxarray
from rasterio.windows import Window
from sat_lib.landsat_read import get_landsat_scene
from shapely.geometry import Point
import a301_lib


the_lon, the_lat = -123.2460, 49.2606
location = Point(the_lon, the_lat)
the_date = "2015-06-14"
```

```{code-cell} ipython3
the_window = Window(col_off=2671, row_off=1352, width=234, height=301)
out_dict = get_landsat_scene(the_date,the_lon,the_lat,the_window)
```

```{code-cell} ipython3
out_dict.keys()
```

+++ {"user_expressions": []}

### the function

```{code-cell} ipython3
def find_ndvi(out_dict):
    band4 = out_dict['b4_ds']
    band5 = out_dict['b5_ds']
    fmask = out_dict['fmask_ds']
    ndvi = (band5 - band4)/(band5 + band4)
    ndvi = ndvi*fmask
    return ndvi
```

+++ {"tags": [], "user_expressions": []}

### the plot

Use a greyscale palette in the ndvi range 0-0.8

```{code-cell} ipython3
ndvi = find_ndvi(out_dict)
#
# read the day from one of the dataArrays
#
day = out_dict['b5_ds'].day
pal = copy(plt.get_cmap("Greys_r"))
pal.set_bad("0.75")  # 75% grey for out-of-map cells
pal.set_over("w")  # color cells > vmax white
pal.set_under("k")  # color cells < vmin black
vmin = 0.0  #anything under this is colored black
vmax = 0.8  #anything over this is colored white
from matplotlib.colors import Normalize
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
fig, ax = plt.subplots(1,1,figsize=(8,8*1.3))
ndvi.plot(ax=ax,norm=the_norm,cmap = pal)
ax.set(title = f"Landsat ndvi for {day}");
```

+++ {"user_expressions": []}

### write out the geotiff

```{code-cell} ipython3
outfile = a301_lib.data_share / "pha/landsat/ndvi.tif"
ndvi.rio.to_raster(outfile)
```
