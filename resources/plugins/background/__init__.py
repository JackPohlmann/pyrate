import importlib as il

import pyrate.resources.plugins as plugins
from pyrate.core.background import BaseBackground 


class BaseBgPlugin(plugins.BasePlugin):
    """Base class for atmosphere plugin.
    Good place for storing shared variables.
    """
    pass


class Background(BaseBackground):
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
    return plugins.params(*['background', plugin])
