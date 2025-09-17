#!/usr/bin/env python3

# Photon License Scanning and Validation Tool
# This tool is intended for use by developers to aid
# in license scanning of source code and validation
# of license expressions.
#
# Examples
#
# Scanning
# photon-lic-tool.py scan --path <absolute path> --yaml scancode-output.yaml
#
# Validation
# photon-lic-tool.py validate -f SPECS/kpatch/license.txt
# or
# photon-lic-tool.py validate -i "Apache-2.0 AND GPL-1.0-Only"
#
# License DB Operations
# photon-lic-tool.py lic-db --trim
# or
# photon-lic-tool.py lic-db --restore

import sys
import os
import yaml
import atexit
import common

from argparse import ArgumentParser
from DockerUtil import DockerUtil
from Comparator import Comparator
from ExpCleaner import ExpCleaner
from Validator import Validator
from Scanner import Scanner
from common import err_exit, pr_err, SignalContext

def scan(args):
    scanner = Scanner()
    if not args.config_yaml:
        scanner.scan(
            build_spec=args.build_spec,
            score=args.score,
            yaml_out=args.yaml,
            cpus=args.cpus,
            docker=args.docker,
            path=args.path,
            alt_src_url=args.alt_src_url,
            extra_repo_urls=args.extra_repo_urls,
        )
    else:
        scanner.scan_config_yaml(
            build_spec=args.build_spec,
            score=args.score,
            yaml_out=args.yaml,
            cpus=args.cpus,
            docker=args.docker,
            path=args.path,
            alt_src_url=args.alt_src_url,
            extra_repo_urls=args.extra_repo_urls,
            config_yaml=args.config_yaml,
        )


def validate(args):
    validator = Validator()
    validator.validate(file=args.f, stdin=args.i)


def lic_db(args):
    from LicDB import LicDB

    lic_db = LicDB()

    if args.trim:
        try:
            lic_db.trim_lic_db()
        except Exception as e:
            pr_err(f"Failed to trim license database: {e}")
            lic_db.restore_lic_db()
            err_exit()

    if args.restore:
        try:
            lic_db.restore_lic_db()
        except Exception as e:
            err_exit(f"Failed to restore license database: {e}")


def clean_exp(args):
    cleaner = ExpCleaner()
    cleaner.clean_exp(file=args.f, stdin=args.i)


def compare_exps(args):
    comparator = Comparator()

    if not args.a:
        err_exit("Please input expression A with -a <exp>")

    if not args.b:
        err_exit("Please input expression B with -b <exp>")

    comparator.compare_exps(args.a, args.b)


def docker_entry(args):
    docker_util = DockerUtil()
    if args.build:
        docker_util.ensure_docker_image()

    if args.clean_img:
        docker_util.clean_docker_image()


# Set global variables from config.yaml
def parse_config(config_path=None):
    if not config_path:
        err_exit("Configuration YAML file is required!")

    with open(config_path, "r") as config_f:
        config_yaml = yaml.load(config_f, Loader=yaml.SafeLoader)

    try:
        common.ignore_list = config_yaml["license_ignore_list"]
        common.disallowed_licenses = config_yaml["disallowed_licenses"]
        common.redis_host = config_yaml["redis_host"]
        common.redis_port = config_yaml["redis_port"]
        common.redis_ttl = config_yaml["redis_ttl"]
        common.no_trimming = config_yaml["no_trimming"]
    except KeyError as exception:
        err_exit(f"Missing required field in {config_path}!\n{exception}")


