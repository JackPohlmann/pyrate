# Plugins directory
The only contents in this directory should be:

1)  __init__.py:
    The main wrapper for loading and managing plugins.
    * Base plugin object and extended plugin objects (atm,targ,etc.).
    * Functions for managing the docker installation.
    * A function that utilizes __import__('<plugin_name>').
    * A function 'test' that checks if the plugin is valid (how does this interact with accuracy testing?)
        
2)  _template.py
    Template for new plugins if necessary.

3)  <plugin_name>.py
    The actual files for controlling installed plugins.
