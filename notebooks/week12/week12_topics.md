
# Week 12

* Monday topics

  - Review {ref}`subset_map`

  - By tonight (midnight) for Assignment 6b in {ref}`assignments`:

    - save your notebook in a301_lib.data_share, with your name and "assign6b"
      in the file name (no spaces).  It does not matter what folder below data_share you
      put it in, as long as I can find it with `.glob("**/*assign6b*")`.
      I'll log in as you and run the notebook from that folder.

  - Read {ref}`notes_on_radar` along with Stull pages 245-248 for {ref}`assign6c` and come
    prepared to talk about the discussion questions.

    1) Why does the returned power decrease as $1/R^2$ and not the roundtrip spreading of $1/R^4$ ?

    2) We have "hardwired" in a wavelength of 10 cm, a beam width of 0.95 deg, etc.
       which is specific to the WSR-88D radar.  We
       are also assuming that we are using the same antenna to receive and to transmit

    3) Transmitted power is 750,000 Watts, Received power can be as low as $10^{-15}$ Watts

    4) Suppose you are given $Z_1$ in $mm^6\,m^{-3}$, c in m/s,
       $\Delta t$ in s and $\lambda$ in cm.  How do you convert
       $Z_1 c  \Delta t/\lambda^2$ to $km^2$?

    5) The reflectivity goes down as b and K increase and goes up as
       $L_a$ and R increase -- explain.

    6) Why is the width of the radar sample volume proportional to $\Delta t/2$
       instead of $\Delta t$ ?

  - Go over the radar equation (Stull 8.28, p. 246)

    * {ref}`stull-radar-app`

  - Introduce

    * {ref}`heating-rate-profile`

- Topics for this week:

    - For Wednesday: Read this [mission description](https://cloudsat.atmos.colostate.edu/mission/)
      and [instrument description](https://cloudsat.atmos.colostate.edu/instrument)

    - For next Wednesday 10am:

      - Modify {ref}`heating-rate-profile` so that you calculate and store the
            temperature profile as a function of time by computing

          $$
          T(t + \Delta t) = T(t) + \frac{dT}{dt} \Delta t
          $$

        for each level, integrating forward in 1 hour timesteps $\Delta t$ until the atmosphere's
        temperature profile stops changing.  (We'll turn this into an
        animation)

      - Write out a geotiff and png file for your Modis level2 water vapor retrieval from
        {ref}`assign5asol`, changing the crs
        given by `swath_def.compute_optimal_bb_area` (which is specfic to your particular scene)
        to a new laea projection with a central latitude and longitude and bounding box
        that could work
        for multiple scenes.  That is, write out a new geotiff that uses pyresample with a
        new  crs and and area extent that, instead of looking something like this:

        ```
          dump area definition:
          Area ID: laea_otf
          Description: On-the-fly laea area
          Projection: {'datum': 'WGS84', 'lat_0': '39.4580671712606',
            'lon_0': '-121.464976619873',
            'no_defs': 'None', 'proj': 'laea', 'type': 'crs',
            'units': 'm', 'x_0': '0', 'y_0': '0'}
          Number of columns: 499
          Number of rows: 448
          Area extent: (-1238434.2527, -1155685.6368, 1529176.4655, 1278445.1434)

          x and y pixel dimensions in meters:
          5546.3140647124765
          5433.327634487678
        ```

        using the laea projection, but with
        a `lat_0` and `lon_0` of -121 deg E and 39 deg N. and and an area extent that corresponds
        to corner latitudes and longitudes that need to be specified to at most 3 decimal places.
        (although the transformed corner x,y values in laea coords will still require 11 digits
        to specify)

    - Friday

      * Regridding assignment notebook: {ref}`assign7a`

      * Radiative equilibrium assignment notebook: {ref}`assign7b`
