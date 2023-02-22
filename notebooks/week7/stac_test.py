import numpy
from pathlib  import Path
from sat_lib.landsat.landsat_metadata import landsat_metadata
import inspect
from pystac_client import Client
from shapely.geometry import Point


the_dir = Path() / "landsat_scenes"
the_file = list(the_dir.glob("**/*2015*MTL.txt"))[0]
the_meta = landsat_metadata(the_file)
# for item in inspect.getmembers(the_meta):
#     print(item)
#     #print(f"{item}: {getattr(the_meta,item).default('NA')}")

# connect to the STAC endpoint
cmr_api_url = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD"
client = Client.open(cmr_api_url)

# setup search
search = client.search(
    collections=["HLSL30.v2.0"],
    intersects=Point(-123.120, 49.2827),
    datetime="2015-06-01/2015-06-30"
) # nasa cmr cloud cover filtering is currently broken: https://github.com/nasa/cmr-stac/issues/239
# retrieve search results
items = search.get_all_items()
print(len(items))
print(list(items))





