import a301_lib
import numpy as np
from matplotlib import pyplot as plt
from pyhdf.SD import SD
from pyhdf.SD import SDC
from pathlib import Path
from contextlib import contextmanager
import os
import sys

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)

if  __name__ == "__main__":
    work_dir = Path(sys.argv[1]).resolve()
    if not work_dir.is_dir():
        raise ValueError(f"{str(work_dir)} doesn't exist")
    print(f"cd to {work_dir}")
    with cd(work_dir):
        all_files = list(work_dir.glob("*hdf"))
        print(f"found {all_files}")
        out_dir = Path()/"out_dir"
        out_dir.mkdir(parents=True, exist_ok=True)
        for a_file in all_files:
            print(f"reading {a_file}")
            str_file = str(a_file)
            the_sd = SD(str_file, SDC.READ)
            print(the_sd.info())
            datasets_dict = the_sd.datasets()
            for idx, sds in enumerate(datasets_dict.keys()):
                print(idx, sds)
            out=the_sd.attributes()
            print(list(out.keys()))


            

