# This file holds global constants and common/general functions

import sys
import subprocess
import site
import os
import shutil
import json
import time
import yaml

try:
    import license_expression
except ImportError:
    print("license_expression import failed, do 'pip3 install license_expression'")
    raise

try:
    from license_tree import license_tree
except ImportError:
    print(
        'Failed to import local library "license_tree".'
        + "license_tree is found in "
        + "photon/tools/scripts/photon-lic-tool/license_tree"
    )
    raise

################ Constants ######################################
user_home = os.path.expanduser("~")
ph_scan_tool_dir = f"{user_home}/.ph-scanner-tool"

# Absolute path to the tool's parent directory
tool_dir_path = os.path.abspath(os.path.dirname(__file__))

# Default value, will also be overwritten in photon-lic-tool.py
tool_filename = "photon-lic-tool.py"

if os.geteuid() == 0:
    site_pkg_dir = site.getsitepackages()[0]
else:
    site_pkg_dir = site.getusersitepackages()[0]

db_dir = f"{site_pkg_dir}/licensedcode/data/licenses"
rules_dir = f"{site_pkg_dir}/licensedcode/data/rules/"

ph_scan_dir = f"{ph_scan_tool_dir}/scan_dir"
tmp_lic_db = f"{ph_scan_tool_dir}/unofficial-license.db"
tmp_rules_dir = f"{ph_scan_tool_dir}/unofficial-rules.db"
rpm_install_root = f"{ph_scan_dir}/rpmbuild"
rpm_build_root = f"{rpm_install_root}/usr/src/photon"
config_path = f"{tool_dir_path}/photon-lic-tool.yaml"
cached_yaml_fn = "cached.yaml"

sc_toolkit_cicd_ver = "32.2.1"

spdx_data_base_url = "https://raw.githubusercontent.com/spdx/license-list-data/"
spdx_license_list_ext = "refs/heads/main/json/licenses.json"
spdx_exceptions_list_ext = "refs/heads/main/json/exceptions.json"
#################################################################

################ Globals from config yaml #######################
ignore_list = []
disallowed_licenses = []

# Optional redis cache to speed up scanning
redis_host = None
redis_port = None
redis_ttl = "31536000"  # Default to 1 year (seconds)

# Config option to disable license trimming on scans or other commands
no_trimming = False

# List of files to skip during scanning, as they will fail the scanner
known_failures = []
###################################################################


def err_exit(msg=None):
    if msg:
        pr_err(msg)

    cleanup()
    sys.exit(1)


def run_cmd(cmd, ignore_rc=False, quiet=False, capture=True):
    result = None

    if not cmd:
        return None

    if type(cmd) is str:
        cmd = cmd.split()

    if not quiet:
        print(f"RUNNING CMD: {' '.join(cmd)}")

    if capture:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        result = subprocess.run(cmd)

    if not ignore_rc and result.returncode != 0:
        err_exit(f"Failed to run command {cmd}\n: {result.stdout.decode()}")

    return result


def pr_err(msg):
    print(f"{msg}", file=sys.stderr)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


# rpm */SOURCES dir requires all patches to be on the first level,
# instead of nested inside directories as in the Photon spec dir
# so use this function to copy without preserving directory structure.
def copy_flat(src_dir=None, dst_dir=None):
    if not src_dir or not dst_dir:
        return

    for root, _, files in os.walk(src_dir):
        for filename in files:
            src_path = os.path.join(root, filename)
            dst_path = os.path.join(dst_dir, filename)
            shutil.copy2(src_path, dst_path)


def cleanup():
    if os.path.exists(ph_scan_dir):
        shutil.rmtree(ph_scan_dir)

    if os.path.exists(rpm_install_root):
        shutil.rmtree(rpm_install_root)


def download_file(input_url=None, output_path=None, allow_failure=False):
    try:
        import requests
    except ImportError:
        pr_err("requests not found, install with 'pip install requests'")
        raise

    if not input_url or not output_path:
        err_exit("download_file() requires input url and output path!")

    print(f"DOWNLOADING FILE: {input_url}")

    retries = 5
    while retries > 0:
        response = requests.get(input_url, stream=True)

        if response.status_code != 200:
            retries -= 1
            if retries > 0:
                pr_err(
                    f"{input_url} returned code: {response.status_code}, "
                    "retrying after delay..."
                )
                time.sleep(5)
            elif not allow_failure:
                err_exit(
                    f"ERROR: Exhausted all retries getting {input_url}!\n"
                    f"Final error code: {response.status_code}"
                )

            else:
                return -1

            continue

        with open(output_path, "wb") as out_f:
            for chunk in response.iter_content(chunk_size=8192):
                out_f.write(chunk)
        break

    return 0


