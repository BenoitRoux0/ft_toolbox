import sys
from argparse import ArgumentParser

import requests


def set_list_parser(parser: ArgumentParser):
    parser.add_argument("ide", nargs="?", default="all")


def list_cmd(args, config_fttb):
    if args.ide == "all":
        codes = ",".join(config_fttb['aliases'].values())
        res = requests.get(
            f"https://data.services.jetbrains.com/products?fields=name,intellijProductCode,description,categories&code={codes}")

        if not res.ok:
            print("request failed")
            sys.exit()

        ides = res.json()

        for ide in ides:
            if ide['intellijProductCode'] is not None and ide['categories'] is not None:
                if "IDE" in ide['categories']:
                    print(f"{ide['name']}\n{ide['description']}\n")
