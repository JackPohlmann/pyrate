"""
Outgoing

Generate the outgoing radiance.

This is the file that should handle settings for target.

"""

import pyrate.core


# Generate the outgoing data
def run():
    # Sign
    pyrate.core.HDSTRUCT['last'].append(__name__)

    # Run the sub-modules
    pyrate.core.target.run()
    pyrate.core.pixel.run()

    # Sign and return
    pyrate.core.HDSTRUCT['last'].append(__name__)

    return
