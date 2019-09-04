# PyRate python library

import os

# Info
__version__ = '0.1.0'
__description__ = 'Python Radiometric Target Embedder'
__author__ = 'Jack Pohlmann'
__email__ = 'jack.t.pohlmann@gmail.com'

# Constants
PYRATE_DIR = os.path.dirname(__file__)
PYRATE_DOCKER_DIR = os.path.join(PYRATE_DIR,'docker')


import pyrate.core
import pyrate.plugins
