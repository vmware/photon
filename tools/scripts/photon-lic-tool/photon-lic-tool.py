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
import subprocess
import shutil
import site
import multiprocessing
import re
import yaml
import signal
import json
import requests
import time
from argparse import ArgumentParser

try:
    import license_expression
except ImportError:
    print(
        "license_expression import failed, "
        + "do 'pip3 install license_expression'"
    )
    raise

try:
    from licensedcode.cache import get_index
except ImportError:
    print("licensedcode import failed, do 'pip3 install scancode-toolkit'")
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

# Constants
ph_scan_tool_dir = "/var/opt/ph-scanner-tool"
ph_scan_dir = f"{ph_scan_tool_dir}/scan_dir"
tmp_lic_db = f"{ph_scan_tool_dir}/unofficial-license.db"
tmp_rules_dir = f"{ph_scan_tool_dir}/unofficial-rules.db"
db_dir = f"{site.getsitepackages()[0]}/licensedcode/data/licenses"
rules_dir = f"{site.getsitepackages()[0]}/licensedcode/data/rules/"
rpm_install_root = f"{ph_scan_tool_dir}/rpmbuild"
rpm_build_root = f"{rpm_install_root}/usr/src/photon"

ignore_list = []
disallowed_licenses = []


def pr_err(msg):
    print(f"\n{msg}\n", file=sys.stderr)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def cleanup():
    if os.path.exists(ph_scan_dir):
        shutil.rmtree(ph_scan_dir)

    if os.path.exists(rpm_install_root):
        shutil.rmtree(rpm_install_root)


def sig_handler(sig, frame):
    err_exit()


def err_exit(msg=None):
    if msg:
        pr_err(msg)

    cleanup()
    sys.exit(1)


def run_cmd(cmd, ignore_rc=False, quiet=False):
    if not cmd:
        return None

    if type(cmd) is str:
        cmd = cmd.split()

    if not quiet:
        print(f"RUNNING CMD: {cmd}")

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    if not ignore_rc and result.returncode != 0:
        err_exit(f"Failed to run command {cmd}\n: {result.stdout.decode()}")

    return result


# check if scancode package is up to date
# it is important to have an updated license DB
def check_scancode_ver():
    print("Checking scancode-toolkit version before run...")
    result = run_cmd("pip list -o")

    lines = result.stdout.decode().split("\n")
    for line in lines:
        if "scancode" in line:
            print(
                "WARNING: scancode-toolkit may be out of date! Please update"
            )
            print(line)
            return
    print("scancode-toolkit up to date")


def trim_license_file(
    license_filename=None,
    taint=None,
    taint_lock=None,
    rule_ignore_list=None,
    rule_ignore_lock=None,
):
    ret = 0
    if license_filename is None:
        return -1

    with open(f"{db_dir}/{license_filename}", "r") as lic_f:
        key = ""
        lic_str = ""
        for line in lic_f:
            if line.startswith("key:"):
                key = line.split(":")[1].strip()
            elif line.startswith("spdx_license_key"):
                lic_str = line.split(":")[1].strip()

            if (
                lic_str
                and lic_str.startswith("LicenseRef")
                and "unknown-spdx" not in lic_str
            ):
                # dont search with this file,
                # move to some temp location
                res = run_cmd(
                    f"mv {db_dir}/{license_filename} {tmp_lic_db}".split(),
                    ignore_rc=True,
                    quiet=True,
                )
                ret = 0 if res.returncode == 0 else -1

                # ignore all rules that mention this key
                trim_rules_for_key(key, rule_ignore_list, rule_ignore_lock)
                break

    return ret


def trim_job(
    lic_f_list=None,
    rule_ignore_list=None,
    rule_ignore_lock=None,
    taint=None,
    taint_lock=None,
):

    if lic_f_list is None or rule_ignore_list is None:
        return

    for lic_file in lic_f_list:
        with taint_lock:
            if taint.value == 1:
                return

        if (
            trim_license_file(
                lic_file, taint, taint_lock, rule_ignore_list, rule_ignore_lock
            )
            != 0
        ):
            with taint_lock:
                taint.value = 1
            return


