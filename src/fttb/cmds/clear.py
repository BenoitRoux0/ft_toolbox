import os
import shutil


def clear_cmd(config_fttb):
    try:
        shutil.rmtree(config_fttb['cache_path'])
    except FileNotFoundError:
        pass
    os.makedirs(config_fttb['cache_path'])
