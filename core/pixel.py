'''
Pixel

CURRENTLY UNUSED

Module for constructing the pixel. Composed of a background and a target.

NEED TO SCALE SAIGs BY SURFACE AREA (cos2 factor)

'''

import numpy as np
import warnings

try:
    import pyrate.core.saig as saig
except ImportError as e:
    print(e)
    raise ImportError("Meant to be imported as a part of pyrate.core.")


class SPAnchor():
    """
    Sub-Pixel Anchor class

    Wraps a SAIG class with geometric information. Does not inherit from SAIG
    since the anchor points will be set up before computing their respective
    SAIGs.
    """

    def __init__(self, coords):
        self.coords = coords
        self.downwell = None
        self.upwell = None
        self.tau = None


def ConstructTarget(pixelObj, background, target, downwell):
    """
    Construct the target.

    Parameters
    ----------
    pixelObj : 

    """
    pass
