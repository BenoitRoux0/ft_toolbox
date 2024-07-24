import os
import shutil
import sys
import tarfile
from argparse import ArgumentParser

import requests

from ..utils import get_code, parse_version, download_file


def set_download_parser(parser: ArgumentParser):
    parser.add_argument("ide", nargs="?", default="all")
    parser.add_argument("version", nargs='?', default="latest")
    parser.add_argument("--type", choices=["release", "eap"], default="release")


def download_ide(ide, version, type, config_fttb):
    ide_code = get_code(ide, config_fttb)
    print("request")
    res = requests.get(
        f"https://data.services.jetbrains.com/products?code={ide_code}&fields=releases"
    )
    if not res.ok:
        print("request failed")
        sys.exit()

    releases = res.json()[0]['releases']
    version = parse_version(ide_code, version, type)
    print(version)

    if os.path.isdir(f"goinfre/ides/fttb/{ide_code}-{version}"):
        return version
    for release in releases:
        if release['version'] == version and release['type'] == type:
            filename = release['downloads']['linux']['link'].split("/")[-1]
            filepath = f".cache/fttb/{filename}"
            download_file(release['downloads']['linux']['link'], filepath)
            file = tarfile.open(filepath)
            file.extractall(path="goinfre/ides/fttb/")
            dst = file.getmembers()[0].name.split('/')[0]
            try:
                shutil.rmtree(f"goinfre/ides/fttb/{ide_code}-{version}")
            except FileNotFoundError:
                pass
            os.rename(f"goinfre/ides/fttb/{dst}", f"goinfre/ides/fttb/{ide_code}-{version}")
            return version
    raise Exception


def download_cmd(args, config_fttb):
    if args.ide == "all":
        print("invalid IDE code")
        return
    download_ide(args.ide, args.version, args.type, config_fttb)
