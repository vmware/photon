#!/usr/bin/env python

from argparse import ArgumentParser
import os.path
import platform
from CommandUtils import CommandUtils
from Logger import Logger
from constants import constants
from PackageManager import PackageManager
import json
import sys
from SpecData import SPECS
from SpecUtils import Specutils
from StringUtils import StringUtils
import collections
import traceback
from PackageInfo import PackageInfo

def main():
    usage = "Usage: %prog [options] <package name>"
    parser = ArgumentParser(usage)
    parser.add_argument("-s",  "--spec-path",  dest="specPath",  default="../../SPECS")
    parser.add_argument("-x",  "--source-path",  dest="sourcePath",  default="../../stage/SOURCES")
    parser.add_argument("-r",  "--rpm-path",  dest="rpmPath",  default="../../stage/RPMS")
    parser.add_argument("-i",  "--install-package", dest="installPackage",  default=False,  action ="store_true")
    parser.add_argument("-p",  "--publish-RPMS-path", dest="publishRPMSPath",  default="../../stage/PUBLISHRPMS")
    parser.add_argument("-e",  "--publish-XRPMS-path", dest="publishXRPMSPath",  default="../../stage/PUBLISHXRPMS")
    parser.add_argument("-l",  "--log-path", dest="logPath",  default="../../stage/LOGS")
    parser.add_argument("-z",  "--top-dir-path", dest="topDirPath",  default="/usr/src/photon")
    parser.add_argument("-b",  "--build-root-path", dest="buildRootPath",  default="/mnt")
    parser.add_argument("-t",  "--threads", dest="buildThreads",  default=1, type=int, help="Number of working threads")
    parser.add_argument("-m",  "--tool-chain-stage", dest="toolChainStage",  default="None")
    parser.add_argument("-c",  "--pullsources-config", dest="pullsourcesConfig",  default="pullsources.conf")
    parser.add_argument("-d",  "--dist", dest="dist",  default="")
    parser.add_argument("-k",  "--input-RPMS-path", dest="inputRPMSPath",   default=None)
    parser.add_argument("-n",  "--build-number", dest="buildNumber",  default="0000000")
    parser.add_argument("-v",  "--release-version", dest="releaseVersion",  default="NNNnNNN")
    parser.add_argument("-u",  "--enable-rpmcheck", dest="rpmCheck",  default=False, action ="store_true")
    parser.add_argument("-a",  "--source-rpm-path",  dest="sourceRpmPath",  default="../../stage/SRPMS")
    parser.add_argument("-w",  "--pkginfo-file",  dest="pkgInfoFile",  default="../../stage/pkg_info.json")
    parser.add_argument("-g",  "--pkg-build-option-file",  dest="pkgBuildOptionFile",  default="../../common/data/pkg_build_options.json")
    parser.add_argument("-q",  "--rpmcheck-stop-on-error", dest="rpmCheckStopOnError",  default=False, action ="store_true")
    parser.add_argument("-bd", "--publish-build-dependencies", dest="publishBuildDependencies", default=False)
    parser.add_argument("-pw", "--package-weights-path", dest="packageWeightsPath", default=None)
    parser.add_argument("-y",  "--generate-pkg-yaml-files",  dest="generatePkgYamlFiles",  default=False, action ="store_true")
    parser.add_argument("-j",  "--pkg-yaml-dir-path",  dest="pkgYamlDirPath",  default="../../stage/")
    parser.add_argument("-f",  "--pkg-blacklist-file",  dest="pkgBlacklistFile",  default=None)
    parser.add_argument("-bt", "--build-type",  dest="pkgBuildType",  default="chroot")
    parser.add_argument("-F",  "--kat-build", dest="katBuild",  default=None)
    parser.add_argument("PackageName", nargs='?')
    options = parser.parse_args()
    cmdUtils=CommandUtils()
    if not os.path.isdir(options.logPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.logPath)

    logger=Logger.getLogger(options.logPath+"/Main")
    errorFlag=False
    package = None
    pkgInfoJsonFile = options.pkgInfoFile
    if not os.path.isdir(options.sourcePath):
        logger.error("Given Sources Path is not a directory:"+options.sourcePath)
        errorFlag = True
    if not os.path.isdir(options.specPath):
        logger.error("Given Specs Path is not a directory:"+options.specPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath):
        logger.error("Given RPMS Path is not a directory:"+options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishXRPMSPath):
        logger.error("Given X RPMS Path is not a directory:"+options.publishXRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath+"/" + platform.machine()):
        logger.error("Given RPMS Path is missing "+platform.machine()+" sub-directory:"+options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishXRPMSPath+"/" + platform.machine()):
        logger.error("Given X RPMS Path is missing "+platform.machine()+" sub-directory:"+options.publishXRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath+"/noarch"):
        logger.error("Given RPMS Path is missing noarch sub-directory:"+options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishXRPMSPath+"/noarch"):
        logger.error("Given X RPMS Path is missing noarch sub-directory:"+options.publishXRPMSPath)
        errorFlag = True
    if not os.path.isfile(options.pkgBuildOptionFile):
        logger.warning("Given JSON File is not a file:"+options.pkgBuildOptionFile)

    if options.inputRPMSPath is not None and not os.path.isdir(options.inputRPMSPath):
        logger.error("Given input RPMS Path is not a directory:"+options.inputRPMSPath)
        errorFlag = True

    if options.packageWeightsPath is not None and not os.path.isfile(options.packageWeightsPath):
        logger.error("Given input Weights file is not a file:"+options.packageWeightsPath)
        errorFlag = True

    if options.generatePkgYamlFiles:
        if options.pkgBlacklistFile is not None and options.pkgBlacklistFile != "" and not os.path.isfile(options.pkgBlacklistFile):
            logger.error("Given package blacklist file is not valid:"+options.pkgBlacklistFile)
            errorFlag = True

    if options.installPackage :
        if not options.PackageName:
            logger.error("Please provide package name")
            errorFlag = True
        else:
            package=options.PackageName

    if errorFlag:
        logger.error("Found some errors. Please fix input options and re-run it.")
        return False


    if not os.path.isdir(options.rpmPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/"+platform.machine())
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/noarch")

    if not os.path.isdir(options.sourceRpmPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.sourceRpmPath)

    if not os.path.isdir(options.buildRootPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.buildRootPath)

    if options.generatePkgYamlFiles:
        if not os.path.isdir(options.pkgYamlDirPath):
            cmdUtils.runCommandInShell("mkdir -p "+options.pkgYamlDirPath)

    logger.info("Source Path :"+options.sourcePath)
    logger.info("Spec Path :" + options.specPath)
    logger.info("Rpm Path :" + options.rpmPath)
    logger.info("Log Path :" + options.logPath)
    logger.info("Top Dir Path :" + options.topDirPath)
    logger.info("Publish RPMS Path :" + options.publishRPMSPath)
    logger.info("Publish X RPMS Path :" + options.publishXRPMSPath)

    if options.installPackage:
        logger.info("Package to build:"+package)

    listBuildOptionPackages = get_packages_with_build_options(options.pkgBuildOptionFile)

    try:
        constants.initialize(options)
        # parse SPECS folder
        SPECS();
        if package == "packages_list":
            buildPackagesList(options.buildRootPath+"/../packages_list.csv")
        elif options.generatePkgYamlFiles:
            blackListPkgs = readBlackListPackages(options.pkgBlacklistFile)
            buildSourcesList(options.pkgYamlDirPath, blackListPkgs, logger)
            buildSRPMList(options.sourceRpmPath, options.pkgYamlDirPath, blackListPkgs, logger)
        elif options.toolChainStage == "stage1":
            pkgManager = PackageManager()
            pkgManager.buildToolChain()
        elif options.toolChainStage == "stage2":
            pkgManager = PackageManager()
            pkgManager.buildToolChainPackages(options.buildThreads)
        elif options.installPackage:
            buildAPackage(package, listBuildOptionPackages, options.pkgBuildOptionFile, options.buildThreads, options.pkgBuildType)
        else:
            buildPackagesForAllSpecs(listBuildOptionPackages, options.pkgBuildOptionFile, logger, options.buildThreads, pkgInfoJsonFile, options.pkgBuildType)

    except Exception as e:
        logger.error("Caught an exception")
        logger.error(str(e))
        # print stacktrace
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)

