from SpecUtils import Specutils
import os
from Logger import Logger

class SerializableSpecObject(object):
    def __init__(self):
        self.listPackages=[]
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

class SerializableSpecObjectsUtils(object):
    
    def __init__(self,logPath):
        self.mapSerializableSpecObjects={}
        self.mapPackageToSpec={}
        self.logger=Logger.getLogger("Serializable Spec objects", logPath )
    
    def readSpecsAndConvertToSerializableObjects(self,specFilesPath):
        listSpecFiles=[]
        self.getListSpecFiles(listSpecFiles,specFilesPath)
        for specFile in listSpecFiles:
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
            specObj.listPatches=spec.getPatchNames()
            specObj.securityHardening=spec.getSecurityHardeningOption()
            for specPkg in specObj.listPackages:
                specObj.installRequiresPackages[specPkg]=spec.getRequires(specPkg)
                self.mapPackageToSpec[specPkg]=specName
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
        if self.mapSerializableSpecObjects[specName].installRequiresPackages.has_key(package):
            return self.mapSerializableSpecObjects[specName].installRequiresPackages[package]
        return None
    
    def getRelease(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].release
        
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
        
    def getSpecName(self,package):
        if self.mapPackageToSpec.has_key(package):
            specName=self.mapPackageToSpec[package]
            if self.mapSerializableSpecObjects.has_key(specName):
                return specName
        self.logger.error("Could not able to find "+package+" package from specs")
        raise Exception("Invalid package:"+package)
    
    def isRPMPackage(self,package):
        if self.mapPackageToSpec.has_key(package):
            specName=self.mapPackageToSpec[package]
            if self.mapSerializableSpecObjects.has_key(specName):
                return True
        return False
    
    def getSecurityHardeningOption(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].securityHardening

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

