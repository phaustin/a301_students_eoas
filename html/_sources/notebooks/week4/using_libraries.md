---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(week4:using_libraries)=
# Working with libraries

+++

We have been starting our notebooks with this command:

```{code-cell} ipython3
import a301_lib
```

This brings in code from [this file](https://github.com/phaustin/a301_students_eoas/blob/main/a301_libraries/a301_lib/src/a301_lib/__init__.py) which sets the path for a301_lib.sat_data etc.

+++

## New modules

+++

I've added two new libraries:

* [rad_lib](https://github.com/phaustin/a301_students_eoas/tree/main/a301_libraries/rad_lib/src/rad_lib)

* [sat_lib](https://github.com/phaustin/a301_students_eoas/tree/main/a301_libraries/sat_lib/src/sat_lib)

With functions that are listed at [https://phaustin.github.io/a301_web/index.html](https://phaustin.github.io/a301_web/index.html)

+++

## Installation

+++

To install, open a terminal and activate a301, then:

           cd ~/repos/a301_students_eoas
           pip install -r requirements.txt --upgrade

+++

## Command line program

+++

To use the `meta_read` command line function to read metadata, open
a terminal, do `conda activate a301` then 

           cd ~/sat_data/your_initials
           meta_read --help
           meta_read MYD*hdf

+++

## To use within a program

```{code-cell} ipython3
import a301_lib
from pathlib import Path
from sat_lib.modismeta_read import parseMeta
the_path = a301_lib.sat_data / "pha"
granules =list(the_path.glob("*hdf"))
parseMeta(granules[0])
```
