import os
import docker

import resources.plugins
import resources.plugins.atmosphere

# import resources.secretary as sec

# Globals
# Docker client
DOCK_CLIENT = docker.from_env()

# load = sec.load
