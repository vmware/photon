import os
import platform
import queue
import json
import operator
from distutils.version import StrictVersion
from SpecUtils import Specutils
from Logger import Logger
from constants import constants



class SerializableSpecObject(object):
    def __init__(self):
        self.listPackages = []
        self.listRPMPackages = []
        self.name = ""
        self.version = ""
        self.release = ""
        self.buildRequirePackages = []
        self.checkBuildRequirePackages = []
        self.installRequiresAllPackages = []
        self.installRequiresPackages = {}
        self.specFile = ""
        self.listSources = []
        self.checksums = {}
        self.listPatches = []
        self.securityHardening = ""
        self.url = ""
        self.sourceurl = ""
        self.license = ""
        self.specDefs = {}


class SerializableSpecObjectsUtils(object):

    def __init__(self, logPath):
        self.mapSerializableSpecObjects = {}
        self.mapPackageToSpec = {}
        self.logger = Logger.getLogger("Serializable Spec objects", logPath)

    def readSpecsAndConvertToSerializableObjects(self, specFilesPath):
        listSpecFiles = []
        self.getListSpecFiles(listSpecFiles, specFilesPath)
        for specFile in listSpecFiles:
            skipUpdating = False
            spec = Specutils(specFile)
            specName = spec.getBasePackageName()
            specObj = SerializableSpecObject()
            specObj.name = specName
            specObj.buildRequirePackages = spec.getBuildRequiresAllPackages()
            specObj.installRequiresAllPackages = spec.getRequiresAllPackages()
            specObj.checkBuildRequirePackages = spec.getCheckBuildRequiresAllPackages()
            specObj.listPackages = spec.getPackageNames()
            specObj.specFile = specFile
            specObj.version = spec.getVersion()
            specObj.release = spec.getRelease()
            specObj.listSources = spec.getSourceNames()
            specObj.checksums = spec.getChecksums()
            specObj.specDefs = spec.getDefinitions()
            specObj.listPatches = spec.getPatchNames()
            specObj.securityHardening = spec.getSecurityHardeningOption()
            specObj.isCheckAvailable = spec.isCheckAvailable()
            specObj.license = spec.getLicense()
            specObj.url = spec.getURL()
            specObj.sourceurl = spec.getSourceURL()
            for specPkg in specObj.listPackages:
                if specPkg in self.mapPackageToSpec:
                    existingObj = self.mapSerializableSpecObjects[self.mapPackageToSpec[specPkg]]
                    if self.compareVersions(existingObj, specObj) == 1:
                        skipUpdating = True
                        break
                specObj.installRequiresPackages[specPkg] = spec.getRequires(specPkg)
                self.mapPackageToSpec[specPkg] = specName
                if spec.getIsRPMPackage(specPkg):
                    specObj.listRPMPackages.append(specPkg)
            if not skipUpdating:
                self.mapSerializableSpecObjects[specName] = specObj

    def getListSpecFiles(self, listSpecFiles, path):
        for dirEntry in os.listdir(path):
            dirEntryPath = os.path.join(path, dirEntry)
            if (os.path.isfile(dirEntryPath) and
                    dirEntryPath.endswith(".spec") and
                    os.path.basename(dirEntryPath) not in
                    constants.skipSpecsForArch.get(platform.machine(), [])):
                listSpecFiles.append(dirEntryPath)
            elif os.path.isdir(dirEntryPath):
                self.getListSpecFiles(listSpecFiles, dirEntryPath)

    def getBuildRequiresForPackage(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].buildRequirePackages

    def getRequiresAllForPackage(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].installRequiresAllPackages

    def getRequiresForPackage(self, package):
        specName = self.getSpecName(package)
        if package in self.mapSerializableSpecObjects[specName].installRequiresPackages:
            return self.mapSerializableSpecObjects[specName].installRequiresPackages[package]
        return None

    def getCheckBuildRequiresForPackage(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].checkBuildRequirePackages

    def getRelease(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].release

    def getVersion(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].version

    def getSpecFile(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].specFile

    def getPatches(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listPatches

    def getSources(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listSources

    def getSHA1(self, package, source):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].checksums.get(source)

    def getPackages(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listPackages

    def getRPMPackages(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listRPMPackages

    @staticmethod
    def getReleaseNum(releaseVal):
        releaseNum = releaseVal.find("%")
        if releaseNum != -1:
            return releaseVal[0:releaseNum]
        else:
            return releaseVal

    def compareVersions(self, existingObj, newObject):
        if StrictVersion(existingObj.version) > StrictVersion(newObject.version):
            return 1
        elif StrictVersion(existingObj.version) < StrictVersion(newObject.version):
            return -1
        else:
            if (int(self.getReleaseNum(existingObj.release)) >
                    int(self.getReleaseNum(newObject.release))):
                return 1
            else:
                return -1

    def getSpecName(self, package):
        if package in self.mapPackageToSpec:
            specName = self.mapPackageToSpec[package]
            if specName in self.mapSerializableSpecObjects:
                return specName
        self.logger.error("Could not able to find " + package + " package from specs")
        raise Exception("Invalid package:" + package)

    def isRPMPackage(self, package):
        if package in self.mapPackageToSpec:
            specName = self.mapPackageToSpec[package]
            if specName in self.mapSerializableSpecObjects:
                return True
        return False

    def getSecurityHardeningOption(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].securityHardening

    def isCheckAvailable(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].isCheckAvailable

    def getListPackages(self):
        return list(self.mapSerializableSpecObjects.keys())

    def getURL(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].url

    def getSourceURL(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].sourceurl

    def getLicense(self, package):
        specName = self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].license

    def printAllObjects(self):
        listSpecs = self.mapSerializableSpecObjects.keys()
        for spec in listSpecs:
            specObj = self.mapSerializableSpecObjects[spec]
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


class SPECS(object):
    __instance = None
    specData = None

    @staticmethod
    def getData():
        """ Static access method. """
        if SPECS.__instance is None:
            SPECS()
        return SPECS.__instance.specData

    def __init__(self):
        """ Virtually private constructor. """
        if SPECS.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SPECS.__instance = self
        self.initialize()

    def initialize(self):
        # Preparse some files
        # adding openjre8 version rpm macro
        if platform.machine() == "x86_64":
            spec = Specutils(constants.specPath + "/openjdk8/openjdk8.spec")
        else:
            spec = Specutils(constants.specPath + "/openjdk8/openjdk8_aarch64.spec")
        java8version = spec.getVersion()
        constants.addMacro("JAVA8_VERSION", java8version)

        # adding kernelversion rpm macro
        spec = Specutils(constants.specPath + "/linux/linux.spec")
        kernelversion = spec.getVersion()
        constants.addMacro("KERNEL_VERSION", kernelversion)

        # adding kernelrelease rpm macro
        kernelrelease = spec.getRelease()
        constants.addMacro("KERNEL_RELEASE", kernelrelease)

        # adding kernelsubrelease rpm macro
        a, b, c = kernelversion.split(".")
        kernelsubrelease = ('%02d%02d%03d%03d' % (int(a),
                                                  int(b), int(c),
                                                  int(kernelrelease.split('.')[0])))
        if kernelsubrelease:
            kernelsubrelease = "." + kernelsubrelease
            constants.addMacro("kernelsubrelease", kernelsubrelease)

        # Full parsing
        self.specData = SerializableSpecObjectsUtils(constants.logPath)
        self.specData.readSpecsAndConvertToSerializableObjects(constants.specPath)


class SpecDependencyGenerator(object):

    def findTotalRequires(self, mapDependencies, depQue, parent):
        while not depQue.empty():
            specPkg = depQue.get()
            try:
                listRequiredPackages = SPECS.getData().getRequiresForPackage(specPkg)
            except Exception as e:
                print("Caught Exception:"+str(e))
                print(specPkg + " is missing")

            for depPkg in listRequiredPackages:
                if depPkg in mapDependencies:
                    if mapDependencies[depPkg] < mapDependencies[specPkg] + 1:
                        mapDependencies[depPkg] = mapDependencies[specPkg] + 1
                        parent[depPkg] = specPkg
                        self.updateLevels(mapDependencies, depPkg, parent, mapDependencies[depPkg])
                else:
                    mapDependencies[depPkg] = mapDependencies[specPkg] + 1
                    parent[depPkg] = specPkg
                    depQue.put(depPkg)

    def findTotalWhoNeedsToBuild(self, depQue, whoNeedsBuild):
        while not depQue.empty():
            specPkg = depQue.get()
            listPackagesRequiredToBuild = SPECS.getData().getBuildRequiresForPackage(specPkg)
            for depPkg in listPackagesRequiredToBuild:
                depSpecPkg = SPECS.getData().getSpecName(depPkg)
                if depSpecPkg not in whoNeedsBuild:
                    whoNeedsBuild.append(depSpecPkg)
                    depQue.put(depSpecPkg)

    def printTree(self, children, curParent, depth):
        if curParent in children:
            for child in children[curParent]:
                print ("\t" * depth + child)
                self.printTree(children, child, depth + 1)

    def getAllPackageNames(self, jsonFilePath):
        jsonData = open(jsonFilePath)
        option_list_json = json.load(jsonData)
        jsonData.close()
        packages = option_list_json["packages"]
        return packages

    def updateLevels(self, mapDependencies, inPkg, parent, level):
        listPackages = SPECS.getData().getPackages(inPkg)
        for depPkg in SPECS.getData().getRequiresForPackage(inPkg):
            if depPkg in listPackages:
                continue
            if depPkg in mapDependencies and mapDependencies[depPkg] < level + 1:
                mapDependencies[depPkg] = level + 1
                parent[depPkg] = inPkg
                self.updateLevels(mapDependencies, depPkg, parent, mapDependencies[depPkg])

    def calculateSpecDependency(self, inputPackages, mapDependencies, parent):
        depQue = queue.Queue()
        for pkg in inputPackages:
            if SPECS.getData().isRPMPackage(pkg):
                if pkg not in mapDependencies:
                    mapDependencies[pkg] = 0
                    parent[pkg] = ""
                    depQue.put(pkg)
                    self.findTotalRequires(mapDependencies, depQue, parent)
            else:
                print("Could not find spec for "+pkg)

    def displayDependencies(self, displayOption, inputType, inputValue, allDeps, parent):
        children = {}
        sortedList = []
        for elem in sorted(allDeps.items(), key=operator.itemgetter(1), reverse=True):
            sortedList.append(elem[0])
        # construct all children nodes
        if displayOption == "tree":
            for k, v in parent.iteritems():
                children.setdefault(v, []).append(k)
            if inputType == "json":
                print("Dependency Mappings for {}".format(inputValue) + " :")
                print("-" * 52 + " {}".format(children))
                print("-" * 52)
            if "" in children:
                for child in children[""]:
                    print(child)
                    self.printTree(children, child, 1)
                print("*" * 18 + " {} ".format(len(sortedList)) +
                      "packages in total " + "*" * 18)
            else:
                if inputType == "pkg" and len(children) > 0:
                    print ("cyclic dependency detected, mappings: \n", children)

        # To display a flat list of all packages
        elif displayOption == "list":
            print (sortedList)

        # To generate a new JSON file based on given input json file
        elif displayOption == "json" and inputType == "json":
            d = {'packages': sortedList}
            with open(inputValue, 'w') as outfile:
                json.dump(d, outfile)

        return sortedList

    def process(self, inputType, inputValue, displayOption, outputFile=None):
        whoNeedsList = []
        inputPackages = []
        whoNeedsBuild = []
        mapDependencies = {}
        parent = {}
        if inputType == "pkg" or inputType == "json":
            if inputType == "pkg":
                inputPackages.append(inputValue)
            else:
                inputPackages = self.getAllPackageNames(inputValue)

            self.calculateSpecDependency(inputPackages, mapDependencies, parent)
            if outputFile is not None:
                return self.displayDependencies(displayOption, inputType, outputFile, mapDependencies, parent)
            else:
                return self.displayDependencies(displayOption, inputType, inputValue, mapDependencies, parent)
        elif inputType == "who-needs":
            for depPkg in SPECS.getData().mapPackageToSpec:
                if inputValue in SPECS.getData().getRequiresForPackage(depPkg):
                    whoNeedsList.append(depPkg)
            print (whoNeedsList)
            return whoNeedsList
        elif inputType == "who-needs-build":
            depQue = queue.Queue()
            depQue.put(inputValue)
            self.findTotalWhoNeedsToBuild(depQue, whoNeedsBuild)
            print ("Following specs need to be build again")
            print (whoNeedsBuild)
            return whoNeedsBuild
