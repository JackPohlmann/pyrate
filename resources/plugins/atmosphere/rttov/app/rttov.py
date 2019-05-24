import os
import h5py
import numpy as np
from cmd import Cmd

import pyrttov
import interface as ri


# ---------- User Variables ---------- #
# These should be changed upon adding functionality to the plugin.

# Supported instruments; check Readme for how to integrate more
INSTRUMENTS = {
                'iasi': "rtcoef_rttov12/rttov9pred101L/rtcoef_metop_2_iasi.H5",
                'iasi_so2': "rtcoef_rttov12/rttov9pred101L/rtcoef_metop_2_iasi_so2.H5",
        }


# ---------- Environment Variables ---------- #

# Installation path for rttov
RTTOV_INSTALL_DIR = os.environ['RTTOV_INSTALL_DIR'] 
# Shared directory
DATA_DIR = ri.DATA_DIR
# Profile directory
PROFILE_DIR = ri.PROFILE_DIR


class rttovEnvironment(Cmd):
    """rttovEnvironment
    Command prompt wrapper for PyRTTOV.
    """
    def do_exit(self, opt):
        """Exit the environment."""
        return True

    def do_init(self, opt):
        """Initialize the Rttov object. Optionally accepts instrument as input."""
        self.instrument = opt if opt else 'iasi'
        # Set up Rttov object
        self.Rttov = pyrttov.Rttov()
        if self.instrument in list(INSTRUMENTS.keys()):
            self.Rttov.FileCoef = INSTRUMENTS[self.instrument]
        else:
            self.Rttov.FileCoef = self.instrument
        # Set options
        self.Rttov.Options.AddInterp = True
        self.Rttov.Options.InterpMode = 4 #4 is highest fidelity, 5 is all-around
        self.Rttov.Options.VerboseWrapper = 0
        self.Rttov.Options.StoreTrans = True
        self.Rttov.Options.StoreRad2 = True
        # Load instrument
        self.Rttov.loadInst()
        return

    def do_load(self, inp):
        """Load an atmospheric profile. Requires inputs for data and resolution."""
        # Convert resolution into a number of profiles
        data, resolution, sun_zen, sun_az = inp.split()
        resolution = int(resolution)
        sun_zen = int(sun_zen)
        sun_az = int(sun_az)
        # Load the data
        data = h5py.File("{}/{}.h5".format(PROFILE_DIR, data), 'r')
        nlevels = len(np.array(data['P']))
        # Set up the profiles
        nprofs = 4*resolution*resolution
        self.Profiles = pyrttov.Profiles(nprofs, nlevels)
        # Set the profile data
        probs = ['GasUnits', 'Skin']
        for key in [key for key in list(data.keys()) if key not in probs]:
            setattr(self.Profiles, key, np.tile(data[key],(nprofs,1)))
            # print('{}\t{}'.format(key, getattr(self.Profiles, key).shape))
        setattr(self.Profiles, 'GasUnits', int(np.squeeze(data['GasUnits'])))
        setattr(self.Profiles, 'Skin', np.tile(list(data['Skin']) + [0],(nprofs,1)))
        # Set angles
        ang_arr = np.empty((resolution, 4*resolution, 4))
        # RTTOV can only handle up to 85 degrees for v9 predicators, otherwise 75
        # zen_leg = 85/resolution if '9pred' in self.Rttov.FileCoef else 75/resolution
        zen_leg = 90/resolution
        az_leg = 90/resolution
        for zen in range(resolution):
            for az in range(4*resolution):
                ang_arr[zen, az] = [zen_leg*zen, az_leg*az, sun_zen, sun_az]
        setattr(self.Profiles, 'Angles', ang_arr.reshape((nprofs,4)))
        # print(self.Profiles.Angles)
        # Load the profiles
        self.Rttov.Profiles = self.Profiles
        return

    def do_run(self, opt):
        """Run the model."""
        self.Rttov.runDirect()
        return

    def do_save(self, opt):
        """Save the data. Optionally accepts name as input ."""
        fname = opt if opt else 'data'
        with h5py.File('{}/{}.h5'.format(DATA_DIR, fname),'w') as tf:
            for key in ri.keys:
                tf[key] = np.copy(ri.get_fromKey[key](self.Rttov))
        return


# Run the command loop
rttovEnvironment().cmdloop()
