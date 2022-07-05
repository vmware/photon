#!/usr/bin/env python3

import os
import re
import sys
import calendar
from datetime import datetime

try:
    from support.pyrpm.spec import Spec, replace_macros
except ModuleNotFoundError:
    from pyrpm.spec import Spec, replace_macros


"""
Error Dictionary:
    - Stores all error messages in a dictionary
    - Prints all error messages section by section
    - Errors will be printed only after parsing whole spec
"""


class ErrorDict:
    def __init__(self, spec_fn):
        self.spec_fn = spec_fn
        self.err_dict = {
            "hdr_check": ["Spec header errors"],
            "version_check": ["Version check errros"],
            "dist_tag": ["Dist tag error"],
            "trailing_space": ["Trailing spaces & empty line errors"],
            "bogus_date": ["Bogus date errors"],
            "changelog": ["Changelog erros"],
            "sub_pkg": ["Sub package errors"],
            "configure": ["Configure erros"],
            "setup": ["Setup errors"],
            "_smp_mflags": ["_smp_mflags errors"],
            "unused_files": ["List of unused files"],
            "others": ["Other errors"],
        }

    # keep err message in a given section
    # if section not found, put it in others
    def update_err_dict(self, sec, err_msg):
        sec = sec if sec in self.err_dict else "others"

        if sec in self.err_dict:
            self.err_dict[sec].append(err_msg)
            # this removes duplicates from list
            self.err_dict[sec] = list(dict.fromkeys(self.err_dict[sec]))

    def print_err_dict(self):
        print("--- List of errors in %s ---" % (self.spec_fn))

        for k, v in self.err_dict.items():
            # proceed if error list has more than 1 item
            try:
                v[1]
            except IndexError:
                continue

            print("\n --- %s ---" % (v[0]))

            for msg in v[1:]:
                if k == "unused_files":
                    print("%s" % (msg))
                else:
                    print("ERROR in %s: %s" % (self.spec_fn, msg))

        print("\n")


def check_spec_header(spec, err_dict):
    ret = False
    sec = "hdr_check"

    # items in the following dict are mandatory part of spec header
    header = {
        "Name": spec.name,
        "Version": spec.version,
        "Release": spec.release,
        "License": spec.license,
        "Vendor": spec.vendor,
        "Summary": spec.summary,
        "Group": spec.group,
        "Distribution": spec.distribution,
    }

    for key, val in header.items():
        err_msg = None

        if not val:
            err_msg = "%s must be present in the spec header" % (key)
        elif key == "Distribution" and val and val != "Photon":
            err_msg = "%s name must be Photon (Given: %s)" % (key, val)
        elif key == "Vendor" and spec.vendor and spec.vendor != "VMware, Inc.":
            err_msg = "%s name must be VMware, Inc. (Given: %s)" % (key, val)

        if err_msg:
            ret = True
            err_dict.update_err_dict(sec, err_msg)

    return ret


# check for version in spec header against latest changelog entry
def check_for_version(spec, err_dict):
    ret = False
    sec = "version_check"

    clog = spec.changelog.splitlines()
    changelog_ver = clog[0].split()[-1]

    # combine Release & Version from header
    release_ver = spec.version + "-" + spec.release.split("%")[0]

    if changelog_ver != release_ver:
        err_msg = ("Changelog & Release version mismatch " "%s != %s") % (
            changelog_ver,
            release_ver,
        )
        err_dict.update_err_dict(sec, err_msg)
        ret = True

    return ret


def check_for_dist_tag(spec, err_dict):
    ret = False
    sec = "dist_tag"

    if "%{?dist}" not in spec.release:
        err_msg = "%%{?dist} tag not found in Release: %s" % (spec.release)
        err_dict.update_err_dict(sec, err_msg)
        ret = True

    return ret


def check_for_trailing_spaces(spec_fn, err_dict):
    ret = False
    ret_dict = {}
    sec = "trailing_space"

    with open(spec_fn) as fp:
        lines = fp.read().splitlines()

    if lines[-1].isspace():
        err_msg = "empty last line found, not needed"
        err_dict.update_err_dict(sec, err_msg)
        ret = True

    key_found = False
    empty_line_count = 0
    for line_num, line in enumerate(lines):
        if not line or line.isspace():
            empty_line_count += 1
        else:
            empty_line_count = 0

        if empty_line_count >= 2:
            err_msg = ("multiple empty lines found at line number" " %d") % (
                line_num + 1
            )
            err_dict.update_err_dict(sec, err_msg)
            empty_line_count = 0
            ret = True

        if line.endswith((" ", "\t")):
            err_msg = ("trailing space(s) found at line number: %s:\n" "%s") % (
                line_num + 1,
                line,
            )
            err_dict.update_err_dict(sec, err_msg)
            ret = True

        if not line.startswith("#") and "RPM_BUILD_ROOT" in line:
            err_msg = (
                "legacy $RPM_BUILD_ROOT found at line: %s\n%s - "
                "use %%{buildroot} instead"
            ) % (line_num + 1, line)
            err_dict.update_err_dict("others", err_msg)
            ret = True

        if line.startswith("%prep"):
            key_found = True
        elif line.startswith("%files"):
            key_found = False

        if key_found:
            ret_dict.update({line_num: line})

    return ret, ret_dict


