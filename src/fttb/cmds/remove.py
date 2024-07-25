import glob
import os
import shutil
import sys
from argparse import ArgumentParser

import requests

from ..utils import get_code, parse_version


def set_remove_parser(parser: ArgumentParser):
    parser.add_argument("ide", nargs="?", default="all")
    parser.add_argument("version", nargs='?', default="all")
    parser.add_argument("--type", choices=["release", "eap", "rc"], default="release")


def remove_all_versions(args, config_fttb):
    ide_code = get_code(args.ide, config_fttb)
    for f in glob.glob(f"{config_fttb['install_path']}/{ide_code}-*"):
        shutil.rmtree(f)


def remove_cmd(args, config_fttb):
    if args.ide == "all":
        print("invalid IDE code")
        return
    if args.version == "all":
        return remove_all_versions(args, config_fttb)
    ide_code = get_code(args.ide, config_fttb)
    
    res = requests.get(
        f"https://data.services.jetbrains.com/products?code={ide_code}&fields=releases")
    if not res.ok:
        print("request failed")
        sys.exit()

    version = parse_version(ide_code, args.version, args.type)

    try:
        shutil.rmtree(f"{config_fttb['install_path']}/{ide_code}-{version}")
    except FileNotFoundError:
        pass
    if not os.path.exists(f"{config_fttb['bin_path']}/{args.ide}"):
        try:
            os.remove(f"{config_fttb['bin_path']}/{args.ide}")
        except FileNotFoundError:
            pass