# Only search for official spdx licenses.
# Scancode-toolkit has many many other licenses that it
# recognizes, but these have no SPDX identifiers yet.
# Also, many of these "unofficial" licenses that scancode
# recognizes can be mapped to some other similar license
# For example, bsd-innosys is just InnoSys version of a BSD-2-Clause.
# Probably it's fine to match bsd-innosys as BSD-2-Clause.
def trim_lic_db():
    lic_file_lists = list()
    num_cpus = (os.cpu_count() + 1) / 2
    processes = list()
    i = 0

    if not os.path.exists(tmp_lic_db) or not os.path.isdir(tmp_lic_db):
        os.makedirs(tmp_lic_db)

    # divide license files into separate lists, to be used for multithreading
    while i < num_cpus:
        lic_f_list = list()
        lic_file_lists.append(lic_f_list)
        i += 1

    i = 0
    for lic_file in os.listdir(db_dir):
        if i >= num_cpus:
            i = 0
        lic_file_lists[i].append(lic_file)
        i += 1

    with multiprocessing.Manager() as manager:
        # ideally this would be set() but that is not supported
        rule_ignore_list = manager.list()
        rule_ignore_lock = manager.Lock()
        # tells us if the lic_db operation failed in one of the threads.
        taint = manager.Value("b", 0)
        taint_lock = manager.Lock()

        print("Ignoring unofficial licenses and rules")
        for lic_f_list in lic_file_lists:
            p = multiprocessing.Process(
                target=trim_job,
                args=(
                    lic_f_list,
                    rule_ignore_list,
                    rule_ignore_lock,
                    taint,
                    taint_lock,
                ),
            )
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        if taint.value == 1:
            restore_lic_db()
            err_exit()

        # move all rule files that have been marked to be ignored
        print("Moving rules which can be ignored...")
        for rule_f in rule_ignore_list:
            # may be duplicates in the list, so check if already moved
            if not os.path.exists(rule_f):
                continue

            shutil.move(rule_f, tmp_rules_dir)

    # reindex with official licenses only
    print(
        "Reindexing license cache without scancode's unofficial licenses, "
        + "this may take a few mins..."
    )
    if get_index(force=True, index_all_languages=True) is None:
        raise Exception("Failed to reindex license cache!")


def get_lic_exp_from_rule_file(rule_f_path=None):
    rule_f = None
    lic_exp_line = ""

    if not rule_f_path:
        return None

    with open(rule_f_path, "r") as rule_f:
        multiline = False
        for line in rule_f:
            if line.startswith("license_expression"):
                lic_exp_line += line.split(":")[-1].strip()
                multiline = True
            elif multiline and re.search("^.*:.*", line):
                break
            elif multiline:
                lic_exp_line += " " + line.strip()

    return lic_exp_line


def trim_rules_for_key(key, rule_ignore_list, rule_ignore_lock):
    with rule_ignore_lock:
        if not os.path.exists(tmp_rules_dir) or not os.path.isdir(
            tmp_rules_dir
        ):
            os.makedirs(tmp_rules_dir)

    for rule_file in os.listdir(rules_dir):
        lic_exp_line = get_lic_exp_from_rule_file(f"{rules_dir}/{rule_file}")

        spdx_ids = [
            exp.strip(" \r\t\n()")
            for exp in re.split("AND|WITH|OR", lic_exp_line)
        ]
        if key in spdx_ids:
            with rule_ignore_lock:
                rule_ignore_list.append(f"{rules_dir}/{rule_file}")


def restore_lic_db():
    if not os.path.exists(tmp_lic_db) or not os.path.exists(tmp_rules_dir):
        return

    print("Restoring scancode database. This may take a few mins...")
    copytree(tmp_lic_db, db_dir)
    copytree(tmp_rules_dir, rules_dir)
    get_index(force=True, index_all_languages=True)
    shutil.rmtree(tmp_lic_db)
    shutil.rmtree(tmp_rules_dir)


