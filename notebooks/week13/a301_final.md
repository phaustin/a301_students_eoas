---
jupytext:
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.7.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(a301_final)=
# A301 final exam

Due midnight, Friday Dec. 11 -- for part 1: leave a notebook in your home folder with your name and
the word "final".  For part 2 I'll set up a gradescope assignment for upload.

## Part 1  (30 points)

1. Rerun the {ref}`landsat1` notebook with a new date to download a second image with the same landsat
   WRS path,row as your first.  Choose a different season, so that your NDVI index will
   change between the two images.

2. Modify the {ref}`rasterio_3bandsII` notebook to read in the B4, B5 and MTL files from
   both images.  (To keep things organized, I called my first image `sceneA` and my second
   image `sceneB` and used those variable names as shortcuts to the full filenames, e.g. sceneA_b5,
   etc.  I stored everything in a dictionary with the scene names as keys.)

3. As before, use rasterio.mask to crop to your 600 row x 400 column polygon so that the two cropped images
   have the same affine_transform and can be compared pixel by pixel.  Calculate the B4 and B5 reflectivities
   and save those  (I added them to my dictionary).

4. Calculate the ndvi for both cropped scenes and plot the B4, B5 and ndvi images using imshow with
   palettes that use vmin and vmax set the appropriate levels. You don't have to bother with adding
   the colorbars to
   the individual images if you don't want, but print out your choices for vmin and vmax along with the image.
   Use `plt.subplots(2,2)` to get a matrix of 4 subplots to save space, and delete
   the unused fourth axis with fig.delaxes(the_ax)

5. Plot a histogram of the difference (ndiff = ndviA - ndviB).

6. Find the row and column with the maximum absolute value of ndiff using the following numpy functions:

         index=np.argmax(ndiff)
         rowmax, colmax =np.unravel_index(index,ndiff.shape)

   Find and print out the longitude and latitude of this pixel.

7. Make a map of the ndiff image using cartopy, and locate the maximum ndiff pixel on the map with a red dot.

+++

## Part 2 (30 points)

Hand in scanned pages using gradescope

[a301_final_2020.pdf](https://drive.google.com/file/d/1C0wPYDu4a4WwCBCpi9skSyxDetub21Tl/view?usp=sharing)
