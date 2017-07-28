#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Harish Udaiya Kumar <hudaiyakumar@vmware.com>
from SpecUtils import Specutils
from SpecData import SerializableSpecObject
from SpecData import SerializedSpecObjects
import sys
import os
from optparse import OptionParser
from jsonwrapper import JsonWrapper

DEFAULT_INPUT_TYPE = "pkg"
DEFAULT_DISPLAY_OPTION = "tree"
SPEC_FILE_DIR = "../../SPECS"
LOG_FILE_DIR = "../../stage/LOGS"


def main():
    usage = os.path.basename(__file__) + "--input-type=[json/pkg/who-needs/build-deps] --pkg=[pkg_name] --file=<JSON_FILE_NAME> --disp=[tree/list/json]"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input-type", dest="input_type", default=DEFAULT_INPUT_TYPE)
    parser.add_option("-p", "--pkg", dest="pkg")
    parser.add_option("-f", "--file", dest="json_file", default="packages_minimal.json")
    parser.add_option("-d", "--disp", dest="display_option", default=DEFAULT_DISPLAY_OPTION) 
    parser.add_option("-s", "--spec-dir", dest="spec_dir", default=SPEC_FILE_DIR)
    parser.add_option("-t", "--stage-dir", dest="stage_dir", default="../../stage")
    parser.add_option("-a", "--input-data-dir", dest="input_data_dir", default="../../common/data/")
    (options,  args) = parser.parse_args() 

    if(False == options.input_data_dir.endswith('/')):
        options.input_data_dir += '/'

    specDeps = SerializedSpecObjects(options.input_data_dir, options.stage_dir)
    displayOption = options.display_option
    abs_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(abs_path)
    os.chdir(dir_name)

    # To display/print package dependencies on console
    if(options.input_type == "pkg" or options.input_type == "who-needs" or options.input_type == "build-deps"):
        targetName = options.pkg
        specDeps.readSpecsAndConvertToSerializableObjects(options.spec_dir, options.input_type, targetName, displayOption)
    elif(options.input_type == "json"):# Generate the expanded package dependencies json file based on package_list_file 
        json_wrapper_option_list = JsonWrapper(options.json_file)
        option_list_json = json_wrapper_option_list.read()
        options_sorted = option_list_json.items()
        for install_option in options_sorted:
            if displayOption == "tree" and install_option[1]["title"] == "ISO Packages":
                continue
            specDeps.readSpecsAndConvertToSerializableObjects(options.spec_dir, options.input_type, install_option[1]["file"], displayOption)

    sys.exit(0)

if __name__=="__main__":
    main()
