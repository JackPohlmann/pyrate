import h5py
import numpy as np

import pyrate.resources.plugins.target as targ

# Parameters
_params = dict(
            start=dict(args=dict(),kwargs=dict()),
            stop=dict(args=dict(),kwargs=dict()),
            load=dict(args=dict(),kwargs=dict()),
            run=dict(args=dict(),kwargs=dict()),
            get=dict(args=dict(),kwargs=dict()),
    )

class Plugin(targ.BaseTargPlugin):
    pass

