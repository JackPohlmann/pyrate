"""
Initialization script to import system.

Need to keep track of:
    1)  Material
    2)  Atm Profile
"""

import os

import pyrate.core
import pyrate.resources

# ---------- Shorthands ---------- #
# Functions
def plug_params(module, plugin):
    return pyrate.resources.plugins.params(*[module, plugin])
# Keys
plug_key = pyrate.core.plug_key
input_key = pyrate.core.input_key
atm_key = 'atmosphere'
bg_key = 'background'
targ_key = 'target'
# Recipe template
template = {
        plug_key: {
                atm_key: '',
                bg_key: '',
                targ_key: '',
            },
        input_key: {
                atm_key: pyrate.resources.plugins._params,
            },
    }

default = {
        plug_key: {
                atm_key: 'rttov',
                bg_key: 'lambertian',
                targ_key: '2d',
            },
        input_key: {
                atm_key: plug_params(atm_key, 'rttov'),
            },
    }


class namedDict():
    """Dictionaries with naming convention built in.

    Items can be called or set using the traditional dictionary method 
    dict[key] = value or can be done using the object named convention
    dict.key = value.
    """
    def __init__(self, **d):
        self.__dict__ = d
        return
    
    def keys(self):
        return list(self.__dict__.keys())

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        return

            
class Recipe(namedDict):
    """PyRATE recipe object."""
    def __init__(self, *args):
        base = args[0] if args else default
        super().__init__(**base)
        # Plugins
        self[plug_key] = namedDict(**self[plug_key])
        # Inputs
        self[input_key] = namedDict(**self[input_key])
        for key in self[input_key].keys():
            self[input_key][key] = namedDict(**self[input_key][key])
        return
    def loadDefaultInputs(self):
        """Load the default plugin inputs."""
        for key in self[plug_key].keys():
            defs = plug_params(key, self[plug_key][key])
            for cmd in self[input_key][key].keys():
                self[input_key][key][cmd] = defs[cmd]
        return
    def run(self):
        """Runs the PyRATE simulation."""
        pass
