import click
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
from pyhdf.HDF import *
from pyhdf.V   import *
from pyhdf.VS  import *
from pyhdf.SD  import *
from .modischan_read import sd_open_file
from .cloudsat import read_swath_attributes
import pprint
pp = pprint.PrettyPrinter(indent=4)


try:
    __version__ = version("sat_lib")
except PackageNotFoundError:
    __version__ = "unknown version"


def format_line(line_dict):
    if 'dims' in line_dict:
        dims = line_dict['dims']
        line = f"dims: {line_dict['dims']}"
    else:
        line = f"dims: [{line_dict['nrecs']}]"
    return line

@click.command()
@click.version_option(__version__)
@click.option('--verbose', '-v', is_flag=True, help="Print all attributes")
@click.argument('hdf_file',type=str,nargs=1)
def main(hdf_file,verbose):
    """
    print information about an hdf4 file

    Parameters
    ----------

    hdf_file: path or str to hdf data

    Returns
    -------

    side effect: printing the hdf_file info
    """
    hdf_path = Path(hdf_file).resolve()
    if not hdf_path.is_file():
        raise ValueError("could not fine {hdf_path}")
    hdfname=str(hdf_path)
    sd = sd_open_file(hdfname)
    hdf = HDF(hdfname, HC.READ)
    vs = hdf.vstart()
    v  = hdf.vgstart()
    attr_dict = read_swath_attributes(v,vs)
    ref = v.find('Data Fields')
    vg = v.attach(ref)
    members = vg.tagrefs()
    var_dict = dict()
    #
    # build a dictionary with all variable names
    #
    for tag, ref in members:
        # Vdata tag
        if tag == HC.DFTAG_VH:
            vd = vs.attach(ref)
            nrecs, intmode, fields, size, name = vd.inquire()
            # nrecs, intmode, fields, size, name = vd.inquire()
            # nrecs.append(vd.inquire()[0]) # number of records of the Vdata
            # names.append(vd.inquire()[-1])# name of the Vdata
            vd.detach()
            row_dict = dict(ref=ref,nrecs=nrecs,intmod=intmode,fields=fields,size=size)
            var_dict[name] = row_dict
        elif tag == HC.DFTAG_NDG:
            sds = sd.select(sd.reftoindex(ref))
            name, rank, dims, the_type, nattrs = sds.info()
            row_dict = dict(ref=ref,rank=rank,dims=dims,the_type=the_type,nattrs=nattrs)
            var_dict[name] = row_dict
            sds.endaccess()
    key_list = list(var_dict.keys())
    key_list.sort()
    for key in key_list:
        value = var_dict[key]
        dims = format_line(value)
        print(f"{key}: {dims}")
    if verbose:
        print("\nAttributes\n")
        pp.pprint(attr_dict)
    v.end()
    vs.end()
    sd.end()
    hdf.close()
