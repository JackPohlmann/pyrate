import abc
import importlib as il

# Load a plugin
def load(module, plugin):
    tmp = il.import_module('.'.join([__name__, module]))
    tmp.load(plugin)
    return

# Run a plugin
def run(plugin, params):
    """General function for running a plugin."""
    plugin.load(list(params['load']['args'].values()),params['load']['kwargs'])
    plugin.run(list(params['run']['args'].values()),params['run']['kwargs'])
    return plugin.get(list(params['get']['args'].values()),params['get']['kwargs'])


# Parameter template
"""Add to each plugin."""
_params = dict(
            start=dict(args=dict(),kwargs=dict()),
            stop=dict(args=dict(),kwargs=dict()),
            load=dict(args=dict(),kwargs=dict()),
            run=dict(args=dict(),kwargs=dict()),
            get=dict(args=dict(),kwargs=dict()),
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
