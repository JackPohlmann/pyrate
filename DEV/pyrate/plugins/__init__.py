# PyRate Plugins
# Author:   Jack Pohlmann
# Date:     August 2019
# 
# Manage PyRate plugins.
#
# TODO: Make sure to add/remove plugins from the internal list upon un/install.

import abc
import os
import shutil
import subprocess
import sys

from pyrate import PYRATE_DIR

PLUGIN_DIR = os.path.join(PYRATE_DIR, 'plugins') 

def install(
        plug_src,
        plug_name=None,
        src_dir=None,
        src_install_cmd=None,
        run_test=False,
    ):
    """Install a new plugin to pyrate."""

    # Determine the plugin file, path, and installation name
    # Might seem overcomplicated but it's actually just generalized
    plug_src, plug_ext = os.path.splitext(plug_src)
    plug_ext = plug_ext if plug_ext else '.py'
    plug_path, plug_src = os.path.split(plug_src)
    plug_name = plug_name if plug_name else plug_src
    plug_file = plug_path + plug_src + plug_ext

    # Create the new plugin directory
    plug_install_dir = os.path.join(PLUGIN_DIR, plug_name)
    if not os.path.exists(plug_install_dir):
        os.makedirs(plug_install_dir)

    # Copy the plugin file to the new directory
    plug_dest = os.path.join(plug_install_dir,'__init__.py')
    shutil.copy(plug_file, plug_dest)

    # Install the source
    if src_dir:
        src_dir_dest = os.path.join(PLUGIN_DIR, plug_name, 'src')
        shutil.copytree(src_dir, src_dir_dest)
        # Run the installation command if given
        if src_install_cmd:
            starting_dir = os.getcwd()
            try:
                os.chdir(src_dir_dest)
                subprocess.run(src_install_cmd.split())
            except:
                # Not sure what to look for
                e = sys.exc_info()[0]
                print(e)
                raise
            finally:
                # Make sure to reset the directory!
                os.chdir(starting_dir)
            
    # Test after installation 
    if run_test:
        test_result = test(plug_name, quiet=True, store_exit=True)
        if not test_result:
            # Uninstall if test fails
            uninstall(plug_name)


def uninstall(plug_name):
    """Uninstall a plugin."""
    plug_dir_path = os.path.join(PLUGIN_DIR, plug_name)
    shutil.rmtree(plug_dir_path)
    return

def load(
        plugin,
        **kwargs,
    ):
    """Loads a plugin and returns the plugin object.

    Passes any keyword arguments to the plugin initialization.
    """
    try:
        plugin = __import__(plugin)
        return plugin.Plugin(**kwargs)
    except ImportError:
        print(f"No such plugin {plugin}.")
        return


def test(
        plugin,
        quiet=False,
        store_exit=False,
    ):
    """Test the validity of a plugin."""
    if quiet: print = lambda *args, **kwargs: None
    test_passed = False
    # Test the plugin
    test_passed = True
    print(f"Test result:\t{test_passed}")
    if store_exit: return test_passed
    else: return


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
    #
    #
    # TODO: Should installation information be stored within the plugin?

    # Runtime options
    opts = {}
    
    def __init__(self,priority=999,*args,**kwargs):
        """Setup the plugin."""
        self.set_opts(**kwargs)
        return

    @abc.abstractmethod
    def __call__(self,*args,**kwargs):
        """Run the plugin."""
        # KISS!
        # Switch to the __init__, __call__ style of plugin to keep the process
        # simple and iterable!
        # *args:    limit to actual input data for manipulation. (numpy arrays)
        # **kwargs: runtime opts.
        self.set_opts(**kwargs)
        return

    def set_opts(**kwargs):
        """Set the runtime options."""
        for key, value in kwargs.items():
            self.opts[key] = value
        return
