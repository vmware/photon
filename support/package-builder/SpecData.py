#!/usr/bion/env python3

import os
import re

from Logger import Logger
from constants import constants
from StringUtils import StringUtils
from distutilsversion import StrictVersion
from distutilsversion import LooseVersion
from SpecParser import SpecParser


class SpecData(object):
    def __init__(self, arch, logPath, specFilesPaths, dist):
        self.arch = arch
        self.dist = dist
        self.logger = Logger.getLogger("SpecData", logPath, constants.logLevel)

        # map default package name to list of SpecObjects. Usually it is just
        # a list with only one element. But, for multiversion spec file this
        # list has as many elements as many versions of given package name
        # are available
        self.mapSpecObjects = {}

        # map subpackage names to default package name
        self.mapPackageToSpec = {}

        # map spec file name to SpecObject
        self.mapSpecFileNameToSpecObj = {}

        self._readSpecs(specFilesPaths)

    # Read all .spec files from the given folder including subfolders,
    # creates corresponding SpecObjects and put them in internal mappings.
    def _readSpecs(self, specFilesPaths):
        for specFile in self._getListSpecFiles(specFilesPaths):
            spec = SpecParser(specFile, self.arch, self.dist)

            # skip the specfile if buildarch differs
            buildarch = spec.packages.get("default").buildarch
            if buildarch not in {"noarch", self.arch}:
                self.logger.debug(f"Skipping spec file: {specFile}")
                continue

            specObj = spec.createSpecObject()

            name = specObj.name
            for specPkg in specObj.listPackages:
                self.mapPackageToSpec[specPkg] = name

            if name not in self.mapSpecObjects:
                self.mapSpecObjects[name] = [specObj]
            else:
                self.mapSpecObjects[name].append(specObj)

            self.mapSpecFileNameToSpecObj[os.path.basename(specFile)] = specObj

        # Sort the multiversion list to make getHighestVersion happy
        for key, value in self.mapSpecObjects.items():
            if len(value) > 1:
                self.mapSpecObjects[key] = sorted(
                    value, key=lambda x: self.compareVersions(x), reverse=True
                )

    def _getListSpecFiles(self, paths):
        listSpecFiles = []
        for path in paths:
            for dirEntry in os.listdir(path):
                dirEntryPath = os.path.join(path, dirEntry)
                if os.path.isfile(dirEntryPath) and dirEntryPath.endswith(".spec"):
                    listSpecFiles.append(dirEntryPath)
                elif os.path.isdir(dirEntryPath):
                    listSpecFiles.extend(self._getListSpecFiles([dirEntryPath]))
        return listSpecFiles

    def _getProperVersion(self, depPkg):
        if not depPkg.compare:
            return self.getHighestVersion(depPkg.package)
        specObjs = self.getSpecObjects(depPkg.package)
        try:
            for obj in specObjs:
                verrel = obj.version
                if depPkg.compare == ">=":
                    if LooseVersion(verrel) >= LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == "<=":
                    if LooseVersion(verrel) <= LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == "=":
                    if LooseVersion(verrel) == LooseVersion(depPkg.version):
                        return obj.version
                    x = obj.version.rsplit("-", 1)[0]
                    y = depPkg.version.rsplit("-", 1)[0]
                    if LooseVersion(x) == LooseVersion(y):
                        return obj.version
                elif depPkg.compare == "<":
                    if LooseVersion(verrel) < LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == ">":
                    if LooseVersion(verrel) > LooseVersion(depPkg.version):
                        return obj.version
        except Exception as e:
            self.logger.error(
                "Exception happened while searching for: "
                + depPkg.package
                + depPkg.compare
                + depPkg.version
            )
            raise e

        # about to throw exception
        availableVersions = []
        for obj in specObjs:
            availableVersions.append(f"{obj.name}-{obj.version}")
        raise Exception("Could not find package: "
                        f"{depPkg.package}{depPkg.compare}{depPkg.version}"
                        " available specs: " + " ".join(availableVersions))

    def _getSpecObjField(self, package, version, field):
        for specObj in self.getSpecObjects(package):
            if specObj.version == version:
                return field(specObj)
        self.logger.error(
            "Could not find " + package + "-" + version + " package from specs"
        )
        raise Exception("Invalid package: " + package + "-" + version)

    def getBuildRequiresForPackage(self, package, version):
        buildRequiresList = []
        for pkg in self._getSpecObjField(
            package, version, field=lambda x: x.buildRequires
        ):
            properVersion = self._getProperVersion(pkg)
            buildRequiresList.append(pkg.package + "-" + properVersion)
        return buildRequiresList

    def getExtraBuildRequiresForPackage(self, package, version):
        packages = []
        for pkg in self._getSpecObjField(
            package, version, field=lambda x: x.extraBuildRequires
        ):
            # no version deps for publishrpms - use just name
            packages.append(pkg.package)
        return packages

    def getBuildRequiresNativeForPackage(self, package, version):
        packages = []
        for pkg in self._getSpecObjField(
            package, version, field=lambda x: x.buildRequiresNative
        ):
            properVersion = self._getProperVersion(pkg)
            packages.append(pkg.package + "-" + properVersion)
        return packages

    def getBuildRequiresForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getBuildRequiresForPackage(package, version)

    # Returns list of [ "pkg1-vers1", "pkg2-vers2",.. ]
    def getRequiresAllForPackage(self, package, version):
        requiresList = []
        for pkg in self._getSpecObjField(
            package, version, field=lambda x: x.installRequires
        ):
            properVersion = self._getProperVersion(pkg)
            requiresList.append(pkg.package + "-" + properVersion)
        return requiresList

    def getRequiresAllForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getRequiresAllForPackage(package, version)

    """
    Get BuildRequires and Requires + all their Requires trees
    Basically list of all subpackages needed to be installed in
    order to build pkg
    """

    def getRequiresTreeForPkg(self, pkg):
        requires = self.getBuildRequiresForPkg(pkg) + self.getRequiresForPkg(
            pkg
        )
        for p in requires:
            for pc in SPECS.getData().getRequiresForPkg(p):
                if pc not in requires:
                    requires.append(pc)
        return requires

    """
    Similar to getRequiresTreeForPkg, but returns smaller list containing
    only base packages
    Can be used to track whether pkg build can be started.
    """

    def getRequiresTreeOfBasePkgsForPkg(self, pkg):
        result = []
        requires = self.getRequiresTreeForPkg(pkg)
        for p in requires:
            bp = self.getBasePkg(p)
            if bp not in result and bp != pkg:
                result.append(bp)
        return result

    def getRequiresForPackage(self, package, version):
        requiresList = []
        for specObj in self.getSpecObjects(package):
            if specObj.version == version:
                if package in specObj.installRequiresPackages:
                    requiresPackages = specObj.installRequiresPackages[package]
                    for pkg in requiresPackages:
                        properVersion = self._getProperVersion(pkg)
                        requiresList.append(pkg.package + "-" + properVersion)
                return requiresList
        self.logger.error(
            "Could not find " + package + "-" + version + " package from specs"
        )
        raise Exception("Invalid package: " + package + "-" + version)

    def getRequiresForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getRequiresForPackage(package, version)

    def getCheckBuildRequiresForPackage(self, package, version):
        checkBuildRequiresList = []
        checkBuildRequiresPackages = self._getSpecObjField(
            package, version, field=lambda x: x.checkBuildRequires
        )
        for pkg in checkBuildRequiresPackages:
            properVersion = self._getProperVersion(pkg)
            checkBuildRequiresList.append(pkg.package + "-" + properVersion)
        return checkBuildRequiresList

    # Returns list of SpecObjects for given subpackage name
    def getSpecObjects(self, package):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName]

    def getPkgNamesFromObj(self, objlist):
        listPkgName = []
        for name in objlist:
            listPkgName.append(name.package)
        return listPkgName

    def getRelease(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.release
        )

    def getVersions(self, package):
        versions = []
        for specObj in self.getSpecObjects(package):
            versions.append(specObj.version)
        return versions

    def getHighestVersion(self, package):
        return self.getSpecObjects(package)[0].version

    def getBuildArch(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.buildarch[package]
        )

    def getSpecFile(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.specFile
        )

    def getPatches(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.listPatches
        )

    def getSources(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.listSources
        )

    def getChecksum(self, package, version, source):
        return self._getSpecObjField(
            package, version, field=lambda x: x.checksums.get(source)
        )

    # returns list of package names (no versions)
    def getPackages(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.listPackages
        )

    def getPackagesForPkg(self, pkg):
        pkgs = []
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        for p in self.getPackages(package, version):
            pkgs.append(p + "-" + version)
        return pkgs

    def getRPMPackages(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.listRPMPackages
        )

    @staticmethod
    def compareVersions(p):
        return LooseVersion(p.version)

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
            return specName in self.mapSpecObjects
        return False

    def getSecurityHardeningOption(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.securityHardening
        )

    def isNetworkRequired(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.networkRequired)

    def isCheckAvailable(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.isCheckAvailable
        )

    def getListPackages(self):
        return list(self.mapSpecObjects.keys())

    def getURL(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.url)

    def getSourceURL(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.sourceurl
        )

    def getLicense(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.license
        )

    def getSummary(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.summary)

    def getDescription(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.descriptions[package])

    # Converts "glibc-devel-2.28" into "glibc-2.28"
    def getBasePkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getSpecName(package) + "-" + version

    def printAllObjects(self):
        listSpecs = self.mapSpecObjects.keys()
        for spec in listSpecs:
            for specObj in self.mapSpecObjects[spec]:
                self.logger.debug(
                    f"-----------Spec: {specObj.name} --------------"
                )
                self.logger.debug(f"Version: {specObj.version}")
                self.logger.debug(f"Release: {specObj.release}")
                self.logger.debug(f"SpecFile: {specObj.specFile}")
                self.logger.debug("Source Files")
                self.logger.debug(specObj.listSources)
                self.logger.debug("Patch Files")
                self.logger.debug(specObj.listPatches)
                self.logger.debug("List RPM packages")
                self.logger.debug(specObj.listPackages)
                self.logger.debug("Build require packages")
                self.logger.debug(
                    self.getPkgNamesFromObj(specObj.buildRequires)
                )
                self.logger.debug("install require packages")
                self.logger.debug(
                    self.getPkgNamesFromObj(specObj.installRequires)
                )
                self.logger.debug(specObj.installRequiresPackages)
                self.logger.debug(
                    f"security_hardening: {specObj.securityHardening}"
                )
                self.logger.debug(f"BuildArch: {specObj.buildarch}")
                self.logger.debug(
                    "------------------------------------------------"
                )


class SPECS(object):
    __instance = None
    specData = {}

    @staticmethod
    def getData(arch=None):
        if not arch:
            arch = constants.currentArch

        """ Static access method. """
        if SPECS.__instance is None:
            SPECS()
        return SPECS.__instance.specData[arch]

    def __init__(self):
        """Virtually private constructor."""
        if SPECS.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SPECS.__instance = self
        self.initialize()

    def initialize(self):
        # Full parsing
        dist = constants.dist[1:]
        self.specData[constants.buildArch] = SpecData(
            constants.buildArch, constants.logPath, constants.specPaths, dist
        )

        if constants.buildArch != constants.targetArch:
            self.specData[constants.targetArch] = SpecData(
                constants.targetArch, constants.logPath, constants.specPaths, dist
            )
