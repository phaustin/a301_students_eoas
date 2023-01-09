# ---
# jupyter:
#   jupytext:
#     notebook_metadata_filter: all,-language_info,-toc,-latex_envs
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import datetime
from pathlib import Path

import numpy as np
import pytz
import rasterio
import seaborn as sns

# %%
from matplotlib import pyplot as plt
from skimage import exposure, img_as_ubyte

# %%
import a301_lib  # noqa

pacific = pytz.timezone("US/Pacific")
date = datetime.datetime.today().astimezone(pacific)
print(f"written on {date}")

# %% [markdown]
# (rasterio_png)=
# # Making a png image
#
# In the cells below I read in bands 3, 4 and 5 from the
# `vancouver_345_refl.tiff` that was produced by the
# {ref}`rasterio_3bands` notebook. and convert it to a png file so
# I can look at it with standard image viewers.   I use "histogram equalization"
# from the scikit-image library to boost the color contrast in each of the bands.  I
# check the histograms using the jointplot function from the seaborn plotting library
# that adds a lot of nice features to matplotlib.  The new normailzed bands are put
# together to make a "false color composite" that shows vegetation as purple.


# %%
notebook_dir = Path().resolve().parent
print(notebook_dir)
week10_scene = notebook_dir / "week10/vancouver_345_refl.tiff"

with rasterio.open(week10_scene) as van_raster:
    b3_refl = van_raster.read(1)
    chan1_tags = van_raster.tags(1)
    b4_refl = van_raster.read(2)
    chan2_tags = van_raster.tags(2)
    b5_refl = van_raster.read(3)
    chan3_tags = van_raster.tags(3)
    crs = van_raster.profile["crs"]
    transform = van_raster.profile["transform"]
    tags = van_raster.tags()
print(tags, chan1_tags)

# %% [markdown]
# ## Note the low reflectivity for band 3

# %%
plt.imshow(b3_refl)

# %% [markdown]
# * Below I do some joint histograms of band3 vs. band 4 to get a feeling for the distribution

# %%
sns.jointplot(
    x=b3_refl.flat,
    y=b4_refl.flat,
    xlim=(0, 0.2),
    ylim=(0.0, 0.2),
    kind="hex",
    color="#4CB391",
)

# %%
sns.jointplot(
    x=b4_refl.flat,
    y=b5_refl.flat,
    kind="hex",
    xlim=(0, 0.3),
    ylim=(0.0, 0.5),
    color="#4CB391",
)

# %% [markdown]
# * I'm okay with changing the data values to get a qualitative feeling
#   for the image.  To do this, I can use the scikit-image equalization module
#   See this doc for more information: https://scikit-image.org/docs/dev/auto_examples/color_exposure/plot_equalize.html

# %%
channels = np.empty([3, b3_refl.shape[0], b3_refl.shape[1]], dtype=np.uint8)
for index, image in enumerate([b3_refl, b4_refl, b5_refl]):
    stretched = exposure.equalize_hist(image)
    channels[index, :, :] = img_as_ubyte(stretched)

# %%
plt.imshow(channels[0, :, :])

# %% [markdown]
# https://seaborn.pydata.org/generated/seaborn.jointplot.html

# %%
the_data = {"band3": channels[0, ...].flat, "band4": channels[1, ...].flat}
sns.jointplot(
    x="band3",
    y="band4",
    data=the_data,
    xlim=(0, 255),
    ylim=(0.0, 255),
    kind="hex",
    color="#4CB391",
)

# %% [markdown]
# ## Write out the png
#
# Now that I have 3 bands scaled from 0-255, I can write them out as
# a png file, with new tags

# %%
png_filename = notebook_dir / "week10/vancouver_345_stretched.png"
num_chans, height, width = channels.shape
with rasterio.open(
    png_filename,
    "w",
    driver="PNG",
    height=height,
    width=width,
    count=num_chans,
    dtype=channels.dtype,
    crs=crs,
    transform=transform,
    nodata=0.0,
) as dst:
    chan_tags = [
        "LC8_Band3_refl_counts",
        "LC8_Band4_refl_counts",
        "LC8_Band5_refl_counts",
    ]
    dst.update_tags(**tags)
    dst.update_tags(written_on=str(datetime.date.today()))
    dst.update_tags(history="written by scene_image.md")
    dst.write(channels)
    keys = ["3", "4", "5"]
    for index, chan_name in enumerate(keys):
        chan_name = f"band_{chan_name}"
        valid_range = "0,255"
        dst.update_tags(index + 1, name=chan_name)
        dst.update_tags(index + 1, valid_range=valid_range)

# %% [markdown]
# ## View the image
#
# Here's the finished image -- since Band 4 is the wavelength that
# plants use for photosynthesis, it's reflectivity values are
# very low for vegetated pixels.  Only Band 3 (green now mapped to blue) and
# Band 5 (near-ir now mapped to red) are reflecting, which makes purple.
#
#
# Image(filename=png_filename, width="80%")
