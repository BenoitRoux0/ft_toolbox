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
    parser.add_argument("--type", choices=["release", "eap"], default="release")


def remove_all_versions(args, config_fttb):
    ide_code = get_code(args.ide, config_fttb)
    for f in glob.glob(f"goinfre/ides/fttb/{ide_code}-*"):
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
        shutil.rmtree(f"goinfre/ides/fttb/{ide_code}-{version}")
    except FileNotFoundError:
        pass
    if not os.path.exists(f"bin/{args.ide}"):
        try:
            os.remove(f"bin/{args.ide}")
        except FileNotFoundError:
            pass
