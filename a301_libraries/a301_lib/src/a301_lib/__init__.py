from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
import sys
home_dir = Path().home()
work_dir = home_dir / 'work'
data_share = home_dir / 'shared_files'
sat_data = home_dir / 'sat_data'

try:
    __version__ = version("a301_lib")
except PackageNotFoundError:
    __version__ = "unknown version"

try:
    from ._version import version_tuple
except ImportError:
    version_tuple = (0, 0, "unknown version")

print("in a301_lib init")
