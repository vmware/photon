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
        self.whoNeedsMe = []
        self.buildRequiresAllPackages = []
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
        self.skipMeForCurrArch = "true"


class SpecObjectsUtils(object):

    def __init__(self, logPath):
        self.mapSpecObjects = {}
        self.mapPackageToSpec = {}
        self.mapSpecFileNameToSpecObj = {}
        self.logger = Logger.getLogger("Serializable Spec objects", logPath, constants.logLevel)

    def readSpecsAndConvertToSerializableObjects(self, specFilesPath):
        listSpecFiles = []
        self.getListSpecFiles(listSpecFiles, specFilesPath)
        for specFile in listSpecFiles:
            spec = Specutils(specFile)
            specName = spec.getBasePackageName()
            specObj = SpecObject()
            specObj.name = specName
            specObj.buildRequiresAllPackages = spec.getBuildRequiresAllPackages()
            specObj.extraBuildRequires = spec.getExtraBuildRequires()
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
                if (specObj.buildarch[specPkg] == "noarch" or 
                    platform.machine() == specObj.buildarch[specPkg]):
                    specObj.skipMeForCurrArch = "false"
                    self.mapPackageToSpec[specPkg] = specName
                    if spec.getIsRPMPackage(specPkg):
                        specObj.listRPMPackages.append(specPkg)

            if specObj.skipMeForCurrArch == "false":
                if specName in self.mapSpecObjects:
                    self.mapSpecObjects[specName].append(specObj)
                else:
                    self.mapSpecObjects[specName]=[specObj]
                self.mapSpecFileNameToSpecObj[os.path.basename(specFile)]=specObj
        for key, value in self.mapSpecObjects.items():
            if len(value) > 1:
                self.mapSpecObjects[key] = sorted(value,
                                                  key=lambda x : self.compareVersions(x),
                                                  reverse=True)
        # To create the upward deps
        for specName in self.mapSpecObjects:
            for specObj in self.mapSpecObjects[specName]:
                for pkgRequired in specObj.buildRequiresAllPackages:
                    specRequired = self.mapPackageToSpec[pkgRequired.package]
                    if specRequired+".spec" in self.mapSpecFileNameToSpecObj:
                        specRequiredObj = self.mapSpecFileNameToSpecObj[specRequired+".spec"]
                        specRequiredObj.whoNeedsMe.append(specObj)

    def getListSpecFiles(self, listSpecFiles, path):
        for dirEntry in os.listdir(path):
            dirEntryPath = os.path.join(path, dirEntry)
            if (os.path.isfile(dirEntryPath) and
                    dirEntryPath.endswith(".spec")):
#                    os.path.basename(dirEntryPath) not in
#                    constants.skipSpecsForArch.get(platform.machine(), [])):
                listSpecFiles.append(dirEntryPath)
            elif os.path.isdir(dirEntryPath):
                self.getListSpecFiles(listSpecFiles, dirEntryPath)

    def _getProperVersion(self,depPkg):
        if (depPkg.compare == ""):
            return self.getHighestVersion(depPkg.package)
        specObjs=self.getSpecObj(depPkg.package)
        try:
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
        except Exception as e:
            self.logger.error("Exception happened while searching for: " + depPkg.package + depPkg.compare + depPkg.version)
            raise e

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
        for pkg in self._getSpecObjField(package, version, field=lambda x : x.buildRequiresAllPackages):
            properVersion = self._getProperVersion(pkg)
            buildRequiresList.append(pkg.package+"-"+properVersion)
        return buildRequiresList

    def getExtraBuildRequiresForPackage(self, package, version):
        packages=[]
        for pkg in self._getSpecObjField(package, version, field=lambda x : x.extraBuildRequires):
            # no version deps for publishrpms - use just name
            packages.append(pkg.package)
        return packages

    def getBuildRequiresForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getBuildRequiresForPackage(package, version)

    # Returns list of [ "pkg1-vers1", "pkg2-vers2",.. ]
    def getRequiresAllForPackage(self, package, version):
        requiresList=[]
        for pkg in self._getSpecObjField(package, version, field=lambda x : x.installRequiresAllPackages):
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
        pkgs=[]
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        for p in self.getPackages(package, version):
            pkgs.append(p+"-"+version)
        return pkgs

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
        self.logger.error("Could not find " + package + " package from specs")
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
            for specObj in self.mapSpecObjects[spec]:
                self.logger.debug("-----------Spec:"+specObj.name+"--------------")
                self.logger.debug("Version:"+specObj.version)
                self.logger.debug("Release:"+specObj.release)
                self.logger.debug("SpecFile:"+specObj.specFile)
                self.logger.debug("Source Files")
                self.logger.debug(specObj.listSources)
                self.logger.debug("Patch Files")
                self.logger.debug(specObj.listPatches)
                self.logger.debug("List RPM packages")
                self.logger.debug(specObj.listPackages)
                self.logger.debug("Build require packages")
                self.logger.debug(self.getPkgNamesFromObj(specObj.buildRequiresAllPackages))
                self.logger.debug("install require packages")
                self.logger.debug(self.getPkgNamesFromObj(specObj.installRequiresAllPackages))
                self.logger.debug(specObj.installRequiresPackages)
                self.logger.debug("security_hardening: " + specObj.securityHardening)
                self.logger.debug("------------------------------------------------")


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

