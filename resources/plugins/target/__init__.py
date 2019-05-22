import importlib as il

import pyrate.resources.plugins as plugins
from pyrate.core.target import BaseTarget 


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
    global plugMod
    plugMod = il.import_module('.'.join([__name__, plugname]))
    global Plugin
    Plugin = plugMod.Plugin()
    Plugin.start(**kwargs)
    return

def params(plugin):
    """Use the plugins.params function to return plugin parameters."""
    return plugins.params(*['target', plugin])
