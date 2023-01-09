.. include:: ../refs.txt

.. _syllabus:

ATSC 301: syllabus
++++++++++++++++++

:Instructor:   Dr. Phil Austin
:Email:        paustin@eos.ubc.ca
:Office:       EOS South 157, 604-822-2175
:Office hours: TBD

Course objectives
=================

By the end of this course you should have a good understanding of


1. how radiation is emitted, absorbed, transmitted and reflected by
   surfaces, clouds, and the atmosphere  (the "forward problem")

2. how radiometers, radars and lidars are used to infer 
   temperature and surface and cloud properties (the "inverse problem")

3. how to map spatial remote sensing data the earth's surface using geographic 

4. how to write clear, documented and tested code that can ingest, manipulate and display
   data, and how to turn equations into computer algorithms in Python
   

Sample lecture learning objectives (provided with each lecture)
===============================================================

1. Understand the principals that determine satellite sensor wavelength, spatial
   resolution, sampling frequencies

2. Use standard satellite data archives to obtain and analyze global atmospheric
   and surface measurements

3. Calculate the net absorption/emission/scattering of the atmosphere
   given vertical profiles of temperature, gas, aerosol, clouds (the forward problem)

4. Use passive and active radiance measurements from satellites or ground based sensors to determine
   vegetation characteristics, surface temperature, atmospheric temperature

5. Calculate rain rate, doppler velocities, attenuation given cloud drop size distributions

6. Use a standard gis package (qgis) to overlay satellite data with lat/lon characteristics

7. Write python programs to analyze satellite and climate data for MODIS and Cloudsat data


Evaluation
==========

===============================  =====
Weekly Assignments               | 45%

Mid-term                         | 20%

Final (including takehome part)  | 35%
===============================  =====


* a reminder about the `UBC code of conduct <http://science.ubc.ca/students/new/conduct>`_


Required texts (all available for free)
=======================================

* Stull, `Practical Meteorology`_ chapters 2, 3, 6 and 8 plus handouts

* VanderPlas, `A Whirlwind Tour of Python`_  (`html version <./whirlwind/Index.html>`_)

* Vanderplas, `Python Data Science Handbook`_ 
  

Week by week topics (subject to change)
=======================================

======= =============  ===============================================
Week 1  9/9 - 9/11     | Introduction, course outline, Python intro
                       | Assignment: Jupyter intro                          

Week 2  9/14 - 9/18    | Python continued
                       | Assignment: Use python for plotting and integration


Week 3  9/21 - 9/25    | Blackbody radiation, equilibrium temperature, 
                       | Kirchoff's law
                       | Assignment1: Brightness temperatures

Week 4  9/28 - 10/2    | Beers law, absorption/emission, 
                       | Assignment2: Stull problems
                       
Week 5  10/5 - 10/9    | Schwartzchild eqn with absorption and emission
                       | Assignment3: Split window

Week 6  10/12 - 10/16  | Absorption and emission continued
                       | Monday: Thanksgiving                                     
                       | Assignment: Two-stream model with emission

Week 7  10/19 - 10/23  | Satellites continued: Ft. McMurray Fire
                       | Assignment: mid-term review, mid-term

Week 8  10/26 - 10/30  | Rain radar
                       | Assignment: Cloudsat precipitation data

Week 9  11/2 - 11/6    | Doppler radar
                       | Assignment: Interpreting doppler data
                       
Week 10 11/9 - 11/13   | Mapping with gis I
                       | Assignment: Vector layers

Week 11 11/16 - 11/20  | Mapping with gis II
                       | Map projections and shape files

Week 12 11/23 - 11/27  | Mapping with gis III
                       | Raster/vector overlays and true color

Week 13 11/30 - 12/2   | Catch-up, review

======= =============  ===============================================
