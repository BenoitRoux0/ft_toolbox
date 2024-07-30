import os.path
import pydoc
import sys
from argparse import ArgumentParser

import requests

from ..utils import get_code


def set_list_parser(parser: ArgumentParser):
    parser.add_argument("ide", nargs="?", default="all")
    parser.add_argument("--installed", action='store_true')


def list_cmd(args, config_fttb):
    if args.ide == "all":
        codes = ",".join(config_fttb['aliases'].values())
        res = requests.get(
            f"https://data.services.jetbrains.com/products?"
            f"fields=name,intellijProductCode,description,categories&"
            f"code={codes}")

        if not res.ok:
            print("request failed")
            sys.exit()

        ides = res.json()

        for ide in ides:
            if ide['intellijProductCode'] is not None and ide['categories'] is not None:
                if "IDE" in ide['categories']:
                    print(f"{ide['name']}\n{ide['description']}\n")
    else:
        ide_code = get_code(args.ide, config_fttb)
        res = requests.get(
            f"https://data.services.jetbrains.com/products?code={ide_code}&fields=releases")
        if not res.ok:
            print("request failed")
            sys.exit()

        releases = res.json()[0]['releases']
        page = ""
        for release in releases:
            if args.installed:
                if os.path.exists(f"{config_fttb['install_path']}/{ide_code}-{release['version']}"):
                    page += f"{release['date']}\n{release['type']}\n{release['version']}\n\n"
            else:
                page += f"{release['date']}\n{release['type']}\n{release['version']}\n\n"
        pydoc.pager(page)

