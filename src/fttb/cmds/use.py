import os
from argparse import ArgumentParser

import requests

from ..cmds.download import download_ide
from ..utils import get_code, parse_version, VersionError


def set_use_parser(parser: ArgumentParser):
    parser.add_argument("ide", nargs="?", default="all")
    parser.add_argument("version", nargs='?', default="latest")
    parser.add_argument("--type", choices=["release", "eap", "rc"], default="release")


def generate_entry(ide, ide_code, version, type, config_fttb):
    version = parse_version(ide_code, version, type)
    
    res = requests.get(
        f"https://data.services.jetbrains.com/products?code={ide_code}&fields=name,intellijProductCode,description,categories")
    
    template_file_res = requests.get(
        "https://gist.githubusercontent.com/BenoitRoux0/ece685d71749e9d52a1c03b09a5b6e74/raw/dd5bd0f2a2f24c157a26aa7c97121f883dd6eeef/template.desktop")
    entry = template_file_res.content.decode()
    entry = entry.replace(
        "{name}",
        res.json()[0]['name']
    )
    entry = entry.replace(
        "{desc}",
        res.json()[0]['description']
    )
    entry = entry.replace(
        "{exec}",
        f"{config_fttb['install_path']}/{ide_code}-{version}/bin/{ide}.sh %U"
    )
    entry = entry.replace(
        "{icon}",
        f"{config_fttb['install_path']}/{ide_code}-{version}/bin/{ide}.svg"
    )
    entry_file = open(f"{os.getenv('HOME')}/.local/share/applications/{ide}.desktop", "w+")
    entry_file.write(entry)
    entry_file.close()
    try:
        os.remove(f"{config_fttb['bin_path']}/{ide}")
    except FileNotFoundError:
        pass
    os.symlink(f"{config_fttb['install_path']}/{ide_code}-{version}/bin/{ide}.sh", f"{config_fttb['bin_path']}/{ide}")


def use_cmd(args, config_fttb):
    ide_code = get_code(args.ide, config_fttb)
    try:
        version = parse_version(ide_code, args.version, args.type)
    except VersionError:
        print("bad version")
        return
    download_ide(args.ide, version, args.type, config_fttb)
    generate_entry(args.ide, ide_code, version, args.type, config_fttb)
