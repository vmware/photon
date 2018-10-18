#!/usr/bin/env python3

from argparse import ArgumentParser
import os.path
import platform
import collections
import traceback
import sys
import json
import copy
from CommandUtils import CommandUtils
from Logger import Logger
from constants import constants
from PackageManager import PackageManager
from SpecData import SPECS
from PackageInfo import PackageInfo

def main():
    usage = "Usage: %prog [options] <package name>"
    parser = ArgumentParser(usage)
    parser.add_argument("-s", "--spec-path", dest="specPath", default="../../SPECS")
    parser.add_argument("-x", "--source-path", dest="sourcePath",
                        default="../../stage/SOURCES")
    parser.add_argument("-r", "--rpm-path", dest="rpmPath",
                        default="../../stage/RPMS")
    parser.add_argument("-i", "--install-package", dest="installPackage",
                        default=False, action="store_true")
    parser.add_argument("-p", "--publish-RPMS-path", dest="publishRPMSPath",
                        default="../../stage/PUBLISHRPMS")
    parser.add_argument("-e", "--publish-XRPMS-path", dest="publishXRPMSPath",
                        default="../../stage/PUBLISHXRPMS")
    parser.add_argument("-l", "--log-path", dest="logPath", default="../../stage/LOGS")
    parser.add_argument("-y", "--log-level", dest="logLevel", default="error")
    parser.add_argument("-z", "--top-dir-path", dest="topDirPath", default="/usr/src/photon")
    parser.add_argument("-b", "--build-root-path", dest="buildRootPath", default="/mnt")
    parser.add_argument("-t", "--threads", dest="buildThreads",
                        default=1, type=int, help="Number of working threads")
    parser.add_argument("-m", "--tool-chain-stage", dest="toolChainStage", default="None")
    parser.add_argument("-c", "--pullsources-config", dest="pullsourcesConfig",
                        default="pullsources.conf")
    parser.add_argument("-d", "--dist-tag", dest="dist", default="")
    parser.add_argument("-k", "--input-RPMS-path", dest="inputRPMSPath", default=None)
    parser.add_argument("-n", "--build-number", dest="buildNumber", default="0000000")
    parser.add_argument("-v", "--release-version", dest="releaseVersion", default="NNNnNNN")
    parser.add_argument("-u", "--enable-rpmcheck", dest="rpmCheck",
                        default=False, action="store_true")
    parser.add_argument("-a", "--source-rpm-path", dest="sourceRpmPath",
                        default="../../stage/SRPMS")
    parser.add_argument("-w", "--pkginfo-file", dest="pkgInfoFile",
                        default="../../stage/pkg_info.json")
    parser.add_argument("-g", "--pkg-build-option-file", dest="pkgBuildOptionFile",
                        default="../../common/data/pkg_build_options.json")
    parser.add_argument("-q", "--rpmcheck-stop-on-error", dest="rpmCheckStopOnError",
                        default=False, action="store_true")
    parser.add_argument("-bd", "--publish-build-dependencies", dest="publishBuildDependencies",
                        default=False)
    parser.add_argument("-pw", "--package-weights-path", dest="packageWeightsPath", default=None)
    parser.add_argument("-bt", "--build-type", dest="pkgBuildType", default="chroot")
    parser.add_argument("-F", "--kat-build", dest="katBuild", default=None)
    parser.add_argument("-pj", "--packages-json-input", dest="pkgJsonInput", default=None)
    parser.add_argument("PackageName", nargs='?')
    options = parser.parse_args()
    cmdUtils = CommandUtils()
    if not os.path.isdir(options.logPath):
        cmdUtils.runCommandInShell("mkdir -p " + options.logPath)

    logger = Logger.getLogger("Main", options.logPath, options.logLevel)
    errorFlag = False
    package = None
    pkgInfoJsonFile = options.pkgInfoFile
    if not os.path.isdir(options.sourcePath):
        logger.error("Given Sources Path is not a directory:" + options.sourcePath)
        errorFlag = True
    if not os.path.isdir(options.specPath):
        logger.error("Given Specs Path is not a directory:" + options.specPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath):
        logger.error("Given RPMS Path is not a directory:" + options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishXRPMSPath):
        logger.error("Given X RPMS Path is not a directory:" + options.publishXRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath + "/" + platform.machine()):
        logger.error("Given RPMS Path is missing " + platform.machine()+
                     " sub-directory:"+options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishXRPMSPath+"/" + platform.machine()):
        logger.error("Given X RPMS Path is missing "+platform.machine()+
                     " sub-directory:"+options.publishXRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath+"/noarch"):
        logger.error("Given RPMS Path is missing noarch sub-directory:"+
                     options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishXRPMSPath+"/noarch"):
        logger.error("Given X RPMS Path is missing noarch sub-directory:"+
                     options.publishXRPMSPath)
        errorFlag = True
    if not os.path.isfile(options.pkgBuildOptionFile):
        logger.warning("Given JSON File is not a file:"+options.pkgBuildOptionFile)

    if options.inputRPMSPath is not None and not os.path.isdir(options.inputRPMSPath):
        logger.error("Given input RPMS Path is not a directory:"+options.inputRPMSPath)
        errorFlag = True

    if options.packageWeightsPath is not None and not os.path.isfile(options.packageWeightsPath):
        logger.error("Given input Weights file is not a file:"+options.packageWeightsPath)
        errorFlag = True

    if options.pkgJsonInput is not None and not os.path.isfile(options.pkgJsonInput):
        logger.error("Given input packages file is not a file:"+options.pkgJsonInput)
        errorFlag = True

    if options.installPackage:
        if not options.PackageName:
            logger.error("Please provide package name")
            errorFlag = True
        else:
            package = options.PackageName

    if errorFlag:
        logger.error("Found some errors. Please fix input options and re-run it.")
        return False

    if not os.path.isdir(options.rpmPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/"+platform.machine())
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/noarch")

    if not os.path.isdir(options.sourceRpmPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.sourceRpmPath)

    if not os.path.isdir(options.buildRootPath):
        cmdUtils.runCommandInShell("mkdir -p " + options.buildRootPath)

    logger.debug("Source Path :"+options.sourcePath)
    logger.debug("Spec Path :" + options.specPath)
    logger.debug("Rpm Path :" + options.rpmPath)
    logger.debug("Log Path :" + options.logPath)
    logger.debug("Log Level :" + options.logLevel)
    logger.debug("Top Dir Path :" + options.topDirPath)
    logger.debug("Publish RPMS Path :" + options.publishRPMSPath)
    logger.debug("Publish X RPMS Path :" + options.publishXRPMSPath)

    if options.installPackage:
        logger.debug("Package to build:" + package)

    get_packages_with_build_options(options.pkgBuildOptionFile)

    try:

        constants.setSpecPath(options.specPath)
        constants.setSourcePath(options.sourcePath)
        constants.setRpmPath(options.rpmPath)
        constants.setSourceRpmPath(options.sourceRpmPath)
        constants.setTopDirPath(options.topDirPath)
        constants.setLogPath(options.logPath)
        constants.setLogLevel(options.logLevel)
        constants.setDist(options.dist)
        constants.setBuildNumber(options.buildNumber)
        constants.setReleaseVersion(options.releaseVersion)
        constants.setPrevPublishRPMRepo(options.publishRPMSPath)
        constants.setPrevPublishXRPMRepo(options.publishXRPMSPath)
        constants.setBuildRootPath(options.buildRootPath)
        constants.setPullSourcesConfig(options.pullsourcesConfig)
        constants.setInputRPMSPath(options.inputRPMSPath)
        constants.setRPMCheck(options.rpmCheck)
        constants.setRpmCheckStopOnError(options.rpmCheckStopOnError)
        constants.setPublishBuildDependencies(options.publishBuildDependencies)
        constants.setPackageWeightsPath(options.packageWeightsPath)
        constants.setKatBuild(options.katBuild)

        constants.initialize()
        # parse SPECS folder
        SPECS()
        if options.toolChainStage == "stage1":
            pkgManager = PackageManager()
            pkgManager.buildToolChain()
        elif options.toolChainStage == "stage2":
            pkgManager = PackageManager()
            pkgManager.buildToolChainPackages(options.buildThreads)
        elif options.installPackage:
            buildAPackage(package, options.buildThreads, options.pkgBuildType)
        elif options.pkgJsonInput:
            buildPackagesInJson(logger, options.buildThreads, pkgInfoJsonFile,
                                     options.pkgJsonInput, options.pkgBuildType)
        else:
            buildPackagesForAllSpecs(logger, options.buildThreads, pkgInfoJsonFile,
                                     options.pkgBuildType)
    except Exception as e:
        logger.error("Caught an exception")
        logger.error(str(e))
        # print stacktrace
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)


