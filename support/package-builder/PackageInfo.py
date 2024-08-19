#!/usr/bin/env python3

import json
import os

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
        self.logger = Logger.getLogger(logName, logPath, constants.logLevel)
        self.pkgList = {}
        self.cmdUtils = CommandUtils()

    def loadPackagesData(self):
        listPackages = SPECS.getData().getListPackages()
        listPackages.sort()
        pkgUtils = PackageUtils(self.logName, self.logPath)
        for package in listPackages:
            for version in SPECS.getData().getVersions(package):
                srpmFile = pkgUtils.findSourceRPMFile(package, version)
                debugrpmFile = pkgUtils.findDebugRPMFile(package, version)
                listRPMPackages = SPECS.getData().getRPMPackages(package, version)
                for rpmPkg in listRPMPackages:
                    rpmFile = pkgUtils.findRPMFile(rpmPkg, version)
                    if rpmFile is not None:
                        listPkgAttributes = {
                            "sourcerpm": srpmFile,
                            "rpm": rpmFile,
                            "debugrpm": debugrpmFile,
                        }
                        self.pkgList[f"{rpmPkg}-{version}"] = listPkgAttributes
                        self.logger.debug(
                            f"Added {rpmPkg}-{version} to package info json"
                        )
                    else:
                        self.logger.debug(f"Missing rpm file for package: {rpmPkg}")

    def writePkgListToFile(self, fileName):
        self.logger.debug("Writing package list to the json file")
        dirPath = os.path.dirname(fileName)
        if dirPath and not os.path.isdir(dirPath):
            self.cmdUtils.runBashCmd(f"mkdir -p {dirPath}")
        with open(fileName, "w+") as pkgInfoFile:
            json.dump(self.pkgList, pkgInfoFile, indent=4)
