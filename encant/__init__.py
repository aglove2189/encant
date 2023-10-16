import argparse
import io
import os
import platform
import re
import shutil
import tarfile
from typing import Union

import requests

RELEASE_URL = "https://api.github.com/repos/indygreg/python-build-standalone/releases"
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), ".snakes")
sysname = platform.system().lower()
machine = platform.machine().lower()
machine = {"arm64": "aarch64", "amd64": "x86_64"}.get(machine, machine)


def get(version: str) -> str:
    r = requests.get(RELEASE_URL)
    r.raise_for_status()
    for row in r.json():
        for asset in row["assets"]:
            name = asset["name"]
            if all([i in name for i in (sysname, machine, version, "install_only")]):
                return asset["browser_download_url"]
    raise ValueError(
        f"{version} not found for {sysname}_{machine}. Either you have a typo or this version was "
        "never released by indygreg: https://github.com/indygreg/python-build-standalone/releases."
    )


def extract(obj: bytes, version: str, path: Union[str, os.PathLike]) -> None:
    with tarfile.open(mode="r|*", fileobj=io.BytesIO(obj)) as tf:
        tf.extractall(path)

    fsrc = os.path.join(path, "python")
    fdest = os.path.join(path, version)
    if os.path.exists(fdest):
        print(f"{fdest} already exists, overwriting")
    shutil.copytree(fsrc, fdest, dirs_exist_ok=True)
    shutil.rmtree(fsrc)
    print(f"Successfully added {version} to {fdest}")


def add(version: str) -> None:
    url = get(version)
    r = requests.get(url)

    if version.count(".") == 1:
        # if a user only provides the major.minor version, we need to parse out the actual version
        # pulled from the releases. e.g. 3.10 will pull and save out 3.10.13
        version = re.search(r"3\.[0-9]+\.[0-9]+", url)[0]
        print(f"major.minor only version detected, pulling latest: {version}")

    extract(r.content, version, path=DEFAULT_OUTPUT_DIR)


def list() -> None:
    print(*os.listdir(DEFAULT_OUTPUT_DIR), sep="\n")


def remove(version: str) -> None:
    path = os.path.join(DEFAULT_OUTPUT_DIR, version)
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Successfully removed {version}")
    else:
        print(f"{version} doesn't seem to exist")


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    add_parser = subparsers.add_parser("add", help="add a python version")
    subparsers.add_parser("list", help="list all python versions added")
    remove_parser = subparsers.add_parser("remove", help="remove a python version")
    for command in (add_parser, remove_parser):
        command.add_argument("version", type=str, nargs="+", help="python version")

    args = parser.parse_args()
    if args.command == "add":
        [add(version) for version in args.version]
    elif args.command == "list":
        list()
    elif args.command == "remove":
        [remove(version) for version in args.version]
    elif args.command is None:
        parser.print_help()
    else:
        print(f"ERROR: unknown command '{args.command}'")


if __name__ == "__main__":
    cli()
