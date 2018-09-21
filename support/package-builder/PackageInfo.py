import json
import os.path
from Logger import Logger
from constants import constants
from CommandUtils import CommandUtils
from PackageUtils import PackageUtils
from SpecData import SPECS

class PackageInfo(object):

    def __init__(self, logName=None, logPath=None):
        if logName is None:
            logName = "PackageInfo"
        if logPath is None:
            logPath = constants.logPath
        self.logName = logName
        self.logPath = logPath
        self.logger = Logger.getLogger(logName, logPath)
        self.pkgList = {}

    def loadPackagesData(self):
        listPackages = SPECS.getData().getListPackages()
        listPackages.sort()
        listRPMFiles = []
        cmdUtils = CommandUtils()
        for package in listPackages:
            version = SPECS.getData().getVersion(package)
            release = SPECS.getData().getRelease(package, version)
            listRPMPackages = SPECS.getData().getRPMPackages(package)
            srpmFileName = package + "-" + version + "-" + release + ".src.rpm"
            srpmFiles = cmdUtils.findFile(srpmFileName, constants.sourceRpmPath)
            srpmFile = None
            if len(srpmFiles) == 1:
                srpmFile = srpmFiles[0]
            debugrpmFileName = package + "-debuginfo-" + version + "-" + release + "*"
            debugrpmFiles = cmdUtils.findFile(debugrpmFileName, constants.rpmPath)
            debugrpmFile = None
            if len(debugrpmFiles) == 1:
                debugrpmFile = debugrpmFiles[0]
            pkgUtils = PackageUtils(self.logName, self.logPath)
            for rpmPkg in listRPMPackages:
                rpmFile = pkgUtils.findRPMFileForGivenPackage(rpmPkg)
                if rpmFile is not None:
                    listRPMFiles.append(rpmFile)
                    listPkgAttributes = {"sourcerpm":srpmFile, "rpm":rpmFile,
                                         "debugrpm":debugrpmFile}
                    self.pkgList[rpmPkg] = listPkgAttributes
                    self.logger.debug("Added " + rpmPkg + " rpm package to the list")
                else:
                    self.logger.error("Missing rpm file for package:" + rpmPkg)

    def writePkgListToFile(self, fileName):
        self.logger.info("Writing package list to the json file")
        cmdUtils = CommandUtils()
        dirPath = os.path.basename(fileName)
        if not os.path.isdir(dirPath):
            cmdUtils.runCommandInShell("mkdir -p " + dirPath)
        with open(fileName, 'w+') as pkgInfoFile:
            json.dump(self.pkgList, pkgInfoFile, indent=4)
