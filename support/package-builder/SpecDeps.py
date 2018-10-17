#! /usr/bin/python3
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Harish Udaiya Kumar <hudaiyakumar@vmware.com>
import sys
import os
from argparse import ArgumentParser
import shutil
import traceback
from SpecData import SpecDependencyGenerator, SPECS
from jsonwrapper import JsonWrapper
from constants import constants
from CommandUtils import CommandUtils
from StringUtils import StringUtils
from Logger import Logger

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
    parser.add_argument("-d", "--display-option", dest="display_option", default=DEFAULT_DISPLAY_OPTION)
    parser.add_argument("-s", "--spec-path", dest="spec_path", default=SPEC_FILE_DIR)
    parser.add_argument("-l", "--log-path", dest="log_path", default=LOG_FILE_DIR)
    parser.add_argument("-y", "--log-level", dest="log_level", default="info")
    parser.add_argument("-t", "--stage-dir", dest="stage_dir", default="../../stage")
    parser.add_argument("-a", "--input-data-dir", dest="input_data_dir", default="../../common/data/")
    parser.add_argument("-o", "--output-dir", dest="output_dir", default="../../stage/common/data")
    options = parser.parse_args()

    constants.setSpecPath(options.spec_path)
    constants.setLogPath(options.log_path)
    constants.setLogLevel(options.log_level)
    constants.initialize()

    cmdUtils = CommandUtils()
    logger = Logger.getLogger("SpecDeps", options.log_path, options.log_level)

    if not os.path.isdir(options.output_dir):
        cmdUtils.runCommandInShell2("mkdir -p "+options.output_dir)

    if not options.input_data_dir.endswith('/'):
        options.input_data_dir += '/'
    try:
        specDeps = SpecDependencyGenerator(options.log_path, options.log_level)

        if options.input_type == "remove-upward-deps":
            whoNeedsList = specDeps.process("get-upward-deps", options.pkg, options.display_option)
            logger.info("Removing upward dependencies: " + str(whoNeedsList))
            for pkg in whoNeedsList:
                package, version = StringUtils.splitPackageNameAndVersion(pkg)
                release = SPECS.getData().getRelease(package, version)
                for p in SPECS.getData().getPackages(package,version):
                    buildarch=SPECS.getData().getBuildArch(p, version)
                    rpmFile = "stage/RPMS/" + buildarch + "/" + p + "-" + version + "-" + release + ".*" + buildarch+".rpm"
                    logger.info("*** rm -f %s" % (rpmFile))
                    cmdUtils.runCommandInShell2("rm -f "+rpmFile)
        elif options.input_type == "print-upward-deps":
            whoNeedsList = specDeps.process("get-upward-deps", options.pkg, options.display_option)
            logger.info("Upward dependencies: " + str(whoNeedsList))
        # To display/print package dependencies on console
        elif (options.input_type == "pkg" or
                options.input_type == "who-needs"):
            specDeps.process(options.input_type, options.pkg, options.display_option)

        elif options.input_type == "json":
            list_json_files = options.json_file.split("\n")
            # Generate the expanded package dependencies json file based on package_list_file
            logger.info("Generating the install time dependency list for all json files")
            for json_file in list_json_files:
                shutil.copy2(json_file, options.output_dir)
                json_wrapper_option_list = JsonWrapper(json_file)
                option_list_json = json_wrapper_option_list.read()
                options_sorted = option_list_json.items()
                for install_option in options_sorted:
                    output_file = None
                    input_value = os.path.join(os.path.dirname(json_file), install_option[1]["file"])
                    if options.display_option == "tree" and install_option[1]["title"] == "ISO Packages":
                        continue
                    if options.display_option == "json":
                        output_file = os.path.join(options.output_dir, install_option[1]["file"])
                    specDeps.process(options.input_type, input_value, options.display_option, output_file)
    except Exception as e:
        traceback.print_exc()
        sys.stderr.write(str(e))
        sys.stderr.write("Failed to generate dependency lists from spec files\n")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
