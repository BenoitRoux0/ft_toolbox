import sys
from argparse import ArgumentParser

import requests

from ..utils import get_code


def set_infos_parser(parser: ArgumentParser):
    parser.add_argument("ide", nargs="?", default="all")


def infos_cmd(args, config_fttb):
    ide = get_code(args.ide, config_fttb)
    res = requests.get(
        f"https://data.services.jetbrains.com/products?"
        f"fields=name,intellijProductCode,description,categories&"
        f"code={ide}"
    )

    if not res.ok:
        print("request failed")
        sys.exit()

    if len(res.json()) == 0:
        return
    ide = res.json()[0]

    print(f"{ide['name']}\ncode: {ide['intellijProductCode']}\n{ide['description']}\n")
