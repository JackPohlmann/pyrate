"""
Initialize core modules.

Houses the main run function.

"""

import sys

import core.incoming
import core.atmosphere
import core.background
import core.outgoing
import core.target
import core.tests


# These variables should be wrapped up in params and comp_dict
# SIMULATOR = None
# ATMDATA = None

# BG_TARGET = None
# SP_TARGET = None

INSTRUCT = None
HDSTRUCT = {}  # Computational dict; stores all data and passes it thru


# Keys
plug_key = 'plugins'
input_key = 'inputs'


# Initialize
def init(instruct):
    """Initialize variables."""
    global INSTRUCT
    global HDSTRUCT
    INSTRUCT = instruct
    HDSTRUCT['last'] = [__name__]

    return


# Main function
def run():
    """Run the simulation."""
    if not INSTRUCT:
        raise NotImplementedError("Need to initialize instructions first.")

    try:
        """run stuff."""
        core.incoming.run()
        HDSTRUCT['last'].append(__name__)
        core.outgoing.run()
        HDSTRUCT['last'].append(__name__)
    except:
        e = sys.exc_info()[0]
        last = HDSTRUCT['last'][-1]
        print()
        print("An exception occured in module: {}".format(last))
        print()
        print(e)
        print()
        print("Check HDSTRUCT['last'] for a trace of modules.")
    finally:
        """Format the output data."""
        return HDSTRUCT


# Test function; super basic
def test(key='all'):
    if key=='all':
        dotest = core.tests.test_all
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
