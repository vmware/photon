#! /usr/bin/python3
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Harish Udaiya Kumar <hudaiyakumar@vmware.com>
import sys
import os
from argparse import ArgumentParser
from SpecData import SerializedSpecObjects
from jsonwrapper import JsonWrapper

DEFAULT_INPUT_TYPE = "pkg"
DEFAULT_DISPLAY_OPTION = "tree"
SPEC_FILE_DIR = "../../SPECS"
LOG_FILE_DIR = "../../stage/LOGS"

def main():
    usage = "Usage: %prog [options]"
    parser = ArgumentParser(usage)
    parser.add_argument("-i", "--input-type", dest="input_type", default=DEFAULT_INPUT_TYPE)
    parser.add_argument("-p", "--pkg", dest="pkg")
    parser.add_argument("-f", "--file", dest="json_file", default="packages_minimal.json")
    parser.add_argument("-d", "--disp", dest="display_option", default=DEFAULT_DISPLAY_OPTION)
    parser.add_argument("-s", "--spec-dir", dest="spec_dir", default=SPEC_FILE_DIR)
    parser.add_argument("-t", "--stage-dir", dest="stage_dir", default="../../stage")
    parser.add_argument("-a", "--input-data-dir", dest="input_data_dir",
                        default="../../common/data/")
    options = parser.parse_args()

    if not options.input_data_dir.endswith('/'):
        options.input_data_dir += '/'
    try:
        specDeps = SerializedSpecObjects(options.input_data_dir, options.stage_dir)
        displayOption = options.display_option
        abs_path = os.path.abspath(__file__)
        dir_name = os.path.dirname(abs_path)
        os.chdir(dir_name)

        # To display/print package dependencies on console
        if(options.input_type == "pkg" or
           options.input_type == "who-needs" or
           options.input_type == "who-needs-build"):
            targetName = options.pkg
            specDeps.readSpecsAndConvertToSerializableObjects(options.spec_dir,
                                                              options.input_type,
                                                              targetName, displayOption)
        elif options.input_type == "json":
        # Generate the expanded package dependencies json file based on package_list_file
            json_wrapper_option_list = JsonWrapper(options.json_file)
            option_list_json = json_wrapper_option_list.read()
            options_sorted = option_list_json.items()
            for install_option in options_sorted:
                if displayOption == "tree" and install_option[1]["title"] == "ISO Packages":
                    continue
                specDeps.readSpecsAndConvertToSerializableObjects(
                    options.spec_dir,
                    options.input_type, install_option[1]["file"],
                    displayOption)
    except Exception as _:
        sys.stderr.write("Failed to generate dependency lists from spec files\n")
        sys.exit(1)

    sys.stderr.write("Successfully generated dependency lists from spec files\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
