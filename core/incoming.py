"""
Incoming

Generate the incoming radiance.

This is the file that should handle any settings for atm/bg.

"""

import pyrate.core


def run():
    # Run the sub-modules
    pyrate.core.atmosphere.run()
    pyrate.core.background.run()

    # Sign and return
    pyrate.core.HDSTRUCT['last'].append(__name__)

    return
