import numpy as np
#
# get Stull's c_1 and c_2 from fundamental constants
#
# c=2.99792458e+08  #m/s -- speed of light in vacuum
# h=6.62606876e-34  #J s  -- Planck's constant
# k=1.3806503e-23  # J/K  -- Boltzman's constant

c, h, k = 299_792_458.0, 6.626_070_04e-34, 1.380_648_52e-23
c1 = 2.0 * h * c ** 2.0
c2 = h * c / k
sigma = 2.0 * np.pi ** 5.0 * k ** 4.0 / (15 * h ** 3.0 * c ** 2.0)
print(sigma)


def Elambda(wavel, Temp):
    """
    Calculate the blackbody radiant exitence (Stull 2.13)

    Parameters
    ----------

      wavel: float or array
           wavelength (meters)

      Temp: float
           temperature (K)

    Returns
    -------

    Elambda:  float or arr
           monochromatic radiant exitence (W/m^2/m)
    """
    Elambda_val = c1 * np.pi / (wavel ** 5.0 * (np.exp(c2 / (wavel * Temp)) - 1))
    return Elambda_val
