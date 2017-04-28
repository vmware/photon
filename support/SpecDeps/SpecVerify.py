#!/usr/bin/python2
#
#Copyright (C) 2015 vmware inc.
#
#Author:    Harish    Udaiya    Kumar    <hudaiyakumar@vmware.com>
from SpecUtils import Specutils
from SpecData import SerializableSpecObject
from SpecData import SerializedSpecObjects
from RepoDeps import RepoQueryDependency
import sys
import os
from argparse import ArgumentParser
from jsonwrapper import JsonWrapper

DEFAULT_INPUT_TYPE      =    "json"
DEFAULT_DISPLAY_OPTION  =    "tree"
SPEC_FILE_DIR           =    "../../SPECS"
INPUT_DATA_DIR          =    "../../common/data"

def reportMissing(pkg,specDepList, repoDepList, excludeList):
    missingList = [];
    if None != repoDepList:
        for repoItem in repoDepList:
            if repoItem not in excludeList and (None == specDepList or repoItem  not in specDepList):
                missingList.append(repoItem)
    if missingList:
        if len(pkg) <= 7:
            print pkg, "missing\t\t->", missingList
        else:
            print pkg, "missing\t->", missingList

def    main():
    usage = os.path.basename(__file__)    +    "--input-type=[json/pkg]    --pkg=[pkg_name]    --file=<JSON_FILE_NAME>    --repo-file=<photon>.repo"
    parser = ArgumentParser(usage)
    parser.add_argument("-i",    "--input-type",    dest="input_type",    default=DEFAULT_INPUT_TYPE)
    parser.add_argument("-p",    "--pkg",    dest="pkg")
    parser.add_argument("-f",    "--file",    dest="json_file",    default="packages_full.json")
    parser.add_argument("-s",    "--spec-dir",    dest="spec_dir",    default=SPEC_FILE_DIR)
    parser.add_argument("-a",    "--input-data-dir",    dest="input_data_dir",    default=INPUT_DATA_DIR)
    parser.add_argument("-r",    "--repo-file",    dest    =    "repo_file",    default="")
    excludeList = ["bash","glibc","libgcc","pkg-config","filesystem"]
    options = parser.parse_args()

    if(options.repo_file    ==    ""):
        print "Error! repo file not provided"
        print usage
        return

    if(False    ==    options.input_data_dir.endswith('/')):
        options.input_data_dir    +=    '/'

    specDeps = SerializedSpecObjects(options.input_data_dir,    "")
    repoDeps = RepoQueryDependency(options.repo_file)
    displayOption = None
    abs_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(abs_path)
    os.chdir(dir_name)

    if(options.input_type == "pkg"):
        targetName = options.pkg
        specDepList = specDeps.readSpecsAndConvertToSerializableObjects(options.spec_dir,    options.input_type,    targetName,    displayOption)
        repoDepList = repoDeps.getRequiresList(targetName)
        reportMissing(targetName,specDepList,repoDepList,excludeList)
    elif(options.input_type == "json"):
        filePath = options.input_data_dir    +    options.json_file
        data = specDeps.get_all_package_names(filePath)
        for pkg in data:
            specDepList = specDeps.readSpecsAndConvertToSerializableObjects(options.spec_dir,    "pkg"    ,    pkg,    displayOption)
            repoDepList = repoDeps.getRequiresList(pkg)
            reportMissing(pkg,specDepList,repoDepList,excludeList)
    sys.exit(0)

if    __name__=="__main__":
                main()
