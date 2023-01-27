
# Week 3

## Week 3 learning goals

- read and plot Modis Aqua brightness temperature data

- Use the cartopy module to put that data on a map

## Week 3 topics for Monday

* Get through question 2 in {ref}`assign1`

* Download the lat/lon of your pixels at full resolution by doing the following
  search on https://ladsweb.modaps.eosdis.nasa.gov/
  
  - Go to data -> find data -> filename search
  - Enter the first part of you image name in the following format:
  
       MYD03.A2013222.2105*
       
    replacing my date and time with yours

* Introduce coordinate systems {ref}`week3:coords`

  - For Wednesday, read pages 1-24 of [Understanding map projections](https://drive.google.com/file/d/1araPnZwMui9tBTPyLO_UHVC2DDEIdZ0p/view?usp=sharing) 

## Week 3 topics for Wednesday

- Finish up {ref}`assign1`

  - Troubleshooting 1:  note that when you do 
  
         data_dir = a301_lib.sat_data / 'pha'
         latlons = np.load( data_dir / 'lonlat.npz')
         
    You get back a dictionary-like object that will give you its keys:
    
         print(list(latlons.keys()))
         
  - Troubleshooting 2: Python caches imports, so if you make changes
    to `planck_invert.py`, you won't see these changes when you rerun the
    cell, unless you restart the kernel and rerun

- Reading the geometry data:  {ref}`modis_geom`

- Making a map with {ref}`cartopy`

- [What is your map projection?](https://xkcd.com/977/)


## Week 3 topics for Friday

- Finish up {ref}`assign1`

- Sanity check your radiances using my {ref}`radiance_check` notebook

- Continue on making a map with {ref}`cartopy`

## For Monday

- Read Stull chapter 2 p. 42 and Stull chapter 8 p. 219-226

- Continue on creating a notebook that sets the cartopy extent to the 4 corners of your Modis granule


## new references

### Resources for NumPy

1. Nice short complement to text book reading:
   [Introducing numpy arrays](https://pythonnumericalmethods.berkeley.edu/notebooks/chapter02.07-Introducing_numpy_arrays.html)

2. More extensive documentation:  
   [numpy user guide](https://numpy.org/doc/stable/user/)

###  Resources for Matplotlib

1. [Visualization and plotting]( https://pythonnumericalmethods.berkeley.edu/notebooks/chapter12.00-Visualization-and-Plotting.html)

2. [Matlab user tutorial](https://matplotlib.org/stable/tutorials/introductory/usage.html)

