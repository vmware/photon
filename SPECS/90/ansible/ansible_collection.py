#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText 2022 Maxwell G <gotmax@e.email>

"""
This script uses Ansible Collection metadata from galaxy.yml to figure out the
namespace, name, and version of the collection being packaged.

``ansible_collection.py install`` (used by %ansible_collecton_install) uses
this information to find and install the collection artifact that was just
built with %ansible_collection_build. It also generates a files list for use
with `%files -f`.

``ansible_collection.py test`` (used by %ansible_test_unit) parses galaxy.yml
to determine the collection namespace and name that's needed to create the
directory structure that ansible-test expects. After creating a temporary build
directory with the needed structure, the script runs ansible-test units with
the provided arguments.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, Optional, Sequence, Union

from yaml import CSafeLoader, load


class CollectionError(Exception):
    pass


class AnsibleCollection:
    def __init__(self, collection_srcdir: Optional[Path] = None) -> None:
        self.collection_srcdir = collection_srcdir or Path.cwd()
        self.data = self._load_data()
        self.namespace = self.data["namespace"]
        self.name = self.data["name"]
        self.version = self.data["version"]

    def _load_data(self) -> Dict[str, Any]:
        path = self.collection_srcdir / "galaxy.yml"
        if not path.exists():
            raise CollectionError(f"{path} does not exist!")
        print(f"Loading collection metadata from {path}")

        with open(path, encoding="utf-8") as file:
            return load(file, Loader=CSafeLoader)

    def install(self, destdir: Union[str, Path]) -> None:
        artifact = self.collection_srcdir / Path(
            f"{self.namespace}-{self.name}-{self.version}.tar.gz"
        )
        if not artifact.exists() and not artifact.is_file():
            raise CollectionError(
                f"{artifact} does not exist! Did you run %ansible_collection_build?"
            )

        args = (
            "ansible-galaxy",
            "collection",
            "install",
            "-n",
            "-p",
            str(destdir),
            str(artifact),
        )
        print(f"Running: {args}")
        print()
        # Without this, the print statements are shown after the command
        # output when building in mock.
        sys.stdout.flush()
        subprocess.run(args, check=True, cwd=self.collection_srcdir)
        print()

    def write_filelist(self, filelist: Path) -> None:
        filelist.parent.mkdir(parents=True, exist_ok=True)
        contents = "%{ansible_collections_dir}/" + self.namespace
        print(f"Writing filelist to {filelist}")
        with open(filelist, "w", encoding="utf-8") as file:
            file.write(contents)

    def unit_test(self, extra_args: Sequence) -> None:
        with TemporaryDirectory() as temp:
            temppath = Path(temp) / "ansible_collections" / self.namespace / self.name
            shutil.copytree(
                self.collection_srcdir,
                temppath,
            )
            args = ("ansible-test", "units", *extra_args)
            print(f"Running: {args}")
            print()
            # Without this, the print statements are shown after the command
            # output when building in mock.
            sys.stdout.flush()
            subprocess.run(args, cwd=temppath, check=True)


def parseargs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "Install and test Ansible Collections in an rpmbuild environment"
    )
    subparsers = parser.add_subparsers(dest="action")
    install_parser = subparsers.add_parser(
        "install",
        help="Run ansible-galaxy collection install and write filelist",
    )
    install_parser.add_argument(
        "--collections-dir",
        required=True,
        help="Collection destination directory",
        type=Path,
    )
    install_parser.add_argument(
        "--filelist",
        type=Path,
        required=True,
        help="%%{ansible_collection_filelist}",
    )

    test_parser = subparsers.add_parser(
        "test",
        help="Run ansible-test unit after creating the necessary directory structure",
    )
    test_parser.add_argument(
        "extra_args", nargs="*", help="Extra arguments to pass to ansible-test"
    )
    args = parser.parse_args()
    # add_subparsers does not support required on Python 3.6
    if not args.action:
        parser.print_usage()
        sys.exit(2)
    return args


def main():
    args = parseargs()
    collection = AnsibleCollection()
    if args.action == "install":
        collection.install(args.collections_dir)
        collection.write_filelist(args.filelist)
    elif args.action == "test":
        collection.unit_test(args.extra_args)


if __name__ == "__main__":
    try:
        main()
    except (CollectionError, subprocess.CalledProcessError) as err:
        sys.exit(err)
