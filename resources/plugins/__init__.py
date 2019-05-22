import abc
import importlib as il


def runPlugin(plugin, params):
    """General function for running a plugin."""
    plugin.load(params['load']['args'],params['load']['kwargs'])
    plugin.run(params['run']['args'],params['run']['kwargs'])
    return plugin.get(params['get']['args'],params['get']['kwargs'])


# Parameter template
"""Add to each plugin."""
_params = { 
        'start': {'args':[],'kwargs':{}},
        'stop': {'args':[],'kwargs':{}},
        'load': {'args':[],'kwargs':{}},
        'run': {'args':[],'kwargs':{}},
        'get': {'args':[],'kwargs':{}},
    }

# Return parameters
def params(*args):
    if not args:
        return _params
    elif len(args)==1:
        tmp = il.import_module('.'.join(['resources.plugins', args[0]]))
    else:
        module, plugin = args
        tmp = il.import_module('.'.join(['resources.plugins', module, plugin]))
    return tmp._params
    


class BasePlugin(abc.ABC):
    """Base class for RASPy plugin."""

    @abc.abstractmethod
    def start(self, *args, **kwargs):
        """Start the plugin."""
        pass

    @abc.abstractmethod
    def stop(self, *args, **kwargs):
        """Stop the plugin."""
        pass

    @abc.abstractmethod
    def load(self, *args, **kwargs):
        """Load inputs."""
        pass

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        """Run the plugin."""
        pass

    @abc.abstractmethod
    def get(self, *args, **kwargs):
        """Return the output."""
        pass
