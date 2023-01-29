#!/usr/bin/env python
"""
a301.hdftools.h5dump
_________________

Dump groups, datasets and attributes for an hdf5 file

to run from the command line::

   python -m sat_lib.hdftools.h5dump h5file

to run from a python script::

   from e582utils.h5dump import dumph5
   outstring=dumph5(filename)
"""

import h5py
import argparse
import sys
from io import StringIO


def print_attrs(obj_name, obj,fileobj):
    """
    print attributes of obj with name obj_name to
    the StringIO instance fileobj

    this function is called recursively by h5py.visititems()

    """
    if obj.parent.name == '/':
        fileobj.write('{}\n'.format('_' * 15))
        fileobj.write('root group object {}\n'.format(repr(obj)))
        fileobj.write('{}\n'.format('_' * 15))
    else:
        fileobj.write('member of group: {}: {}\n'.format(obj.parent.name, obj))
    try:
        for key, val in obj.attrs.items():
            fileobj.write("    {}: {}\n".format(key, val))
    except IOError:
        fileobj.write('this is an HDFStore pandas dataframe\n')
        fileobj.write('{} {}\n'.format(the_name, obj))
        fileobj.write('{}\n'.format('-' * 20))


def dumph5(filename):
    """
    create a string listing data and metadata from an hdf5 file

    Parameters
    ----------

    filename: str
       path to file

    Returns
    -------

    outstring: str
      string with dump information
    """
    filename = str(filename)
    print(f"opening {filename}")
    if isinstance(filename, h5py._hl.files.File):
        raise Exception('need string filename')
    with h5py.File(filename, 'r') as infile:
        with StringIO() as store:
            #
            # visititems functions only take one argument so
            # make a closure tat includes the fileobj store
            #
            def callback(name,obj):
                return print_attrs(name,obj,store)
            
            print('+' * 20,file=store)
            print('found the following top-level items: ',file=store)
            for name, object in infile.items():
                print('{}: {}'.format(name, object),file=store)
            print('+' * 20,file=store)
            infile.visititems(callback)
            print('-------------------',file=store)
            print("attributes for the root file",file=store)
            print('-------------------',file=store)
            try:
                for key, value in infile.attrs.items():
                    print("attribute name: ", key, "--- value: ", value,file=store)
            except IOError:
                pass
            
            outstring=store.getvalue()
    return outstring


def main(filename,do_print=True):
    """
    args: optional -- if missing then args will be taken from command line
          or pass [h5_file] -- list with name of h5_file to open
    """
    outstring=dumph5(filename)
    if do_print:
        print(outstring)
    else:
        return(outstring)

