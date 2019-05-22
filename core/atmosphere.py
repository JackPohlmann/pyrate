import abc

import core


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
        core.base_help(cls)
        return


# This one
def run():
    # Load data/plugin
    atm_dict = core.INSTRUCT[__name__]
    plugin = atm_dict[core.plug_key]     # This should be a function
    inputs = atm_dict[core.input_key]

    # Run and check
    atmosphere = plugin(inputs)
    assert isinstance(atmosphere, BaseAtmosphere), "Plugin must return a BaseAtmosphere object."

    # Set outputs
    core.HDSTRUCT[down_key] = getattr(atmosphere, down_key)
    core.HDSTRUCT[up_key] = getattr(atmosphere, up_key)
    core.HDSTRUCT[tau_key] = getattr(atmosphere, tau_key)
    
    return