# run rpmbuild -bp to get the source RPM to scan
def extract_src_rpm(rpm_path=None):
    dist_tag = None
    rpm_build_cmds = []

    if rpm_path is None:
        return None

    if not os.path.exists(rpm_install_root):
        os.makedirs(rpm_build_root)

    # clean the working dir
    shutil.rmtree(rpm_install_root)

    result = run_cmd(f"rpm -i {rpm_path} --root {rpm_install_root}")
    if result.returncode != 0:
        pr_err("Failed to install source RPM!")
        return None

    # should only be one spec file here, since it's a clean dir
    spec_fn = ""
    for spec in os.listdir(f"{rpm_build_root}/SPECS"):
        spec_fn = spec
        break

    rpm_build_cmds = [
        "rpmbuild",
        "-bp",
        "--nodeps",
        "--define",
        f"%_topdir {rpm_build_root}",
        "--define",
        "%with_check 0",
    ]

    if spec_fn.startswith("linux"):
        src_rpm_basename = os.path.basename(rpm_path)
        dist_tag = (
            re.search(r"\.ph.*\.src", src_rpm_basename).group().split(".")[1]
        )

        rpm_build_cmds += ["--define", f"%dist .{dist_tag}"]

    rpm_build_cmds.append(f"{rpm_build_root}/SPECS/{spec_fn}")

    result = run_cmd(
        rpm_build_cmds,
        ignore_rc=True,
    )

    if result.returncode != 0:
        print(
            f"Failed to prep src rpm for {spec_fn}:\n{result.stdout.decode()}"
        )
        return None

    # extract any nested archives that weren't extracted by
    # rpmbuild -bp.
    # Do this as a best effort, as extractcode may fail.
    # For example, extractcode seems to struggle with test
    # data archives in many packages.
    run_cmd(f"extractcode {rpm_build_root}/BUILD", ignore_rc=True)

    return rpm_build_root


# get list of exceptions from spdx repo
def get_exceptions_list():
    exception_list = []
    exceptions_json_loc = "/tmp/exceptions.json"
    exceptions_json = None
    retries = 3

    if os.path.exists(exceptions_json_loc):
        os.remove(exceptions_json_loc)

    while retries > 0:
        # download latest version of exceptions.json from github
        response = requests.get(
            "https://raw.githubusercontent.com/spdx/license-list-data/"
            + "refs/heads/main/json/exceptions.json"
        )

        if response.status_code == 200:
            with open(exceptions_json_loc, "wb") as exc_file:
                exc_file.write(response.content)
            break
        else:
            retries -= 1
            if retries > 0:
                pr_err(
                    "Failed to get exceptions list, retrying after delay..."
                )
                time.sleep(5)
            else:
                err_exit(
                    "ERROR: Exhausted all retries, couldn't get exceptions list!"
                )

    with open(exceptions_json_loc, "r") as spdx_exceptions_json:
        exceptions_json = json.load(spdx_exceptions_json)

    for exception in exceptions_json["exceptions"]:
        exception_list.append(exception["licenseExceptionId"])

    os.remove(exceptions_json_loc)

    return exception_list


# cleans any ignorable SPDX IDs from the expression, such as standalone
# exceptions or other license IDs in the ignore list like "LicenseRef-unknown-spdx"
def cleanup_license_expression(
    ignore_list=None, exception_list=None, license_exp=None
):
    if not license_exp:
        return None

    lic_tree = license_tree.create_exp_tree(
        license_exp, exception_list, ignore_list
    )
    parsed_exp = license_tree.render_exp_tree(lic_tree)

    # remove duplicates - this returns a set
    top_lvl_exps = extract_top_level_expressions(parsed_exp)
    parsed_exp = " AND ".join(top_lvl_exps)

    # do some cleanup for us
    if parsed_exp:
        licensing = license_expression.get_spdx_licensing()
        return licensing.parse(parsed_exp).render()

    return parsed_exp


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
            spdx_exp = (
                spdx_exp[:start_pos]
                + " " * len(paran_str)
                + spdx_exp[end_pos:]
            )
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


