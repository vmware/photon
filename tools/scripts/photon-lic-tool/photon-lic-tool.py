#!/usr/bin/python

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
import signal
import shutil
import yaml
from argparse import ArgumentParser

from DockerUtil import DockerUtil
from Comparator import Comparator
from ExpCleaner import ExpCleaner
from Validator import Validator
from Scanner import Scanner
from LicDB import LicDB
import common
from common import err_exit, pr_err, read_license_from_file

try:
    import scancode_config
except ImportError:
    print("Failed to import scancode_config, do 'pip3 install scancode-toolkit'")
    raise


def sig_handler(sig, frame):
    err_exit()


# check if scancode package is up to date
# it is important to have an updated license DB
def check_scancode_ver():
    print("Checking scancode-toolkit version before run...")
    sc_version = scancode_config.__version__

    if sc_version != common.sc_toolkit_cicd_ver:
        err_exit(
            "scancode-toolkit version does not match CI/CD version!\n"
            + f"Local version: {sc_version}\n"
            + f"CI/CD version: {common.sc_toolkit_cicd_ver}\n"
        )

    print("scancode-toolkit up to date")


def scan(args):
    scanner = Scanner()
    scanner.scan(
        build_spec=args.build_spec,
        score=args.score,
        yaml=args.yaml,
        cpus=args.cpus,
        docker=args.docker,
        path=args.path,
        alt_src_url=args.alt_src_url,
    )


def validate(args):
    validator = Validator()
    license_expressions = {}

    # read from file
    if args.f:
        license_expressions = read_license_from_file(args.f)
    # read from stdin
    elif args.i:
        license_expressions["stdin"] = args.i
    else:
        err_exit("License expression must be provided!")

    validator.validate(license_expressions)


def lic_db(args):
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
    license_expressions = dict()
    cleaner = ExpCleaner()

    if args.i:
        license_expressions["stdin"] = args.i
    elif args.f:
        license_expressions = read_license_from_file(args.f)

    cleaner.clean_exp(license_expressions)


def compare_exps(args):
    comparator = Comparator()
    comparator.compare_exps(args.a, args.b)


def docker_entry(args):
    docker_util = DockerUtil()
    if args.build:
        docker_util.create_docker_image()

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
            common.known_failures = config_yaml["known_failures"]
        except KeyError as exception:
            err_exit(f"Missing required field in {config_path}!\n{exception}")


