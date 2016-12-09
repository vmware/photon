#!/usr/bin/env python

from optparse import OptionParser
import os.path
from CommandUtils import CommandUtils
from Logger import Logger
from constants import constants
from PackageManager import PackageManager
import json
import sys
from SpecUtils import Specutils
from StringUtils import StringUtils
import collections
import traceback
from PackageInfo import PackageInfo

def main():
    usage = "Usage: %prog [options] <package name>"
    parser = OptionParser(usage)
    parser.add_option("-s",  "--spec-path",  dest="specPath",  default="../../SPECS")
    parser.add_option("-x",  "--source-path",  dest="sourcePath",  default="../../stage/SOURCES")
    parser.add_option("-r",  "--rpm-path",  dest="rpmPath",  default="../../stage/RPMS")
    parser.add_option("-i",  "--install-package", dest="installPackage",  default=False,  action ="store_true")
    parser.add_option("-p",  "--publish-RPMS-path", dest="publishRPMSPath",  default="../../stage/PUBLISHRPMS")
    parser.add_option("-l",  "--log-path", dest="logPath",  default="../../stage/LOGS")
    parser.add_option("-z",  "--top-dir-path", dest="topDirPath",  default="/usr/src/photon")
    parser.add_option("-b",  "--build-root-path", dest="buildRootPath",  default="/mnt")
    parser.add_option("-t",  "--threads", dest="buildThreads",  default=1, type="int", help="Number of working threads")
    parser.add_option("-m",  "--tool-chain-stage", dest="toolChainStage",  default="None")
    parser.add_option("-c",  "--pullsources-config", dest="pullsourcesConfig",  default="pullsources.conf")
    parser.add_option("-d",  "--dist", dest="dist",  default="")
    parser.add_option("-k",  "--input-RPMS-path", dest="inputRPMSPath",   default=None)
    parser.add_option("-n",  "--build-number", dest="buildNumber",  default="0000000")
    parser.add_option("-v",  "--release-version", dest="releaseVersion",  default="NNNnNNN")
    parser.add_option("-u",  "--enable-rpmcheck", dest="rpmCheck",  default=False, action ="store_true")
    parser.add_option("-a",  "--source-rpm-path",  dest="sourceRpmPath",  default="../../stage/SRPMS")
    parser.add_option("-w",  "--pkginfo-file",  dest="pkgInfoFile",  default="../../stage/pkg_info.json")
    parser.add_option("-g",  "--pkg-build-option-file",  dest="pkgBuildOptionFile",  default="../../common/data/pkg_build_options.json")
    parser.add_option("-q",  "--rpmcheck-stop-on-error", dest="rpmCheckStopOnError",  default=False, action ="store_true")

    (options,  args) = parser.parse_args()
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
    if not os.path.isdir(options.publishRPMSPath+"/x86_64"):
        logger.error("Given RPMS Path is missing x86_64 sub-directory:"+options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath+"/noarch"):
        logger.error("Given RPMS Path is missing noarch sub-directory:"+options.publishRPMSPath)
        errorFlag = True

    if not os.path.isfile(options.pkgBuildOptionFile):
        logger.warning("Given JSON File is not a file:"+options.pkgBuildOptionFile)

    if options.inputRPMSPath is not None and not os.path.isdir(options.inputRPMSPath):
        logger.error("Given input RPMS Path is not a directory:"+options.publishRPMSPath)
        errorFlag = True

    if options.installPackage :
        if len(args) != 1:
            logger.error("Please provide package name")
            errorFlag = True
        else:
            package=args[0]

    if errorFlag:
        logger.error("Found some errors. Please fix input options and re-run it.")
        return False


    if not os.path.isdir(options.rpmPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/x86_64")
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/noarch")

    if not os.path.isdir(options.sourceRpmPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.sourceRpmPath)

    if not os.path.isdir(options.buildRootPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.buildRootPath)

    logger.info("Source Path :"+options.sourcePath)
    logger.info("Spec Path :" + options.specPath)
    logger.info("Rpm Path :" + options.rpmPath)
    logger.info("Log Path :" + options.logPath)
    logger.info("Top Dir Path :" + options.topDirPath)
    logger.info("Publish RPMS Path :" + options.publishRPMSPath)

    if options.installPackage:
        logger.info("Package to build:"+package)

    listBuildOptionPackages = get_packages_with_build_options(options.pkgBuildOptionFile)

    try:
        constants.initialize(options)
        if package == "packages_list":
            buildPackagesList(options.buildRootPath+"/../packages_list.csv")
        elif package == "sources_list":
            if not os.path.isdir("../../stage/yaml_sources"):
                cmdUtils.runCommandInShell("mkdir -p ../../stage/yaml_sources")
            buildSourcesList('../../stage/yaml_sources',logger)
        elif package == "srpms_list":
            if not os.path.isdir("../../stage/yaml_srpms"):
                cmdUtils.runCommandInShell("mkdir -p ../../stage/yaml_srpms")
            buildSRPMList(options.sourceRpmPath,"../../stage/yaml_srpms",logger)
        elif options.toolChainStage == "stage1":
            pkgManager = PackageManager()
            pkgManager.buildToolChain()
        elif options.toolChainStage == "stage2":
            pkgManager = PackageManager()
            pkgManager.buildToolChainPackages(options.buildThreads)
        elif options.installPackage:
            buildAPackage(package, listBuildOptionPackages, options.pkgBuildOptionFile, options.buildThreads)
        else:
            buildPackagesForAllSpecs(listBuildOptionPackages, options.pkgBuildOptionFile, logger, options.buildThreads, pkgInfoJsonFile)
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
    listPackages =  constants.specData.getListPackages()
    listPackages.sort()
    for package in listPackages:
        name = package
        version = constants.specData.getVersion(package)
        license = constants.specData.getLicense(package)
        listPatches = constants.specData.getPatches(package)
        url = constants.specData.getURL(package)
        listSourceNames = constants.specData.getSources(package)
        sources = ""
        patches = ""
        if listPatches is not None:
            patches = " ".join(listPatches)
        if listSourceNames is not None:
            sources = " ".join(listSourceNames)
        csvFile.write(name+","+version+","+license+","+url+","+sources+","+patches+"\n")
    csvFile.close()

def buildSourcesList(yamlDir, logger, singleFile=True):
    strUtils = StringUtils()
    if singleFile:
        yamlFile = open(yamlDir+"/sources_list.yaml", "w")
    listPackages =  constants.specData.getListPackages()
    listPackages.sort()
    import PullSources
    for package in listPackages:
        ossname = package
        ossversion = constants.specData.getVersion(package)
        modified = False
        listPatches = constants.specData.getPatches(package)
        if listPatches is not None and len(listPatches) > 0 :
            modified = True
        url = constants.specData.getSourceURL(package)
        if url is None:
            url = constants.specData.getURL(package)

        sourceName = None
        listSourceNames = constants.specData.getSources(package)
        if len(listSourceNames) >0:
            sourceName=listSourceNames[0]
            sha1 = constants.specData.getSHA1(package, sourceName)
            if sha1 is not None:
                PullSources.get(sourceName, sha1, yamlDir, constants.pullsourcesConfig)

        if not singleFile:
            yamlFile = open(yamlDir+"/"+ossname+"-"+ossversion+".yaml", "w")
        yamlFile.write("vmwsource:"+ossname+":"+ossversion+":\n")
        yamlFile.write("  repository: VMWsource\n")
        yamlFile.write("  name: '"+ossname+"'\n")
        yamlFile.write("  version: '"+ossversion+"'\n")
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

def buildSRPMList(srpmPath, yamlDir, logger, singleFile=True):
    strUtils = StringUtils()
    if singleFile:
        yamlFile = open(yamlDir+"/srpm_list.yaml", "w")
    listPackages =  constants.specData.getListPackages()
    listPackages.sort()
    cmdUtils = CommandUtils()
    for package in listPackages:
        ossname = package
        ossversion = constants.specData.getVersion(package)
        ossrelease = constants.specData.getRelease(package)

        listFoundSRPMFiles = cmdUtils.findFile(ossname+"-"+ossversion+"-"+ossrelease+".src.rpm",srpmPath)
        srpmName = None
        if len(listFoundSRPMFiles) == 1:
            srpmFullPath = listFoundSRPMFiles[0];
            srpmName = os.path.basename(srpmFullPath)
            cpcmd = "cp "+ srpmFullPath +" "+yamlDir+"/"
            returnVal = cmdUtils.runCommandInShell(cpcmd)
            if not returnVal:
                logger.error("Copy SRPM File is failed for package:"+ossname)
        else:
             logger.error("SRPM file is not found:" +ossname)

        if not singleFile:
            yamlFile = open(yamlDir+"/"+ossname+"-"+ossversion+"-"+ossrelease+".yaml", "w")

        yamlFile.write("baseos:"+ossname+":"+ossversion+"-"+ossrelease+":\n")
        yamlFile.write("  repository: BaseOS\n")
        yamlFile.write("  name: '"+ossname+"'\n")
        yamlFile.write("  version: '"+ossversion+"-"+ossrelease+"'\n")
        yamlFile.write("  baseos-style: rpm\n")
        yamlFile.write("  baseos-source: '"+str(srpmName)+"'\n")
        yamlFile.write("  baseos-osname: 'photon'\n")
        yamlFile.write("\n")
        if not singleFile:
            yamlFile.close()

    if singleFile:
        yamlFile.close()
    logger.info("Generated srpm yaml files for all packages")

def buildAPackage(package, listBuildOptionPackages, pkgBuildOptionFile, buildThreads):
    listPackages=[]
    listPackages.append(package)
    pkgManager = PackageManager()
    if constants.rpmCheck:
        constants.setTestForceRPMS(listPackages[:])
    pkgManager.buildPackages(listPackages, listBuildOptionPackages, pkgBuildOptionFile, buildThreads)

def buildPackagesForAllSpecs(listBuildOptionPackages, pkgBuildOptionFile, logger, buildThreads, pkgInfoJsonFile):
    listPackages = constants.specData.getListPackages()

    logger.info("List of packages to build:")
    logger.info(listPackages)
    if constants.rpmCheck:
        constants.setTestForceRPMS(listPackages[:])
    pkgManager = PackageManager()
    pkgManager.buildPackages(listPackages, listBuildOptionPackages, pkgBuildOptionFile, buildThreads)

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