def buildPackagesList(csvFilename):
    csvFile = open(csvFilename, "w")
    csvFile.write("Package,Version,License,URL,Sources,Patches\n")
    listPackages =  SPECS.getData().getListPackages()
    listPackages.sort()
    for package in listPackages:
        name = package
        for version in SPECS.getData().getVersions(package):
                license = SPECS.getData().getLicense(package, version)
                listPatches = SPECS.getData().getPatches(package, version)
                url = SPECS.getData().getURL(package, version)
                listSourceNames = SPECS.getData().getSources(package,version)
                sources = ""
                patches = ""
                if listPatches is not None:
                        patches = " ".join(listPatches)
                if listSourceNames is not None:
                        sources = " ".join(listSourceNames)
                csvFile.write(name+","+version+","+license+","+url+","+sources+","+patches+"\n")
                csvFile.close()

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
        cmdUtils.runCommandInShell("mkdir -p "+yamlSourceDir)
    if singleFile:
        yamlFile = open(yamlSourceDir+"/sources_list.yaml", "w")
    listPackages =  SPECS.getData().getListPackages()
    listPackages.sort()
    import PullSources
    for package in listPackages:
        if package in blackListPkgs:
            continue
        ossname = package
        for version in SPECS.getData().getVersions(package):
                modified = False
                listPatches = SPECS.getData().getPatches(package, version)
                if listPatches is not None and len(listPatches) > 0 :
                        modified = True
                url = SPECS.getData().getSourceURL(package, version)
                if url is None:
                        url = SPECS.getData().getURL(package, version)

                sourceName = None
                listSourceNames = SPECS.getData().getSources(package, version)
                if len(listSourceNames) >0:
                        sourceName=listSourceNames[0]
                        sha1 = SPECS.getData().getSHA1(package, sourceName, version)
                        if sha1 is not None:
                                PullSources.get(package, sourceName, sha1, yamlSourceDir, constants.pullsourcesConfig, logger)

                if not singleFile:
                        yamlFile = open(yamlSourceDir+"/"+ossname+"-"+version+".yaml", "w")
                yamlFile.write("vmwsource:"+ossname+":"+version+":\n")
                yamlFile.write("  repository: VMWsource\n")
                yamlFile.write("  name: '"+ossname+"'\n")
                yamlFile.write("  version: '"+version+"'\n")
                yamlFile.write("  url: "+str(url)+"\n")
                yamlFile.write("  license: UNKNOWN\n")
                if sourceName is not None:
                        yamlFile.write("  vmwsource-distribution: "+str(sourceName)+"\n")
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
        cmdUtils.runCommandInShell("mkdir -p "+yamlSrpmDir)
    if singleFile:
        yamlFile = open(yamlSrpmDir+"/srpm_list.yaml", "w")
    listPackages =  SPECS.getData().getListPackages()
    listPackages.sort()
    for package in listPackages:
        if package in blackListPkgs:
            continue
        ossname = package
        for ossversion in SPECS.getData().getVersions(package):
                ossrelease = SPECS.getData().getRelease(package, ossversion)

                listFoundSRPMFiles = cmdUtils.findFile(ossname+"-"+ossversion+"-"+ossrelease+".src.rpm",srpmPath)
                srpmName = None
                if len(listFoundSRPMFiles) == 1:
                        srpmFullPath = listFoundSRPMFiles[0];
                        srpmName = os.path.basename(srpmFullPath)
                        cpcmd = "cp "+ srpmFullPath +" "+yamlSrpmDir+"/"
                        returnVal = cmdUtils.runCommandInShell(cpcmd)
                        if not returnVal:
                                logger.error("Copy SRPM File is failed for package:"+ossname)
                else:
                        logger.error("SRPM file is not found:" +ossname)

                if not singleFile:
                        yamlFile = open(yamlSrpmDir+"/"+ossname+"-"+ossversion+"-"+ossrelease+".yaml", "w")

                yamlFile.write("baseos:"+ossname+":"+ossversion+"-"+ossrelease+":\n")
                yamlFile.write("  repository: BaseOS\n")
                yamlFile.write("  name: '"+ossname+"'\n")
                yamlFile.write("  version: '"+ossversion+"-"+ossrelease+"'\n")
                yamlFile.write("  url: 'http://www.vmware.com'\n")
                yamlFile.write("  baseos-style: rpm\n")
                yamlFile.write("  baseos-source: '"+str(srpmName)+"'\n")
                yamlFile.write("  baseos-osname: 'photon'\n")
                yamlFile.write("\n")
                if not singleFile:
                        yamlFile.close()

        if singleFile:
                yamlFile.close()
        logger.info("Generated srpm yaml files for all packages")

