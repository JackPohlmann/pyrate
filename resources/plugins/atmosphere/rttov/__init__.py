import os
import docker
import h5py
import numpy as np
import math
import atexit
import warnings

import pyrate.resources.plugins.atmosphere as atm
from pyrate.resources import DOCK_CLIENT 
import pyrate.resources.plugins.atmosphere.rttov.app.interface as ri
from pyrate.core.saig import SAIG


# ---------- Module Vars ---------- #

# Mount points
MOUNT_DIR_HOST = os.path.dirname(os.path.abspath(__file__)) + '/app'
MOUNT_DIR_CLIENT = '/usr/src/app'

# Data directory
DATA_DIR = '{}/{}'.format(MOUNT_DIR_HOST, ri.DATA_DIR)

# Parameters
_params = dict(
            start=dict(inst=None),
            stop=dict(),
            load=dict(profile='prof0',resolution=2,sun_angles=(45,180)),
            run=dict(),
            get=dict(fname='data'),
    )


# Clean up
def clean():
    for f in os.listdir(DATA_DIR):
        if f.endswith('.h5'):
            os.remove(os.path.join(DATA_DIR,f))
    return


class Plugin(atm.BaseAtmPlugin):
    """Rttov plugin."""
    image = 'jpohlmann93/rttov:latest'
    run_cmd = 'bash -c "python ./rttov.py < controller"'

    def __init__(self):
        """Use this to initialize the docker container."""
        self.container = DOCK_CLIENT.containers.run(self.image,
                command=self.run_cmd,
                detach=True,
                remove=True,
                volumes={MOUNT_DIR_HOST:{'bind':MOUNT_DIR_CLIENT,'mode':'rw'}})
        self.container.exec_run('bash -c "cat > controller"', detach=True)
        atexit.register(self.stop)
        return

    def _send_cmd(self, cmd):
        """Send command to the python CMD within the container.
        If used manually the Docker container will eject if an unsupported 
        command is used."""
        cmd = 'bash -c "echo {} > controller"'.format(cmd)
        _ = self.container.exec_run(cmd) 
        return

    def start(self, inst=None):
        """Initialize the system."""
        # Load session settings next
        cmd = 'init' if not inst else 'init {}'.format(inst)
        self._send_cmd(cmd)
        return

    def stop(self, **kwargs):
        """Manually stop the system. Will remove the Docker Container as well."""
        self._send_cmd('exit')
        return

    def load(self, profile='prof0', resolution=1, sun_angles=(45,180)):
        """Load profile data.
        This can be done by moving the necessary data to a shared directory
        (mounted with the 'bind' option) and sending a command to load it.

        resolution: number of rays per 90 degrees
        NOTE: res=10 uses approx 48Gb of memory. res=5 uses approx 12Gb.
          This is all done using IASI (8461 channels) on the highest fidelity
          setting (4), so the memory usage can be expected to be towards the
          higher end. Still, need to keep an eye on this.
        """
        # if resolution>5:
        #     rws = 'Resolutions greater than 5 result in significant memory usage.'
        #     warnings.warn(rws)
        #     print('A resolution of 5 may use up to 12 Gb of memory.')
        #     while pyrate.WARNINGS:
        #         ans = input("Continue? [y/n] ")
        #         if ans=='y':
        #             break
        #         elif ans=='n':
        #             raise RuntimeError("Rejected load.")
        #         else:
        #             print("Unkown input.")
        sun_zen, sun_az = sun_angles
        cmd = 'load {} {} {} {}'.format(profile, resolution, sun_zen, sun_az)
        self._send_cmd(cmd)
        return

    def run(self, **kwargs):
        """Run the plugin.
        Runs whatever is set up. Make sure to place output data in the shared
        directory.
        """
        self._send_cmd('run')
        return

    def get(self, fname='data'):
        """Grab the data saved in the shared directory.
        Convert it to the necessary format specified by BaseAtmosphere.
        """
        fpath = '{}/{}.h5'.format(DATA_DIR, fname)
        # Clear out file if it's already there
        if fname + '.h5' in os.listdir(DATA_DIR):
            os.remove(fpath)
        # Grab data from the specified output file
        self._send_cmd('save {}'.format(fname))
        atm_kwargs = {}
        while True:
            try:
                with h5py.File(fpath,'r') as tf:
                    for key in atm.Atmosphere.required_attributes:
                        atm_kwargs[key] = np.array(tf[key])
                break
            except OSError:
                # Wait until file is there
                pass
        # Calc resolution
        reso = atm_kwargs[atm.saig_keys[0]].shape[0]
        reso = int(math.sqrt(reso/4))
        # Separate these two just in case
        ddim = atm_kwargs[atm.saig_keys[0]].shape[-1]
        for key in atm.saig_keys:
            dgrid = atm_kwargs[key].reshape((reso, 4*reso, ddim))
            atm_kwargs[key] = SAIG(dgrid, (0,90), (0,360))
        # Initialize the output
        return atm.Atmosphere(**atm_kwargs)
