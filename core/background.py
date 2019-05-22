import abc

import pyrate.core


# Keys
bg_key = 'background'


# Base class
class BaseBackground(abc.ABC):
    """Base background output class."""
    required_attributes = [
            bg_key,
        ]
    def __init__(self,):
        """Perform basic checks on children."""
        missing_attriubtes = []
        for attribute in BaseBackground.required_attributes:
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


# Run the simulation
def run():
    """Do stuff.
    
    1) Load
    2) Simulate
    3) Return
    
    """

    # Load data/plugin
    bg_dict = pyrate.core.INSTRUCT[__name__]
    plugin = bg_dict[pyrate.core.plug_key]
    inputs = bg_dict[pyrate.core.input_key]
    inputs[pyrate.core.atmosphere.down_key] = pyrate.core.HDSTRUCT[pyrate.core.atmosphere.down_key]

    # Run and check
    """Need to use the plugins here."""
    background = plugin(inputs)
    assert isinstance(background, BaseBackground), "Plugin must return a BaseBackground object."

    # Set outputs
    pyrate.core.HDSTRUCT[bg_key] = getattr(background, bg_key)

    return
