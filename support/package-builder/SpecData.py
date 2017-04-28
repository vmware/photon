from SpecUtils import Specutils
import os
from Logger import Logger
from distutils.version import StrictVersion

class SerializableSpecObject(object):
    def __init__(self):
        self.listPackages=[]
        self.listRPMPackages=[]
        self.name=""
        self.version=""
        self.release=""
        self.buildRequirePackages=[]
        self.installRequiresAllPackages=[]
        self.installRequiresPackages={}
        self.specFile=""
        self.listSources=[]
        self.checksums={}
        self.listPatches=[]
        self.securityHardening=""
        self.url=""
        self.sourceurl=""
        self.license=""
        self.specDefs={}

class SerializableSpecObjectsUtils(object):

    def __init__(self,logPath):
        self.mapSerializableSpecObjects={}
        self.mapPackageToSpec={}
        self.logger=Logger.getLogger("Serializable Spec objects", logPath )
        self.userDefinedMacros={}

    def readSpecsAndConvertToSerializableObjects(self,specFilesPath):
        listSpecFiles=[]
        self.getListSpecFiles(listSpecFiles,specFilesPath)
        for specFile in listSpecFiles:
            skipUpdating = False
            spec=Specutils(specFile)
            specName=spec.getBasePackageName()
            specObj=SerializableSpecObject()
            specObj.name=specName
            specObj.buildRequirePackages=spec.getBuildRequiresAllPackages()
            specObj.installRequiresAllPackages=spec.getRequiresAllPackages()
            specObj.listPackages=spec.getPackageNames()
            specObj.specFile=specFile
            specObj.version=spec.getVersion()
            specObj.release=spec.getRelease()
            specObj.listSources=spec.getSourceNames()
            specObj.checksums=spec.getChecksums()
            specObj.specDefs=spec.getDefinitions()
            specObj.listPatches=spec.getPatchNames()
            specObj.securityHardening=spec.getSecurityHardeningOption()
            specObj.isCheckAvailable=spec.isCheckAvailable()
            specObj.license=spec.getLicense()
            specObj.url=spec.getURL()
            specObj.sourceurl=spec.getSourceURL()
            for specPkg in specObj.listPackages:
                if specPkg in self.mapPackageToSpec:
                    existingObj = self.mapSerializableSpecObjects[self.mapPackageToSpec[specPkg]]
                    if self.compareVersions(existingObj,specObj) == 1:
                        skipUpdating = True
                        break;
                specObj.installRequiresPackages[specPkg]=spec.getRequires(specPkg)
                self.mapPackageToSpec[specPkg]=specName
                if spec.getIsRPMPackage(specPkg):
                    specObj.listRPMPackages.append(specPkg)
            if skipUpdating == False:
                self.mapSerializableSpecObjects[specName]=specObj

    def getListSpecFiles(self,listSpecFiles,path):
        for dirEntry in os.listdir(path):
            dirEntryPath = os.path.join(path, dirEntry)
            if os.path.isfile(dirEntryPath) and dirEntryPath.endswith(".spec"):
                listSpecFiles.append(dirEntryPath)
            elif os.path.isdir(dirEntryPath):
                self.getListSpecFiles(listSpecFiles,dirEntryPath)

    def getBuildRequiresForPackage(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].buildRequirePackages

    def getRequiresAllForPackage(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].installRequiresAllPackages

    def getRequiresForPackage(self, package):
        specName=self.getSpecName(package)
        if package in self.mapSerializableSpecObjects[specName].installRequiresPackages:
            return self.mapSerializableSpecObjects[specName].installRequiresPackages[package]
        return None

    def addMacro(self, macroName, macroValue):
        if macroName == "":
            self.logger.error("Given invalid macro: name:"+macroName+" value:"+macroValue)
            return
        self.userDefinedMacros[macroName]=macroValue

    def getRPMMacros(self):
        return self.userDefinedMacros

    def processData(self, package, data):
        #User macros
        for macroName in self.userDefinedMacros.keys():
            value = self.userDefinedMacros[macroName]
            macro="%{?"+macroName+"}"
            if data.find(macro) != -1:
                data = data.replace(macro,value)
                continue
            macro="%{"+macroName+"}"
            if data.find(macro) != -1:
                data = data.replace(macro,value)
                continue
            macro="%"+macroName
            if data.find(macro) != -1:
                data = data.replace(macro,value)
        #Spec definitions
        specName=self.getSpecName(package)
        specDefs =  self.mapSerializableSpecObjects[specName].specDefs
        for macroName in specDefs.keys():
            value = specDefs[macroName]
            macro="%{?"+macroName+"}"
            if data.find(macro) != -1:
                data = data.replace(macro,value)
                continue
            macro="%{"+macroName+"}"
            if data.find(macro) != -1:
                data = data.replace(macro,value)
                continue
            macro="%"+macroName
            if data.find(macro) != -1:
                data = data.replace(macro,value)
        return data

    def getRelease(self, package):
        specName=self.getSpecName(package)
        return self.processData(package, self.mapSerializableSpecObjects[specName].release)

    def getVersion(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].version

    def getSpecFile(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].specFile

    def getPatches(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listPatches

    def getSources(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listSources

    def getSHA1(self, package, source):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].checksums.get(source)

    def getPackages(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listPackages

    def getRPMPackages(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listRPMPackages

    def getReleaseNum(self, releaseVal):
        id = releaseVal.find("%")
        if (id != -1):
            return releaseVal[0:id]
        else:
            return releaseVal

    def compareVersions(self, existingObj, newObject):
        if StrictVersion(existingObj.version) > StrictVersion(newObject.version):
            return 1;
        elif StrictVersion(existingObj.version) < StrictVersion(newObject.version):
            return -1
        else:
            if int(self.getReleaseNum(existingObj.release)) > int(self.getReleaseNum(newObject.release)):
                return 1;
            else:
                return -1;

    def getSpecName(self,package):
        if package in self.mapPackageToSpec:
            specName=self.mapPackageToSpec[package]
            if specName in self.mapSerializableSpecObjects:
                return specName
        self.logger.error("Could not able to find "+package+" package from specs")
        raise Exception("Invalid package:"+package)

    def isRPMPackage(self,package):
        if package in self.mapPackageToSpec:
            specName=self.mapPackageToSpec[package]
            if specName in self.mapSerializableSpecObjects:
                return True
        return False

    def getSecurityHardeningOption(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].securityHardening

    def isCheckAvailable(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].isCheckAvailable

    def getListPackages(self):
        return self.mapSerializableSpecObjects.keys()

    def getURL(self, package):
        specName=self.getSpecName(package)
        url = self.mapSerializableSpecObjects[specName].url
        if url is None:
            return None
        return self.processData(package, url)

    def getSourceURL(self, package):
        specName=self.getSpecName(package)
        sourceurl = self.mapSerializableSpecObjects[specName].sourceurl
        if sourceurl is None:
            return None
        return self.processData(package, sourceurl)

    def getLicense(self, package):
        specName=self.getSpecName(package)
        license = self.mapSerializableSpecObjects[specName].license
        if license is None:
            return None
        return self.processData(package, license)

    def printAllObjects(self):
        listSpecs=self.mapSerializableSpecObjects.keys()
        for spec in listSpecs:
            specObj=self.mapSerializableSpecObjects[spec]
            self.logger.info("-----------Spec:"+specObj.name+"--------------")
            self.logger.info("Version:"+specObj.version)
            self.logger.info("Release:"+specObj.release)
            self.logger.info("SpecFile:"+specObj.specFile)
            self.logger.info(" ")
            self.logger.info("Source Files")
            self.logger.info(specObj.listSources)
            self.logger.info(" ")
            self.logger.info("Patch Files")
            self.logger.info(specObj.listPatches)
            self.logger.info(" ")
            self.logger.info(" ")
            self.logger.info("List RPM packages")
            self.logger.info(specObj.listPackages)
            self.logger.info(" ")
            self.logger.info(" ")
            self.logger.info("Build require packages")
            self.logger.info(specObj.buildRequirePackages)
            self.logger.info(" ")
            self.logger.info(" ")
            self.logger.info("install require packages")
            self.logger.info(specObj.installRequiresAllPackages)
            self.logger.info(" ")
            self.logger.info(specObj.installRequiresPackages)
            self.logger.info("security_hardening: " + specObj.securityHardening)
            self.logger.info("------------------------------------------------")

