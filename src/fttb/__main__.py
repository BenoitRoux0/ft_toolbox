#!/bin/python3
import os

import argparse

from .cmds.update import update_cmd
from .cmds.config import set_config_parser, config_cmd
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
config_parser = subparsers.add_parser('config', help='config fttb')
set_config_parser(config_parser)
subparsers.add_parser('clear', help='clear download cache')
subparsers.add_parser('update', help='update versions lists')


def main(cmd_args):
    create_config()
    config_fttb = open_config(f"{os.getenv('HOME')}/.config/fttb/config.json")
    if cmd_args.command == "list":
        list_cmd(cmd_args, config_fttb)
    elif cmd_args.command == "download":
        download_cmd(cmd_args, config_fttb)
    elif cmd_args.command == "use":
        use_cmd(cmd_args, config_fttb)
    elif cmd_args.command == "infos":
        infos_cmd(cmd_args, config_fttb)
    elif cmd_args.command == "clear":
        clear_cmd(config_fttb)
    elif cmd_args.command == "remove":
        remove_cmd(cmd_args, config_fttb)
    elif cmd_args.command == "config":
        config_cmd(cmd_args)
    elif cmd_args.command == "update":
        update_cmd()


if __name__ == '__main__':
    args = parser.parse_args()
    if os.environ.get("HOME", None) is None:
        print("HOME is unset")
        exit()
    main(args)