def strip_license_id(lic_id=None):
    if not lic_id:
        return ""

    lic_id = lic_id.strip()

    # strip any overarching parantheses from the expression
    if lic_id.startswith("(") and lic_id.endswith(")"):
        # check to see if these parantheses match
        # there is a chance they dont, ex) (A AND B) AND (C AND D)
        i = 0
        open_paran = 0
        for char in lic_id:
            if char == "(":
                open_paran += 1
            elif char == ")":
                open_paran -= 1

            if open_paran == 0:
                break

            i += 1

        # if we get the closing paran for the very first one
        # at the end, then strip it from both ends
        if i == len(lic_id) - 1:
            lic_id = lic_id[1:-1]

    return lic_id


# cleans any ignorable SPDX IDs from the expression, such as standalone
# exceptions or other license IDs in the ignore list like
# "LicenseRef-unknown-spdx"
def cleanup_license_expression(ignore_list=None, exception_list=None, license_exp=None):
    if not license_exp:
        return None

    lic_tree = license_tree.create_exp_tree(license_exp, exception_list, ignore_list)
    parsed_exp = license_tree.render_exp_tree(lic_tree)

    # remove duplicates - this returns a set
    top_lvl_exps = extract_top_level_expressions(parsed_exp)
    parsed_exp = " AND ".join(top_lvl_exps)

    # do some cleanup for us
    if parsed_exp:
        licensing = license_expression.get_spdx_licensing()
        return licensing.parse(parsed_exp).render()

    return parsed_exp


# to get the top level license expressions, we can't
# simply split with "AND". We need to split on all AND/OR,
# but keep all parantheses together
def extract_top_level_expressions(spdx_exp=None):
    if not spdx_exp:
        return ""

    # this should not have duplicates.
    # not using a set because want to preserve order
    expressions = []
    i = 0
    start_pos = 0
    end_pos = 0
    paran_str = ""
    original_exp = spdx_exp.strip()
    while i < len(spdx_exp):
        # get everything inside the parantheses
        if spdx_exp[i] == "(":
            start_pos = i
            open_paran = 1
            i += 1
            while open_paran > 0 and i < len(spdx_exp):
                if spdx_exp[i] == "(":
                    open_paran += 1
                elif spdx_exp[i] == ")":
                    open_paran -= 1
                i += 1

            end_pos = i

            paran_str = spdx_exp[start_pos:end_pos]
            if paran_str not in expressions:
                expressions.append(paran_str)
            spdx_exp = spdx_exp[:start_pos] + " " * len(paran_str) + spdx_exp[end_pos:]
        i += 1

    # Handle top level OR - whole expression should be concatenated
    # and put inside parantheses. Any OR left over will be a top level OR
    if "OR" in spdx_exp:
        exp = f"{original_exp}"
        if exp not in expressions:
            expressions.append(exp)
    else:
        # get the rest of the licenses without the parantheses
        # All "OR" expressions should already be in parantheses
        for exp in spdx_exp.split("AND"):
            exp = strip_license_id(exp)
            if not exp or exp.isspace() or exp in expressions:
                continue

            expressions.append(exp)

    return expressions


# From extractcode (universal extractor), get the list of all recognizable
# archive extensions. We can use this to determine if a file is an archive.
# Modeled from print_archive_formats() in:
# https://github.com/aboutcode-org/extractcode/blob/main/src/extractcode/cli.py#L35
def get_all_extractable_exts():
    from itertools import groupby
    from extractcode.archive import archive_handlers

    exts = set()

    kindkey = lambda x: x.kind
    by_kind = groupby(sorted(archive_handlers, key=kindkey), key=kindkey)
    for kind, handlers in by_kind:
        for handler in handlers:
            for ext in handler.extensions:
                exts.add(ext)

    return exts


# Checks if the file path or URL points to an extractable file.
def is_extractable(file_path=None):
    if not file_path:
        return None

    extractable_exts = get_all_extractable_exts()

    for ext in extractable_exts:
        if file_path.endswith(ext):
            return True

    return False


