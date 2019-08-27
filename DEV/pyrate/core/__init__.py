# Placeholder
# 
# * Main module 'workflow' should be contained here.
# 
# * This should be the location of all core.<mod> imports, NOT the main script.
# 
# * The recipe object should be defined here?
#   OKAY: probably won't cause any problems with recursive imports.
#   NOTE: This requires that each core.<mod> should be completely standalone.

# Core directory globals
GLOB1 = "temporary global var"
GLOB2 = "temporary global var"
GLOB3 = "temporary global var"

# This is an example of how it would go:
def main(plugin_list,data_obj,**kwargs):
    # Sort plugins by priority
    plugin_list = sorted(plugin_list,key=(lambda pl: pl.priority))
    # Let the plugins do their thing with the data
    for plugin in plugin_list:
        plugin(data_obj)
    return data_obj
