import abc

import core


# Keys
targ_key = 'target'
proj_key = 'projected'  # Projected area ratio (SAIG)


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
        core.base_help(cls)
        return


# Run the simulation
def run():
    # Set up plugin
    targ_dict = core.INSTRUCT[__name__]
    plugin = targ_dict[core.plug_key]
    inputs = targ_dict[core.input_key]

    # Append previously computed values
    inputs[core.down_key] = core.HDSTRUCT[core.down_key]
    inputs[core.background.bg_key] = core.HDSTRUCT[core.background.bg_key]

    # Run and check
    target = plugin(inputs)
    assert isinstance(target, BaseTarget), "Plugin must return a BaseTarget object."

    # Set output
    core.HDSTRUCT[targ_key] = target.__dict__[targ_key]
    core.HDSTRUCT[proj_key] = target.__dict__[proj_key]

    return
