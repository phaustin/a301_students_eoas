import numpy as np
from skimage import exposure, img_as_ubyte
import xarray


def make_false_color(the_ds, band_names):
    """
    given a landsat dataset created by get_landsat_datascene, return
    a histogram-equalized false color image with rgb mapped
    to the bands in the order they appear in the list band_names

    example usage:

    landsat_654 = make_false_color(the_ds,['B06','B05','B04'])

    Parameters
    ----------

    the_ds: xarray.DataSet
       output og get_landsat_datascene -- must contain at least 3 bands and Fmask
    band_names: list[str]
       list of strings with the names of the bands to be mapped to red, green and blue
    """
    #
    # create an empty array with the same shape as Fmask
    #
    the_ds = the_ds.squeeze()
    Fmask = the_ds["Fmask"].data
    rgb_names = ["band_red", "band_green", "band_blue"]
    scene_dict = dict()
    for the_rgb, the_band in zip(rgb_names, band_names):
        # print(f"{the_rgb=}, {the_band=}")
        scene_dict[the_rgb] = the_ds[the_band]
    crs = the_ds.rio.crs
    transform = the_ds.rio.transform()
    bool_mask = np.empty_like(Fmask, dtype=np.int8)
    #
    # Below is True for all nan pixels
    #
    nan_mask = np.isnan(Fmask)
    #
    # flip this with logical_not so good pixels
    # are flagged True
    #
    good_mask = np.logical_not(nan_mask)
    #
    # assign 0 to nans, 1 to good values
    #
    bool_mask[nan_mask] = 0
    bool_mask[good_mask] = 1
    # print("Hello II")
    # print(f"{scene_dict.keys()=}")
    for key, image in scene_dict.items():
        # print(f"{key=}")
        scene_dict[key] = exposure.equalize_hist(image.data, mask=bool_mask)
    # print(f"{bool_mask.shape=}")

    nrows, ncols = bool_mask.shape
    band_values = np.empty([3, nrows, ncols], dtype=np.uint8)
    for index, key in enumerate(rgb_names):
        stretched = scene_dict[key]
        band_values[index, :, :] = img_as_ubyte(stretched)

    keep_attrs = ["cloud_cover", "date", "day", "target_lat", "target_lon"]
    all_attrs = the_ds.attrs
    attr_dict = {key: value for key, value in all_attrs.items() if key in keep_attrs}
    attr_dict["history"] = "written by make_false_color"
    attr_dict["landsat_rgb_bands"] = band_names
    band_nums = [int(item[-1]) for item in band_names]
    coords = {"band": band_nums, "y": the_ds["y"], "x": the_ds["x"]}
    dims = ["band", "y", "x"]
    # print(f"{dims=}")
    # print(f"{band_values.shape=}")
    false_color = xarray.DataArray(
        band_values, coords=coords, dims=dims, attrs=attr_dict
    )
    false_color.rio.write_crs(crs, inplace=True)
    false_color.rio.write_transform(transform, inplace=True)
    return false_color
