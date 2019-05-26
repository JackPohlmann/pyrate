import sys
import h5py
import numpy as np
from math import sin, cos, pi
from scipy.integrate import dblquad

import pyrate.resources.plugins.background as bg
import pyrate.core.saig as saig
from pyrate.resources.dependencies.math import d2r
from pyrate.resources.dependencies.radiometry import planck
from pyrate.core.keys import bg_key


# Parameters
_params = dict(
            start=dict(),
            stop=dict(),
            load=dict(emiss=0.8),
            run=dict(),
            get=dict(),
    )
    

class Plugin(bg.BaseBgPlugin):

    def start(self):
        pass
    def stop(self):
        pass
    def load(self, emiss=0.8, temp=300.0):
        self.downwell = bg.get_downwell()
        # Need to handle emissivity
        # Just gonna leave it as a GB for now
        if type(emiss) in [int, float]:
            self.emiss = emiss
        else:
            # need some sort of objec that initializes as follows:
            # self.emiss = emissObj(emiss_array, wnums_to_interpolate_onto)
            self.emiss = emiss * bg.get_wavenums()
        self.refl = 1 - self.emiss
        self.temp = temp
        return

    def run(self,):
        # Do dbl integral here
        integrand = lambda az, zen, ii: self.downwell.get(zen,az)[ii]*cos(d2r(zen))*sin(d2r(zen))
        wnums = bg.get_wavenums()
        nchans = len(wnums)
        dblquad_args = (integrand,0,90,lambda y: 0,lambda y:360,)
        self.integrated_rad = np.empty((nchans))
        # self.integrated_rad = threaded_dblquad(nchans, *dblquad_args)
        for ii in range(nchans):
            sys.stdout.write('\r\tIntegration... {:.2f}%'.format((ii+1)/nchans*100))
            self.integrated_rad[ii] = dblquad(*dblquad_args, args=(ii,))[0]
        print()
        self.emitted = planck(wnums, self.temp)
        return

    def get(self, **kwargs):
        # Convert to saig and then to background output class
        # Note that this works if emiss is spectral or not
        background = saig.dummySAIG(lambda zen, az: \
                    self.refl*self.integrated_rad/pi + \
                    self.emiss*self.emitted)
        background._integrated_rad = self.integrated_rad
        return bg.Background(**{bg_key:background})
