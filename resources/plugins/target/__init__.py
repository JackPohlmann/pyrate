import importlib as il

import pyrate.core
import pyrate.resources.plugins as plugins
from pyrate.core.target import BaseTarget 
from pyrate.core.keys import bg_key, targ_key, wav_key


# Plugins list
Plugins = []

def get_background():
    return pyrate.core.HDSTRUCT[bg_key]

def get_wavenums():
    return pyrate.core.HDSTRUCT[wav_key]


class BaseTargPlugin(plugins.BasePlugin):
    """Base class for atmosphere plugin.
    Good place for storing shared variables.
    """
    pass


class Target(BaseTarget):
    """Official return class."""
    def __init__(self, **kwargs):
        for key in super().required_attributes:
            setattr(self, key, kwargs[key])
        super().__init__()
        return


def load(plugname, **kwargs):
    """Load a plugin."""
    plugMod = il.import_module('.'.join([__name__, plugname]))
    global Plugins
    Plugins.append(plugMod)
    Plugin = plugMod.Plugin()
    Plugin.start(**kwargs)
    return Plugin

def params(plugin):
    """Use the plugins.params function to return plugin parameters."""
    return plugins.params(*['target', plugin])
