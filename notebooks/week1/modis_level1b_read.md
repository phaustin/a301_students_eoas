---
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info,-toc
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

(modis_level1b)=
# Reading modis level1b data

## Background

https://mcst.gsfc.nasa.gov/l1b/software-system-overview

https://modis.gsfc.nasa.gov/about/specifications.php

https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/intro-to-hdf4/

modis swath:  https://svs.gsfc.nasa.gov/3348

```{code-cell} ipython3
:trusted: true

import pprint
from pathlib import Path

import a301_lib
import numpy as np
from matplotlib import pyplot as plt
from pyhdf.SD import SD
from pyhdf.SD import SDC
from matplotlib.colors import Normalize
```

```{code-cell} ipython3
:trusted: true

print(a301_lib.sat_data)
type(a301_lib.sat_data)
```

## get all files from the data_dir that end in hdf

a301_lib.sat_data is a `PosixPath` object, which is the way that python is able to treat all folder paths the same, whether they look like `C:\Users\phil` or `/Users/home/phil`

There is only 1 hdf file in `sat_data`, so the cell below returns a list of length 1

```{code-cell} ipython3
:trusted: true

hdf4_dir = a301_lib.sat_data 
all_files = list(hdf4_dir.glob("*hdf"))
print(all_files)
```

Now read that file (converting PosixPath into a string since the pyhdf library is
expecting a string).  Use the `.info` method to get the number of datasets and attributes

```{code-cell} ipython3
:trusted: true

file_name = str(all_files[0])
print(f"reading {file_name}")
the_file = SD(file_name, SDC.READ)
stars = "*" * 50
print(
    (
        f"\n{stars}\n"
        f"number of datasets, number of attributes\n"
        f"={the_file.info()}\n"
        f"{stars}\n"
        f"\nHere is the help file for the info funtion:\n"
    )
)
#help(SD.info)
```

## Find the dataset and print their indices

We know we've got 31 datasets in the file -- what are their names?

```{code-cell} ipython3
:trusted: true

datasets_dict = the_file.datasets()

for idx, sds in enumerate(datasets_dict.keys()):
    print(idx, sds)

#breakpoint()
```

 ## open one of the datasets (number 4, EV_1KM_Emissive) and get its shape and data type
 
 The "Earth View Emissive" dataset contains all the longwave channels, and all the 2030 rows and 1354 columns for each
 pixel in each channel

```{code-cell} ipython3
:trusted: true

longwave_data = the_file.select("EV_1KM_Emissive")  # select sds
print(longwave_data.info())
```

## Get the first row of the first channel and find its numpy dtype

uint16 is "unsigned 16 bit integer", which is how the modis raw counts are stored.  By using
2 8-bit words (2 bytes) for each measurement they can represent (2**16)-1 = 65535 radiance values.  This means, however that every measurement has to be converted from uin16 to float32 before it
can be used

```{code-cell} ipython3
:trusted: true

data_row = longwave_data[0, 0, :]  # get sds data
print(data_row.shape, data_row.dtype)
```

## get all the rows and columns for the first channel

```{code-cell} ipython3
:trusted: true

longwave_data[0, :, :]
```

## Find the attributes for EV_1KM_Emissive

In order to make the conversion from int to float, we need to
multiply by a scale factor and subtract an offset.  These are
stored as attributes in the hdf file, and they are different
for each of the 16 channels.  Use `pprint` to pretty-print the big
dictionary.

```{code-cell} ipython3
:trusted: true

pprint.pprint(longwave_data.attributes())
```

## Print the first 1000 characters of the Metadata.0 string

Date, orbit number, etc. are stored in a long string attribute called 'StructMetadata.0'.
The \t character is a tab stop so the file is easier to read with an editor.

```{code-cell} ipython3
:trusted: true

pprint.pprint(the_file.attributes()["StructMetadata.0"][:1000])
```

## Now plot the data using imshow

Start over again and make a plot.  We need to be
able to identify particular bands  -- the channel numbers
are stored in the "Band_1KM_Emissive" dataset

```{code-cell} ipython3
:trusted: true

longwave_bands = the_file.select("Band_1KM_Emissive")
#
# close the file
#
longwave_bands.info()
```

```{code-cell} ipython3
:trusted: true

band_nums = longwave_bands.get()
print(f"here are the modis channels in the emissive dataset \n{band_nums}")
```

