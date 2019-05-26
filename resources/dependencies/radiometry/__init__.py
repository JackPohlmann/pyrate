import numpy as np
from math import pi
from scipy.constants import c, h, k


# Planckian
def planck(wavs, temp, wnums=True):
    """Planckian function

    So far only supports wavenumbers.
    """
    wavs = np.array(wavs)
    numer = 2*h*(c**2)*(wavs**3)
    denom = np.exp(h*c*wavs / (k*temp)) - 1
    return numer / denom

