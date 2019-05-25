"""
Initialization script to import system.

Need to keep track of:
    1)  Material
    2)  Atm Profile
"""

import os

import pyrate.core as _core
import pyrate.resources as _resources


# ---------- Shorthands ---------- #
# Functions
def plug_params(module, plugin):
    return _resources.plugins.params(*[module, plugin])
load_plug = _resources.plugins.load
# Keys
plug_key = _core.plug_key
input_key = _core.input_key
atm_key = _core.atm_key
bg_key = _core.bg_key
targ_key = _core.targ_key

# ---------- Global parameters ---------- #
Verbose = True


# ---------- Basic recipes ---------- #  
# Recipe template
template = {
        plug_key: {
                atm_key: '',
                bg_key: '',
                targ_key: '',
            },
        input_key: {
                atm_key: _resources.plugins._params,
            },
    }
# Default recipe
default = {
        plug_key: {
                atm_key: 'rttov',
                bg_key: 'lambertian',
                targ_key: '2d',
            },
        input_key: {
                atm_key: plug_params(atm_key, 'rttov'),
                bg_key: plug_params(bg_key, 'lambertian'),
                targ_key: plug_params(targ_key, '2d'),
            },
    }
simple = {
        plug_key: {
                atm_key: 'rttov',
                bg_key: 'lambertian',
            },
        input_key: {
                atm_key: plug_params(atm_key, 'rttov'),
                bg_key: plug_params(bg_key, 'lambertian'),
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
        self._formerPlugs = self[plug_key].copy()
        self[plug_key] = namedDict(**self[plug_key])
        # Inputs
        self[input_key] = namedDict(**self[input_key])
        for key in self[input_key].keys():
            self[input_key][key] = namedDict(**self[input_key][key])
        # Pre-initialize
        self.coreInst = 0
        self.Data = 0
        return

    def __del__(self):
        """Makes sure to stop the associated plugins."""
        for mod in self.coreInst.keys():
            self.coreInst[mod][plug_key].stop()
    
    def loadDefaultInputs(self):
        """Load the default plugin inputs."""
        for mod in self[plug_key].keys():
            defs = plug_params(mod, self[plug_key][mod])
            for cmd in self[input_key][mod].keys():
                self[input_key][mod][cmd] = defs[cmd]
        return
    
    def _gen_core_instructions(self):
        """Converts the Plugin/Input setup into instructions used by the core
        module."""
        tmp_coreInst = {}
        for mod in self[plug_key].keys():
            inputs = self[input_key][mod]
            tmp_coreInst[mod] = {}
            # Check for a newly loaded plugin
            if (self.coreInst and self[plug_key][mod]!=self._formerPlugs[mod]):
                self.coreInst[plug_key].stop()
                self._formerPlugs[mod] = self[plug_key][mod]
                plugObj = load_plug(mod, self[plug_key][mod], **inputs['start'])
            elif not self.coreInst:
                tmp_coreInst[mod] = {}
                plugObj = load_plug(mod, self[plug_key][mod], **inputs['start'])
            else:
                plugObj = self.coreInst[mod][plug_key]
            plugFunc = lambda inps: _resources.plugins.run(plugObj, inps)
            # tmp_coreInst[mod]['plugObj'] = plugObj
            tmp_coreInst[mod][plug_key] = plugObj
            tmp_coreInst[mod][input_key] = inputs
        self.coreInst = tmp_coreInst.copy()

    def run(self):
        """Runs the PyRATE simulation."""
        if not self.coreInst: self._gen_core_instructions()
        _core.init(self.coreInst)
        _core.run()
        self.Data = _core.HDSTRUCT.copy()
        _ = self.Data.pop('last')
        self.Data = namedDict(**self.Data)
        return

    def tree(self):
        for key0 in [plug_key,input_key]:
            print()
            print(key0)
            for key1 in self[key0].keys():
                print('|')
                print('+-- ' + key1, end='')
                if type(self[key0][key1])==namedDict:
                    print()
                    for key2 in self[key0][key1].keys():
                        print('|   |')
                        print('|   +-- ' + key2 + ' = ' + str(self[key0][key1][key2]))
                else:
                   print(' = ' + self[key0][key1]) 

