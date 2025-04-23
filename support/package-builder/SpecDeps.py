#!/usr/bin/env python3

import sys
import os
import json
import queue
import operator
import shutil
import traceback

from SpecData import SPECS
from constants import constants
from Logger import Logger
from argparse import ArgumentParser

DEFAULT_INPUT_TYPE = "pkg"
DEFAULT_DISPLAY_OPTION = "tree"
SPEC_FILE_DIR = "../../SPECS"
LOG_FILE_DIR = "../../stage/LOGS"


class SpecDependencyGenerator(object):
    def __init__(self, logPath, logLevel):
        self.logger = Logger.getLogger("SerializableSpecobjects", logPath, logLevel)

    def findTotalRequires(self, mapDependencies, depQue, parent):
        while not depQue.empty():
            specPkg = depQue.get()
            try:
                listRequiredPackages = SPECS.getData().getRequiresForPkg(specPkg)
            except Exception as e:
                self.logger.info(f"Caught Exception: {e}")
                self.logger.info(f"{specPkg} is missing")
                raise e

            for depPkg in listRequiredPackages:
                if depPkg in mapDependencies:
                    if mapDependencies[depPkg] < mapDependencies[specPkg] + 1:
                        mapDependencies[depPkg] = mapDependencies[specPkg] + 1
                        parent[depPkg] = specPkg
                        self.updateLevels(
                            mapDependencies,
                            depPkg,
                            parent,
                            mapDependencies[depPkg],
                        )
                else:
                    mapDependencies[depPkg] = mapDependencies[specPkg] + 1
                    parent[depPkg] = specPkg
                    depQue.put(depPkg)

    def getBasePackagesRequired(self, pkg):
        listBasePackagesRequired = []
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
                    depBasePkg = f"{depPackage}-{version}"
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
            archSpecificPkgs = f"packages_{constants.buildArch}"
            if archSpecificPkgs in option_list_json:
                packages += option_list_json[archSpecificPkgs]

            return packages

    def updateLevels(self, mapDependencies, inPkg, parent, level):
        listPackages = SPECS.getData().getPackagesForPkg(inPkg)
        for depPkg in SPECS.getData().getRequiresForPkg(inPkg):
            if depPkg in listPackages:
                continue
            if depPkg in mapDependencies and mapDependencies[depPkg] < level + 1:
                mapDependencies[depPkg] = level + 1
                parent[depPkg] = inPkg
                self.updateLevels(
                    mapDependencies, depPkg, parent, mapDependencies[depPkg]
                )

    def calculateSpecDependency(self, inputPackages, mapDependencies, parent):
        depQue = queue.Queue()
        for package in inputPackages:
            if SPECS.getData().isRPMPackage(package):
                version = SPECS.getData().getHighestVersion(package)
                pkg = f"{package}-{version}"
                if pkg not in mapDependencies:
                    mapDependencies[pkg] = 0
                    parent[pkg] = ""
                    depQue.put(pkg)
                    self.findTotalRequires(mapDependencies, depQue, parent)
            else:
                self.logger.info(f"Could not find spec for: {package}")

    def displayDependencies(
        self, displayOption, inputType, inputValue, allDeps, parent
    ):
        children = {}
        sortedList = []
        for elem in sorted(allDeps.items(), key=operator.itemgetter(1), reverse=True):
            sortedList.append(elem[0])
        # construct all children nodes
        if displayOption == "tree":
            for k, v in parent.items():
                children.setdefault(v, []).append(k)
            if inputType == "json":
                self.logger.info(f"Dependency Mappings for {inputValue} :")
                self.logger.info("-" * 52 + f" {children}")
                self.logger.info("-" * 52)
            if "" in children:
                for child in children[""]:
                    self.logger.info(child)
                    self.printTree(children, child, 1)
                self.logger.info(
                    "*" * 18
                    + " {} ".format(len(sortedList))
                    + "packages in total "
                    + "*" * 18
                )
            else:
                if inputType == "pkg" and len(children) > 0:
                    self.logger.info(
                        "cyclic dependency detected, mappings: \n", children
                    )

        # To display a flat list of all packages
        elif displayOption == "list":
            self.logger.info(sortedList)

        # To generate a new JSON file based on given input json file
        elif displayOption == "json" and inputType == "json":
            d = {"packages": sortedList}
            with open(inputValue, "w") as outfile:
                json.dump(d, outfile)

        return sortedList

    # Returns list of RPM names of all packages excluding src.rpm
    def listRPMfilenames(self, includeDebuginfoRPMs=False):
        output = []
        arch = constants.currentArch
        for base_package in SPECS.getData().getListPackages():
            for version in SPECS.getData().getVersions(base_package):
                listRPMPackages = SPECS.getData().getRPMPackages(base_package, version)
                for package in listRPMPackages:
                    buildarch = SPECS.getData(arch).getBuildArch(package, version)
                    filename = os.path.join(
                        buildarch,
                        f"{package}-{version}.{buildarch}.rpm",
                    )
                    output.append(filename)
                """
                TODO: support '%global debug_package %{nil}' parsing, to
                exclude such packages
                """
                if (
                    includeDebuginfoRPMs
                    and SPECS.getData(arch).getBuildArch(base_package, version) == arch
                ):
                    filename = os.path.join(
                        buildarch,
                        f"{base_package}-debuginfo-{version}.{buildarch}.rpm",
                    )
                    output.append(filename)

        return output

    def process(self, inputType, inputValue, displayOption, outputFile=None):
        whoNeedsList = []
        inputPackages = []
        mapDependencies = {}
        parent = {}
        if inputType == "pkg" or inputType == "json":
            if inputType == "pkg":
                inputPackages.append(inputValue)
            else:
                inputPackages = self.getAllPackageNames(inputValue)
            self.calculateSpecDependency(inputPackages, mapDependencies, parent)
            if outputFile is not None:
                return self.displayDependencies(
                    displayOption,
                    inputType,
                    outputFile,
                    mapDependencies,
                    parent,
                )
            return self.displayDependencies(
                displayOption,
                inputType,
                inputValue,
                mapDependencies,
                parent,
            )
        elif inputType == "get-upward-deps":
            depList = []
            for specFile in inputValue.split(":"):
                if specFile in SPECS.getData().mapSpecFileNameToSpecObj:
                    specObj = SPECS.getData().mapSpecFileNameToSpecObj[specFile]
                    whoNeedsList.append(f"{specObj.name}-{specObj.version}")
                    depList.append(f"{specObj.name}-{specObj.version}")
            self.findTotalWhoNeeds(depList, whoNeedsList)
            return whoNeedsList

        elif inputType == "who-needs":
            for depPackage in SPECS.getData().mapPackageToSpec:
                pkg = f"{inputValue}-" + SPECS.getData().getHighestVersion(inputValue)
                for version in SPECS.getData().getVersions(depPackage):
                    depPkg = depPackage + "-" + version
                    if pkg in SPECS.getData().getRequiresForPkg(depPkg):
                        whoNeedsList.append(depPkg)
            self.logger.info(whoNeedsList)
            return whoNeedsList

        elif inputType == "all-requires":
            pkg = f"{inputValue}-" + SPECS.getData().getHighestVersion(inputValue)
            requires = SPECS.getData().getRequiresTreeOfBasePkgsForPkg(pkg)
            requires.sort()
            self.logger.info(requires)
            return requires

        elif inputType == "is-toolchain-pkg":
            for specFile in inputValue.split(":"):
                if specFile in SPECS.getData().mapSpecFileNameToSpecObj:
                    specObj = SPECS.getData().mapSpecFileNameToSpecObj[specFile]
                    if (specObj.name in constants.listCoreToolChainPackages) or (
                        specObj.name in constants.listToolChainPackages
                    ):
                        return True
            return False


