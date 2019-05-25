import sys
import h5py
import numpy as np
from math import sin, cos, pi
from scipy.integrate import dblquad

import pyrate.resources.plugins.background as bg
import pyrate.core.saig as saig

# Parameters
_params = dict(
            start=dict(),
            stop=dict(),
            load=dict(emiss=1.0),
            run=dict(),
            get=dict(),
    )

def progBar(cval, mval):
    pstr = '['
    prog = list('-'*48)
    chk = mval / 48
    loc = int(cval//chk)
    val = int(cval % chk / chk * 10)
    prog[:loc+1] = list('#'*loc)
    prog[loc] = str(val)
    out = '[' + ''.join(prog) + ']'
    sys.stdout.write('\r' + out)
    return
    

class Plugin(bg.BaseBgPlugin):

    def start(self):
        pass
    def stop(self):
        pass
    def load(self, emiss=1.0):
        self.downwell = bg.get_downwell()
        # Need to handle emissivity
        # Just gonna leave it as a GB for now
        if type(emiss)==int:
            self.emiss = emiss
        else:
            # need some sort of objec that initializes as follows:
            # self.emiss = emissObj(emiss_array, wnums_to_interpolate_onto)
            self.emiss = emiss * bg.get_wavenums()

    def run(self, **kwargs):
        # Do dbl integral here
        d2r = lambda d: pi*d / 180
        integrand = lambda az, zen, ii: self.downwell.get(zen,az)[ii]*cos(d2r(zen))*sin(d2r(zen))
        wnums = bg.get_wavenums()
        nchans = len(wnums)
        self.integrated_rad = np.empty((len(wnums)))
        for ii in range(nchans):
            progBar(ii, nchans)
            self.integrated_rad[ii] = dblquad(integrand,0,90,lambda y: 0,lambda y:360, args=(ii,))[0]
        _ = sys.stdout.write('\n')

    def get(self, **kwargs):
        # Convert to saig and then to background output class
        # Note that this works if emiss is spectral or not
        background = saig.dummySAIG(self.emiss*self.integrated_rad/pi)
        return background
