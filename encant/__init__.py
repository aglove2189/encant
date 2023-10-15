import argparse
import io
import os
import re
import shutil
import tarfile

import requests
from loguru import logger

RELEASE_URL = "https://api.github.com/repos/indygreg/python-build-standalone/releases"
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), ".snakes")
sysname, _, _, _, machine = os.uname()
sysname = sysname.lower()
machine = "aarch64" if machine == "arm64" else machine


def get(version: str) -> str:
    r = requests.get(RELEASE_URL)
    r.raise_for_status()
    for row in r.json():
        for asset in row["assets"]:
            name = asset["name"]
            if all([i in name for i in (sysname, machine, version, "install_only")]):
                return asset["browser_download_url"]
    raise ValueError(
        f"{version} not found. Either you have a typo or this version was never released by "
        "indygreg: https://github.com/indygreg/python-build-standalone/releases"
    )


def extract(obj: bytes, version: str, path: str | os.PathLike) -> None:
    with tarfile.open(mode="r|*", fileobj=io.BytesIO(obj)) as tf:
        tf.extractall(path)

    fsrc = os.path.join(path, "python")
    fdest = os.path.join(path, version)
    if os.path.exists(fdest):
        logger.warning(f"{fdest} already exists, overwriting")
    shutil.copytree(fsrc, fdest, dirs_exist_ok=True)
    shutil.rmtree(fsrc)
    logger.success(f"{version} written to {fdest}")


def main(version: str, path: str | os.PathLike = DEFAULT_OUTPUT_DIR) -> None:
    url = get(version)
    r = requests.get(url)

    if version.count(".") == 1:
        # if a user only provides the major.minor version, we need to parse out the actual version
        # pulled from the releases. e.g. 3.10 will pull and save out 3.10.13
        version = re.search(r"3\.[0-9]+.[0-9]+", url)[0]
        logger.info(f"major.minor only version detected, pulling latest: {version}")

    extract(r.content, version, path=path)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("version", type=str, help="python version to pull")
    parser.add_argument(
        "--path",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f"path to save to, defaults to {DEFAULT_OUTPUT_DIR}",
    )
    args = parser.parse_args()
    main(args.version, args.path)


if __name__ == "__main__":
    cli()
