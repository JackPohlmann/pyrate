import sys
import h5py
import numpy as np
from math import sin, cos, pi
from scipy.integrate import dblquad

import pyrate.resources.plugins.target as targ
import pyrate.core.saig as saig
from pyrate.resources.dependencies.math import d2r
from pyrate.resources.dependencies.radiometry import planck
from pyrate.core.keys import targ_key, proj_key

# Parameters
_params = dict(
            start=dict(),
            stop=dict(),
            load=dict(emiss=1.0, coverage=0.2, temp=300.0),
            run=dict(),
            get=dict(),
    )

class Plugin(targ.BaseTargPlugin):

    def start(self):
        pass
    def stop(self):
        pass
    def load(self, emiss=1.0, coverage=0.2, temp=330.0):
        self.downwell = targ.get_downwell()
        # Need to handle emissivity
        # Just gonna leave it as a GB for now
        if type(emiss) in [int, float]:
            self.emiss = emiss
        else:
            # need some sort of objec that initializes as follows:
            # self.emiss = emissObj(emiss_array, wnums_to_interpolate_onto)
            self.emiss = emiss * targ.get_wavenums()
        self.refl = 1 - self.emiss
        self.coverage = coverage
        self.temp = temp
        return

    def run(self,):
        # Do dbl integral here
        integrand = lambda az, zen, ii: self.downwell.get(zen,az)[ii]*cos(d2r(zen))*sin(d2r(zen))
        wnums = targ.get_wavenums()
        nchans = len(wnums)
        dblquad_args = (integrand,0,90,lambda y: 0,lambda y:360,)
        # Integrate the sky radiance
        # Skip if target is a BB
        if np.any(self.emiss!=1):
            # Try to get it from the background
            bg = targ.get_background()
            if '_integrated_rad' in bg.__dict__.keys():
                self.integrated_rad = bg._integrated_rad
            # Otherwise just integrate it
            else:
                self.integrated_rad = np.empty((nchans))
                for ii in range(nchans):
                    sys.stdout.write('\r\tIntegration... {:.2f}%'.format((ii+1)/nchans*100))
                    self.integrated_rad[ii] = dblquad(*dblquad_args, args=(ii,))[0]
            print()
        # Set to zeros if BB -- could be anything
        else:
            self.integrated_rad = np.zeros((nchans,))
        self.emitted = planck(wnums, self.temp)
        return

    def get(self, **kwargs):
        # Convert to saig and then to background output class
        # Note that this works if emiss is spectral or not
        target = saig.dummySAIG(lambda zen, az: \
                    self.refl*self.integrated_rad/pi + \
                    self.emiss*self.emitted)
        proj = saig.dummySAIG(lambda zen, az: cos(d2r(zen)) * self.coverage)
        return targ.Target(**{targ_key:target, proj_key:proj})
