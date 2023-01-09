---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(stull-radar-app)=
# Stull page 246 -- application

This notebook runs through the sample problem on page 246 of
[Stull Chapter 8](https://www.eoas.ubc.ca/books/Practical_Meteorology/prmet102/Ch08-satellite_radar-v102b.pdf)

```{code-cell}
import numpy as np
from numpy import log10
from numpy.testing import assert_almost_equal
```

```{code-cell}
def findPr(Z,K2,La,R,R1=None,Pt=None,b=None):
   """
    solve stull eqn 8.23
    input: Z (mm^6/m^3), K2 (unitless), La (unitless),R (km)
           plus radar coefficients appropriate to given radar (like Nexrad)
    output: returns Pr in W 
   """ 
   Pr=Pt*b*K2/La**2.*(R1/R)**2.*Z
   return Pr
```

```{code-cell}
def finddbz(Pr,K2,La,R,R1=None,Pt=None,b=None):
   """calculate dbZ using Stull 8.28
      with Pr the returned power in Watts
   """
   dbZ=10.*log10(Pr/Pt) + 20.*log10(R/R1) - \
       10.*log10(K2/La**2.) - 10.*log10(b)
   return dbZ
```

```{code-cell}
def findRR_snow(dbZ):
   """
    find the rain rate in mm/hr using Stull 8.29
    dbZ:  reflectivity in dbZ referenced to 1 mm^6/m^3
   """
   #given that for snow Z=2000*RR**2. 
   a1_snow=0.02236   #(1/2000.)**(1./2.)
   a2_snow=0.5   #RR=(1/2000)**(1./2.)*Z**(1/2.)
   Z=10**(dbZ/10.)
   RR=a1_snow*Z**a2_snow
   return RR
```

```{code-cell}
def findRR_rain(dbZ):
   """
    find the rain rate in mm/hr using Stull 8.29
    dbZ:  reflectivity in dbZ referenced to 1 mm^6/m^3
   """
   #given that for rain Z=300*RR**1.4
   #a1_rain=(1/300.)**(1/1.4) = 0.017
   #a2_rain=1/1.4  = 0.714
   Z=10**(dbZ/10.)
   a1_rain=0.017  
   a2_rain=0.714  
   RR=a1_rain*Z**a2_rain
   return RR
```

```{code-cell}
def main():
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
    print(the_text.format(**values))


    q1text="""
        Q1: Suppose a Nexrad radar (Stull p.~246)  is
        receiving a signal with returned power Pr = -58 dBm.  Using the radar
        equation find the precipitation rate under the assumption that
        there is no attenuation and that it is a rainstorm (i.e. liquid water)
        100 km away from the radar.
    """

    
    print(q1text)
    
    K2=0.93  #stull p. 245
    Pr=10**(-5.8)*1.e-3  #dBm=-58, convert from mWatts to Watts
    La=1
    R=100.  #km
    dbZ=finddbz(Pr,K2,La,R,**nexrad)
    RR=findRR_rain(dbZ)
    the_answ={'Prval':Pr,'R':R,'dbZval':dbZ,'RRval':RR}
    q1ans= """
        Q1 answer: With the returned power at {Prval:8.3g} Watts and the range at {R:4.1f} km,
                   the radar reflectivity with no attenuation is {dbZval:5.2f} dbZ and the
                   rain rate is {RRval:5.2f} mm/hr
        """
    print(q1ans.format(**the_answ))

    q2text="""
        Q2: Now keep everything the same, but make the mistake of guessing that it's a snowstorm,
        which means that K2=0.208 and we use the snowfall Z-RR relation
        of Z=2000*RR**2.
    """
    print(q2text)
    K2=0.208 #p. 245
    dbZ=finddbz(Pr,K2,La,R,**nexrad)
    RR=findRR_snow(dbZ)
    the_answ['RRval']=RR
    the_answ['dbZval']=dbZ
    q2ans= """
        Q2 answer: With the returned power at {Prval:8.3g} Watts and the range at {R:4.1f} km,
                   the radar reflectivity with no attenuation is {dbZval:5.2f} dbZ assuming snow,
                   and the liquid equivalent rain rate is {RRval:5.2f} mm/hr
        """
    print(q2ans.format(**the_answ))

    q3text="""
        Q3: Now assume it's rain, but make the mistake of guessing that there's a factor of La=2
        attenuation between the target and the rainstorm
    """

    print(q3text)

    K2=0.93 #p. 245
    La=2.
    dbZ=finddbz(Pr,K2,La,R,**nexrad)
    RR=findRR_rain(dbZ)
    the_answ['RRval']=RR
    the_answ['dbZval']=dbZ

    q3ans= """
        Q3 answer: With the returned power at {Prval:8.3g} Watts and the range at {R:4.1f} km,
                   the radar reflectivity with 3 dB attenuation is {dbZval:5.2f} dbZ assuming rain,
                   and the  rain rate is {RRval:5.2f} mm/hr
        """

    print(q3ans.format(**the_answ))
```

```{code-cell}
main()
```