# parse scan yaml output and produce a valid SPDX expression
def parse_scan_yaml(yaml_fn=None, ignore_unofficial=True):
    license_exps = set()
    lic_str = None
    exceptions_list = None

    if yaml_fn is None:
        pr_err("No yaml file passed to parse function!")
        return None

    exceptions_list = get_exceptions_list()
    ignore_list = ["LicenseRef-scancode-unknown-spdx"]

    print("Opening " + yaml_fn)
    with open(yaml_fn, "r") as yaml_f:
        scancode_yaml = yaml.load(yaml_f, Loader=yaml.SafeLoader)
        for license_detection in scancode_yaml["license_detections"]:
            spdx_exp = license_detection["license_expression_spdx"]

            if not spdx_exp:
                continue

            # A little on the logic here:
            # License expressions reported by scancode are typically for one file only
            # For cases with ANDs, e.g A AND B, this is the license expression for 1 file.
            # So, if we have another file which is licensed under C, how to construct the
            # overall expression? There are two options:
            # 1. (A AND B) AND C
            # 2. A AND B AND C
            #
            # Option 1 preserves the license expression for each file, whereas option 2
            # combines into one expression. Option 2 should be correct, because we are
            # attempting to provide terms under which the entire package is to be licensed
            # under. It should be accurate to say the entire package needs to be licensed
            # under the terms of A and B and C.
            #
            # C can also be a composite expression such as (C OR D) - ORs should be preserved
            # within parantheses, because the OR operator is disjunctive. The conjunctive AND
            # must be used at the top level to connect all license expressions.
            #
            # What about crazier expressions like:
            # ((A AND B) OR C) AND D
            #
            # It should be handled in the same way - keep the OR together.
            # For expressions such as ((A AND B) AND C) AND D, these will be flattened by the
            # license_tree API in cleanup_license_expression().
            spdx_exps = extract_top_level_expressions(spdx_exp)
            for exp in spdx_exps:
                exp = strip_license_id(exp)
                exp = cleanup_license_expression(
                    ignore_list=ignore_list,
                    exception_list=exceptions_list,
                    license_exp=exp,
                )
                license_exps.add(exp)

    for exp in license_exps:
        if exp is None or exp == "":
            continue

        # Add parantheses now, then we can flatten the expression later
        if (
            ("AND" in exp or "OR" in exp)
            and not (exp.startswith("(") and exp.endswith(")"))
            and len(license_exps) > 1
        ):
            exp = f"({exp})"

        if lic_str is None:
            lic_str = exp
        else:
            lic_str = f"{lic_str} AND {exp}"

    # Cleanup extra parantheses, connectors, etc., from the final expression
    lic_str = cleanup_license_expression(
        ignore_list=ignore_list,
        exception_list=exceptions_list,
        license_exp=lic_str,
    )

    return lic_str


