# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.1-dev
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import numpy as np
from numpy import log10
from numpy.testing import assert_almost_equal


# %%
def findPr(Z,K2,La,R,R1=None,Pt=None,b=None,Z1=None):
   """
    solve stull eqn 8.23
    input: Z (mm^6/m^3), K2 (unitless), La (unitless),R (km)
           plus radar coefficients appropriate to given radar (like Nexrad)
    output: returns Pr in W 
   """ 
   Pr=Pt*b*K2/La**2.*(R1/R)**2.*Z
   return Pr


# %%
if __name__=="__main__":
    #stull p. 246 sample appliation
    # given

    #coefficents for nexrad
    R1=2.17e-10#range factor, km, Stull 8.25
    Pt=750.e3 #transmitted power, W, stull p. 246
    b=14255 #equipment factor, Stull 8.26

    nexrad=dict(R1=R1,Pt=Pt,b=b)

    Z=1.e4  #Z of 40 dbZ
    R=20    #range of 20 km
    K2=0.93  #liquid water
    La=1   #no attenuation
    power_watts=findPr(Z,K2,La,R,**nexrad)
    the_text="""
           Stull problem on p. 246: start with 40 dbZ at 20 km and
           find Pr:
           Here is the Pr: {Prval:10.5g} Watts
           Here is  dbm -- decibels re 1 mWatt: {dBm:5.3f},
    """
    values={'Prval':power_watts,'dBm':10*log10(power_watts*1.e3)}
    print   the_text.format(**values)

# %%
