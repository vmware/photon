#! /usr/bin/python3
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Harish Udaiya Kumar <hudaiyakumar@vmware.com>
import sys
import os
import json
import queue
import operator
from argparse import ArgumentParser
import shutil
import traceback
from SpecData import SPECS
from jsonwrapper import JsonWrapper
from constants import constants
from CommandUtils import CommandUtils
from StringUtils import StringUtils
from Logger import Logger

DEFAULT_INPUT_TYPE = "pkg"
DEFAULT_DISPLAY_OPTION = "tree"
SPEC_FILE_DIR = "../../SPECS"
LOG_FILE_DIR = "../../stage/LOGS"


class SpecDependencyGenerator(object):

    def __init__(self, logPath, logLevel):
        self.logger = Logger.getLogger("Serializable Spec objects", logPath, logLevel)

    def findTotalRequires(self, mapDependencies, depQue, parent):
        while not depQue.empty():
            specPkg = depQue.get()
            try:
                listRequiredPackages = SPECS.getData().getRequiresForPkg(specPkg)
            except Exception as e:
                self.logger.info("Caught Exception:"+str(e))
                self.logger.info(specPkg + " is missing")
                raise e

            for depPkg in listRequiredPackages:
                if depPkg in mapDependencies:
                    if mapDependencies[depPkg] < mapDependencies[specPkg] + 1:
                        mapDependencies[depPkg] = mapDependencies[specPkg] + 1
                        parent[depPkg] = specPkg
                        self.updateLevels(mapDependencies, depPkg, parent, mapDependencies[depPkg])
                else:
                    mapDependencies[depPkg] = mapDependencies[specPkg] + 1
                    parent[depPkg] = specPkg
                    depQue.put(depPkg)

    def getBasePackagesRequired(self, pkg):
        listBasePackagesRequired=[]
        listPackagesRequired = SPECS.getData().getBuildRequiresForPkg(pkg)
        listPackagesRequired.extend(SPECS.getData().getRequiresAllForPkg(pkg))
        for p in listPackagesRequired:
            basePkg = SPECS.getData().getBasePkg(p)
            if basePkg not in listBasePackagesRequired:
                listBasePackagesRequired.append(basePkg)
        return listBasePackagesRequired


    def findTotalWhoNeeds(self, depList, whoNeeds):
        while depList:
            pkg = depList.pop(0)
            for depPackage in SPECS.getData().getListPackages():
                for version in SPECS.getData().getVersions(depPackage):
                    depBasePkg = depPackage+"-"+version
                    if depBasePkg in whoNeeds:
                        continue
                    if pkg in self.getBasePackagesRequired(depBasePkg):
                        whoNeeds.append(depBasePkg)
                        if depBasePkg not in depList:
                            depList.append(depBasePkg)

    def printTree(self, children, curParent, depth):
        if curParent in children:
            for child in children[curParent]:
                self.logger.info("\t" * depth + child)
                self.printTree(children, child, depth + 1)

    def getAllPackageNames(self, jsonFilePath):
        with open(jsonFilePath) as jsonData:
            option_list_json = json.load(jsonData)
            packages = option_list_json["packages"]
            return packages

    def updateLevels(self, mapDependencies, inPkg, parent, level):
        listPackages = SPECS.getData().getPackagesForPkg(inPkg)
        for depPkg in SPECS.getData().getRequiresForPkg(inPkg):
            if depPkg in listPackages:
                continue
            if depPkg in mapDependencies and mapDependencies[depPkg] < level + 1:
                mapDependencies[depPkg] = level + 1
                parent[depPkg] = inPkg
                self.updateLevels(mapDependencies, depPkg, parent, mapDependencies[depPkg])

    def calculateSpecDependency(self, inputPackages, mapDependencies, parent):
        depQue = queue.Queue()
        for package in inputPackages:
            if SPECS.getData().isRPMPackage(package):
                for version in SPECS.getData().getVersions(package):
                    pkg = package+"-"+version
                    if pkg not in mapDependencies:
                        mapDependencies[pkg] = 0
                        parent[pkg] = ""
                        depQue.put(pkg)
                        self.findTotalRequires(mapDependencies, depQue, parent)
            else:
                self.logger.info("Could not find spec for " + package)

    def displayDependencies(self, displayOption, inputType, inputValue, allDeps, parent):
        children = {}
        sortedList = []
        for elem in sorted(allDeps.items(), key=operator.itemgetter(1), reverse=True):
            sortedList.append(elem[0])
        # construct all children nodes
        if displayOption == "tree":
            for k, v in parent.iteritems():
                children.setdefault(v, []).append(k)
            if inputType == "json":
                self.logger.info("Dependency Mappings for {}".format(inputValue) + " :")
                self.logger.info("-" * 52 + " {}".format(children))
                self.logger.info("-" * 52)
            if "" in children:
                for child in children[""]:
                    self.logger.info(child)
                    self.printTree(children, child, 1)
                self.logger.info("*" * 18 + " {} ".format(len(sortedList)) +
                      "packages in total " + "*" * 18)
            else:
                if inputType == "pkg" and len(children) > 0:
                    self.logger.info("cyclic dependency detected, mappings: \n", children)

        # To display a flat list of all packages
        elif displayOption == "list":
            self.logger.info(sortedList)

        # To generate a new JSON file based on given input json file
        elif displayOption == "json" and inputType == "json":
            d = {'packages': sortedList}
            with open(inputValue, 'w') as outfile:
                json.dump(d, outfile)

        return sortedList

    def process(self, inputType, inputValue, displayOption, outputFile=None):
        whoNeedsList = []
        inputPackages = []
        whatNeedsBuild = []
        mapDependencies = {}
        parent = {}
        if inputType == "pkg" or inputType == "json":
            if inputType == "pkg":
                inputPackages.append(inputValue)
            else:
                inputPackages = self.getAllPackageNames(inputValue)

            self.calculateSpecDependency(inputPackages, mapDependencies, parent)
            if outputFile is not None:
                return self.displayDependencies(displayOption, inputType, outputFile, mapDependencies, parent)
            else:
                return self.displayDependencies(displayOption, inputType, inputValue, mapDependencies, parent)
        elif inputType == "get-upward-deps":
            depList = []
            for specFile in inputValue.split(":"):
                if specFile in SPECS.getData().mapSpecFileNameToSpecObj:
                    specObj = SPECS.getData().mapSpecFileNameToSpecObj[specFile]
                    whoNeedsList.append(specObj.name+"-"+specObj.version)
                    depList.append(specObj.name+"-"+specObj.version)
            self.findTotalWhoNeeds(depList, whoNeedsList)
            return whoNeedsList

        elif inputType == "who-needs":
            for depPackage in SPECS.getData().mapPackageToSpec:
                pkg=inputValue+"-"+SPECS.getData().getHighestVersion(inputValue)
                for version in SPECS.getData().getVersions(depPackage):
                    depPkg = depPackage+"-"+version
                    self.logger.info(depPkg)
                    if pkg in SPECS.getData().getRequiresForPkg(depPkg):
                        whoNeedsList.append(depPkg)
            self.logger.info(whoNeedsList)
            return whoNeedsList

        elif inputType == "is-toolchain-pkg":
            for specFile in inputValue.split(":"):
                if specFile in SPECS.getData().mapSpecFileNameToSpecObj:
                    specObj = SPECS.getData().mapSpecFileNameToSpecObj[specFile]
                    if (specObj.name in constants.listCoreToolChainPackages) \
                        or (specObj.name in constants.listToolChainPackages):
                        return True
            return False

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
        cmdUtils.runCommandInShell("mkdir -p "+options.output_dir)

    if not options.input_data_dir.endswith('/'):
        options.input_data_dir += '/'
    try:
        specDeps = SpecDependencyGenerator(options.log_path, options.log_level)

        if options.input_type == "remove-upward-deps":
            isToolChainPkg = specDeps.process("is-toolchain-pkg", options.pkg, options.display_option)
            if isToolChainPkg:
                logger.info("Removing all staged RPMs since toolchain packages were modified")
                cmdUtils.runCommandInShell("rm -rf stage/RPMS/")
            else:
                whoNeedsList = specDeps.process("get-upward-deps", options.pkg, options.display_option)
                logger.info("Removing upward dependencies: " + str(whoNeedsList))
                for pkg in whoNeedsList:
                    package, version = StringUtils.splitPackageNameAndVersion(pkg)
                    release = SPECS.getData().getRelease(package, version)
                    for p in SPECS.getData().getPackages(package,version):
                        buildarch=SPECS.getData().getBuildArch(p, version)
                        rpmFile = "stage/RPMS/" + buildarch + "/" + p + "-" + version + "-" + release + ".*" + buildarch+".rpm"
                        cmdUtils.runCommandInShell("rm -f "+rpmFile)

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
