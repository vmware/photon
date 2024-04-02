#!/usr/bin/env python3

import os
import json
import sys
import traceback

from argparse import ArgumentParser
from Logger import Logger
from constants import constants
from CommandUtils import CommandUtils
from SpecData import SPECS

cmdUtils = CommandUtils()


def main():
    usage = "Usage: %prog [options] <package name>"
    parser = ArgumentParser(usage)
    parser.add_argument(
        "-s", "--spec-path", dest="specPath", default="../../SPECS"
    )
    parser.add_argument(
        "-l", "--log-path", dest="logPath", default="../../stage/LOGS"
    )
    parser.add_argument(
        "-a",
        "--source-rpm-path",
        dest="sourceRpmPath",
        default="../../stage/SRPMS",
    )
    parser.add_argument(
        "-j", "--output-dir", dest="outputDirPath", default="../../stage/"
    )
    parser.add_argument("-z", "--log-level", dest="logLevel", default="info")
    parser.add_argument(
        "-c",
        "--pullsources-config",
        dest="pullsourcesConfig",
        default="pullsources.conf",
    )
    parser.add_argument(
        "-f", "--pkg-blacklist-file", dest="pkgBlacklistFile", default=None
    )
    parser.add_argument(
        "-p",
        "--generate-pkg-list",
        dest="generatePkgList",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-y",
        "--generate-yaml-files",
        dest="generateYamlFiles",
        default=False,
        action="store_true",
    )
    parser.add_argument("-d", "--dist-tag", dest="dist", default="")

    options = parser.parse_args()
    errorFlag = False

    try:
        logName = "GenerateYamlFiles"
        logger = Logger.getLogger(logName, options.logPath, options.logLevel)

        if options.generateYamlFiles:
            if (
                options.pkgBlacklistFile is not None
                and options.pkgBlacklistFile != ""
                and not os.path.isfile(options.pkgBlacklistFile)
            ):
                logger.error(
                    "Given package blacklist file is not valid: "
                    f"{options.pkgBlacklistFile}"
                )
                errorFlag = True

        if not os.path.isdir(options.specPath):
            logger.error(
                f"Given Specs Path is not a directory: {options.specPath}"
            )
            errorFlag = True

        if not os.path.isdir(options.sourceRpmPath):
            logger.error(
                f"Given SRPM Path is not a directory: {options.sourceRpmPath}"
            )
            errorFlag = True

        if options.generateYamlFiles and not os.path.isfile(
            options.pullsourcesConfig
        ):
            logger.error(
                "Given Source config file is not a valid file: "
                f"{options.pullsourcesConfig}"
            )
            errorFlag = True

        if options.dist:
            dist_tag = options.dist
            logger.info(f"release tag is {dist_tag}")

        if errorFlag:
            logger.error(
                "Found some errors. Please fix input options and re-run it."
            )
            sys.exit(1)

        if options.generateYamlFiles:
            if not os.path.isdir(options.outputDirPath):
                cmdUtils.runBashCmd(f"mkdir -p {options.outputDirPath}")

        constants.setSpecPath(options.specPath)
        constants.setSourceRpmPath(options.sourceRpmPath)
        constants.setLogPath(options.logPath)
        constants.setLogLevel(options.logLevel)
        constants.setPullSourcesURL(get_baseurl(options.pullsourcesConfig))
        constants.initialize()

        # parse SPECS folder
        SPECS()

        if options.generatePkgList:
            buildPackagesList(f"{options.outputDirPath}/packages_list.csv")
        elif options.generateYamlFiles:
            blackListPkgs = readBlackListPackages(options.pkgBlacklistFile)
            buildSourcesList(options.outputDirPath, blackListPkgs, logger)
            buildSRPMList(
                options.sourceRpmPath,
                options.outputDirPath,
                blackListPkgs,
                dist_tag,
                logger,
            )

    except Exception as e:
        print(f"Caught Exception: {e}")
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)


def get_baseurl(conf_file):
    with open(conf_file) as jsonFile:
        config = json.load(jsonFile)
    return config["baseurl"]


def buildPackagesList(csvFilename):
    with open(csvFilename, "w") as csvFile:
        csvFile.write("Package,Version,License,URL,Sources,Patches\n")
        listPackages = SPECS.getData().getListPackages()
        listPackages.sort()
        for package in listPackages:
            name = package
            for version in SPECS.getData().getVersions(package):
                packagelicense = SPECS.getData().getLicense(package, version)
                listPatches = SPECS.getData().getPatches(package, version)
                url = SPECS.getData().getURL(package, version)
                listSourceNames = SPECS.getData().getSources(package, version)
                sources = ""
                patches = ""
                if listPatches is not None:
                    patches = " ".join(listPatches)
                if listSourceNames is not None:
                    sources = " ".join(listSourceNames)
                csvFile.write(
                    f"{name},{version},{packagelicense},{url},{sources},"
                    f"{patches}\n"
                )


