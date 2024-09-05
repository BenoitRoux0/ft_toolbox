import os
from argparse import ArgumentParser

import requests

from ..cmds.download import download_ide
from ..utils import get_code, parse_version, VersionError


def set_use_parser(parser: ArgumentParser):
    parser.add_argument("ide", nargs="?", default="all")
    parser.add_argument("version", nargs='?', default="latest")
    parser.add_argument("--type", dest="type", choices=["release", "eap", "rc"], default="release")


def is_used(ide, ide_code, version, config_fttb):
    if not os.path.exists(f"{config_fttb['bin_path']}/{ide}") or \
            not os.path.exists(f"{os.getenv('HOME')}/.local/share/applications/{ide}.desktop"):
        return False
    if not os.path.realpath(
            f"{config_fttb['bin_path']}/{ide}") != f"{config_fttb['install_path']}/{ide_code}-{version}/bin/{ide}.sh":
        return False
    with open(f"{os.getenv('HOME')}/.local/share/applications/{ide}.desktop", "r") as entry_file:
        for line in entry_file:
            if line.startswith("Exec="):
                if version not in line:
                    return False
    return True


def generate_entry(ide, ide_code, version, config_fttb):
    if is_used(ide, ide_code, version, config_fttb):
        return
    res = requests.get(
        "https://data.services.jetbrains.com/products?"
        f"code={ide_code}&"
        "fields=name,intellijProductCode,description,categories")

    template_file_res = requests.get(
        "https://gist.githubusercontent.com/BenoitRoux0/ece685d71749e9d52a1c03b09a5b6e74/raw"
        "/dd5bd0f2a2f24c157a26aa7c97121f883dd6eeef/template.desktop")
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
        f"{config_fttb['install_path']}/{ide_code}-{version}/bin/{ide} %U"
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
    os.symlink(f"{config_fttb['install_path']}/{ide_code}-{version}/bin/{ide}", f"{config_fttb['bin_path']}/{ide}")


def use_cmd(args, config_fttb):
    ide_code = get_code(args.ide, config_fttb)
    try:
        version = parse_version(ide_code, args.version, args.type)
    except VersionError:
        print("bad version")
        return
    download_ide(ide_code, version, args.type, config_fttb)
    generate_entry(args.ide, ide_code, version, config_fttb)