def parse_input():
    parser = ArgumentParser(description="Photon License Tool")

    subparsers = parser.add_subparsers(
        help="""--help|-h for more info on individual sub-commands.
 Works recursively for all levels."""
    )

    # Define subcommand metadata
    commands = {
        "validate": {
            "help": "Validate a given SPDX expression for semantic correctness. Does not validate accuracy.",
            "func": validate,
            "args": [
                (
                    "-f",
                    {
                        "action": "store",
                        "help": "Read SPDX expression from input file. Format: License: <expression>",
                    },
                ),
                (
                    "-i",
                    {
                        "action": "store",
                        "help": "Read SPDX expression directly from stdin",
                    },
                ),
            ],
        },
        "scan": {
            "help": "Scan all files in the given file (tarball, SRPM, etc.) and produce an SPDX expression.",
            "func": scan,
            "args": [
                (
                    "--path",
                    {
                        "action": "store",
                        "help": "Path to file/directory to be scanned.",
                    },
                ),
                (
                    "--yaml",
                    {
                        "action": "store",
                        "help": "Output YAML mapping SPDX IDs to files.",
                    },
                ),
                (
                    "--score",
                    {
                        "action": "store",
                        "help": "Minimum license matching score.",
                    },
                ),
                (
                    "--redis_host",
                    {"action": "store", "help": "Redis host for caching."},
                ),
                (
                    "--redis_port",
                    {"action": "store", "help": "Redis port for caching."},
                ),
                (
                    "--redis_ttl",
                    {"action": "store", "help": "TTL for Redis entries."},
                ),
                (
                    "--docker",
                    {
                        "action": "store_true",
                        "help": "Run scan inside Docker container.",
                    },
                ),
                (
                    "--cpus",
                    {"action": "store", "help": "Number of CPUs to use."},
                ),
                (
                    "--no_trim",
                    {
                        "action": "store_true",
                        "help": "Do not trim unofficial licenses.",
                    },
                ),
                (
                    "--alt_src_url",
                    {"action": "store", "help": "Alternative source URL."},
                ),
                (
                    "--extra_repo_urls",
                    {
                        "action": "store",
                        "help": "Comma-separated extra tdnf repo URLs.",
                    },
                ),
                (
                    "--build_spec",
                    {
                        "action": "store_true",
                        "help": "Path is a SPEC file to build and scan.",
                    },
                ),
                (
                    "--config_yaml",
                    {
                        "action": "store",
                        "help": "Path to output newly scanned config.yaml",
                    },
                ),
            ],
        },
        "lic-db": {
            "help": "Operations on the scancode license database.",
            "func": lic_db,
            "args": [
                (
                    "--trim",
                    {
                        "action": "store_true",
                        "help": "Trim unofficial licenses from DB.",
                    },
                ),
                (
                    "--restore",
                    {
                        "action": "store_true",
                        "help": "Restore DB with all licenses.",
                    },
                ),
            ],
        },
        "clean-exp": {
            "help": "Cleanup/flatten the given SPDX expression.",
            "func": clean_exp,
            "args": [
                (
                    "-i",
                    {
                        "action": "store",
                        "help": "Read SPDX expression from stdin.",
                    },
                ),
                (
                    "-f",
                    {
                        "action": "store",
                        "help": "Read SPDX expression from file.",
                    },
                ),
            ],
        },
        "compare": {
            "help": "Compare two license expressions for equivalency.",
            "func": compare_exps,
            "args": [
                (
                    "-a",
                    {
                        "action": "store",
                        "help": "SPDX expression A (stdin or file).",
                    },
                ),
                (
                    "-b",
                    {
                        "action": "store",
                        "help": "SPDX expression B (stdin or file).",
                    },
                ),
            ],
        },
        "docker": {
            "help": "Manipulate Docker capabilities.",
            "func": docker_entry,
            "args": [
                (
                    "--build",
                    {
                        "action": "store_true",
                        "help": "Build the Docker image.",
                    },
                ),
                (
                    "--clean-img",
                    {"action": "store_true", "help": "Delete Docker image."},
                ),
            ],
        },
    }

    for cmd_name, cmd_data in commands.items():
        sub_p = subparsers.add_parser(cmd_name, help=cmd_data["help"])
        for arg_name, arg_opts in cmd_data.get("args", []):
            sub_p.add_argument(arg_name, **arg_opts)
        sub_p.set_defaults(func=cmd_data["func"])

    return parser.parse_args()


def set_global_options(args):
    if not args:
        return

    # command line options get precedence over config options
    if "redis_host" in args and args.redis_host:
        common.redis_host = args.redis_host
    if "redis_port" in args and args.redis_port:
        common.redis_port = args.redis_port
    if "redis_ttl" in args and args.redis_ttl:
        common.redis_ttl = args.redis_ttl
    if "no_trim" in args and args.no_trim:
        common.no_trimming = True
    else:
        common.no_trimming = common.no_trimming.lower() == "true"

    common.tool_filename = os.path.basename(__file__)


def main():
    # print help if no args given on cmdline
    if len(sys.argv) <= 1:
        sys.argv.append("--help")

    atexit.register(common.cleanup)

    parse_config(common.config_path)

    args = parse_input()

    set_global_options(args)

    def default_handler(sig, frame):
        raise Exception("Interrupted")

    with SignalContext(default_handler):
        args.func(args)

    atexit.unregister(common.cleanup)


if __name__ == "__main__":
    main()
