# Folder for managing the docker installation process.

This directory should not be installed via setup.py.

## Contents:

- Dockerfile

- Makefile (when setting up the container)

- Commands for installing supported plugins.


## Setting up the container

- Mount the container info to the host's pyrate/docker/ directory.
  * This is so that the local installation (wrapper) can see what the container
    is capable of handling.

- Mount the host's specified workdir to the container's *app*/ directory.
  * This is so that generated data ends up in the appropriate host location.
  * This is also where the instruction file/object will end up to be run by the
    container's installation.

- Make sure to clean up temporary instruction files (unless otherwise specified)!
