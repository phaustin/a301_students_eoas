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
Weekly Assignments/Quizzes       | 50%

Mid-term                         | 15%

Final (including takehome part)  | 35%
===============================  =====


* a reminder about the `UBC code of conduct <http://science.ubc.ca/students/new/conduct>`_

Rerferences/Texts (all available for free)
==========================================

* Stull, `Practical Meteorology`_ chapters 2, 3, 6 and 8 plus handouts

* Kazarinoff: `Problem Solving with Python`_

* VanderPlas, `A Whirlwind Tour of Python`_

* Vanderplas, `Python Data Science Handbook`_ 


Week by week topics (subject to change)
=======================================

======= =============  ===============================================
Week 1  1/9 - 9/13     | Introduction, course outline, Python intro
                       | Assignment: Jupyter intro                          

Week 2  1/16 - 9/20    | Python continued
                       | Assignment: Use python for plotting and integration


Week 3  1/23 - 1/27    | Blackbody radiation, equilibrium temperature, 
                       | Kirchoff's law
                       | Assignment1: Brightness temperatures

Week 4  1/30 - 2/3     | Beers law, absorption/emission, 
                       | Assignment2: Stull problems
                       
Week 5  2.6  0  2/10   | Schwartzchild eqn with absorption and emission
                       | Assignment3: Split window

Week 6  2/13 - 2/17    | Absorption and emission continued
                       | Monday: Thanksgiving                                     
                       | Assignment: Two-stream model with emission

Week 7  2/27 -  3/3    | Satellites continued: Ft. McMurray Fire
                       | Assignment: mid-term review, mid-term

Week 8  3/6 - 3/10     | Rain radar
                       | Assignment: Cloudsat precipitation data

Week 9  3/13 - 3/17    | Doppler radar
                       | Assignment: Interpreting doppler data
                       
Week 10 3/20 - 3/24    | Mapping with gis I
                       | Assignment: Vector layers

Week 11 3/27 - 3/31    | Mapping with gis II
                       | Map projections and shape files

Week 12 4/3 - 4/7      | Mapping with gis III
                       | Raster/vector overlays and true color

Week 13 4/10 - 4/14    | Catch-up, review

======= =============  ===============================================