# check against weekday abbreviation for the given date in changelog
def check_for_bogus_date(line, cur_date, err_dict):
    ret = False
    sec = "bogus_date"

    day_abbr = calendar.day_abbr[cur_date.weekday()]
    if day_abbr != line[1]:
        err_msg = "bogus date found at:\n%s" % (line)
        err_dict.update_err_dict(sec, err_msg)
        ret = True

    return ret


# No empty lines allowed in changelog
# Changelog lines should start with '*', '-', ' ' or '\t'
# '-' & ' ' should not be present before '*'
# Successive lines starting with '*' not allowed
def check_changelog(spec, err_dict):
    ret = False
    hyphen = True
    asterisk = False
    sec = "changelog"
    date_format = "%a-%b-%d-%Y"
    prev_date = {"date": None, "entry": None}

    changelog = spec.changelog.splitlines()

    for line in changelog:
        err_msg = None
        if not line:
            err_msg = "empty line in changelog"
            err_dict.update_err_dict(sec, err_msg)
            ret = True
            continue

        if line.startswith("*"):
            asterisk = True
            if not hyphen:
                err_msg = "Successive author & version info at:\n%s" % (line)
                err_dict.update_err_dict(sec, err_msg)
                ret = True
            hyphen = False
        elif line.startswith("-"):
            hyphen = True
            if not asterisk:
                err_msg = (
                    "description given before author & version info at:" "\n%s"
                ) % (line)
                err_dict.update_err_dict(sec, err_msg)
                ret = True
            continue
        elif line.startswith((" ", "\t")) and asterisk and hyphen:
            continue
        else:
            err_msg = "invalid entry in changelog at: %s" % (line)
            err_dict.update_err_dict(sec, err_msg)
            ret = True
            continue

        line_str = line
        line = line.split()

        date_text = "-".join(line[1:5])
        try:
            cur_date = datetime.strptime(date_text, date_format)
        except ValueError:
            err_msg = "-%s-" % (date_text)
            err_dict.update_err_dict(sec, err_msg)
            ret = True
            continue

        if check_for_bogus_date(line, cur_date, err_dict):
            ret = True

        # dates should be in chronological order
        if prev_date["date"] and cur_date > prev_date["date"]:
            err_msg = (
                "dates not in chronological order in between:\n" "%s and\n%s"
            ) % (line_str, prev_date["entry"])
            err_dict.update_err_dict(sec, err_msg)
            ret = True

        prev_date["date"] = cur_date
        prev_date["entry"] = line_str

    return ret


def check_sub_pkg(spec, err_dict):
    ret = False
    sec = "sub_pkg"

    for pkg in spec.packages:
        err_msg = ""
        if pkg.is_subpackage:
            if pkg.build_requires:
                err_msg = "BuildRequires found in sub package %s\n" % (pkg)

            subpkg_hdr = [pkg.name, pkg.summary, pkg.description]
            if "" in subpkg_hdr or None in subpkg_hdr:
                err_msg += (
                    "One of Name/Summary/Description is missing in sub" " package %s"
                ) % (pkg)

            if err_msg:
                ret = True
                err_dict.update_err_dict(sec, err_msg)

    return ret


def check_for_configure(lines_dict, err_dict):
    ret = False
    sec = "configure"

    opt_list = ["prefix", "exec-prefix", "bindir" "sbindir" "libdir"]
    opt_list += ["includedir", "sysconfdir", "datadir", "libexecdir"]
    opt_list += ["sharedstatedir", "mandir", "infodir", "localstatedir"]

    lines = list(lines_dict.values())

    def check_for_opt(line):
        ret = False

        for opt in opt_list:
            opt = "--" + opt
            if line.find(opt) >= 0:
                err_msg = "%s can be omitted when using %%configure" % (opt)
                err_dict.update_err_dict(sec, err_msg)
                ret = True

        return ret

    # options in opt_list can be in same line or in continued line
    for idx, line in enumerate(lines):
        err_msg = None
        if line.startswith("./configure") or line.startswith("%configure"):
            if line.startswith("./configure"):
                err_msg = "Use %%configure instead of ./configure"
                err_dict.update_err_dict(sec, err_msg)
                ret = True

            prev_line = lines[idx - 1]
            if prev_line.endswith("\\"):
                err_msg = (
                    "Trailing backslash before configure found." " Use export instead"
                )

                err_dict.update_err_dict(sec, err_msg)
                ret = True

            _ret = check_for_opt(line)
            ret = True if ret else _ret
            # if configure is multi lined
            while line.endswith("\\"):
                idx += 1
                line = lines[idx]
                _ret = check_for_opt(line)
                ret = True if ret else _ret

    return ret


