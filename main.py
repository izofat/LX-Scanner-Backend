import os
import subprocess

from app import run
from lx_scanner_backend.logger import Logger
from settings import INPUT_FILE_PATH


def make_output_directory():
    if os.path.exists(INPUT_FILE_PATH):
        return

    try:
        os.makedirs(INPUT_FILE_PATH)
    except PermissionError:
        Logger.info(
            "Permission denied: Unable to create directory"
            " '%s'. Attempting to use sudo.",
            INPUT_FILE_PATH,
        )
        result = subprocess.run(["sudo", "mkdir", "-p", INPUT_FILE_PATH], check=True)
        if result.returncode == 0:
            subprocess.run(
                ["sudo", "chown", f"{os.getlogin()}:{os.getlogin()}", INPUT_FILE_PATH],
                check=True,
            )
            Logger.info("Directory '%s' created with sudo.", INPUT_FILE_PATH)
        else:
            Logger.info("Failed to create directory even with sudo.")


if __name__ == "__main__":
    make_output_directory()
    run()