def buildAPackage(package, listBuildOptionPackages, pkgBuildOptionFile, buildThreads, pkgBuildType):
    listPackages=[]
    listPackages.append(package)
    pkgManager = PackageManager(pkgBuildType=pkgBuildType)
    if constants.rpmCheck:
        constants.setTestForceRPMS(listPackages[:])
    pkgManager.buildPackages(listPackages, listBuildOptionPackages, pkgBuildOptionFile, buildThreads, pkgBuildType)

def buildPackagesForAllSpecs(listBuildOptionPackages, pkgBuildOptionFile, logger, buildThreads, pkgInfoJsonFile, pkgBuildType):
    listPackages = SPECS.getData().getListPackages()

    logger.info("List of packages to build:")
    logger.info(listPackages)
    if constants.rpmCheck:
        constants.setTestForceRPMS(listPackages[:])
    pkgManager = PackageManager(pkgBuildType=pkgBuildType)
    pkgManager.buildPackages(listPackages, listBuildOptionPackages, pkgBuildOptionFile, buildThreads, pkgBuildType)

    #Generating package info file which is required by installer
    logger.info("Writing Package info to the file:"+pkgInfoJsonFile)
    pkgInfo = PackageInfo()
    pkgInfo.loadPackagesData()
    pkgInfo.writePkgListToFile(pkgInfoJsonFile)

def get_packages_with_build_options(pkg_build_options_file):
    packages = []
    if os.path.exists(pkg_build_options_file):
        jsonData = open(pkg_build_options_file)
        pkg_build_option_json = json.load(jsonData, object_pairs_hook=collections.OrderedDict)
        jsonData.close()
        pkgs_sorted = pkg_build_option_json.items()
        for pkg in pkgs_sorted:
            p =  pkg[0].encode('utf-8')
            packages.append(str(p))

    return packages

def get_all_package_names(build_install_option):
    base_path = os.path.dirname(build_install_option)
    jsonData = open(build_install_option)
    option_list_json = json.load(jsonData, object_pairs_hook=collections.OrderedDict)
    jsonData.close()
    options_sorted = option_list_json.items()
    packages = []

    for install_option in options_sorted:
        filename = os.path.join(base_path, install_option[1]["file"])
        jsonData=open(filename)
        package_list_json = json.load(jsonData)
        jsonData.close()
        packages = packages + package_list_json["packages"]

    return packages

if __name__=="__main__":
    main()
