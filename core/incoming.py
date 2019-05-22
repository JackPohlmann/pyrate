"""
Incoming

Generate the incoming radiance.

This is the file that should handle any settings for atm/bg.

"""

import core


def run():
    # Run the sub-modules
    core.atmosphere.run()
    core.background.run()

    # Sign and return
    core.HDSTRUCT['last'].append(__name__)

    return