def parse_input():
    parser = ArgumentParser(description="Photon License Tool")
    subparsers = parser.add_subparsers(
        help="""--help|-h for more info on individual sub-commands.
Works recursively for all levels."""
    )

    ########## VALIDATE ##############################
    validate_sub_p = subparsers.add_parser(
        "validate",
        help="""Validate a given SPDX expression for
semantic correctness. Does not validate accuracy.""",
    )
    validate_sub_p.add_argument(
        "-f",
        action="store",
        help="""Read SPDX expression from input file.
This assumes the format: License: <spdx expression>""",
    )
    validate_sub_p.add_argument(
        "-i", action="store", help="Read SPDX expression directly from stdin"
    )
    validate_sub_p.set_defaults(func=validate)
    ########## END VALIDATE ###########################

    ########## SCAN ###################################
    scan_sub_p = subparsers.add_parser(
        "scan",
        help="""Scan all files in the given file,
i.e tarball, src RPM, etc. Produces a full SPDX expression.""",
    )
    scan_sub_p.add_argument(
        "--path", action="store", help="Path to file/directory to be scanned."
    )
    scan_sub_p.add_argument(
        "--yaml",
        action="store",
        help="""Optional. Produce yaml document mapping each
SPDX identifier to the file it was discovered in. Save to the specified path.""",
    )

    scan_sub_p.add_argument(
        "--score",
        action="store",
        help="Optional. Set the minimum license matching score.",
    )

    scan_sub_p.add_argument(
        "--redis_host",
        action="store",
        help="Optional. Host name for redis cache. Both host and port are required.",
    )

    scan_sub_p.add_argument(
        "--redis_port",
        action="store",
        help="Optional. Port for redis cache. Both host and port are required.",
    )

    scan_sub_p.add_argument(
        "--redis_ttl",
        action="store",
        help="Optional. TTL for entries in the redis cache",
    )

    scan_sub_p.add_argument(
        "--docker",
        action="store_true",
        help="Optional. Run scan inside docker container.",
    )

    scan_sub_p.add_argument(
        "--cpus",
        action="store",
        help="Optional. Number of CPUs to use for scanning",
    )

    scan_sub_p.add_argument(
        "--no_trim",
        action="store_true",
        help="""Do not trim license DB to remove unofficial licenses before
scanning. Also will not restore license DB after the scan.""",
    )

    scan_sub_p.add_argument(
        "--alt_src_url",
        action="store",
        help="""Provide an alternative URL to download sources from,
in addition to packages.vmware.com""",
    )

    scan_sub_p.add_argument(
        "--build_spec",
        action="store_true",
        help="""Indicates that the path given points to a SPEC file within Photon,
and the package source should be built and scanned. Otherwise, scan will just be
for the SPEC file only.""",
    )

    scan_sub_p.set_defaults(func=scan)
    ########## END SCAN ###################################

    ########## LIC-DB ###################################
    licdb_sub_p = subparsers.add_parser(
        "lic-db",
        help="Operations on the scancode license database",
    )
    licdb_sub_p.add_argument(
        "--trim",
        action="store_true",
        help="""Trim DB by removing unofficial (non-SPDX)
licenses. Does NOT impact the database index used for license expression
validation.""",
    )
    licdb_sub_p.add_argument(
        "--restore", action="store_true", help="Restore DB with all licenses"
    )

    licdb_sub_p.set_defaults(func=lic_db)
    ########## END LIC-DB ###################################

    ########## CLEAN ###################################
    clean_sub_p = subparsers.add_parser(
        "clean-exp",
        help="Cleanup/flatten the given expression",
    )

    clean_sub_p.add_argument(
        "-i", action="store", help="Read SPDX expression directly from stdin"
    )

    clean_sub_p.add_argument(
        "-f",
        action="store",
        help="""Read SPDX expression from input file.
This assumes the format: License: <spdx expression>""",
    )

    clean_sub_p.set_defaults(func=clean_exp)
    ########## END CLEAN ###################################

    ########## COMPARE ###################################
    compare_sub_p = subparsers.add_parser(
        "compare",
        help="Compare two license expressions for equivalency",
    )

    compare_sub_p.add_argument(
        "-a", action="store", help="SPDX expresssion A. Can be stdin or file."
    )

    compare_sub_p.add_argument(
        "-b", action="store", help="SPDX expression B. Can be stdin or file."
    )

    compare_sub_p.set_defaults(func=compare_exps)
    ########## END COMPARE ###################################

    docker_sub_p = subparsers.add_parser(
        "docker",
        help="Manipulate docker capabilities",
    )

    docker_sub_p.add_argument(
        "--build", action="store_true", help="Build the docker image"
    )

    docker_sub_p.add_argument(
        "--clean-img", action="store_true", help="Force deletion of docker image."
    )

    docker_sub_p.set_defaults(func=docker_entry)

    args = parser.parse_args()

    return args


# check for prerequisites before running
def check_prereqs(cmd_name=None):
    ret = 0

    if cmd_name == "--help":
        return ret

    # these are required only for scanning
    if cmd_name is None or cmd_name == "scan":
        # check for rpm command existence
        if not shutil.which("rpm"):
            pr_err(
                "'rpm' command not found, please install with "
                + "'tdnf install -y rpm'"
            )
            ret = -1

        # check for scancode command existence
        if not shutil.which("scancode"):
            pr_err(
                "'scancode' command not found, please install with "
                + "'pip3 install scancode-toolkit'"
            )
            ret = -1

        # check for extractcode command existence
        if not shutil.which("extractcode"):
            pr_err(
                "'extractcpde' command not found, please install with "
                + "'tdnf install -y extractcode'"
            )
            ret = -1

        # check for rpmbuild command existence
        if not shutil.which("rpmbuild"):
            pr_err(
                "'rpmbuild' command not found, please install with "
                + "'tdnf install -y rpm-build'"
            )
            ret = -1

    # check for pip3 command existence
    if not shutil.which("pip3"):
        pr_err(
            "'pip3' command not found, please install with "
            + "'tdnf install -y python3-pip'"
        )
        ret = -1

    # check for rpmspec command existence, required for reading from spec files
    if not shutil.which("rpmspec"):
        pr_err(
            "'rpmspec' command not found, please install with "
            + "'tdnf install -y rpm-build'"
        )
        ret = -1

    return ret


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

    if check_prereqs(sys.argv[1]) < 0:
        return -1

    check_scancode_ver()

    # proper cleanup on unexpected exits
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    parse_config(common.config_path)

    args = parse_input()

    set_global_options(args)

    args.func(args)


if __name__ == "__main__":
    main()