def scan(args):
    input_fp = None
    yaml_fn = "scan-results.yaml"
    ignore_unofficial = not args.a
    score = 90 if args.score is None else args.score
    cwd = os.getcwd()
    scan_dir = None

    check_scancode_ver()

    if not args.path:
        err_exit("ERROR: No input given for scan!")

    input_fp = args.path.strip()

    if os.path.exists(ph_scan_dir):
        # clean out the dir if anything there before
        shutil.rmtree(ph_scan_dir)

    # filepath relative to ph_scan_dir
    while input_fp[-1] == "/":
        input_fp = input_fp[:-1]
    input_file = os.path.basename(input_fp)

    if os.path.isdir(input_fp):
        os.makedirs(f"{ph_scan_dir}/{input_file}")
        copytree(input_fp, f"{ph_scan_dir}/{input_file}")
    else:
        os.makedirs(f"{ph_scan_dir}")
        shutil.copy2(input_fp, f"{ph_scan_dir}")

    os.chdir(ph_scan_dir)

    if input_file.endswith(".src.rpm"):
        scan_dir = extract_src_rpm(input_file) + "/BUILD"
        if not scan_dir:
            err_exit("Failed to extract {input_file} as .src.rpm")
    elif not os.path.isdir(input_file):
        # extract with scancode universal extractor
        print(f"Extracting output from {input_file}...")
        res = run_cmd(str(f"extractcode {input_file}").split())
        if res.returncode != 0:
            err_exit(f"ERROR: Extraction of {input_file} failed!")

        if os.path.exists(f"{input_file}-extract"):
            scan_dir = f"{input_file}-extract"
        else:
            # if not an archive, just use the whole default scan dir
            scan_dir = ph_scan_dir
    else:
        scan_dir = input_file

    if ignore_unofficial:
        print(
            "Trimming license DB to include only valid SPDX licenses "
            + "before scan..."
        )
        try:
            trim_lic_db()
        except Exception as e:
            pr_err(f"Failed to trim license database: {e}")
            restore_lic_db()
            err_exit()
    else:
        print("Restoring license DB to include all licenses")
        restore_lic_db()

    # run the scan
    result = run_cmd(
        [
            "scancode",
            "--license",
            "-n",
            str(multiprocessing.cpu_count()),
            "--only-findings",
            "--license-score",
            str(score),
            "--yaml",
            f"{ph_scan_dir}/{yaml_fn}",
            scan_dir,
        ]
    )

    if result.returncode != 0:
        pr_err("ERROR: scancode failed during scanning process :(")
        if ignore_unofficial:
            restore_lic_db()
        err_exit()

    if ignore_unofficial:
        print("Restoring license DB after scan completion")
        restore_lic_db()

    # Produce full SPDX expression using scancode output results
    spdx_exp = parse_scan_yaml(
        yaml_fn=yaml_fn, ignore_unofficial=ignore_unofficial
    )

    if args.yaml:
        if args.yaml.startswith("/"):
            yaml_path = args.yaml
        else:
            # local file, relative path
            yaml_path = f"{cwd}/{args.yaml}"

        shutil.copy(yaml_fn, yaml_path)
        print(f"Detailed scan yaml produced at: {yaml_path}")

    os.chdir(cwd)

    print(f"SPDX Expression: {spdx_exp}")

    try:
        shutil.rmtree(ph_scan_dir)
        if input_file.endswith(".src.rpm"):
            shutil.rmtree(rpm_build_root)
            shutil.rmtree(rpm_install_root)
    except Exception as e:
        pr_err(f"Failed to remove temp dir(s) after scan: {e}")


def read_license_from_file(file_path=None):
    license_expressions = dict()
    lines = []

    if not file_path:
        return None

    if not os.path.exists(file_path):
        err_exit(f"ERROR: Invalid license file path: {file_path}")

    # check for license.txt first
    # rpmspec reads from /usr/src/photon/SOURCES/license.txt, instead
    # of the local dir - so we need to manually check for license.txt.
    spec_license_txt = f"{os.path.dirname(file_path)}/license.txt"
    if file_path.endswith(".spec") and os.path.exists(spec_license_txt):
        spec_license_txt = f"{os.path.dirname(file_path)}/license.txt"
        file_path = spec_license_txt
    elif file_path.endswith(".spec"):
        result = run_cmd(
            [
                "rpmspec",
                "-q",
                '--queryformat="License: %{Name}: %{License}\n"',
                file_path,
            ]
        )
        if result.returncode != 0:
            err_exit(
                f"Failed to extract license line from spec file!: {result.stdout}"
            )

        for line in result.stdout.decode().split("\n"):
            line = line.strip(" \r\t\n\"'")
            if line.startswith("License:"):
                line_spl = line.split(":")
                # (sub)package name : license expression
                license_expressions[line_spl[1].strip()] = line_spl[2].strip()

        if not license_expressions:
            err_exit(f"ERROR: No license expression found in {file_path}")

        return license_expressions

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


