# PyRate Plugins
# Author:   Jack Pohlmann
# Date:     August 2019
# 
# Manage PyRate plugins.

import abc


def installPlugin(plugin,name=None,fpath='.',test=True):
    """Install a new plugin to pyrate.
    Run this from within the plugin to be installed."""
    # Copy file to the pyrate plugins folder.
    if test: testPlugin(plugin)
    pass


def testPlugin(plugin):
    """Test the validity of a plugin."""
    # What does this do at this point?
    # Test this against actual data? --> % error or tolerance
    pass


# class Installer(abc.ABC):
#     """Pyrate Plugin installer class."""
#     def __init__(self,*args,**kwargs):
#         for key,value in kwargs.items():
#             setattr(self,key,value)
#         return
#         
#     def install(self):
#         """Install the plugin specified by the installer object."""
#         pass


class BasePlugin(abc.ABC):
    """Abstract PyRate Plugin class."""

    # TODO: Find a good way to implement the priority system.
    #
    # Current idea~~
    # This could be simplified to two digits.
    # 0-9:       Preprocessing
    # 10-19:     Independent data generation (atmosphere,source)
    # 20-29:     Dependent on <20 priority
    # 30-39:     Dependent on <30 priority
    # X0-X9:     Dependent on <X0 priority
    # 90-99:     Postprocessing
    # 100+:      Unset, ignored
    #
    # Another idea~~
    # Use a 'depends-on' attribute with keys from the constants file.
    # This requires prior knowledge of the data being generated.
    #
    # Best (likely) idea~~
    # Combine a bit of both of the above; eg.:
    #     PyRate uses the number system internally.
    #     Externally, plugin types can be used to auto-set priority.

    def __init__(self,priority=999,*args,**kwargs):
        """Setup the plugin."""
        pass

    def __call__(self,*args,**kwargs):
        """Run the plugin."""
        # KISS!
        # Switch to the __init__, __call__ style of plugin to keep the process
        # simple and iterable!
        # *args:    limit to actual input data for manipulation. (numpy arrays)
        # **kwargs: runtime flags.
        pass


#     def test(self):
#         """Test if plugin is valid."""
#         pass