def readBlackListPackages(pkgBlackListFile):
    blackListPkgs = []
    if pkgBlackListFile is not None and pkgBlackListFile != "":
        with open(pkgBlackListFile) as jsonFile:
            config = json.load(jsonFile)
            if "packages" in config:
                blackListPkgs = config["packages"]
    return blackListPkgs


def buildSourcesList(yamlDir, blackListPkgs, logger, singleFile=True):
    yamlSourceDir = os.path.join(yamlDir, "yaml_sources")
    if not os.path.isdir(yamlSourceDir):
        cmdUtils.runBashCmd(f"mkdir -p {yamlSourceDir}")
    if singleFile:
        yamlFile = open(f"{yamlSourceDir}/sources_list.yaml", "w")
    listPackages = SPECS.getData().getListPackages()
    listPackages.sort()

    import PullSources

    for package in listPackages:
        if package in blackListPkgs:
            continue
        ossname = package
        for version in SPECS.getData().getVersions(package):
            modified = False
            listPatches = SPECS.getData().getPatches(package, version)
            if listPatches:
                modified = True
            url = SPECS.getData().getSourceURL(package, version)
            if not url:
                url = SPECS.getData().getURL(package, version)

            sourceName = None
            listSourceNames = SPECS.getData().getSources(package, version)
            if listSourceNames:
                sourceName = listSourceNames[0]
                sha512 = SPECS.getData().getChecksum(
                    package, version, sourceName
                )
                if sha512:
                    PullSources.get(
                        package,
                        sourceName,
                        sha512,
                        yamlSourceDir,
                        constants.getPullSourcesURLs(package),
                        logger,
                    )

            if not singleFile:
                yamlFile = open(
                    f"{yamlSourceDir}/{ossname}-{version}.yaml",
                    "w",
                )

            version = version.split("-")[0]

            yamlFile.write(f"vmwsource:{ossname}:{version}:\n")
            yamlFile.write("  repository: VMWsource\n")
            yamlFile.write(f"  name: '{ossname}'\n")
            yamlFile.write(f"  version: '{version}'\n")
            yamlFile.write(f"  url: {url}\n")
            yamlFile.write("  license: UNKNOWN\n")
            if sourceName is not None:
                yamlFile.write(
                    "  vmwsource-distribution: {sourceName}\n"
                )
            if modified:
                yamlFile.write("  modified: true\n")
            yamlFile.write("\n")
            if not singleFile:
                yamlFile.close()

    if singleFile:
        yamlFile.close()
    logger.debug("Generated source yaml files for all packages")


def buildSRPMList(
    srpmPath, yamlDir, blackListPkgs, dist_tag, logger, singleFile=True
):
    yamlSrpmDir = os.path.join(yamlDir, "yaml_srpms")
    if not os.path.isdir(yamlSrpmDir):
        cmdUtils.runBashCmd(f"mkdir -p {yamlSrpmDir}")
    if singleFile:
        yamlFile = open(f"{yamlSrpmDir}/srpm_list.yaml", "w")
    listPackages = SPECS.getData().getListPackages()
    listPackages.sort()

    for package in listPackages:
        if package in blackListPkgs:
            continue
        ossname = package
        for ossversion in SPECS.getData().getVersions(package):
            srpm_file_name = f"{ossname}-{ossversion}.src.rpm"
            logger.info(f"srpm name is {srpm_file_name}")
            listFoundSRPMFiles = cmdUtils.findFile(srpm_file_name, srpmPath)

            srpmName = None
            if len(listFoundSRPMFiles) == 1:
                srpmFullPath = listFoundSRPMFiles[0]
                srpmName = os.path.basename(srpmFullPath)
                cpcmd = f"cp {srpmFullPath} {yamlSrpmDir}/"
                _, _, returnVal = cmdUtils.runBashCmd(cpcmd)
                if returnVal:
                    logger.error(
                        f"Copy SRPM File is failed for package: {ossname}"
                    )
            else:
                logger.error(f"SRPM file is not found: {ossname}")

            if not singleFile:
                yamlFile = open(
                    f"{yamlSrpmDir}/{ossname}-{ossversion}.yaml",
                    "w",
                )

            yamlFile.write(f"baseos:{ossname}:{ossversion}:\n")
            yamlFile.write("  repository: BaseOS\n")
            yamlFile.write(f"  name: '{ossname}'\n")
            yamlFile.write(f"  version: '{ossversion}'\n")
            yamlFile.write("  url: 'http://www.vmware.com'\n")
            yamlFile.write("  baseos-style: rpm\n")
            yamlFile.write(f"  baseos-source: '{srpmName}'\n")
            yamlFile.write("  baseos-osname: 'photon'\n")
            yamlFile.write("\n")
            if not singleFile:
                yamlFile.close()

    if singleFile:
        yamlFile.close()
    logger.debug("Generated SRPM yaml files for all packages")


if __name__ == "__main__":
    main()
