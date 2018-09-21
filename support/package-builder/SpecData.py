import os
import platform
import queue
import json
import operator
from distutils.version import StrictVersion
from SpecUtils import Specutils
from Logger import Logger
from constants import constants
from StringUtils import StringUtils
from distutils.version import LooseVersion


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
                # TODO add multiversioning support
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

    def _getProperVersion(self,depPkg):
        if (depPkg.compare == ""):
            return self.getHighestVersion(depPkg.package)
        specObjs=self.getSpecObj(depPkg.package)
        for obj in specObjs:
                verrel=obj.version+"-"+obj.release
                if depPkg.compare == ">=":
                       if LooseVersion(verrel) >= LooseVersion(depPkg.version):
                                return obj.version
                elif depPkg.compare == "<=":
                        if LooseVersion(verrel) <= LooseVersion(depPkg.version):
                                return obj.version
                elif depPkg.compare == "=":
                        if LooseVersion(verrel) == LooseVersion(depPkg.version):
                                return obj.version
                        if LooseVersion(obj.version) == LooseVersion(depPkg.version):
                                return obj.version
                elif depPkg.compare == "<":
                        if LooseVersion(verrel) < LooseVersion(depPkg.version):
                                return obj.version
                elif depPkg.compare == ">":
                        if LooseVersion(verrel) > LooseVersion(depPkg.version):
                                return obj.version

        # about to throw exception
        availableVersions=""
        for obj in specObjs:
            availableVersions+=" "+obj.name+"-"+obj.version+"-"+obj.release
        raise Exception("Can not find package: " + depPkg.package + depPkg.compare + depPkg.version + " available specs:"+availableVersions)

    def _getSpecObjField(self, package, version, field):
        specName = self.getSpecName(package)
        for specObj in self.mapSpecObjects[specName]:
            if specObj.version == version:
                return field(specObj)
        self.logger.error("Could not able to find " + package +
                          "-" + version + " package from specs")
        raise Exception("Invalid package: " + package + "-" + version)

    def getBuildRequiresForPackage(self, package, version):
        buildRequiresList=[]
        buildRequiresPackages = self._getSpecObjField(package, version, field=lambda x : x.buildRequirePackages)
        for pkg in buildRequiresPackages:
            properVersion = self._getProperVersion(pkg)
            buildRequiresList.append(pkg.package+"-"+properVersion)
        return buildRequiresList

    def getBuildRequiresForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getBuildRequiresForPackage(package, version)

    def getBuildRequiresForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getBuildRequiresForPackage(package, version)

    # Returns list of [ "pkg1-vers1", "pkg2-vers2",.. ]
    def getRequiresAllForPackage(self, package, version):
        requiresList=[]
        requiresPackages = self._getSpecObjField(package, version, field=lambda x : x.installRequiresAllPackages)
        for pkg in requiresPackages:
            properVersion = self._getProperVersion(pkg)
            requiresList.append(pkg.package+"-"+properVersion)
        return requiresList

    def getRequiresAllForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getRequiresAllForPackage(package, version)

    def getRequiresForPackage(self, package, version):
        requiresList=[]
        specName = self.getSpecName(package)
        for specObj in self.mapSpecObjects[specName]:
            if specObj.version == version:
                if package in specObj.installRequiresPackages:
                    requiresPackages = specObj.installRequiresPackages[package]
                    for pkg in requiresPackages:
                        properVersion = self._getProperVersion(pkg)
                        requiresList.append(pkg.package+"-"+properVersion)
                return requiresList
        self.logger.error("Could not able to find " + package +
                          "-" + version + " package from specs")
        raise Exception("Invalid package: " + package + "-" + version)

    def getRequiresForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getRequiresForPackage(package, version)

    def getCheckBuildRequiresForPackage(self, package, version):
        checkBuildRequiresList=[]
        checkBuildRequiresPackages = self._getSpecObjField(package, version, field=lambda x : x.checkBuildRequirePackages)
        for pkg in checkBuildRequiresPackages:
            properVersion = self._getProperVersion(pkg)
            checkBuildRequiresList.append(pkg.package+"-"+properVersion)
        return checkBuildRequiresList

    def getSpecObj(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName]

    def getPkgNamesFromObj(self, objlist):
        listPkgName=[]
        for name in objlist:
                listPkgName.append(name.package)
        return listPkgName

    def getRelease(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.release)

    def getVersions(self, package):
        versions=[]
        specName = self.getSpecName(package)
        for specObj in self.mapSpecObjects[specName]:
            versions.append(specObj.version)
        return versions

    def getHighestVersion(self, package):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][0].version

    def getBuildArch(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.buildarch[package])

    def getSpecFile(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.specFile)

    def getPatches(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listPatches)

    def getSources(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listSources)

    def getSHA1(self, package, version, source):
        return self._getSpecObjField(package, version, field=lambda x : x.checksums.get(source))

    # returns list of package names (no versions)
    def getPackages(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listPackages)

    def getPackagesForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getPackages(package, version)

    def getRPMPackages(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listRPMPackages)

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

    def getSecurityHardeningOption(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.securityHardening)

    def isCheckAvailable(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.isCheckAvailable)

    def getListPackages(self):
        return list(self.mapSpecObjects.keys())

    def getURL(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.url)

    def getSourceURL(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.sourceurl)

    def getLicense(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.license)

    # Converts "glibc-devel-2.28" into "glibc-2.28"
    def getBasePkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getSpecName(package)+"-"+version


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
                listRequiredPackages = SPECS.getData().getRequiresForPkg(specPkg)
            except Exception as e:
                print("Caught Exception:"+str(e))
                print(specPkg + " is missing")
                raise e

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
            listPackagesRequiredToBuild = SPECS.getData().getBuildRequiresForPkg(specPkg)
            for depPkg in listPackagesRequiredToBuild:
                depSpecPkg = SPECS.getData().getBasePkg(depPkg)
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
        listPackages = SPECS.getData().getPackagesForPkg(inPkg)
        for depPkg in SPECS.getData().getRequiresForPkg(inPkg):
            package, version = StringUtils.splitPackageNameAndVersion(depPkg)
            if package in listPackages:
                continue
            if depPkg in mapDependencies and mapDependencies[depPkg] < level + 1:
                mapDependencies[depPkg] = level + 1
                parent[depPkg] = inPkg
                self.updateLevels(mapDependencies, depPkg, parent, mapDependencies[depPkg])

    def calculateSpecDependency(self, inputPackages, mapDependencies, parent):
        depQue = queue.Queue()
        for package in inputPackages:
            if SPECS.getData().isRPMPackage(package):
                for version in SPECS.getData().getVersions(package):
                    pkg = package+"-"+version
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
                pkg=inputValue+"-"+SPECS.getData().getHighestVersion(inputValue)
                if pkg in SPECS.getData().getRequiresForPkg(depPkg):
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
