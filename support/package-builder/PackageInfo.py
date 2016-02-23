import json
from Logger import Logger
from constants import constants
import os.path
from CommandUtils import CommandUtils

class SourcePackageInfo(object):
     sourcePkgList = {}
     logger = None


     @staticmethod
     def setLogging(logName=None,logPath=None):
        if logName is None:
            logName = "SourcePackageInfo"
        if logPath is None:
            logPath = constants.logPath
        SourcePackageInfo.logger=Logger.getLogger(logName,logPath)

     @staticmethod
     def loadPkgInfoFromFile(filePath):
         SourcePackageInfo.logger.info("Loading source package list from the json file")
         if not os.path.isfile(filePath):
             return
         pkgInfoFile = open(filePath,'r')
         SourcePackageInfo.sourcePkgList = json.load(pkgInfoFile)
         pkgInfoFile.close()

     @staticmethod
     def addSRPMData(packageName,version,release,arch,srpmFile):
         listPkgAttributes={"name":packageName,"version":version,"release":release,"arch":arch,"sourcerpm":srpmFile}
         SourcePackageInfo.sourcePkgList[packageName]=listPkgAttributes
         SourcePackageInfo.logger.info("Added source package to the list:"+packageName)

     @staticmethod
     def writePkgListToFile(fileName):
         SourcePackageInfo.logger.info("Writing source package list to the json file")
         cmdUtils=CommandUtils()
         dirPath=os.path.basename(fileName)
         if not os.path.isdir(dirPath):
             cmdUtils.runCommandInShell("mkdir -p "+dirPath)
         pkgInfoFile = open(fileName,'w+')
         json.dump(SourcePackageInfo.sourcePkgList, pkgInfoFile,indent=4)
         pkgInfoFile.close()