def main():
    usage = "Usage: %prog [options]"
    parser = ArgumentParser(usage)
    parser.add_argument(
        "-i", "--input-type", dest="input_type", default=DEFAULT_INPUT_TYPE
    )
    parser.add_argument("-p", "--pkg", dest="pkg")
    parser.add_argument(
        "-f", "--file", dest="json_file", default="packages_minimal.json"
    )
    parser.add_argument(
        "-d",
        "--display-option",
        dest="display_option",
        default=DEFAULT_DISPLAY_OPTION,
    )
    parser.add_argument(
        "-s",
        "--spec-path",
        dest="spec_paths",
        nargs="+",
        default=[SPEC_FILE_DIR],
        help="Paths to spec files",
    )
    parser.add_argument("-l", "--log-path", dest="log_path", default=LOG_FILE_DIR)
    parser.add_argument("-y", "--log-level", dest="log_level", default="info")
    parser.add_argument("-t", "--stage-dir", dest="stage_dir", default="../../stage")
    parser.add_argument(
        "-a",
        "--input-data-dir",
        dest="input_data_dir",
        default="../../common/data/",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        default="../../stage/common/data",
    )
    options = parser.parse_args()

    constants.setSpecPaths(options.spec_paths)
    constants.setLogPath(options.log_path)
    constants.setLogLevel(options.log_level)
    constants.initialize()

    logger = Logger.getLogger("SpecDeps", options.log_path, options.log_level)

    os.makedirs(options.output_dir, exist_ok=True)

    if not options.input_data_dir.endswith("/"):
        options.input_data_dir += "/"
    try:
        specDeps = SpecDependencyGenerator(options.log_path, options.log_level)

        if options.input_type == "print-upward-deps":
            whoNeedsList = specDeps.process(
                "get-upward-deps", options.pkg, options.display_option
            )
            logger.info(f"Upward dependencies: {whoNeedsList}")
        # To display/print package dependencies on console
        elif (
            options.input_type == "pkg"
            or options.input_type == "who-needs"
            or options.input_type == "all-requires"
        ):
            specDeps.process(options.input_type, options.pkg, options.display_option)

        elif options.input_type == "json":
            list_json_files = options.json_file.split("\n")
            """
            Generate the expanded package dependencies json file based on
            package_list_file
            """
            logger.info(
                "Generating the install time dependency list for all " "json files"
            )
            if list_json_files:
                shutil.copy2(
                    os.path.dirname(list_json_files[0])
                    + "/build_install_options_all.json",
                    options.output_dir,
                )
            for json_file in list_json_files:
                output_file = None
                if options.display_option == "json":
                    output_file = os.path.join(
                        options.output_dir,
                        os.path.splitext(os.path.basename(json_file))[0]
                        + "_expanded.json",
                    )
                    specDeps.process(
                        options.input_type,
                        json_file,
                        options.display_option,
                        output_file,
                    )
                    shutil.copyfile(
                        json_file,
                        os.path.join(options.output_dir, os.path.basename(json_file)),
                    )
    except Exception as e:
        traceback.print_exc()
        sys.stderr.write(str(e))
        sys.stderr.write("Failed to generate dependency lists from spec files\n")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
