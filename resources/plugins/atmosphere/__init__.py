import importlib as il

import resources.plugins as plugins
from core.atmosphere import BaseAtmosphere


class BaseAtmPlugin(plugins.BasePlugin):
    """Base class for atmosphere plugin.
    Good place for storing shared variables.
    """
    pass


class Atmosphere(BaseAtmosphere):
    """Official return class."""
    def __init__(self, **kwargs):
        for key in super().required_attributes:
            setattr(self, key, kwargs[key])
        super().__init__()
        return


def load(plugname, **kwargs):
    """Load a plugin."""
    modpath = 'resources.plugins.atmosphere.'
    global plugMod
    plugMod = il.import_module(''.join([modpath, plugname]))
    global Plugin
    Plugin = plugMod.Plugin()
    Plugin.start(**kwargs)
    return

def params(plugin):
    """Use the plugins.params function to return plugin parameters."""
    return plugins.params(*['atmosphere', plugin])
