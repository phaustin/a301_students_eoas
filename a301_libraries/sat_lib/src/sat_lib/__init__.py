from pathlib import Path
from .modis_chans import modischan_dict
print("in sat_lib init")
root_dir = Path(__file__).resolve().parent
version_file= root_dir / 'VERSION_satlib.txt'
if not version_file.is_file():
    __version__ = 'no_version'
    try:
        with open(version_file,'w') as f:
            f.write(__version__)
    except:
        __version_file__=None
else:
    with open(version_file) as f:
        __version__=f.read().strip()

