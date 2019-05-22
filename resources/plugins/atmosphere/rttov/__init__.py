import os
import docker
import h5py
import numpy as np
import atexit

import pyrate.resources.plugins.atmosphere as atm
from pyrate.resources import DOCK_CLIENT 
import pyrate.resources.plugins.atmosphere.rttov.app.interface as ri


# ---------- Module Vars ---------- #

# Mount points
MOUNT_DIR_HOST = os.path.dirname(os.path.abspath(__file__)) + '/app'
MOUNT_DIR_CLIENT = '/usr/src/app'

# Data directory
DATA_DIR = '{}/{}'.format(MOUNT_DIR_HOST, ri.DATA_DIR)

# Parameters
_params = dict(
            start=dict(args=dict(),kwargs=dict(inst=None)),
            stop=dict(args=dict(),kwargs=dict()),
            load=dict(args=dict(prof='prof0',res=0),kwargs=dict()),
            run=dict(args=dict(),kwargs=dict()),
            get=dict(args=dict(),kwargs=dict(fname=None)),
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

    def start(self, *args, **kwargs):
        """Initialize the system."""
        # Load session settings next
        cmd = 'init' if ('inst' not in list(kwargs.keys())) \
                else 'init {}'.format(kwargs['inst'])
        self._send_cmd(cmd)
        return

    def stop(self, *args, **kwargs):
        """Manually stop the system. Will remove the Docker Container as well."""
        self._send_cmd('exit')
        return

    def load(self, *args, **kwargs):
        """Load profile data.
        This can be done by moving the necessary data to a shared directory
        (mounted with the 'bind' option) and sending a command to load it.
        """
        profile, resolution = args
        # print('{} {}'.format(profile, resolution))
        # self._send_cmd('load {}'.format(profile, resolution))
        cmd = 'load {} {}'.format(profile, resolution)
        self._send_cmd(cmd)
        return

    def run(self, *args, **kwargs):
        """Run the plugin.
        Runs whatever is set up. Make sure to place output data in the shared
        directory.
        """
        self._send_cmd('run')
        return

    def get(self, *args, **kwargs):
        """Grab the data saved in the shared directory.
        Convert it to the necessary format specified by BaseAtmosphere.
        """
        fname = 'data' if ('fname' not in list(kwargs.keys())) \
                else kwargs['fname']
        # Grab data from the specified output file
        self._send_cmd('save {}'.format(fname))
        atm_kwargs = {}
        with h5py.File('{}/{}.h5'.format(DATA_DIR, fname),'r') as tf:
            for key in atm.Atmosphere.required_attributes:
                atm_kwargs[key] = np.array(tf[key])
        # Initialize the output
        return atm.Atmosphere(**atm_kwargs)
