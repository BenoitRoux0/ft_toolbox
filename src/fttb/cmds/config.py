import os
from argparse import ArgumentParser
from ..utils import open_config


def set_config_parser(parser: ArgumentParser):
    parser.add_argument("--cache-path", dest="cache_path", help="set download cache path")
    parser.add_argument("--install-path", dest="install_path", help="set ides installation path")
    parser.add_argument("--bin-path", dest="bin_path", help="set ides binaries path")


def config_cmd(args):
    config_fttb = open_config(f"{os.getenv('HOME')}/.config/fttb/config.json")
    if args.cache_path is not None:
        config_fttb['cache_path'] = args.cache_path
    if args.install_path is not None:
        config_fttb['install_path'] = args.install_path
    if args.bin_path is not None:
        config_fttb['bin_path'] = args.bin_path