Note that only channels 20 to 36 are in the Emissive dataset (see [the Modis channel listing](https://modis.gsfc.nasa.gov/about/specifications.php))

+++

Note that only channels 20 to 36 are in the Emissive dataset (see [the Modis channel listing](https://modis.gsfc.nasa.gov/about/specifications.php))

+++

## find the index for channel 30

Count the items in the vector above and convince yourself that channel 30 is index 9, starting from 0

But there's a better way: use numpy.searchsorted to find the index with the closest value
to 30:

We also need to turn that index (type int64) into a plain python int so it can be used to specify the channel

```{code-cell} ipython3
:trusted: true

ch30_index = np.searchsorted(band_nums, 30.0)
print(f"make sure our index datatime in int64: {ch30_index.dtype}")
ch30_index = int(ch30_index)
print(f"channel 30 is located at index {ch30_index}")


# ## Read channel 30 at index 9 into a numpy array of type uint16
```

## Now get the data for channel 30

```{code-cell} ipython3
:trusted: true

ch30_data = longwave_data[ch30_index, :, :]
print(ch30_data.shape)
print(ch30_data.dtype)
#breakpoint()
```

Plot the channel 30 image

Use [imshow with a colorbar](https://matplotlib.org/gallery/color/colorbar_basics.html#sphx-glr-gallery-color-colorbar-basics-py)

```{code-cell} ipython3
:trusted: true

fig, ax = plt.subplots(1, 1, figsize=(10, 14))
CS = ax.imshow(ch30_data)
cax = fig.colorbar(CS)
ax.set_title("uncalibrated counts")
#
# add a label to the colorbar and flip it around 270 degrees
# (just my personal preference for labels)
#
out = cax.ax.set_ylabel("Chan 30 raw counts")
out.set_verticalalignment("bottom")
out.set_rotation(270)
print(ch30_data.shape)
```

## Now convert the raw counts to radiances

We need to find the right scale and offset for channel 30

+++

To turn the raw counts into pixel radiances, you need to apply equation 5.8 on p. 36 of the
[modis users guide](https://www.dropbox.com/s/ckd3dv4n7nxc9p0/modis_users_guide.pdf?dl=0):

$Radiances = (RawData - offset) \times scale$

We have just read the RawData,  the offset and the scale are stored in two vectors that are attributes of the Emissive dataset.  We'll make a version of the figure above, but plot Channel 30 radiance (in W/m^2/micron/sr), rather than raw counts.

```{code-cell} ipython3
:trusted: true

scales = longwave_data.attributes()["radiance_scales"]
offsets = longwave_data.attributes()["radiance_offsets"]
ch30_scale = scales[ch30_index]
ch30_offset = offsets[ch30_index]
print(f"scale: {ch30_scale}, offset: {ch30_offset}")
```

```{code-cell} ipython3
:trusted: true

ch30_calibrated = (ch30_data - ch30_offset) * ch30_scale
```

## Plot the Channel 30 radiances

Do these look right?  How would you tell?

```{code-cell} ipython3
:trusted: true

fig, ax = plt.subplots(1, 1, figsize=(10, 14))
vmin = 0.0
vmax = 10
the_norm = Normalize(vmin=vmin, vmax=vmax, clip=False)
CS = ax.imshow(ch30_calibrated,norm=the_norm)
cax = fig.colorbar(CS)
ax.set_title("Channel 30 radiance")
#
# add a label to the colorbar and flip it around 270 degrees
#
out = cax.ax.set_ylabel("Chan radiance $(W\,m^{-2}\,\mu m^{-1}\,sr^{-1})$")
out.set_verticalalignment("bottom")
out.set_rotation(270)
ch30_calibrated.shape
```

## Write the radiances out for safekeeping

Follow the example here: https://hdfeos.org/software/pyhdf.php

```{code-cell} ipython3
:trusted: true

# Create an HDF file
outname = "ch30_out.hdf"
sd = SD(outname, SDC.CREATE | SDC.WRITE | SDC.TRUNC)

# Create a dataset
sds = sd.create("ch30", SDC.FLOAT64, ch30_calibrated.shape)

# Fill the dataset with a fill value
sds.setfillvalue(0)

# Set dimension names
dim1 = sds.dim(0)
dim1.setname("row")
dim2 = sds.dim(1)
dim2.setname("col")

# Assign an attribute to the dataset
sds.units = "W/m^2/micron/sr"

# Write data
sds[:, :] = ch30_calibrated

# Close the dataset
sds.endaccess()

# Flush and close the HDF file
sd.end()
```

Did this work?  See if the file exists:

```{code-cell} ipython3
:trusted: true

hdf_files = list(Path().glob("*hdf"))
print(hdf_files)
```

## move all of this into a function

```{code-cell} ipython3
:trusted: true

file_name = str(all_files[0])
print(f"reading {file_name}")
the_file = SD(file_name, SDC.READ)
the_band=30

def readband(the_file,the_band):
    """
    read and calibrate a MODIS band from an open hdf4 SD dataset
    
    Parameters
    ----------
    
       the_file:pyhdf.SD object
           the dataset open for reading
       the_band: int
           band number for MODIS (1-36)
           
    Returns
    -------
       the_chan_calibrated: ndarray
           the pixel radiances in W/m^2/sr/micron
    """
    longwave_data = the_file.select("EV_1KM_Emissive")  # select sds
    longwave_bands = the_file.select("Band_1KM_Emissive")
    band_nums = longwave_bands.get()
    thechan_index = int(np.searchsorted(band_nums, the_band))
    print(thechan_index)
    thechan_data = longwave_data[thechan_index, :, :]
    scales = longwave_data.attributes()["radiance_scales"]
    offsets = longwave_data.attributes()["radiance_offsets"]
    thechan_scale = scales[thechan_index]
    thechan_offset = offsets[thechan_index]
    thechan_calibrated = (thechan_data - thechan_offset) * thechan_scale
    return thechan_calibrated

ch_radiance = readband(the_file,the_band)
from matplotlib import pyplot as plt
plt.hist(ch_radiance.flat)
plt.show()
```

## close the file

```{code-cell} ipython3
:trusted: true

the_file.end()
```
