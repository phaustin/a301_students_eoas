# Week 1

## Week 1 learning objectives

* Define and using monochromatic blackbody flux (Stull equation 2.13)

* Install a working a301 environment on your laptop

* Clone the course notebooks to `~/repos/a301_eoas_students`

* Install the `a301_lib` python module using pip

* Download a Modis satellite image and plot the channel 30 image 


## Important links

* [Course canvas page](https://canvas.ubc.ca/courses/105407)

* [Course piazza page](https://piazza.com/class/lcoeg8tsp9zxq)

* Installation instructions and the environment.yml file on [Dropbox](https://www.dropbox.com/sh/uosacqkiw7f5rmk/AABKGhCMXXkI3Q21U49uFIEya?dl=0)

## For Wednesday's class

* Use the piazza link on canvas to sign up for an account

* Go to https://github.com and get a github account if  you don't have one.

* Send me a message on canvas with your github user id

* Read Stull Chapter 2 through page 38.  (https://www.eoas.ubc.ca/books/Practical_Meteorology/)

* Go over https://phaustin.github.io/Problem-Solving-with-Python/

* Get an account on https://open.jupyter.ubc.ca and go over Section 3   in https://phaustin.github.io/Problem-Solving-with-Python/ if you aren't familiar with how Jupyter notebooks work.

## For Friday's class

* For Friday: Read my {ref}`week2_beerslaw` notes

* Work through Kazarinoff Chapters 6 (Numpy) and 7 (Plotting)

* For class discussion 

  - why does python have both tuples and lists?

  - How do we measure flux?

###  More installation

* Installing libraries and notebooks: clone our course notebooks by doing the following in a shell:

        cd ~/repos/a301
        conda activate a301
        git clone https://github.com/phaustin/a301_students_eoas.git

        
* and then install our first library:  `a301_lib`

        pip install -r requirements.txt
        
### Downloading data
        
* Go over {ref}`satellite` 
        
* Introduce {ref}`modis_level1b`

## For Monday's class

1) Following the directions in {ref}`satellite`  pick a satellite scene and store it in ~/sat_data

2) Modify {ref}`modis_level1b` to plot Channel 30 for your scene

3) If you have trouble finding a scene, Friday's image is in the Dropbox folder at https://www.dropbox.com/sh/uosacqkiw7f5rmk/AABKGhCMXXkI3Q21U49uFIEya?dl=0


