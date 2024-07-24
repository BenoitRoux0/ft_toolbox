import os
import shutil


def clear_cmd():
    try:
        shutil.rmtree(".cache/fttb")
    except FileNotFoundError:
        pass
    os.makedirs(".cache/fttb")
