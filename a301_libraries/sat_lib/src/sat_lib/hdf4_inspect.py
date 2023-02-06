import a301_lib
import click
from pyhdf.SD import SD
from pyhdf.SD import SDC
from pathlib import Path


@click.command()
@click.argument('hdf_file',type=str,nargs=1)
def main(hdf_file):
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
    the_sd = SD(str(hdf_path), SDC.READ)
    print(the_sd.info())
    datasets_dict = the_sd.datasets()
    print("\n\nDatasets\n\n")
    for idx, sds in enumerate(datasets_dict.keys()):
        print(idx, sds)
    out=the_sd.attributes()
    print("\n\nattributes\n\n")
    print(list(out.keys()))
