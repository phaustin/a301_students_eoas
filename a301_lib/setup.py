#!/usr/bin/env python

# Setup script for PyPI; use CMakeFile.txt to build extension modules

from setuptools import setup


setup(
    name='a301_lib',
    packages=['a301_lib'],
    classifiers=[
        'License :: OSI Approved :: BSD License'
    ],
    long_description="""python tools for a301""")