def buildAPackage(package, buildThreads, pkgBuildType):
    listPackages = [package]
    pkgManager = PackageManager(pkgBuildType=pkgBuildType)
    if constants.rpmCheck:
        constants.setTestForceRPMS(copy.copy(listPackages))
    pkgManager.buildPackages(listPackages, buildThreads, pkgBuildType)

def buildPackagesInJson(logger, buildThreads, pkgInfoJsonFile, pkgJsonInput, pkgBuildType):
    listPackages = []
    with open(pkgJsonInput) as jsonData:
        pkg_list_json = json.load(jsonData)
        listPackages = pkg_list_json["packages"]
    if constants.rpmCheck:
        constants.setTestForceRPMS(copy.copy(listPackages))
    pkgManager = PackageManager(pkgBuildType=pkgBuildType)
    pkgManager.buildPackages(listPackages, buildThreads, pkgBuildType)

    # Generating package info file which is required by installer
    logger.debug("Writing Package info to the file:" + pkgInfoJsonFile)
    pkgInfo = PackageInfo()
    pkgInfo.loadPackagesData()
    pkgInfo.writePkgListToFile(pkgInfoJsonFile)

def buildPackagesForAllSpecs(logger, buildThreads, pkgInfoJsonFile, pkgBuildType):
    listPackages = SPECS.getData().getListPackages()
    if constants.rpmCheck:
        constants.setTestForceRPMS(copy.copy(listPackages))
    pkgManager = PackageManager(pkgBuildType=pkgBuildType)
    pkgManager.buildPackages(listPackages, buildThreads, pkgBuildType)

    # Generating package info file which is required by installer
    logger.debug("Writing Package info to the file:" + pkgInfoJsonFile)
    pkgInfo = PackageInfo()
    pkgInfo.loadPackagesData()
    pkgInfo.writePkgListToFile(pkgInfoJsonFile)


def get_packages_with_build_options(pkg_build_options_file):
    if os.path.exists(pkg_build_options_file):
        with open(pkg_build_options_file) as jsonData:
            pkg_build_option_json = json.load(jsonData, object_pairs_hook=collections.OrderedDict)
            constants.setBuildOptions(pkg_build_option_json)

def get_all_package_names(build_install_option):
    base_path = os.path.dirname(build_install_option)
    packages = []

    with open(build_install_option) as jsonData:
        option_list_json = json.load(jsonData, object_pairs_hook=collections.OrderedDict)
        options_sorted = option_list_json.items()

        for install_option in options_sorted:
            filename = os.path.join(base_path, install_option[1]["file"])
            with open(filename) as pkgJsonData:
                package_list_json = json.load(pkgJsonData)
            packages = packages + package_list_json["packages"]

    return packages


if __name__ == "__main__":
    main()
