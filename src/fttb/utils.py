import json
import os
import sys

import requests


class VersionError(Exception):
    pass


def get_latest(ide, version_type: str | None, releases):
    for release in releases:
        if version_type is None or release["type"] == version_type:
            return release['version']
    raise VersionError


def parse_version(ide, version, version_type: str | None):
    print("get latest")
    print("request")
    res = requests.get(
        f"https://data.services.jetbrains.com/products?code={ide}&fields=releases")
    if not res.ok:
        print("request failed")
        sys.exit()

    releases = res.json()[0]['releases']
    if version == "latest":
        return get_latest(ide, version_type, releases)
    for release in releases:
        if release['version'] == version and (version_type is None or release["type"] == version_type):
            return version
    raise VersionError


def open_config(path):
    file = open(path, "r")
    conf = json.load(file)
    return conf


def get_code(name, config_fttp: dict):
    if name in config_fttp.values():
        return name
    if name in config_fttp['aliases'].keys():
        return config_fttp['aliases'][name]
    return name


def download_file(url, dst):
    with open(dst, "wb") as f:
        print("request")
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(100 * dl / total_length)
                print(f"{done}%", end="\r")
                sys.stdout.flush()
            print("")


def create_config():
    try:
        os.makedirs(".config/fttb")
    except FileExistsError:
        pass
    try:
        os.makedirs("bin")
    except FileExistsError:
        pass
    try:
        os.makedirs(".cache/fttb")
    except FileExistsError:
        pass
    try:
        os.makedirs("goinfre/ides/fttb")
    except FileExistsError:
        pass
    if not os.path.exists(".config/fttb/config.json"):
        download_file(
            "https://gist.githubusercontent.com/BenoitRoux0/16b18e10cfd53dcf31a28cb1b38e4303/raw/85e83c6f716fb1ccba39cb88520d0c03f54d9f3e/config.json",
            ".config/fttb/config.json")
