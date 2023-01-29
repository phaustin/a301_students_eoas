#!/usr/bin/env python
"""
list all contents of an hdf5 file

Usage:  h5_list h5_file
"""
from pathlib import Path
import a301_lib
from sat_lib.hdftools import h5dump
import sys

if __name__ == "__main__":
    print(f"sys.argv shows following command line arguments:\n{sys.argv}\n")
    doprint=True
    the_file = Path(sys.argv[1])
    if the_file.is_file():
        h5dump.main(the_file, doprint)
    
