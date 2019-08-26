#!/usr/bin/env python3
# PyRate: Python Radiometric Target Embedder
# Author: Jack Pohlmann
# Date: Aug, 2019
# 
# PyRate CLI.
# NOTE: This is not the PyRate python module. See __init__.py.
#
#
# Comment syntax:
# 
#| ############ [arg] ############
#| Top-level command: pyrate [arg]
#|  
#| #### [subarg]
#| Lower-level command: pyrate [arg] [subarg]
#| 
#| # comment
#| Regular comment
#| 
#| # {{{X
#| # }}}X
#| Vim manual folds (dev)

import argparse

VERSION = "0.1.1"
DESCRIPTION = "CLI for managing PyRate installation."

parser = argparse.ArgumentParser(description=DESCRIPTION,prog='PyRate')
parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {VERSION}')
subparser = parser.add_subparsers()


############ PLUGIN ############
# {{{1
plugin_desc = "manage plugins."
plugin_parser = subparser.add_parser(
        'plugin',
        description=plugin_desc,help=plugin_desc)
plugin_sp = plugin_parser.add_subparsers()

#### LIST
# {{{2
list_desc = "list plugins."
plugin_list = plugin_sp.add_parser(
        'list',
        description=list_desc,help=list_desc)
def do_plugin_list(args):
    """List plugins."""
    if args.installed:
        print("Would list installed plugins!")
    if args.tracked:
        print("Would list tracked plugins!")
    if not (args.installed or args.tracked):
        print("Would list all plugins!")
    pass
plugin_list.set_defaults(func=do_plugin_list)
# Opts
plugin_list.add_argument(
        '-i','--installed',
        action='store_true',
        help="list installed (committed) plugins.")
plugin_list.add_argument(
        '-t','--tracked',
        action='store_true',
        help="list tracked (uncommitted) plugins.")
# }}}2

#### INSTALL
# {{{2
plug_install_desc = "install given plugins."
plugin_install = plugin_sp.add_parser('install',
        description=plug_install_desc,help=plug_install_desc)
def do_plugin_install(args):
    """Install plugins."""
    if args.local:
        """This should just change the path to the source."""
        print(f"Checking path {args.local}")
    for mod in args.mods:
        if args.local: print("\t",end='')
        print(f"This would install \"{mod}\" if it existed...")
plugin_install.set_defaults(func=do_plugin_install)
# Args
plugin_install.add_argument(
        'mods',
        nargs='*',
        help="plugins to install.")
# Opts
plugin_install.add_argument(
        '-l','--local',
        metavar='path',
        default=None,
        help="path to local installation of plugin source.")
# }}}2

#### REMOVE
# {{{2
plug_remove_desc = "remove plugins."
plugin_remove = plugin_sp.add_parser('remove',
        description=plug_remove_desc,help=plug_remove_desc)
def do_plugin_remove(args):
    """Remove plugins."""
    for mod in args.mods:
        print(f'would have removed {mod}.')
    pass
plugin_remove.set_defaults(func=do_plugin_remove)
plugin_remove.add_argument(
        'mods',
        nargs='*',
        help="plugins to remove.")
# }}}2
# }}}1


############ DOCKER ############
# {{{1
docker_desc = "manage the PyRate docker container."
docker_parser = subparser.add_parser(
        'docker',
        description=docker_desc,help=docker_desc)
# TODO: use the python-docker library to manage the docker container.
# }}}1


# Main
if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
