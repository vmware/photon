#!/usr/bin/python3
#
# Copyright (C) 2015 vmware inc.
#
# Author:    Harish    Udaiya    Kumar    <hudaiyakumar@vmware.com>

from SpecData import SpecDependencyGenerator
from RepoDeps import RepoQueryDependency
import sys
import os
import traceback
from argparse import ArgumentParser
from constants import constants

DEFAULT_INPUT_TYPE = "json"
DEFAULT_DISPLAY_OPTION = "tree"
SPEC_FILE_DIR = "../../SPECS"
LOG_FILE_DIR = "../../stage/LOGS"
INPUT_DATA_DIR = "../../common/data"


def reportMissing(pkg, specDepList, repoDepList, excludeList):
    missingList = []
    if repoDepList is not None:
        for repoItem in repoDepList:
            if repoItem not in excludeList and (specDepList is None or repoItem not in specDepList):
                missingList.append(repoItem)
    if missingList:
        if len(pkg) <= 7:
            print pkg, "missing\t\t->", missingList
        else:
            print pkg, "missing\t->", missingList


def main():
    usage = "Usage: %prog [options]"
    parser = ArgumentParser(usage)
    parser.add_argument("-i", "--input-type", dest="input_type", default=DEFAULT_INPUT_TYPE)
    parser.add_argument("-p", "--pkg", dest="pkg")
    parser.add_argument("-f", "--file", dest="json_file", default="packages_full.json")
    parser.add_argument("-s", "--spec-dir", dest="spec_dir", default=SPEC_FILE_DIR)
    parser.add_argument("-l", "--log-dir", dest="log_dir", default=LOG_FILE_DIR)
    parser.add_argument("-a", "--input-data-dir", dest="input_data_dir", default=INPUT_DATA_DIR)
    parser.add_argument("-r", "--repo-file", dest="repo_file", default="")
    excludeList = ["bash", "glibc", "libgcc", "pkg-config", "filesystem"]
    options = parser.parse_args()

    if options.repo_file == "":
        print "Error! repo file not provided"
        print usage
        sys.exit(1)

    constants.setSpecPath(options.spec_dir)
    constants.setLogPath(options.log_dir)
    constants.initialize()
    specDepList = SpecDependencyGenerator()
    repoDeps = RepoQueryDependency(options.repo_file)
    displayOption = None

    try:
        if options.input_type == "pkg":
            targetName = options.pkg
            specDepList.process(options.input_type, targetName, displayOption)
            repoDepList = repoDeps.getRequiresList(targetName)
            reportMissing(targetName, specDepList, repoDepList, excludeList)
        elif options.input_type == "json":
            filePath = os.path.join(options.input_data_dir, options.json_file)
            data = SpecDependencyGenerator.getAllPackageNames(filePath)
            for pkg in data:
                specDepList.process("pkg", pkg, displayOption)
                repoDepList = repoDeps.getRequiresList(pkg)
                reportMissing(pkg, specDepList, repoDepList, excludeList)
    except Exception as e:
        print ("Caught Exception: " + str(e))
        traceback.print_exc()
        print("Failed to generate missing dependencies")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
