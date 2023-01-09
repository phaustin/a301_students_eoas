.. include:: ../refs.txt

.. _testing:

Notes on testing
++++++++++++++++


Using numpy.testing to test functions
=====================================

The numpy testing module provides some functions to compare function calculations to
expected answers: http://docs.scipy.org/doc/numpy/reference/routines.testing.html

I have written some test examples in sat_lib.radiation.py. The code  includes the following test functions which use numpy.testing.assert_array_almost_equal to compare sample cases with known results:

.. highlight:: python
   :linenothreshold: 5



.. code-block:: python
   :linenos: 
   :emphasize-lines: 21

    def test_planck_wavelen():
        """
           test planck function for several wavelengths
           and Temps
        """
        #
        # need Temp in K and wavelen in m
        #
        the_temps=[200., 250., 350.]
        the_wavelens=np.array([8.,10.,12.])*1.e-6
        out=[]
        for a_temp in the_temps:
            for a_wavelen in the_wavelens:
                #
                # convert to W/m^2/micron/sr
                #
                the_bbr=Blambda(a_wavelen,a_temp)*1.e-6
                out.append(the_bbr)
        answer=[  0.4521,   0.8954,   1.1955,   2.7324,   3.7835,   3.9883,
                  21.4495,  19.8525,  16.0931]
        np.testing.assert_array_almost_equal(out,answer,decimal=4)
        return None

When the test is run by a program called `pytest <http://doc.pytest.org/en/latest/>`_ like this::

  pytest radiation.py

the file will be scanned for any functions with the word "test" (any capitalization)  and each test
will be run.  The test will succeed if the two arrays (out and answer) are the same at each index to within 4 decimal places.  If they aren't then an error message will be printed.


.. code-block:: python
   :linenos:
   :emphasize-lines: 24

    def test_planck_inverse():
        """
           test planck inverse for several round trips
           and Temps
        """
        #
        # need Temp in K and wavelen in m
        #
        the_temps=[200., 250., 350.]
        the_wavelens=np.array([8.,10.,12.])*1.e-6
        out=[]
        for a_temp in the_temps:
            for a_wavelen in the_wavelens:
                #
                # convert to W/m^2/micron/sr
                #
                the_bbr=Blambda(a_wavelen,a_temp)
                out.append((a_wavelen,the_bbr))

        brights=[]
        for wavelen,bbr in out:
            brights.append(planckInvert(wavelen,bbr))
        #
        # does planckInvert give us back the original temperatures?
        #
        answer=[200.0, 200.0, 200.0, 250.0, 250.0, 250.0, 350.0, 350.0, 350.0]
        np.testing.assert_array_almost_equal(brights,answer,decimal=10)
        return None

Similarly, this test will fail if any temperature is disagrees in the 10th decimal place or lower.        
        
Run tests with pytest
=====================

Once you've installed pytest (with conda install pytest), the tests can be run in two ways:

1.  Use pytest directly (the -v flag makes the output verbose)::

      $ pytest sat_lib/radiation.py -v
      
      ============================================= test session starts
      platform darwin -- Python 3.5.2, pytest-3.0.3, py-1.4.31, pluggy-0.4.0 -- /Users/phil/mini35/bin/python
      cachedir: .cache
      rootdir: /Users/phil, inifile: 
      plugins: hypothesis-3.4.2
      collected 2 items 

      repos/a301_2016/a301lib/radiation.py::test_planck_wavelen PASSED
      repos/a301_2016/a301lib/radiation.py::test_planck_inverse PASSED

      ============================================= 2 passed in 0.22 seconds

2. Execute the radiation.py module, which will run all the code that is below
   __name == "__main__" line:

   .. code-block:: python
      :linenos:
      :emphasize-lines: 1

        if __name__ == "__main__":
        #
        # the variable __file__ contains the name of this file
        # so the result of the following line will be the same as if
        # you typed:
        #
        # pytest ~/pythonlibs/a301lib/radiation.py -q
        #
        # in a terminal  (the -q means 'suppress most of output')
        #
        print('testing {}'.format(__file__))
        pytest.main([__file__, '-q'])
      

Why have two different ways to run the tests?  With approach 2) I don't need to
know where the module is, python finds it and runs it::

     $ python -m sat_lib.radiation
     testing sat_lib/radiation.py
     ..
     2 passed in 0.01 seconds
     ~  phil@rail%

Test failure
============

To see what happens when a test fails, try changing one of the expected answers
to an incorrect value

.. code-block:: python

        answer=[999.0, 200.0, 200.0, 250.0, 250.0, 250.0, 350.0, 350.0, 350.0]

Now run the test and look at the failure report::

  $ python -m sat_lib.radiation
    testing sat_lib/radiation.py
    .F
    ======================================= FAILURES =======================================
    _________________________________ test_planck_inverse __________________________________
    
        def test_planck_inverse():
            """
               test planck inverse for several round trips
               and Temps
            """
            #
            # need Temp in K and wavelen in m
            #
            the_temps=[200., 250., 350.]
            the_wavelens=np.array([8.,10.,12.])*1.e-6
            out=[]
            for a_temp in the_temps:
                for a_wavelen in the_wavelens:
                    #
                    # convert to W/m^2/micron/sr
                    #
                    the_bbr=Blambda(a_wavelen,a_temp)
                    out.append((a_wavelen,the_bbr))
        
            brights=[]
            for wavelen,bbr in out:
                brights.append(planckInvert(wavelen,bbr))
            answer=[999.0, 200.0, 200.0, 250.0, 250.0, 250.0, 350.0, 350.0, 350.0]
    >       np.testing.assert_array_almost_equal(brights,answer,decimal=10)
    E       AssertionError: 
    E       Arrays are not almost equal to 10 decimals
    E       
    E       (mismatch 11.111111111111114%)
    E        x: array([ 200.,  200.,  200.,  250.,  250.,  250.,  350.,  350.,  350.])
    E        y: array([ 999.,  200.,  200.,  250.,  250.,  250.,  350.,  350.,  350.])
    
    ../sat_lib/radiation.py:114: AssertionError
    1 failed, 1 passed in 0.06 seconds