def check_setup(lines_dict, err_dict):
    ret = False
    sec = "setup"
    bypass_str = "# Using autosetup is not feasible"

    lines = list(lines_dict.values())

    for idx, line in enumerate(lines):
        if line.startswith("%autosetup"):
            continue

        if line.startswith("%setup"):
            if lines[idx - 1] == bypass_str:
                continue
            err_msg = (
                "\nUse %%autosetup instead of %%setup\n"
                "If using %%autosetup is not feasible, "
                "put the following comment '%s' right "
                "above your every %%setup command"
            ) % (bypass_str)
            err_dict.update_err_dict(sec, err_msg)
            ret = True

    return ret


def check_make_smp_flags(lines_dict, err_dict):
    ret = False
    sec = "_smp_mflags"
    bypass_str = "# make doesn't support _smp_mflags"

    err_msg = (
        "(at line number {line}): Use _smp_mflags with make\n"
        "If using _smp_mflags is not feasible, put the following "
        "comment '{bstr}' right above your every make "
        "command"
    )

    lines = list(lines_dict.values())
    line_nums = list(lines_dict.keys())

    for idx, line in enumerate(lines):

        if (
            (not line.startswith("make"))
            or (lines[lines.index(line) - 1] == bypass_str)
            or (sec in line)
        ):
            continue

        if re.split("[^a-z]", line)[0] != "make":
            continue

        flag_found = False
        while lines[idx] and lines[idx].endswith("\\"):
            idx += 1
            if sec in lines[idx]:
                flag_found = True
                break

        if not flag_found:
            e_msg = err_msg.format(line=line_nums[idx] + 1, bstr=bypass_str)
            err_dict.update_err_dict(sec, e_msg)
            ret = True

    return ret


def check_for_unused_files(spec_fn, err_dict):
    ret = False
    sec = "unused_files"
    dirname = os.path.dirname(spec_fn)

    if not hasattr(check_for_unused_files, "prev_dir"):
        check_for_unused_files.prev_dir = None

    if not hasattr(check_for_unused_files, "prev_ret"):
        check_for_unused_files.prev_ret = None

    if dirname == check_for_unused_files.prev_dir:
        return check_for_unused_files.prev_ret

    check_for_unused_files.prev_dir = dirname

    other_files = []
    source_patch_list = []

    def populate_list(src_list, dest_list):
        for s in src_list:
            s = replace_macros(s, tmp)
            if type(s) == str:
                dest_list.append(s)
            if type(s) == list:
                dest_list += s

    for r, _, fns in os.walk(dirname):
        for fn in fns:
            if not fn.endswith(".spec"):
                fn = os.path.basename(fn)
                other_files.append(fn)
                continue

            fn = os.path.join(r, fn)
            tmp = Spec.from_file(fn)
            populate_list(tmp.sources, source_patch_list)
            populate_list(tmp.patches, source_patch_list)

    # keep only basenames in source list
    source_patch_list = [os.path.basename(s) for s in source_patch_list]

    fns = set(other_files) - set(source_patch_list)
    if not fns:
        check_for_unused_files.prev_ret = ret
        return ret

    ret = True
    err_msg = "List of unused files in: %s" % (dirname)
    err_dict.update_err_dict(sec, err_msg)
    for r, _, _fns in os.walk(dirname):
        for _fn in _fns:
            if _fn in fns:
                _fn = os.path.join(r, _fn)
                err_dict.update_err_dict(sec, _fn)

    check_for_unused_files.prev_ret = ret
    return ret


def check_for_sha1_usage(spec, err_dict):
    if hasattr(spec, "sha1"):
        err_dict.update_err_dict("others", "sha1 usage found, use sha512")
        return True
    return False


def check_specs(files_list):
    ret = False
    for spec_fn in files_list:
        if not spec_fn.endswith(".spec"):
            continue

        print("Checking spec file: %s" % (spec_fn))

        if not os.path.isfile(spec_fn):
            print("%s has been deleted in this changeset" % (spec_fn))
            continue

        err_dict = ErrorDict(spec_fn)
        spec = Spec.from_file(spec_fn)

        err, lines_dict = check_for_trailing_spaces(spec_fn, err_dict)

        if any(
            [
                check_spec_header(spec, err_dict),
                check_for_version(spec, err_dict),
                check_for_dist_tag(spec, err_dict),
                check_changelog(spec, err_dict),
                check_sub_pkg(spec, err_dict),
                check_for_configure(lines_dict, err_dict),
                check_setup(lines_dict, err_dict),
                check_make_smp_flags(lines_dict, err_dict),
                check_for_unused_files(spec_fn, err_dict),
                check_for_sha1_usage(spec, err_dict),
            ]
        ):
            err = True

        if err:
            ret = True
            err_dict.print_err_dict()

    return ret


if __name__ == "__main__":
    files = []

    arglen = len(sys.argv)
    if arglen >= 2:
        for arg in range(1, arglen):
            if sys.argv[arg].endswith(".spec"):
                files.append(sys.argv[arg])
    else:
        dirname = "SPECS/"
        for r, d, fns in os.walk(dirname):
            for fn in fns:
                if fn.endswith(".spec"):
                    files.append(os.path.join(r, fn))

    if check_specs(files):
        print("ERROR: spec check failed")
        sys.exit(1)

    sys.exit(0)
