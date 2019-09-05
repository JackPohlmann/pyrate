#!/usr/bin/env python3
# vim: fdm=marker
#
# PyRate: Python Radiometric Target Embedder
# Author: Jack Pohlmann
# Date: Aug, 2019
# 
# PyRate CLI.
# NOTE: This is not the PyRate python module. See pyrate/__init__.py.
#
#
# Comment syntax:
# 
# ############ [arg] ############
# Top-level command: pyrate [arg]
#  
# #### [subarg]
# Lower-level command: pyrate [arg] [subarg]
# 
# # comment
# Regular comment

import argparse

import pyrate
import pyrate.plugins as plugins


parser = argparse.ArgumentParser(
        description=pyrate.__description__,
        prog='PyRate',
    )
parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {pyrate.__version__}',
    )
subparser = parser.add_subparsers()

def set_help_default(some_parser):
    """Set a (sub)parser's default behavior to display its help text.'"""
    some_parser.set_defaults(
            func=(lambda *args: some_parser.parse_args(['--help'])))
    return

set_help_default(parser)


############ PLUGIN ############
# {{{1
plugin_desc = "manage plugins."
plugin_parser = subparser.add_parser(
        'plugin',
        description=plugin_desc,help=plugin_desc)
set_help_default(plugin_parser)
plugin_sp = plugin_parser.add_subparsers()

#### LIST
# {{{2
list_desc = "list plugins."
plugin_list = plugin_sp.add_parser(
        'list',
        description=list_desc,help=list_desc)
def do_plugin_list(args):
    """List plugins."""
    # TODO: add support for command line options.
    plugins.list(display=True)
    return

plugin_list.set_defaults(func=do_plugin_list)
# Opts
# plugin_list.add_argument(
#         '-l','--loud',
#         action='store_true',
#         help="more detailed descriptions."
#         )
# plugin_list.add_argument(
#         '-i','--installed',
#         action='store_true',
#         help="list installed (committed) plugins.")
# plugin_list.add_argument(
#         '-t','--tracked',
#         action='store_true',
#         help="list tracked (uncommitted) plugins.")
# }}}2

#### INSTALL
# {{{2
plug_install_desc = "install a plugin."
plugin_install = plugin_sp.add_parser('install',
        description=plug_install_desc,help=plug_install_desc)
def do_plugin_install(args):
    """Install plugins."""
    plugins.install(
            args.plugin,
            plug_name=args.name,
            src=args.src,
            cmd=args.cmd,
            run_test=args.test
        )
    return

plugin_install.set_defaults(func=do_plugin_install)
# Args
plugin_install.add_argument(
        'plugin',
        help="plugin to install."
    )
# Opts
plugin_install.add_argument(
        '-n','--name',
        help="name of plugin once installed.",
    )
plugin_install.add_argument( #Might be unnecessary
        '--src',
        help="directory of plugin source."
    )
plugin_install.add_argument(
        '--cmd',
        help="command to run to install the plugin source.",
    )
plugin_install.add_argument(
        '-t','--test',
        help="test plugins to install.",
        action='store_true',
    )
# }}}2

#### UNINSTALL
# {{{2
plug_uninstall_desc = "uninstall a plugin."
plugin_uninstall = plugin_sp.add_parser('uninstall',
        description=plug_uninstall_desc,help=plug_uninstall_desc)
def do_plugin_uninstall(args):
    """Uninstall plugins."""
    plugins.uninstall(
            args.plugin,
        )
    return

plugin_uninstall.set_defaults(func=do_plugin_uninstall)
# Args
plugin_uninstall.add_argument(
        'plugin',
        help="plugin to uninstall."
    )

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


############ ############
# {{{1
container_desc = "manage the PyRate container container."
container_parser = subparser.add_parser(
        'container',
        description=container_desc,help=container_desc)
set_help_default(container_parser)
# TODO: use the python-docker library to manage the docker container.
# }}}1


# Main
if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)