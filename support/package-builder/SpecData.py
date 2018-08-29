import os
import platform
import queue
import json
import operator
from distutils.version import StrictVersion
from SpecUtils import Specutils
from Logger import Logger
from constants import constants



class SpecObject(object):
    def __init__(self):
        self.listPackages = []
        self.listRPMPackages = []
        self.name = ""
        self.version = ""
        self.release = ""
        self.buildarch = {}
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


class SpecObjectsUtils(object):

    def __init__(self, logPath):
        self.mapSpecObjects = {}
        self.mapPackageToSpec = {}
        self.logger = Logger.getLogger("Serializable Spec objects", logPath)

    def readSpecsAndConvertToSerializableObjects(self, specFilesPath):
        listSpecFiles = []
        self.getListSpecFiles(listSpecFiles, specFilesPath)
        for specFile in listSpecFiles:
            spec = Specutils(specFile)
            specName = spec.getBasePackageName()
            specObj = SpecObject()
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
                specObj.installRequiresPackages[specPkg] = spec.getRequires(specPkg)
                specObj.buildarch[specPkg] = spec.getBuildArch(specPkg)
                self.mapPackageToSpec[specPkg] = specName
                if spec.getIsRPMPackage(specPkg):
                    specObj.listRPMPackages.append(specPkg)
            if specName in self.mapSpecObjects:
                self.mapSpecObjects[specName].append(specObj)
            else:
                self.mapSpecObjects[specName]=[specObj]
        for key, value in self.mapSpecObjects.items():
            if len(value) > 1:
                self.mapSpecObjects[key] = sorted(value,
                                                  key=lambda x : self.compareVersions(x),
                                                  reverse=True)

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

    def getBuildRequiresForPackage(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].buildRequirePackages

    def getRequiresAllForPackage(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].installRequiresAllPackages

    def getRequiresForPackage(self, package, index=0):
        specName = self.getSpecName(package)
        if package in self.mapSpecObjects[specName][index].installRequiresPackages:
            return self.mapSpecObjects[specName][index].installRequiresPackages[package]
        return None

    def getCheckBuildRequiresForPackage(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].checkBuildRequirePackages

    def getSpecObj(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName]

    def getPkgNamesFromObj(self, objlist):
        listPkgName=[]
        listPkgNames=list(set(objlist))
        for name in listPkgNames:
                listPkgName.append(name.package)
        listPkgName=list(set(listPkgName))
        return listPkgName

    def getRelease(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].release

    def getVersion(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].version

    def getBuildArch(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].buildarch[package]

    def getSpecFile(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].specFile

    def getPatches(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].listPatches

    def getSources(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].listSources

    def getSHA1(self, package, source, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].checksums.get(source)

    def getPackages(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].listPackages

    def getRPMPackages(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].listRPMPackages

    @staticmethod
    def compareVersions(p):
        return (StrictVersion(p.version))

    def getSpecName(self, package):
        if package in self.mapPackageToSpec:
            specName = self.mapPackageToSpec[package]
            if specName in self.mapSpecObjects:
                return specName
        self.logger.error("Could not able to find " + package + " package from specs")
        raise Exception("Invalid package:" + package)

    def isRPMPackage(self, package):
        if package in self.mapPackageToSpec:
            specName = self.mapPackageToSpec[package]
            if specName in self.mapSpecObjects:
                return True
        return False

    def getSecurityHardeningOption(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].securityHardening

    def isCheckAvailable(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].isCheckAvailable

    def getListPackages(self):
        return list(self.mapSpecObjects.keys())

    def getURL(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].url

    def getSourceURL(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].sourceurl

    def getLicense(self, package, index=0):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][index].license

    def getNumberOfVersions(self, package):
        specName=self.getSpecName(package)
        return len(self.mapSpecObjects[specName])

    def printAllObjects(self):
        listSpecs = self.mapSpecObjects.keys()
        for spec in listSpecs:
            specObj = self.mapSpecObjects[spec]
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
            self.logger.info(self.getPkgNamesFromObj(specObj.buildRequirePackages))
            self.logger.info(" ")
            self.logger.info(" ")
            self.logger.info("install require packages")
            self.logger.info(self.getPkgNamesFromObj(specObj.installRequiresAllPackages))
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

        # adding openjre9 version rpm macro
        if platform.machine() == "x86_64":
            spec = Specutils(constants.specPath + "/openjdk9/openjdk9.spec")
            java9version = spec.getVersion()
            constants.addMacro("JAVA9_VERSION", java9version)


        # adding openjre10 version rpm macro
        if platform.machine() == "x86_64":
            spec = Specutils(constants.specPath + "/openjdk10/openjdk10.spec")
            java10version = spec.getVersion()
            constants.addMacro("JAVA10_VERSION", java10version)

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
        self.specData = SpecObjectsUtils(constants.logPath)
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
        with open(jsonFilePath) as jsonData:
            option_list_json = json.load(jsonData)
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
