# DEV folder

Use this directory as a temporary "root" folder until the structure is transferred.


## Dependencies

- Python 3 (written in python3.7)


## NOTES

- As an example, the Docker python module has a file named 'constants.py'.
  This seems similar to the pyrate 'keys.py' but could be extended (there is precedent!)


## TODO

- Favor setup.py over makefile!
  * Makefile depends on a UNIX-like environment (ie. cygwin on Windows).
    This has obvious downsides for Windows machines!
  * Looking at the below points: a makefile can be included in the docker installing.

- Should HDF5 be a mandatory specification? (Probably?)

- Should data be passed directly between sections or written to temporary files?

- Refrain from using shell scripts (possible Windows use). Rely on Python scripts
  in order to manage the Docker container. 
  *  Shell scripts can be used within the Docker container, but shouldn't be used outside of it.


## Local installation files
*   pyrate.json
    Information regarding the local PyRate installation.
    * $PYRATE_INSTALL_DIR, etc.?
    * DO NOT EDIT DIRECTLY
    * Should be hosted on the LOCAL host and used by the DOCKER container.

*   pyrate.config [?]
    Configuration file for
    
*   <plugin_name>/
    Installation directories for plugin dependencies.

