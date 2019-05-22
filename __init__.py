"""
Initialization script to import system.

Need to keep track of:
    1)  Material
    2)  Atm Profile
"""



import core
import resources


# Function shortnames
rpaparams = resources.plugins.atmosphere.params
#rpbparams: background plugin
#rptparams: target plugin

template = {
        core.plug_key: {
                core.atmosphere.__name__: 'rttov',
                core.background.__name__: 'lambertian',
                core.target.__name__: '2d',
            },
        core.input_key: {
                core.atmosphere.__name__: rpaparams('rttov'),
            },
    }

            
class Recipe():
    """PyRATE recipe object."""
    def __init__(self, *args):
        base = args[0] if args else template
        setattr(self, core.plug_key, self.subRecipe(base[core.plug_key]))
        setattr(self, core.input_key, self.subRecipe(base[core.input_key]))
        return

    class subRecipe():
        def __init__(self, d):
            self.__dict__ = d
            return
