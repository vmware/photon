#!/usr/bin/env python3
# pylint: disable=invalid-name,missing-docstring
import os
import json
import sys
import traceback
from argparse import ArgumentParser
from Logger import Logger
from constants import constants
from CommandUtils import CommandUtils
from SpecData import SPECS



def main():
    usage = "Usage: %prog [options] <package name>"
    parser = ArgumentParser(usage)
    parser.add_argument("-s", "--spec-path", dest="specPath",
                        default="../../SPECS")
    parser.add_argument("-l", "--log-path", dest="logPath",
                        default="../../stage/LOGS")
    parser.add_argument("-a", "--source-rpm-path", dest="sourceRpmPath",
                        default="../../stage/SRPMS")
    parser.add_argument("-j", "--output-dir", dest="outputDirPath",
                        default="../../stage/")
    parser.add_argument("-c", "--pullsources-config", dest="pullsourcesConfig",
                        default="pullsources.conf")
    parser.add_argument("-f", "--pkg-blacklist-file", dest="pkgBlacklistFile",
                        default=None)
    parser.add_argument("-p", "--generate-pkg-list", dest="generatePkgList",
                        default=False, action="store_true")
    parser.add_argument("-y", "--generate-yaml-files", dest="generateYamlFiles",
                        default=False, action="store_true")

    options = parser.parse_args()
    errorFlag = False
    cmdUtils = CommandUtils()

    try:
        if not os.path.isdir(options.logPath):
            cmdUtils.runCommandInShell("mkdir -p " + options.logPath)
        logger = Logger.getLogger(options.logPath + "/generateYamlFiles")

        if options.generateYamlFiles:
            if (options.pkgBlacklistFile is not None and
                    options.pkgBlacklistFile != "" and
                    not os.path.isfile(options.pkgBlacklistFile)):
                logger.error("Given package blacklist file is not valid:"
                             + options.pkgBlacklistFile)
                errorFlag = True

        if not os.path.isdir(options.specPath):
            logger.error("Given Specs Path is not a directory:" + options.specPath)
            errorFlag = True

        if not os.path.isdir(options.sourceRpmPath):
            logger.error("Given SRPM Path is not a directory:" + options.sourceRpmPath)
            errorFlag = True

        if options.generateYamlFiles and not os.path.isfile(options.pullsourcesConfig):
            logger.error("Given Source config file is not a valid file:"
                         + options.pullsourcesConfig)
            errorFlag = True

        if errorFlag:
            logger.error("Found some errors. Please fix input options and re-run it.")
            sys.exit(1)

        if options.generateYamlFiles:
            if not os.path.isdir(options.outputDirPath):
                cmdUtils.runCommandInShell("mkdir -p "+options.outputDirPath)

        constants.setSpecPath(options.specPath)
        constants.setSourceRpmPath(options.sourceRpmPath)
        constants.setLogPath(options.logPath)
        constants.setPullSourcesConfig(options.pullsourcesConfig)
        constants.initialize()

        # parse SPECS folder
        SPECS()

        if options.generatePkgList:
            buildPackagesList(options.outputDirPath + "/packages_list.csv")
        elif options.generateYamlFiles:
            blackListPkgs = readBlackListPackages(options.pkgBlacklistFile)
            buildSourcesList(options.outputDirPath, blackListPkgs, logger)
            buildSRPMList(options.sourceRpmPath, options.outputDirPath, blackListPkgs, logger)

    except Exception as e:
        print("Caught Exception: " + str(e))
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)


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
                csvFile.write(name + "," + version + "," + packagelicense + "," + url + "," +
                            sources + "," + patches + "\n")

def readBlackListPackages(pkgBlackListFile):
    blackListPkgs = []
    if pkgBlackListFile is not None and pkgBlackListFile != "":
        with open(pkgBlackListFile) as jsonFile:
            config = json.load(jsonFile)
            if 'packages' in config:
                blackListPkgs = config['packages']
    return blackListPkgs


