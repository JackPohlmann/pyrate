#!/usr/bin/env python3
# Temporary setup.py file
# 
# Local installation:
#     /usr/local/lib
#         core
#     man pages (?)
#         doc
# 
# Docker installation:
#         core
#         docker [building]
#         plugins

import os
import shutil

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

import pyrate

SCRIPTS_PATH = 'scripts'

def build_scripts(*scripts):
    """Move scripts to a specified directory and rename as specified."""
    if not os.path.exists(SCRIPTS_PATH):
        os.makedirs(SCRIPTS_PATH)
    scripts_path = []
    for src_path, script_name in scripts:
        dest_path = os.path.join(SCRIPTS_PATH,script_name)
        if not os.path.exists(dest_path):
            shutil.copy(src_path,dest_path)
        scripts_path += [dest_path]
    return scripts_path

def main():
    setup(
            name='pyrate',
            description=pyrate.__description__,
            version=pyrate.__version__,
            author=pyrate.__author__,
            author_email=pyrate.__email__,
            url='https://github.com/JackPohlmann/pyrate',

            packages=(
                'pyrate',
                'pyrate.core',
                'pyrate.plugins',
            ),

            package_data={
                'pyrate': (
                    'docker/*',
                ),
            },

            scripts=(build_scripts(
                ('pyrate.py','pyrate'),
            )),

            install_requires=(
                'docker',
                'h5py',
                'numpy',
                'scipy',
            ),
        )
    return

if __name__=='__main__':
    main()