def validate(args):
    license_expressions = dict()
    license_exp = ""
    bad_ids = ["unknown-spdx", "LicenseRef", "scancode"]
    spdx_licensing = license_expression.get_spdx_licensing()
    check_scancode_ver()
    errors = 0

    # read from file
    if args.f:
        license_expressions = read_license_from_file(args.f)
    # read from stdin
    elif args.i:
        license_expressions["stdin"] = args.i

    for license_exp in license_expressions:
        print(f"Validating license for {license_exp}")
        license_exp = license_expressions[license_exp]
        print(f"\nLicense found:\n{license_exp}\n")

        # for some reason, the license_expression package, which is used by the
        # official spdx-tools package, returns/uses the same database for both
        # spdx and scancode licenses. So let's do our own filtering here.
        for bad_id in bad_ids:
            if bad_id in license_exp:
                pr_err(f"Bad SPDX identifier {bad_id} in license expression!")
                errors += 1
        try:
            # create license expression object - throws an exception for any
            # validation errors
            spdx_licensing.parse(license_exp, validate=True, strict=True)
        except Exception as e:
            err_exit(
                f"Caught exception while attempting to validate license: {e}"
            )

        # Check for disallowed licenses
        for key in spdx_licensing.license_keys(license_exp):
            if key in disallowed_licenses:
                pr_err(
                    f"Illegal license {key} found in license expression!"
                    + " This is likely a non-permissive license determined by SRP."
                )
                errors += 1

    if errors == 0:
        print("SPDX license validation successful")
    else:
        err_exit(f"Failed to validate SPDX license - found {errors} error(s)")


def lic_db(args):
    check_scancode_ver()

    if args.trim:
        try:
            trim_lic_db()
        except Exception as e:
            pr_err(f"Failed to trim license database: {e}")
            restore_lic_db()
            err_exit()

    if args.restore:
        try:
            restore_lic_db()
        except Exception as e:
            err_exit(f"Failed to restore license database: {e}")


def clean_exp(args):
    license_expressions = dict()
    exceptions_list = []

    if args.i:
        license_expressions["stdin"] = args.i
    elif args.f:
        license_expressions = read_license_from_file(args.f)

    if not license_expressions:
        pr_err("Failed to find license expression!")
        return

    exceptions_list = get_exceptions_list()

    for key in license_expressions:
        lic_exp = license_expressions[key]
        new_exp = cleanup_license_expression(
            ignore_list=[], exception_list=exceptions_list, license_exp=lic_exp
        )

        print(f"\nFor {key}, original expression:\n{lic_exp}")
        print(f"\nNew expression:\n{new_exp}")


def compare_exps(args):
    exp_a = ""
    exp_b = ""
    set_a = set()
    set_b = set()
    diff_a = set()
    diff_b = set()

    if not args.a:
        err_exit("Please input expression A with -a <exp>")

    if not args.b:
        err_exit("Please input expression B with -b <exp>")

    if os.path.isfile(args.a):
        # We expect to find only one license here,
        # different from other callers. In the case of spec files,
        # assume that all subpackages have the same licensing.
        exps_from_file = read_license_from_file(args.a)
        for key in exps_from_file:
            exp_a = exps_from_file[key]
    else:
        exp_a = args.a

    if os.path.isfile(args.b):
        exps_from_file = read_license_from_file(args.b)
        for key in exps_from_file:
            exp_b = exps_from_file[key]
    else:
        exp_b = args.b

    for lic in extract_top_level_expressions(exp_a):
        set_a.add(lic)

    for lic in extract_top_level_expressions(exp_b):
        set_b.add(lic)

    diff_a = set_a.difference(set_b)
    diff_b = set_b.difference(set_a)

    if diff_a:
        print("Exclusive to expression A:")
        for lic in diff_a:
            print(f"\t{lic}")

    if diff_b:
        print("Exclusive to expression B:")
        for lic in diff_b:
            print(f"\t{lic}")

    if diff_a or diff_b:
        err_exit("License expressions are not equivalent")

    print("License expressions are equivalent")
    return 0


