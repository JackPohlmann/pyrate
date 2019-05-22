"""
Initialization script to import system.

Need to keep track of:
    1)  Material
    2)  Atm Profile
"""


PARAMS = {}


# Set things
def set_plugins(plugins):
    global PARAMS
    PARAMS['plugins'] = plugins
