"""
Tests

Tests units.

This is an ugly way to do this. Need to exploit python's unittest module.

"""

import core



class testAtmOut(core.atmosphere.BaseAtmosphere):
    def __init__(self):
        for att in core.atmosphere.BaseAtmosphere.required_attributes:
            self.__dict__[att] = True
        super().__init__()
        return

class testBgOut(core.background.BaseBackground):
    def __init__(self):
        for att in core.background.BaseBackground.required_attributes:
            self.__dict__[att] = True
        super().__init__()
        return

class testTargOut(core.target.BaseTarget):
    def __init__(self):
        for att in core.target.BaseTarget.required_attributes:
            self.__dict__[att] = True
        super().__init__()
        return

# Basic setup
def setup():
    pass


def test_all():

    atm = testAtmOut()
    bg = testBgOut()
    targ = testTargOut()


    def simple_plugin_gen(output):
        def simple_plugin(*args, **kwargs):
            return output
        return simple_plugin

    simple_plugins = {
        core.atmosphere.__name__: simple_plugin_gen(atm),
        core.background.__name__: simple_plugin_gen(bg),
        core.target.__name__: simple_plugin_gen(targ),
    }

    atm_dict = {
        core.plug_key: simple_plugins[core.atmosphere.__name__],
        core.input_key: {'basic':"lettuce"},
    }

    bg_dict = {
        core.plug_key: simple_plugins[core.background.__name__],
        core.input_key: {'basic':"lettuce"},
    }

    targ_dict = {
        core.plug_key: simple_plugins[core.target.__name__],
        core.input_key: {'basic':"lettuce"},
    }

    instruct = {
        core.atmosphere.__name__: atm_dict,
        core.background.__name__: bg_dict,
        core.target.__name__: targ_dict,
    }

    core.init(instruct)

    out = core.run()

    print("Okay!")
    return out
