"""
JSON Manager class
"""

import json
import warnings


fpaths = dict(
    plugins = "resources/secretary/plugins.json",
    settings = "local/settings.json"
)

def load(key):
    with open(fpaths[key],'r') as f:
        return json.load(f)

def add_plugin(input):
    key = 'plugins'
    socket, name = input.split('.')
    with open(fpaths[key],'r') as f:
        info = json.load(f)
    with open(fpaths[key],'w') as f:
        if name not in info[socket]:
            info[socket].append(name)
            _ = f.write(json.dumps(info, sort_keys=True, indent=4))
        else:
            warnings.warn("{} is already a plugin.".format(input))
    return

def remove_plugin(input):
    key = 'plugins'
    socket, name = input.split('.')
    with open(fpaths[key],'r') as f:
        info = json.load(f)
    with open(fpaths[key],'w') as f:
        if name in info[socket]:
            info[socket].remove(name)
            _ = f.write(json.dumps(info, sort_keys=True, indent=4))
        else:
            warnings.warn("{} does not exist.".format(input))
    return