# Set global variables from config.yaml
def parse_config(config_path=None):
    global ignore_list
    global disallowed_licenses

    if not config_path:
        err_exit("Configuration YAML file is required!")

    with open(config_path, "r") as config_f:
        config_yaml = yaml.load(config_f, Loader=yaml.SafeLoader)

        try:
            ignore_list = config_yaml["license_ignore_list"]
            disallowed_licenses = config_yaml["disallowed_licenses"]
        except KeyError as exception:
            err_exit(f"Missing required field in {config_path}!\n{exception}")


def parse_input():
    parser = ArgumentParser(description="Photon License Tool")
    subparsers = parser.add_subparsers(
        help="""--help|-h for more info on individual sub-commands.
Works recursively for all levels."""
    )

    sub_p = subparsers.add_parser(
        "validate",
        help="""Validate a given SPDX expression for
semantic correctness. Does not validate accuracy.""",
    )
    sub_p.add_argument(
        "-f",
        action="store",
        help="""Read SPDX expression from input file.
This assumes the format: License: <spdx expression>""",
    )
    sub_p.add_argument(
        "-i", action="store", help="Read SPDX expression directly from stdin"
    )
    sub_p.set_defaults(func=validate)

    sub_p = subparsers.add_parser(
        "scan",
        help="""Scan all files in the given file,
i.e tarball, src RPM, etc. Produces a full SPDX expression.""",
    )
    sub_p.add_argument(
        "--path", action="store", help="Path to file/directory to be scanned."
    )
    sub_p.add_argument(
        "--yaml",
        action="store",
        help="""Optional. Produce yaml document mapping each
SPDX identifier to the file it was discovered in. Save to the specified path.""",
    )
    sub_p.add_argument(
        "-a",
        action="store_true",
        help="""Optional. Scan for all licenses in the
scancode-toolkit database, instead of typical operation which scans only for
valid SPDX licenses.""",
    )
    sub_p.add_argument(
        "--score",
        action="store",
        help="Optional. Set the minimum license matching score.",
    )

    sub_p.set_defaults(func=scan)

    sub_p = subparsers.add_parser(
        "lic-db",
        help="""Operations on the scancode license
database""",
    )
    sub_p.add_argument(
        "--trim",
        action="store_true",
        help="""Trim DB by removing unofficial (non-SPDX)
licenses. Does NOT impact the database index used for license expression
validation.""",
    )
    sub_p.add_argument(
        "--restore", action="store_true", help="Restore DB with all licenses"
    )

    sub_p.set_defaults(func=lic_db)

    sub_p = subparsers.add_parser(
        "clean-exp",
        help="Cleanup/flatten the given expression",
    )

    sub_p.add_argument(
        "-i", action="store", help="Read SPDX expression directly from stdin"
    )

    sub_p.add_argument(
        "-f",
        action="store",
        help="""Read SPDX expression from input file.
This assumes the format: License: <spdx expression>""",
    )

    sub_p.set_defaults(func=clean_exp)

    sub_p = subparsers.add_parser(
        "compare",
        help="Compare two license expressions for equivalency",
    )

    sub_p.add_argument(
        "-a", action="store", help="SPDX expresssion A. Can be stdin or file."
    )

    sub_p.add_argument(
        "-b", action="store", help="SPDX expression B. Can be stdin or file."
    )

    sub_p.set_defaults(func=compare_exps)

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


def main():
    # print help if no args given on cmdline
    if len(sys.argv) <= 1:
        sys.argv.append("--help")

    if check_prereqs(sys.argv[1]) < 0:
        return -1

    # proper cleanup on unexpected exits
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    parse_config(os.path.dirname(__file__) + "/photon-lic-tool.yaml")

    args = parse_input()
    args.func(args)


if __name__ == "__main__":
    main()
