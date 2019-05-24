"""
Initialize pyrate.core modules.

Houses the main run function.

"""

import sys
import traceback

import pyrate.core.incoming
import pyrate.core.atmosphere
import pyrate.core.background
import pyrate.core.outgoing
import pyrate.core.target
import pyrate.core.saig
#import pyrate.core.tests


# 'Header' variables for running the core modules
INSTRUCT = None
HDSTRUCT = {}  # Computational dict; stores all data and passes it thru


# Keys
plug_key = 'Plugins'
input_key = 'Inputs'
atm_key = 'atmosphere'
bg_key = 'background'
targ_key = 'target'


# Initialize
def init(instruct):
    """Initialize variables."""
    global INSTRUCT
    global HDSTRUCT
    INSTRUCT = instruct
    HDSTRUCT = dict(last=[__name__])
    return


# Main function
def run():
    """Run the simulation."""
    global INSTRUCT
    if not INSTRUCT:
        raise NotImplementedError("Need to initialize instructions first.")

    try:
        """run stuff."""
        pyrate.core.incoming.run()
        HDSTRUCT['last'].append(__name__)
        pyrate.core.outgoing.run()
        HDSTRUCT['last'].append(__name__)
    except:
        e, d, tb = sys.exc_info()
        last = HDSTRUCT['last'][-1]
        print()
        print("An exception occured in module: {}".format(last))
        print()
        print(e)
        print()
        print(d)
        print()
        traceback.print_tb(tb)
        print()
        print("Check HDSTRUCT['last'] for a trace of modules.")
    finally:
        """Format the output data."""
        return HDSTRUCT


# Test function; super basic
def test(key='all'):
    if key=='all':
        dotest = pyrate.core.tests.test_all
    return dotest()


# General help function for base classes
def base_help(cls,):
        """Get help for the class."""
        title = "Help for class {}:".format(cls.__name__)
        numchar = len(title)
        print("\n"+title)
        print("="*numchar)
        print("\nRequired attributes:")
        for att in cls.required_attributes:
            print("\t{}".format(att))
        print("\nSee {}.required_attributes for the above list.\n".format(cls.__name__))
        return
