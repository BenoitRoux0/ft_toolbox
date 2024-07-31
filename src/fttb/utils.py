import json
import os
import sys

import requests


class VersionError(Exception):
    pass


def get_versions_list() -> list[str]:
    with open("/tmp/ft_tb/versions.list", "r") as list_file:
        return list_file.read().splitlines()


def save_versions_list(ide_code):
    with open("/tmp/ft_tb/versions.list", "a") as _:
        os.chmod("/tmp/ft_tb/versions.list", 0o777)
    with open("/tmp/ft_tb/versions.list", "r") as list_file:
        ides = list_file.read().splitlines()
    if ide_code in ides:
        return
    ides.append(ide_code)
    with open("/tmp/ft_tb/versions.list", "w") as list_file:
        list_file.write("\n".join(ides))


def get_all_versions(ide_code):
    versions_list: dict
    if os.path.exists(f"/tmp/ft_tb/{ide_code}-versions.json"):
        os.chmod(f"/tmp/ft_tb/{ide_code}-versions.json", 0o777)
        with open(f"/tmp/ft_tb/{ide_code}-versions.json", "r") as cache_file:
            save_versions_list(ide_code)
            return json.load(cache_file)

    res = requests.get(
        f"https://data.services.jetbrains.com/products?code={ide_code}&fields=releases")
    if not res.ok:
        print("request failed")
        sys.exit()
    releases = res.json()[0]['releases']
    with open(f"/tmp/ft_tb/{ide_code}-versions.json", "w+") as cache_file:
        os.chmod(f"/tmp/ft_tb/{ide_code}-versions.json", 0o777)
        json.dump(releases, cache_file)
    save_versions_list(ide_code)
    return releases


def get_latest(version_type: str | None, releases):
    for release in releases:
        if version_type is None or release["type"] == version_type:
            return release['version']
    raise VersionError


def parse_version(ide_code, version, version_type: str | None):
    releases = get_all_versions(ide_code)
    if version == "latest":
        return get_latest(version_type, releases)
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
    config_fttb: dict
    try:
        os.makedirs(f"{os.getenv('HOME')}/.config/fttb")
    except FileExistsError:
        pass
    if not os.path.exists(f"{os.getenv('HOME')}/.config/fttb/config.json"):
        download_file(
            "https://gist.githubusercontent.com/BenoitRoux0/16b18e10cfd53dcf31a28cb1b38e4303/raw"
            "/676f61b08f669dffda5f60a9f54fb3cc1eb18542/config.json",
            f"{os.getenv('HOME')}/.config/fttb/config.json")
        config_fttb = open_config(f"{os.getenv('HOME')}/.config/fttb/config.json")
        config_fttb['cache_path'] = f"{os.getenv('HOME')}/.cache/fttb"
        config_fttb['install_path'] = f"{os.getenv('HOME')}/goinfre/ides/fttb"
        config_fttb['bin_path'] = f"{os.getenv('HOME')}/bin"
        with open(f"{os.getenv('HOME')}/.config/fttb/config.json", "w") as conf_file:
            json.dump(config_fttb, conf_file)
        print(config_fttb)
    else:
        config_fttb = open_config(f"{os.getenv('HOME')}/.config/fttb/config.json")
    try:
        os.makedirs(config_fttb['bin_path'])
    except FileExistsError:
        pass
    try:
        os.makedirs(config_fttb['cache_path'])
    except FileExistsError:
        pass
    try:
        os.makedirs(config_fttb['install_path'])
    except FileExistsError:
        pass
    try:
        os.makedirs("/tmp/ft_tb")
    except FileExistsError:
        pass
    os.chmod("/tmp/ft_tb", 0o777)
