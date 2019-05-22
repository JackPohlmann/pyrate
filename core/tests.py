"""
Tests

Tests units.

This is an ugly way to do this. Need to exploit python's unittest module.

"""




class testAtmOut(pyrate.core.atmosphere.BaseAtmosphere):
    def __init__(self):
        for att in pyrate.core.atmosphere.BaseAtmosphere.required_attributes:
            self.__dict__[att] = True
        super().__init__()
        return

class testBgOut(pyrate.core.background.BaseBackground):
    def __init__(self):
        for att in pyrate.core.background.BaseBackground.required_attributes:
            self.__dict__[att] = True
        super().__init__()
        return

class testTargOut(pyrate.core.target.BaseTarget):
    def __init__(self):
        for att in pyrate.core.target.BaseTarget.required_attributes:
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
        pyrate.core.atmosphere.__name__: simple_plugin_gen(atm),
        pyrate.core.background.__name__: simple_plugin_gen(bg),
        pyrate.core.target.__name__: simple_plugin_gen(targ),
    }

    atm_dict = {
        pyrate.core.plug_key: simple_plugins[pyrate.core.atmosphere.__name__],
        pyrate.core.input_key: {'basic':"lettuce"},
    }

    bg_dict = {
        pyrate.core.plug_key: simple_plugins[pyrate.core.background.__name__],
        pyrate.core.input_key: {'basic':"lettuce"},
    }

    targ_dict = {
        pyrate.core.plug_key: simple_plugins[pyrate.core.target.__name__],
        pyrate.core.input_key: {'basic':"lettuce"},
    }

    instruct = {
        pyrate.core.atmosphere.__name__: atm_dict,
        pyrate.core.background.__name__: bg_dict,
        pyrate.core.target.__name__: targ_dict,
    }

    pyrate.core.init(instruct)

    out = pyrate.core.run()

    print("Okay!")
    return out
