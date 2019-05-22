"""
Outgoing

Generate the outgoing radiance.

This is the file that should handle settings for target.

"""

import pyrate.core


# Generate the outgoing data
def run():
    # Run the sub-modules
    pyrate.core.target.run()

    # Compile the output
    """Do stuff here. Probably a separate function.
    
    pixel.run()?
    """

    # Sign and return
    pyrate.core.HDSTRUCT['last'].append(__name__)

    return
