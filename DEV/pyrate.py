#!/usr/bin/env python3
# PyRate CLI
# Author: Jack Pohlmann
# Date: Aug, 2019
# 
# This is the initial framework for the PyRate CLI.
# The reason for maintaining a CLI for this project is to simplify the process
# of managing plugins (ie. installation and removal) as well as act as a
# wrapper for managing the PyRate docker environment without needing to use
# docker directly. This should remove some usage overhead.
#
# NOTE: This file should not be imported as the PyRate module. This is a
# command-line interface for the controlling the PyRate installation and should
# be run as a standalone script.
#
#
# Comment syntax:
# 
# ############ [parent_cmd] ############
# Top-level command; pyrate [parent_cmd]
# 
# #### [child_cmd]
# Lower-level command; pyrate [parent_cmd] [child_cmd]
# 
# # comment
# Regular comment

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
plugin_desc = "manage plugins."
plugin_parser = subparser.add_parser(
        'plugin',
        description=plugin_desc,help=plugin_desc)
plugin_sp = plugin_parser.add_subparsers()

#### LIST
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

#### INSTALL
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

#### REMOVE
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

############ DOCKER ############
docker_desc = "manage the PyRate docker container."
docker_parser = subparser.add_parser(
        'docker',
        description=docker_desc,help=docker_desc)
# TODO: use the python-docker library to manage the docker container.



# Main
if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
