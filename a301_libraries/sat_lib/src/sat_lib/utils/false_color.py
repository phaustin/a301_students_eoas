def make_false_color(the_ds,band_names):
"""
given a landsat dataset created by get_landsat_datascene, return
a histogram equalized falxe color image with rgb mapped
to the bands in the order they appear in band_names
"""
    #
    # create an empty array with the same shape as Fmask
    #
    Fmask = the_ds['Fmask']
    bool_mask = np.empty_like(Fmask,dtype = np.int8)
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
    bool_mask
    stretched_dict = dict()
    keys = ['b3','b4','b5']
    images = [masked_b3, masked_b4, masked_b5]
    for key, image in zip(keys,images):
        stretched_dict[key] = exposure.equalize_hist(image.data, mask = bool_mask )
        #
        # uncomment to try this without the mask
        #
        # stretched_dict[key] = exposure.equalize_hist(image.data)
    band_names=['B05','B04','B03']
    keep_attrs = ['cloud_cover','date','day','target_lat','target_lon']
    all_attrs = bands_543.attrs
    attr_dict = {key: value for key, value in all_attrs.items() if key in keep_attrs}
    attr_dict['history']="written by false_color.md"
    attr_dict["landsat_rgb_bands"] = band_names
    false_color=xarray.DataArray(band_values,coords=coords,
                                dims=dims,
                                attrs=attr_dict)
    false_color.rio.write_crs(b3.rio.crs, inplace=True)
    false_color.rio.write_transform(b3.rio.transform(), inplace=True);
