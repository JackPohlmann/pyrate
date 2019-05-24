import abc
import os
from math import sqrt

import pyrate.core


# Keys
down_key = 'downwell'
up_key = 'upwell'
tau_key = 'tau'
wav_key = 'wavenums'

# Base class
class BaseAtmosphere(abc.ABC):
    """Base atmospheric output class."""
    required_attributes = [
            down_key,
            up_key,
            tau_key,
            wav_key,
        ]
    def __init__(self,):
        """Perform basic checks on children."""
        missing_attriubtes = []
        for attribute in BaseAtmosphere.required_attributes:
            try:
                _ = self.__dict__[attribute]
            except AttributeError:
                missing_attriubtes.append(attribute)
        if len(missing_attriubtes) != 0:
            raise NotImplementedError("Missing attributes: {}".format(missing_attriubtes))
        return
    @classmethod
    def help(cls,):
        pyrate.core.base_help(cls)
        return


# This one
def run():
    pyrate.core.HDSTRUCT['last'].append(__name__)
    # Load data/plugin
    atm_dict = pyrate.core.INSTRUCT[pyrate.core.atm_key]
    plugin = atm_dict[pyrate.core.plug_key]     # This should be a function
    inputs = atm_dict[pyrate.core.input_key]

    # Run and check
    atmosphere = plugin(inputs)
    assert isinstance(atmosphere, BaseAtmosphere), "Plugin must return a BaseAtmosphere object."

    # Reshape outputs if necessary
    for key in [down_key, up_key, tau_key]:
        data = getattr(atmosphere, key)
        if len(data.shape)==2:
            res, datadim = data.shape
            res = int(sqrt(res) / 2)
            setattr(atmosphere, key, data.reshape((res, 4*res, datadim)))

    # Set outputs
    for key in BaseAtmosphere.required_attributes:
        pyrate.core.HDSTRUCT[key] = getattr(atmosphere, key)
    
    return
