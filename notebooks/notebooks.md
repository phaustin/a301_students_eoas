# List of notebooks

* {ref}`sec:numpy`
* {ref}`sec:planck`
* {ref}`modis_level1b`
* {ref}`week4:coords`
* {ref}`week4:resample`
* {ref}`scale_heights`
* {ref}`pandas_intro`
* {ref}`level2_wv`
* {ref}`vancouver_visible`
* {ref}`landsat_wrs`
  - find path/row for your scene
* {ref}`landsat1`
  - uses path/row from {ref}`landsat_wrs`
  - writes `week9/landsat_scenes` folder with TIF files  from AWS
* {ref}`landsat2`
  - uses B4.TIFF and B5.TIFF from {ref}`landsat1`
* {ref}`image_zoom`
  - clips an image to 600 rows x 400 cols and produces `week10/small_file.tiff`
* {ref}`rasterio_3bands`
  - uses the affine transform from `small_file.tiff` to clip 3 bands to same window using
    rasterio.Window
  - writes a new 3-band geotiff `week10/vancouver_345_refl.tiff`
* {ref}`rasterio_png`
  - reads `vancouver_345_refl.tiff` and creates a rgb false color png file
    with histogram equalization called `week10/vancouver_345_stretched.png`
* {ref}`vancouver_hires`
  - Reads `week10/vancouver_345_refl.tiff` band 5 and overlays an openstreetmap coastline map
* {ref}`rasterio_3bandsII`
  - repeats the cropping of {ref}`rasterio_3bands` using a fiona/geopandas box shape and
    rasterio.mask
* {ref}`feature_demo`
* {ref}`subset_map`
   - produces geojson files on /home/jovyan with feature subsets
* {ref}`stull-radar-app`
* {ref}`heating-rate-profile`
* {ref}`cloudsat-reflec`

## Assignment solutions

* {ref}`assign1_sol`
* {ref}`assign2_sol`
* {ref}`assign3_solution`
* {ref}`assign4_hydro_sol`
* {ref}`assign5asol`
* {ref}`assign5b_sol`
* {ref}`assign6a-solution`
* {ref}`assign6b_sol`
* {ref}`assign6c_marshall_sol`
* {ref}`assign7a-solution`
* {ref}`assign7b-solution`
