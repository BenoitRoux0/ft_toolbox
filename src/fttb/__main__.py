#!/bin/python3
import os

import argparse

from .cmds.remove import remove_cmd, set_remove_parser
from .cmds.clear import clear_cmd
from .cmds.infos import set_infos_parser, infos_cmd
from .cmds.use import use_cmd, set_use_parser
from .cmds.download import set_download_parser, download_cmd
from .cmds.list import list_cmd, set_list_parser
from .utils import open_config, create_config

parser = argparse.ArgumentParser(description='Jetbrains toolbox cli', prog="fttb")

subparsers = parser.add_subparsers(dest="command")
list_parser = subparsers.add_parser('list', help='list ides')
set_list_parser(list_parser)
download_parser = subparsers.add_parser('download', help='download an ide')
set_download_parser(download_parser)
use_parser = subparsers.add_parser('use', help='use an ide')
set_use_parser(use_parser)
infos_parser = subparsers.add_parser('infos', help='get infos about an ide')
set_infos_parser(infos_parser)
remove_parser = subparsers.add_parser('remove', help='remove an ide')
set_remove_parser(remove_parser)
subparsers.add_parser('clear', help='clear download cache')

os.chdir(os.environ.get("HOME", "./"))

args = parser.parse_args()


def main():
    create_config()
    config_fttb = open_config(".config/fttb/config.json")
    if args.command == "list":
        list_cmd(args, config_fttb)
    elif args.command == "download":
        download_cmd(args, config_fttb)
    elif args.command == "use":
        use_cmd(args, config_fttb)
    elif args.command == "infos":
        infos_cmd(args, config_fttb)
    elif args.command == "clear":
        clear_cmd()
    elif args.command == "remove":
        remove_cmd(args, config_fttb)


if __name__ == '__main__':
    main()
