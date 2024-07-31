import os

from ..utils import get_versions_list, get_all_versions


def update_cmd():
    ides = get_versions_list()
    for ide_code in ides:
        try:
            os.remove(f"/tmp/ft_tb/{ide_code}-versions.json")
        except FileNotFoundError:
            pass
        print(f"update {ide_code}")
        get_all_versions(ide_code)
