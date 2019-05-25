import abc

import pyrate.core
import pyrate.core.keys as pk


# Keys
bg_key = pk.bg_key


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
    print('Generating {}...'.format(bg_key))
    pyrate.core.HDSTRUCT['last'].append(__name__)

    # Load data/plugin
    bg_dict = pyrate.core.INSTRUCT[bg_key]
    plugin = bg_dict[pk.plug_key]
    inputs = bg_dict[pk.input_key]
    # The lines below are bad. The data already exists
    # downwell = pyrate.core.HDSTRUCT[pyrate.core.atmosphere.down_key]
    # inputs['load'] = downwell

    # Run and check
    """Need to use the plugins here."""
    background = pyrate.core.plugins.run(plugin, inputs)
    assert isinstance(background, BaseBackground), "Plugin must return a BaseBackground object."

    # Set outputs
    pyrate.core.HDSTRUCT[bg_key] = getattr(background, bg_key)

    return
