"""
The ``core`` module houses functions that assist in data formatting, input sanitation,
path manipulations, file naming, logical checks, etc for use in other functions within
dnppy. They are short and sweet, and can be used as examples to start defining your own functions!
"""

__author__ = ["jwely",
              "lmakely",
              ]

# local imports
from .run_command import run_command, _flatten_args
from .create_outname import create_outname
from .enf_filelist import *
from .enf_list import *
from .exists import *
from .list_files import *
from .move import *
from .rename import *
from .install_from_wheel import *
