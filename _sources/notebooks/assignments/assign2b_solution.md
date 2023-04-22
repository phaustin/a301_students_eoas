---
celltoolbar: Create Assignment
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
toc-autonumbering: true
---

(assign2b_solution)=
# Assignment 2b solutions: Drawing your satellite swath

Adapt the code in the week4/cartopy_mapping_vancouver.md notebook to show the boundary of your Modis
swath on a Lambert Azimuthal Equal Area map.

+++

## Edit this cell to fetch your granual

```{code-cell} ipython3
:trusted: true

import a301_lib
import warnings
warnings.filterwarnings('ignore')
hdf4_dir = a301_lib.sat_data / "pha"
granules = list(hdf4_dir.glob("MYD02*2105*hdf"))
print(granules[0])
```

```{code-cell} ipython3
:trusted: true

from sat_lib.modismeta_read import parseMeta
granules =list(hdf4_dir.glob("MYD02*2105*hdf"))
print(granules[0].is_file())
meta_dict = parseMeta(granules[0])
meta_dict
```

*  What's in the file?

+++

**This cell sets up the datum and the LAEA projection, with the tangent point at the center of your swath**

```{code-cell} ipython3
:trusted: true

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy
import numpy as np
#
# Datum: radius of the earth in meters
#
radius = 6_371_228

#
# vancouver longitude, latitude indegrees
#
van_lon, van_lat = [-123.1207, 49.2827]
#
# use a simple sphere as the datum
#
globe = ccrs.Globe(ellipse=None, semimajor_axis=radius, semiminor_axis=radius)
geodetic = ccrs.Geodetic()
#
# set up
#
projection = ccrs.LambertAzimuthalEqualArea(
    central_latitude=meta_dict['lat_0'], central_longitude=meta_dict['lon_0'], globe=globe
)
print(f"pro4 program params: {projection.proj4_params}")
```

## Problem 1a -- project your `lon_list` and `lat_list` corners

In the cell below, get two new lists -- a list of x coordinates and a list of y coordinates
that contain the projected coordinates of your swath corners from `meta_dict['lon_list']`
and `meta_dict['lat_list']`

I used a loop and projection.transform_point to transform from geodetic to the projection coordinates.

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-e33700dda7266e50
  locked: false
  points: 2
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGIN SOLUTION
out_x = []
out_y = []
for lon, lat in zip(meta_dict['lon_list'], meta_dict['lat_list']):
    x, y = projection.transform_point(lon,lat,geodetic)
    out_x.append(x)
    out_y.append(y)
out_x.append(out_x[0])
out_y.append(out_y[0])
### END SOLUTION

out_x, out_y
```

### Bonus Vector version: projection.transform_points

Here's a way to tranform arrays of points instead of looping over individual points.  It takes a crs,
an np.array of lons, an np array of lats, and optionally an np.array of heights and returns a 2d numpy
array with the xcoord,ycoord,zcoord for each point

```{code-cell} ipython3
:trusted: true

help(projection.transform_points)
```

Note you get the same answer as with `projection.transform_point`

```{code-cell} ipython3
:trusted: true

lons = np.array(meta_dict['lon_list'])
lats = np.array(meta_dict['lat_list'])
projection.transform_points(geodetic,lons,lats)
```

## Problem 1b -- find your ll_x, ll_y, ur_x and ur_y

Find the lower left and upper right corners of your extent by finding the maximum and minimum y values.
Save these in the variables ll_x, ll_y, ur_x, ur_y

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-9b7fdb2acda2f474
  locked: false
  points: 1
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGΙΝ SOLUTION
ll_x = min(out_x)
ll_y = min(out_y)
ur_x = max(out_x)
ur_y = max(out_y)
### END SOLUTION
```

## Problem 2 -- make the map

Following the cartopy plotting examples, set your map extent in the projected coordinates
with `ax.set_extent` and make a map showing your swath outline as a red rectangle

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: cell-84941f707ad5283f
  locked: false
  points: 3
  schema_version: 3
  solution: true
  task: false
trusted: true
---
### BEGIN SOLUTION
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": projection})
#
# clip with 0,0 in the center:  [xleft, xright, ybot, ytop]
#
new_extent = [ll_x, ur_x, ll_y, ur_y]
ax.set_extent(new_extent, projection)
#
# the simple lon,lat projection is called "geodetic"
#
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
ax.plot(ll_x,ll_y,'ro',markersize=20)
ax.plot(ur_x, ur_y,'ro',markersize=20)
ax.plot(out_x,out_y,'r-',markersize=40)
### END SOLUTION
```

## Bonus problem

Put the location of `(min_lon,min_lat)` and `(max_lon, max_lat)` on the map as blue dots, with the corners
of the extent we used above as red dots.

```{code-cell} ipython3
:trusted: true

ll_corner = (meta_dict['min_lon'], meta_dict['min_lat'])
ur_corner = (meta_dict['max_lon'], meta_dict['max_lat'])
newll_x, newll_y = projection.transform_point(ll_corner[0], ll_corner[1], geodetic)
newur_x, newur_y = projection.transform_point(ur_corner[0], ur_corner[1], geodetic)
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw={"projection": projection})
#
# enlarge the extent to show the max,min lat, lon points on the map
#
new_extent = [1.4*ll_x, 1.2*ur_x, 1.4*ll_y, 1.1*ur_y]
ax.set_extent(new_extent, projection)
#
# the simple lon,lat projection is called "geodetic"
#
ax.gridlines(linewidth=2)
ax.add_feature(cartopy.feature.GSHHSFeature(scale="coarse", levels=[1, 2, 3]))
ax.plot(ll_x,ll_y,'ro',markersize=20)
ax.plot(ur_x, ur_y,'ro',markersize=20)
ax.plot(ll_x,ur_y,'ro',markersize=20)
ax.plot(ur_x, ll_y,'ro',markersize=20)


ax.plot(out_x,out_y,'r-',markersize=40)

#
# now plot blue dots for the min,max lon/lats
#
ax.plot(newll_x,newll_y,'bo',markersize=20)
ax.plot(newur_x,newur_y,'bo',markersize=20)
ax.plot(newll_x,newur_y,'bo',markersize=20)
ax.plot(newur_x,newll_y,'bo',markersize=20);
```

The combination of the skewed swath and the curved longitude and latitude lines means that you get the wrong extent
if you use min,max lon/lat to set your corners -- it will clip your swath at the bottom and the right side.
