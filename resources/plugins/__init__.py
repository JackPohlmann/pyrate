import abc
import importlib as il

# Load a plugin
def load(module, plugin, **kwargs):
    tmp = il.import_module('.'.join([__name__, module]))
    return tmp.load(plugin, **kwargs)

# Run a plugin
def run(plugin, params):
    """General function for running a plugin."""
    plugin.load(**params['load'])
    plugin.run(**params['run'])
    return plugin.get(**params['get'])


# Parameter template
"""Add to each plugin."""
_params = dict(
            start=dict(),
            stop=dict(),
            load=dict(),
            run=dict(),
            get=dict(),
    )

# Return parameters
def params(*args):
    if not args:
        return _params
    elif len(args)==1:
        tmp = il.import_module('.'.join([__name__, args[0]]))
    else:
        module, plugin = args
        tmp = il.import_module('.'.join([__name__, module, plugin]))
    return tmp._params
    


class BasePlugin(abc.ABC):
    """Base class for RASPy plugin."""

    @abc.abstractmethod
    def start(self, **kwargs):
        """Start the plugin."""
        pass

    @abc.abstractmethod
    def stop(self, **kwargs):
        """Stop the plugin."""
        pass

    @abc.abstractmethod
    def load(self, **kwargs):
        """Load inputs."""
        pass

    @abc.abstractmethod
    def run(self, **kwargs):
        """Run the plugin."""
        pass

    @abc.abstractmethod
    def get(self, **kwargs):
        """Return the output."""
        pass
