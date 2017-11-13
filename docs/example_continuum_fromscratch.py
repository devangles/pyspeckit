Creating a Spectrum from scratch
================================

.. include:: <isogrk3.txt>

This example shows the initialization of a pyspeckit object from numpy arrays.

.. code-block:: python

   import numpy as np
   import pyspeckit

   xaxis = np.linspace(-50,150,100.)
   sigma = 10.
   center = 50.

   baseline = np.poly1d([0.1, 0.25])(xaxis)

   synth_data = np.exp(-(xaxis-center)**2/(sigma**2 * 2.)) + baseline

   # Add noise
   stddev = 0.1
   noise = np.random.randn(xaxis.size)*stddev
   error = stddev*np.ones_like(synth_data)
   data = noise+synth_data

   # this will give a "blank header" warning, which is fine
   sp = pyspeckit.Spectrum(data=data, error=error, xarr=xaxis,
                           xarrkwargs={'unit':'km/s'},
                           unit='erg/s/cm^2/AA')

   sp.plotter()

   sp.specfit.Registry.add_fitter('polycontinuum',
                                  pyspeckit.models.polynomial_continuum.poly_fitter(),
                                  2)

   sp.specfit(fittype='polycontinuum', guesses=(0,0), exclude=[30, 70])

   # subtract the model fit to create a new spectrum
   sp_contsub = sp.copy()
   sp_contsub.data -= sp.specfit.get_full_model()
   sp_contsub.plotter()

   # Fit with automatic guesses
   sp_contsub.specfit(fittype='gaussian')

   # Fit with input guesses
   # The guesses initialize the fitter
   # This approach uses the 0th, 1st, and 2nd moments
   amplitude_guess = data.max()
   center_guess = (data*xaxis).sum()/data.sum()
   width_guess = data.sum() / amplitude_guess / np.sqrt(2*np.pi)
   guesses = [amplitude_guess, center_guess, width_guess]
   sp.specfit(fittype='gaussian', guesses=guesses)

   sp.plotter(errstyle='fill')
   sp.specfit.plot_fit()

