---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: -all
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Course folders on a301hub and your laptop

## a301hub

The jupyterhub at  [https://a301hub.eoasubc.xyz](https://a301hub.eoasubc.xyz) launches a container for each user
that has four folders:

1. `/home/jovyan/course_notebooks`  -- this is a read only copy of the files in [github repository](https://github.com/phaustin/a301_students_eoas/tree/main/notebooks) 
that are used to build the [course website](https://eoasubc.xyz/a301_2022/notebooks/index.html)

2. `/home/jovyan/sat_data` -- this is a shared folder where you should put your
   hdf and npz files that are neede by your notebook.  Because it is shared,
   you should make a folder with your initials, e.g.`~/sat_data/pha` (remember
   that `~` here means the home directory of user jovyan) to keep
   your files separate.  The initials don't matter but they should unique for this
   class.
   
3. `/home/jovyan/shared_files` -- this is a place to put material you want to share
   with either myself or the class -- for example a notebook that is exhibiting
   what you think is a bug.  
   
4. `/home/jovyan/work` -- this is a folder that is inside your individual container,
   and that only you can see.  This is where your assignments should go, at least
   before they are due and the answers have been posted.
   
## Your laptop

To keep things consistent, you need to make a folder on your laptop to hold the
satellite data that is identical to the a301hub location, so you can run exactly 
the same notebook on your laptop and on the hub.  Here is the way to use
uses the [pathlib](https://realpython.com/python-pathlib) module to create the folder, using the `a301_lib.sat_data` path that I defined in [a301_lib](https://github.com/phaustin/a301_students_eoas/blob/main/src/a301_lib/a301_lib/__init__.py)


```{code-cell} ipython3
from pathlib import Path
import a301_lib
print(f"the path to the data is {a301_lib.sat_data}")
```

### Make a folder (could also do this with finder/explorer)

```{code-cell} ipython3
sat_folder = a301_lib.sat_data / "pha"
sat_folder.mkdir(exist_ok=True,parents=True)
```

### Open this folder to read satellite data files

If you open your data using the `sat_folder` path above, then it will work both on
your laptop, and on a301hub where I'll run the autograder.  Here's how to find an hdf file 
and open it, assuming that your hdf file also has the date/time string `2013222.2150`

```{code-cell} ipython3
my_data = a301_lib.sat_data / "pha"
print(my_data)
the_files = list(my_data.glob("*2013222.2105*hdf"))
print("here is the list of files (should be only 1 file")
print(the_files)
print("here is the file extracted from the list")
print(the_files[0])
```

If the filename is simple, you can just hardcode it:

```{code-cell} ipython3
my_latlons = a301_lib.sat_data / "pha/lonlat.npz"
```

### Why do we need to wrap in a list()

`pathlib.glob` could potentially return a list with thousands of files,
using up memory.  To avoid this, python made this method an *iterator*, which means that it returns its contents one item at a time, unless
you turn it into a list.  Creating a list with an iterator drains the
iterator of its contents and puts them into the new variable.
