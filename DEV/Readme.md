# Welcome to the pyrate/DEV/ directory! 

Use this directory as a temporary "root" folder until the structure is transferred.


## Dependencies

- Python 3 (written in python3.7)
- NumPy, SciPy(?), H5Py
- (Optionally) python-docker


## NOTES

- STOP TRYING TO HAVE A LOCAL AND DOCKER INSTALLATION THAT COMMUNICATE!
  This is a total overcomplication. Docker is designed to eliminate this.
  - Allow the user to decide how they would like to operate the system, but give them some basic
    tools for installing either locally (setup.py) or in a container (Dockerfile).

- As an example, the Docker python module has a file named 'constants.py'.
  This seems similar to the pyrate 'keys.py' but could be extended (there is precedent!)


## TODO

- Favor setup.py over makefile!
  * Makefile depends on a UNIX-like environment (ie. cygwin on Windows).
    This has obvious downsides for Windows machines!

- Should HDF5 be a mandatory specification?


## Local installation files
*   pyrate.json
    Information regarding the local PyRate installation.
    * $PYRATE_INSTALL_DIR, etc.?
    * DO NOT EDIT DIRECTLY
    * Should be hosted on the LOCAL host and used by the DOCKER container.
