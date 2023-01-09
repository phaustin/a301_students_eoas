---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(landsat_wrs)=
# Landsat: finding wrs path/row

This notebook runs the code that is discussed in this tutorial:
https://www.earthdatascience.org/tutorials/convert-landsat-path-row-to-lat-lon/

```{code-cell} ipython3
import io
import ogr
import shapely.wkt
import shapely.geometry
import urllib.request
import zipfile
#
# first time: download_file=True will
# go to amazon and get vector shape files for
# all the WRS path-row sectors
#
download_file=True
if download_file:
    url = "https://prd-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/WRS2_descending_0.zip"
    r = urllib.request.urlopen(url)
    zip_file = zipfile.ZipFile(io.BytesIO(r.read()))
    zip_file.extractall("landsat-path-row")
    zip_file.close()
shapefile = 'landsat-path-row/WRS2_descending.shp'
wrs = ogr.Open(shapefile)
layer = wrs.GetLayer(0)
lon = -123  # Vancouver lon deg E
lat = 49   # Vancouver lat deg N
point = shapely.geometry.Point(lon, lat)
mode = 'D'  # look for descending (daytime) image
```

* this functions checks to see whether a lat/lon point falls within
  a particular WRS sector (feature)

```{code-cell} ipython3
def checkPoint(feature, point, mode):
    geom = feature.GetGeometryRef() #Get geometry from feature
    shape = shapely.wkt.loads(geom.ExportToWkt()) #Import geometry into shapely to easily work with our point
    if point.within(shape) and feature['MODE']==mode:
        return True
    else:
        return False
```

* loop over all features until you find the one that
  contains the point, then print the path/row

```{code-cell} ipython3
i=0
while not checkPoint(layer.GetFeature(i), point, mode):
    i += 1
feature = layer.GetFeature(i)
path = feature['PATH']
row = feature['ROW']
print('Path: ', path, 'Row: ', row)
```
