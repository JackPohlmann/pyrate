import h5py
import numpy as np
from scipy.integrate import dblquad

import pyrate.resources.plugins.background as bg

down_key = bg.down_key

# Parameters
_params = dict(
            start=dict(),
            stop=dict(),
            load={down_key:None},
            run=dict(),
            get=dict(),
    )

class Plugin(bg.BaseBgPlugin):

    def start(self):
        pass
    def stop(self):
        pass
    def load(self, **kwargs):
        downwell = kwargs[down_key]
        # When does downwell get turned into a SAIG?
        # Do dbl integral here
        
        pass
    def run(self, **kwargs):
        pass
