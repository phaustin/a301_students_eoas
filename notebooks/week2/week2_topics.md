# Week 2

* Learning objectives

  - Understand how to measure monochromatic radiance 
  
  - Begin image analysis of a Modis Channel 30 image

* Review from Week 1

  * Read Stull Chapter 2 through page 38
  
    - Main conceptual topic:  the definiton of radiative flux (section 2.2 plus {ref}`beerslaw`)

  * Intro to Jupyter

## Week 2 topics for Monday

   * make sure your image is working with {ref}`modis_level1b`

   * Review: Sections 4 and 5 of Kazarinoff:  Python REPL and datatypes

* Syncing your notebooks to the current github commit

- As I make changes to the notebooks, I'll push them to the github repository
  at https://github.com/phaustin/a301_students_eoas

- You can see my commit history: https://github.com/phaustin/a301_students_eoas/commits/main

- To bring those commits into your local repository, do the following:

          cd ~/repos/a301_students_eoas
          conda activate a301
          git status

  You should see the following line:

          nothing to commit, working tree clean

  If not, then you need to move the files you've changed out of this repository into your work folder
  because all changes will be overwritten in the next step.  First fetch the changes

          git fetch

  Then reset to include the changes (note there are two dashes in front of hard)

          git reset --hard origin/main

  You should see the commit message from my last commit -- to print the last three commits

          git log -3

* Introduce: Stull Chapter 2 pages 36-42 on the Planck function (eq. 2.13), 
  Stefen-Boltzman (eq: 2.15), inverse square law 

## Week 2 topics for  Wednesday: 

- Read my {ref}`radiance` notes.  -- key idea: how does a satellite camera
actually make the measurement -- it uses a photon counter,
wavelength filter, shutter timer, telescope.  You need to know 
the area of the photon counter, the width of the  wavelength filter,
the total exposure time of the shutter to
turn photon counts into radiance with units of $W\,m^{-2}\,\mu m^{-1}\,sr^{-1}$

- Finish the discussion of the {ref}`modis_level1b` notebook. By the end of class everyone should have this working on their own image.

- Read for Friday:  {ref}`flux_from_radiance`

- Do for Friday {ref}`sec:planck`

- Go over [Kazarinoff Chapter    8](https://phaustin.github.io/Problem-Solving-with-Python/Functions-and-Modules/Introduction.html)


## Week 2 topics for Friday: 

* Introduce:

   * {ref}`assign1`
   * {ref}`sec:debugging`  
   * {ref}`sec:numpy`  
   * {ref}`sec:planck`  
