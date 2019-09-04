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
sys.path.append(PLUGIN_DIR)

def _prompt_input(func):
    """Simple decorator to prompt for input."""
    def new_func(*args,noprompt=False,**kwargs):
        prompt = 'y' if noprompt else input("Continue? y/[n]: ")
        if prompt.lower() in ['y','yes'] or noprompt:
            func(*args,**kwargs)
    return new_func
            

def install(
        plugin,
        plug_name=None,
        src=None,
        cmd=None,
        run_test=False,
    ):
    """Install a new plugin to pyrate."""
    plugin, _ = os.path.splitext(plugin)
    plug_file = plugin + '.py'
    plug_name = plug_name if plug_name else plugin
    if not os.path.isfile(plug_file):
        print(f"No such file '{plug_file}'.")
        return
    # If no source options are given, try to install using the file
    # This is failing to import the plugin when run from the command line
    if not (src or cmd):
        try:
            sys.path.append(os.getcwd())
            check_file = __import__(plugin)
            check_file.install()
            return
        except AttributeError:
            pass
    # Create the new plugin directory
    plug_install_dir = os.path.join(PLUGIN_DIR, plug_name)
    if os.path.exists(plug_install_dir):
        shutil.rmtree(plug_install_dir)
    os.makedirs(plug_install_dir)
    # Copy the plugin file to the new directory
    plug_dest = os.path.join(plug_install_dir,'__init__.py')
    shutil.copy(plug_file, plug_dest)
    # Install the source
    if src:
        src_dest = os.path.join(plug_install_dir, 'src')
        shutil.copytree(src, src_dest)
        # Run the installation command/script if given
        if cmd:
            starting_dir = os.getcwd()
            try:
                os.chdir(src_dest)
                subprocess.run(cmd.split())
            except:
                # Not sure what to look for
                e = sys.exc_info()[0]
                print(e)
                # raise
            finally:
                # Make sure to reset the directory!
                os.chdir(starting_dir)
    # Test after installation 
    if run_test:
        test_result = test(plug_name, quiet=True, store_exit=True)
        if not test_result:
            # Uninstall if test fails
            uninstall(plug_name)
    return


@_prompt_input
def uninstall(plug_name):
    """Uninstall a plugin."""
    if plug_name=='all':
        current_plugins = list()
        for plugin in current_plugins:
            uninstall(plugin,noprompt=True)
        return
    plug_dir_path = os.path.join(PLUGIN_DIR, plug_name)
    shutil.rmtree(plug_dir_path)
    return


def list(display=False):
    """List installed plugins."""
    listdir = os.listdir
    join = os.path.join
    isdir = os.path.isdir
    plugins = [f for f in listdir(PLUGIN_DIR) if isdir(join(PLUGIN_DIR,f))]
    if '__pycache__' in plugins: plugins.remove('__pycache__')
    if display:
        print(*plugins,sep='\n')
    else:
        return plugins


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
        kwargs['priority'] = priority
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

    def set_opts(self,**kwargs):
        """Set the runtime options."""
        for key, value in kwargs.items():
            # self.opts[key] = value
            setattr(self,key,value)
        return
