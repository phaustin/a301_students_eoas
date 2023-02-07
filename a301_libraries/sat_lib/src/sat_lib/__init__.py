from pathlib import Path
from .modis_chans import modischan_dict


from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sat_lib")
except PackageNotFoundError:
    __version__ = "unknown version"

try:
    from ._version import version_tuple
except ImportError:
    version_tuple = (0, 0, "unknown version")

print("in sat_lib init")
