import abc

import pyrate.core
import pyrate.core.keys as pk


# Keys
targ_key = pk.targ_key
proj_key = pk.proj_key


# Base target class
class BaseTarget(abc.ABC):
    """Base target return class."""
    required_attributes = [
            targ_key,
            proj_key,
        ]
    def __init__(self,):
        """Perform basic checks on children."""
        missing_attriubtes = []
        for attribute in BaseTarget.required_attributes:
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
    print('Generating target...')
    pyrate.core.HDSTRUCT['last'].append(__name__)
    # Set up plugin
    targ_dict = pyrate.core.INSTRUCT[targ_key]
    plugin = targ_dict[pk.plug_key]
    inputs = targ_dict[pk.input_key]

    # Run and check
    target = pyrate.core.plugins.run(plugin, inputs)
    assert isinstance(target, BaseTarget), "Plugin must return a BaseTarget object."

    # Set output
    for key in BaseTarget.required_attributes:
        pyrate.core.HDSTRUCT[key] = getattr(target, key)

    return
