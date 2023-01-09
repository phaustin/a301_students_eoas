

# Week 9

* Week 9 Shortwave remote sensing

  * What's complicated about longwave remote sensing:

    - emissivity and temperature of the atmosphere (and land surface) both unknown

  * What's complicated about shortwave remote sensing

    - scattering of solar photons depends on surface, cloud thickness, ice crystals etc.

  * New satellites:

    - MODIS shortwave channels:  [the Modis channel listing](https://modis.gsfc.nasa.gov/about/specifications.php)

    - [Calipso (Caliop lidar)](https://www-calipso.larc.nasa.gov/)  (part of the [A-train](https://cloudsat.atmos.colostate.edu/mission/formation_flying) )

    - [NASA Landsat page](https://www.nasa.gov/mission_pages/landsat/overview/index.html)

    - [Landsat overview](https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python/)

   * New software with a new data format ([geotif](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/fundamentals-raster-data/intro-to-the-geotiff-file-format/) )

    - [Earthpy](https://github.com/earthlab/earthpy) -- U. Colorado GIS notebooks

    - [autogis](https://automating-gis-processes.github.io/site/index.html) -- U. Helsinki GIS notebooks

   * For Wednesday: Read the [Landsat overview](https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/landsat-in-Python/) and
   the
[geotif explainer](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/fundamentals-raster-data/intro-to-the-geotiff-file-format/)

    - Review the Universal Transverse Mercator projection in
      [understanding map projections](https://drive.google.com/file/d/1araPnZwMui9tBTPyLO_UHVC2DDEIdZ0p/view?usp=sharing) (p. 21 and p. 98)

    - Make sure the {ref}`vancouver_visible` notebook works for you.

* Wednesday

  - New cells in the {ref}`vancouver_visible` notebook for the MYD02QM image
  - Introduce [OGR/GDAL](https://gdal.org/faq.html#:~:text=were%20integrated%20together.-,What%20does%20OGR%20stand%20for%3F,to%20OGR%20Simple%20Features%20Library.)  led by [Frank Warmerdam](https://creativecommons.org/2013/08/07/frank-warmerdam-leading-open-geospatial-community-by-action/) and [Fiona/Rasterio](https://sgillies.github.io/foss4g-2014-fiona-rasterio/#/) led by  [Sean Gilles](https://www.linkedin.com/in/sean-gillies-6064b4144)
  - links:
    - [Understanding landsat processing levels](https://www.usgs.gov/core-science-systems/nli/landsat/landsat-data-access?qt-science_support_page_related_con=0#qt-science_support_page_related_con)
    - [Landsat band combinations](https://gisgeography.com/landsat-8-bands-combinations/)
    - [qualitative image interpretation](https://earthobservatory.nasa.gov/features/ColorImage/page2.php)
    - [Landsat history](https://landsat.gsfc.nasa.gov/article/virginia-t-norwood-mother-landsat)

  - finding Landsat images
    - [The WRS coordinate system](https://gisgeography.com/landsat-file-naming-convention/)
    - {ref}`landsat_wrs` notebook
    - Getting images from [AWS using the USGS explorer](https://towardsdatascience.com/access-satellite-imagery-with-aws-and-google-colab-4660178444f5)

    - For Friday:

      - Use the links above to find a Landsat 8 image somewhere on the earth that is:

        - on land
        - less than 20% cloud cover
        - Undergoes some kind of change over a 5 year period -- either seasonal cycles, logging, forest fires etc.
        - Upload the full image filename on piazza
        - Register for a [USGS earth explorer account](https://earthexplorer.usgs.gov/)
        - If you're interested sign up for an [AWS free tier account](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc) (requires credit or debit card)


* Friday

  - go over the {ref}`landsat1` notebook
  - go over the {ref}`landsat2` notebook

  - for Monday -- make both notebooks work for your Landsat image
