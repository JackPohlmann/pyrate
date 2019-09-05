# TODO

Condense dockerfiles into a one and place it in the top-level directory.

This directory (build) should be reserved for installation scripts that are local/container agnostic.

RTTOV is a plugin, so it should ultimately be installed as such via the plugin.install method.
- This would look like:
  * Install HDF5 and Pyrate; this can be done in docker or locally.
  * Install RTTOV using the plugin.install method; this needs to compile RTTOV against HDF5!
  * Use the above method as a simple tutorial on installing custom plugins.

Ensure that it can install with or without RTTOV!
