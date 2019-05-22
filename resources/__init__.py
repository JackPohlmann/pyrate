import os
import docker

import pyrate.resources.plugins
import pyrate.resources.plugins.atmosphere
import pyrate.resources.plugins.background
import pyrate.resources.plugins.target
# import pyrate.resources.secretary as sec

# Globals
# Docker client
DOCK_CLIENT = docker.from_env()

# load = sec.load