# get list of exceptions from spdx repo
def get_exceptions_list():
    exception_list = []
    exceptions_json_loc = "/tmp/exceptions.json"
    exceptions_json = None
    exceptions_url = f"{spdx_data_base_url}/{spdx_exceptions_list_ext}"

    if os.path.exists(exceptions_json_loc):
        os.remove(exceptions_json_loc)

    download_file(exceptions_url, exceptions_json_loc)

    with open(exceptions_json_loc, "r") as spdx_exceptions_json:
        exceptions_json = json.load(spdx_exceptions_json)

    for exception in exceptions_json["exceptions"]:
        exception_list.append(exception["licenseExceptionId"])

    os.remove(exceptions_json_loc)

    return exception_list


# get list of official spdx licenses from spdx repo
def get_official_spdx_list():
    spdx_list = []
    spdx_json_loc = "/tmp/official-spdx.json"
    spdx_json = None
    spdx_url = f"{spdx_data_base_url}/{spdx_license_list_ext}"

    if os.path.exists(spdx_json_loc):
        os.remove(spdx_json_loc)

    download_file(spdx_url, spdx_json_loc)

    with open(spdx_json_loc, "r") as spdx_json:
        spdx_json = json.load(spdx_json)

    for exception in spdx_json["licenses"]:
        spdx_list.append(exception["licenseId"])

    os.remove(spdx_json_loc)

    return spdx_list


# Copies all files for spec to the rpm build root
def copy_spec_to_rpm_build_root(spec_path=None):
    spec_fn = ""

    if not spec_path:
        return

    spec_fn = os.path.basename(spec_path)

    # clean the working dir
    if os.path.exists(rpm_install_root):
        shutil.rmtree(rpm_install_root)

    os.makedirs(f"{rpm_build_root}/SOURCES")

    # just copy everything to SOURCES
    try:
        copy_flat(os.path.dirname(spec_path), f"{rpm_build_root}/SOURCES")
    except Exception as e:
        err_exit(f"Failed to copy Photon spec dir to build root: {e}")

    os.makedirs(f"{rpm_build_root}/SPECS")
    shutil.move(
        f"{rpm_build_root}/SOURCES/{spec_fn}", f"{rpm_build_root}/SPECS/{spec_fn}"
    )


def read_license_from_file(file_path=None):
    license_expressions = dict()
    lines = []

    if not file_path:
        return None

    if not os.path.exists(file_path):
        err_exit(f"ERROR: Invalid license file path: {file_path}")

    if file_path.endswith(".spec") or file_path.endswith(".spec.in"):
        copy_spec_to_rpm_build_root(file_path)

        result = run_cmd(
            [
                "rpmspec",
                "-q",
                '--queryformat="License: %{Name}: %{License}\n"',
                "--define",
                f"%_topdir {rpm_build_root}",
                f"{rpm_build_root}/SPECS/{os.path.basename(file_path)}",
            ],
            ignore_rc=True,
        )

        # clean out rpm build root afterwards
        if os.path.exists(rpm_install_root):
            shutil.rmtree(rpm_install_root)

        if result.returncode != 0:
            err_exit(
                "Failed to extract license line from spec file!: "
                + f"{result.stdout.decode()}"
            )

        for line in result.stdout.decode().split("\n"):
            line = line.strip(" \r\t\n\"'")
            if line.startswith("License:"):
                line_spl = line.split(":")
                # (sub)package name : license expression
                license_expressions[line_spl[1].strip(" \r\t\n\"'")] = line_spl[
                    2
                ].strip(" \r\t\n\"'")

        if not license_expressions:
            err_exit(f"ERROR: No license expression found in {file_path}")

        return license_expressions
    elif file_path.endswith("config.yaml"):
        # parse the config.yaml
        with open(file_path, 'r') as config_yaml_f:
            config_yaml = yaml.load(config_yaml_f, yaml.SafeLoader)

        for source in config_yaml["sources"]:
            # use the archive name as not all will have a true "name" field
            source_name = source["archive"]
            license_concluded = source["spdx"]["package"]["license_concluded"]
            license_declared = source["spdx"]["package"]["license_declared"]

            license_expressions[f"{source_name}_concluded"] = license_concluded
            license_expressions[f"{source_name}_declared"] = license_declared
    else:
        with open(file_path, "r") as input_file:
            # should only be one line...
            lines = [line.rstrip() for line in input_file]

        if not lines:
            err_exit(f"ERROR: {file_path} is empty!")
        elif len(lines) > 1:
            err_exit(
                f"ERROR: More than one line found in {file_path}.  "
                + "Tool expects only one line: License: <SPDX Expression>"
            )

        if lines[0].startswith("License:"):
            license_expressions[file_path] = lines[0].split(":")[1].strip()

        if not license_expressions:
            err_exit(f"ERROR: No license expression found in {file_path}")

    return license_expressions