def buildSourcesList(yamlDir, blackListPkgs, logger, singleFile=True):
    cmdUtils = CommandUtils()
    yamlSourceDir = os.path.join(yamlDir, "yaml_sources")
    if not os.path.isdir(yamlSourceDir):
        cmdUtils.runCommandInShell("mkdir -p " + yamlSourceDir)
    if singleFile:
        yamlFile = open(yamlSourceDir + "/sources_list.yaml", "w")
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
            if url is None:
                url = SPECS.getData().getURL(package, version)

            sourceName = None
            listSourceNames = SPECS.getData().getSources(package, version)
            if listSourceNames:
                sourceName = listSourceNames[0]
                sha1 = SPECS.getData().getSHA1(package, version, sourceName)
                if sha1 is not None:
                    PullSources.get(package, sourceName, sha1, yamlSourceDir,
                                    constants.pullsourcesConfig, logger)

            if not singleFile:
                yamlFile = open(yamlSourceDir + "/" + ossname + "-" + version + ".yaml", "w")
            yamlFile.write("vmwsource:" + ossname + ":" + version + ":\n")
            yamlFile.write("  repository: VMWsource\n")
            yamlFile.write("  name: '" + ossname + "'\n")
            yamlFile.write("  version: '" + ossversion + "'\n")
            yamlFile.write("  url: " + str(url) + "\n")
            yamlFile.write("  license: UNKNOWN\n")
            if sourceName is not None:
                yamlFile.write("  vmwsource-distribution: " + str(sourceName) + "\n")
            if modified:
                yamlFile.write("  modified: true\n")
            yamlFile.write("\n")
            if not singleFile:
                yamlFile.close()

    if singleFile:
        yamlFile.close()
    logger.info("Generated source yaml files for all packages")


def buildSRPMList(srpmPath, yamlDir, blackListPkgs, logger, singleFile=True):
    cmdUtils = CommandUtils()
    yamlSrpmDir = os.path.join(yamlDir, "yaml_srpms")
    if not os.path.isdir(yamlSrpmDir):
        cmdUtils.runCommandInShell("mkdir -p " + yamlSrpmDir)
    if singleFile:
        yamlFile = open(yamlSrpmDir + "/srpm_list.yaml", "w")
    listPackages = SPECS.getData().getListPackages()
    listPackages.sort()
    for package in listPackages:
        if package in blackListPkgs:
            continue
        ossname = package
        for ossversion in SPECS.getData().getVersions(package):
            ossrelease = SPECS.getData().getRelease(package, ossversion)

            listFoundSRPMFiles = cmdUtils.findFile(ossname + "-" + ossversion + "-" + ossrelease
                                                   + ".src.rpm",
                                                   srpmPath)
            srpmName = None
            if len(listFoundSRPMFiles) == 1:
                srpmFullPath = listFoundSRPMFiles[0]
                srpmName = os.path.basename(srpmFullPath)
                cpcmd = "cp " + srpmFullPath + " " + yamlSrpmDir + "/"
                returnVal = cmdUtils.runCommandInShell(cpcmd)
                if not returnVal:
                    logger.error("Copy SRPM File is failed for package:" + ossname)
            else:
                logger.error("SRPM file is not found:" + ossname)

            if not singleFile:
                yamlFile = open(yamlSrpmDir + "/" + ossname + "-" + ossversion + "-"
                                + ossrelease + ".yaml", "w")

            yamlFile.write("baseos:" + ossname + ":" + ossversion + "-" + ossrelease + ":\n")
            yamlFile.write("  repository: BaseOS\n")
            yamlFile.write("  name: '" + ossname + "'\n")
            yamlFile.write("  version: '" + ossversion + "-" + ossrelease + "'\n")
            yamlFile.write("  url: 'http://www.vmware.com'\n")
            yamlFile.write("  baseos-style: rpm\n")
            yamlFile.write("  baseos-source: '" + str(srpmName) + "'\n")
            yamlFile.write("  baseos-osname: 'photon'\n")
            yamlFile.write("\n")
            if not singleFile:
                yamlFile.close()

    if singleFile:
        yamlFile.close()
    logger.info("Generated SRPM yaml files for all packages")


if __name__ == "__main__":
    main()
