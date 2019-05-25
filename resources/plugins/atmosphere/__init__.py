import importlib as il

import pyrate.resources.plugins as plugins
from pyrate.core.atmosphere import BaseAtmosphere, saig_keys

# Use saig_keys to tell plugins which outputs need to be SAIGS

# Keeps track of loaded atm plugins
Plugins = []

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
    plugMod = il.import_module('.'.join([__name__, plugname]))
    global Plugins
    Plugins.append(plugMod)
    Plugin = plugMod.Plugin()
    Plugin.start(**kwargs)
    return Plugin

def params(plugin):
    """Use the plugins.params function to return plugin parameters."""
    return plugins.params(*['atmosphere', plugin])
