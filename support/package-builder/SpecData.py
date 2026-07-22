#!/usr/bin/env python3

import glob
import os
import re
import copy

from Logger import Logger
from constants import constants
from StringUtils import StringUtils
from rpmversion import LooseVersion
from SpecParser import SpecParser
from SpecStructures import dependentPackageData


class SpecData(object):
    def __init__(self, arch, logPath, specFilesPaths):
        self.arch = arch
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

        self.skippedSpecs = set()

        self._readSpecs(specFilesPaths)

        self.generateSpecPkgsMap()

    def _resolveProvider(self, req, providers):
        tmp = copy.deepcopy(req)
        for provider in providers:
                tmp.package = provider
                if self._getProperVersion(tmp):
                    break
        return tmp

    def _calculateInfiniteVersion(self, version):
        infinite_version = []
        for v in version.split("."):
            # Not quite infinite but good enough
            infinite_version.append("9" * 10)

        return ".".join(infinite_version)

    def _calculateMinimumVersion(self, version):
        minimum_version = []
        for v in version.split("."):
            minimum_version.append("0")

        return ".".join(minimum_version)

    def _getUpperBound(self, req):
        if not req.compare:
            return self._calculateInfiniteVersion(req.version)

        if req.compare == "<=":
            return req.version
        elif req.compare == "<":
            # In the case where the last digit is 0, this will give
            # an upper bound of "x.x.-1", which is not a valid version
            # number. But for the purpose of comparison, it will work,
            # since "x.x.0" > "x.x.-1"
            parts = req.version.split(".")
            parts[-1] = str(int(parts[-1]) - 1)
            return ".".join(parts)
        elif ">" in req.compare:
            return self._calculateInfiniteVersion(req.version)
        elif "=" in req.compare:
            return req.version

    def _getLowerBound(self, req):
        if not req.compare:
            return self._calculateMinimumVersion(req.version)

        if req.compare == ">=":
            return req.version
        elif req.compare == ">":
            parts = req.version.split(".")
            parts[-1] = str(int(parts[-1]) + 1)
            return ".".join(parts)
        elif "<" in req.compare:
            return self._calculateMinimumVersion(req.version)
        elif "=" in req.compare:
            return req.version

    def _doesCapabilityMatchReq(self, capability, req):
        if not req.compare:
            return True

        req_ub = self._getUpperBound(req)
        req_lb = self._getLowerBound(req)
        cap_ub = self._getUpperBound(capability)
        cap_lb = self._getLowerBound(capability)

        # Basically we have two sets in the version space, one for the req and
        # other for the capability. We just need to check for intersection. And
        # we can cheat because we only recognize one comparison operation, e.g we
        # don't have something like Provides: 3 < A < 5. So we know that if we
        # have an upper bound, we don't have a lower bound and vice versa.
        if LooseVersion(cap_lb) > LooseVersion(req_ub) or LooseVersion(req_lb) > LooseVersion(cap_ub):
            return False
        return True

    def _populateProviders(self, req, spec):
        pkgName = req.package
        userProvided = constants.providedByUserOverride.get(pkgName)
        if userProvided:
            self.logger.debug(
                f"Using user provided value for {pkgName}: {userProvided} ..."
            )
            return userProvided

        providers = constants.providedBy.get(req, [])
        if not providers:
            # Some provides have versioning, e.g <pkg> >= <version>, so an exact match may not
            # exist. Thus we need to loop all of them and try to find one which fits.
            for cap, provs in constants.providedBy.items():
                if cap.package == req.package:
                    if self._doesCapabilityMatchReq(cap, req):
                        providers = provs
                        break

        if pkgName[0] == '/':
            if not providers:
                raise Exception(
                    f"ERROR: What package provides {pkgName} ? "
                    f"Used in '{spec}' spec."
                )
        elif not providers:
            return pkgName

        if not req.compare or len(providers) == 1:
            return providers[-1]

        resolved = self._resolveProvider(req, providers)

        if not resolved.package:
            raise Exception(f"ERROR: while getting provider for {req.package} ...")

        return resolved.package

    # Read all .spec files from the given folder including subfolders,
    # creates corresponding SpecObjects and put them in internal mappings.
    def _readSpecs(self, specFilesPaths):
        for specFile in self._getListSpecFiles(specFilesPaths):
            spec = SpecParser(specFile, self.arch)
            if spec.skipSpec:
                self.skippedSpecs.add(os.path.basename(specFile))
                continue

            # skip the specfile if buildarch differs
            buildarch = spec.packages.get("default").buildarch
            if buildarch not in {"noarch", self.arch}:
                self.logger.debug(f"Skipping spec file: {specFile}")
                continue

            specObj = spec.createSpecObject()

            name = specObj.name
            for specPkg in specObj.listPackages:
                # Keep every provider of specPkg instead of overwriting.
                self.mapPackageToSpec.setdefault(specPkg, set())
                self.mapPackageToSpec[specPkg].add(name)

            if name not in self.mapSpecObjects:
                self.mapSpecObjects[name] = [specObj]
            else:
                self.mapSpecObjects[name].append(specObj)

            self.mapSpecFileNameToSpecObj[specFile] = specObj

        # Sort the multiversion list to make getHighestVersion happy
        for key, value in self.mapSpecObjects.items():
            if len(value) > 1:
                self.mapSpecObjects[key] = sorted(
                    value, key=lambda x: self.compareVersions(x), reverse=True
                )

        # Resolve "Provides" dependencies to the correct package
        # Needs to be a separate loop since we may run getProperVersion(), and it calls
        # getHighestVersion()
        for key, value in self.mapSpecObjects.items():
            attrs = [
                "installRequires",
                "buildRequires",
            ]
            all_reqs = (
                req
                for item in value
                for attr in attrs
                for req in getattr(item, attr, [])
            )
            for req in all_reqs:
                satisfied = False

                # Prioritize actual pkg/specs over virtual capabilities
                for resolved in self.mapPackageToSpec.get(req.package, []):
                    specObjs = self.mapSpecObjects[resolved]
                    for obj in specObjs:
                        dpkg = dependentPackageData()
                        dpkg.package = obj.name
                        dpkg.version = obj.version
                        dpkg.compare = "="
                        if self._doesCapabilityMatchReq(dpkg, req):
                            satisfied = True
                            break
                    if satisfied:
                        break

                if satisfied:
                    continue

                # If no matching package spec file, try to see if any providers match
                resolved = self._populateProviders(req, key)
                if resolved != req.package:
                    req.package = resolved

    def generateSpecPkgsMap(self):
        if not constants.stagePath:
            return

        lines = []
        append = lines.append
        skipped = self.skippedSpecs

        pkgMap = self.mapSpecObjects

        for specObjs in pkgMap.values():
            for specObj in specObjs:
                specFn = os.path.basename(specObj.specFile)
                skipped.discard(specFn)
                append(f"{specFn}:{','.join(specObj.listPackages)}\n")

        for specFn in skipped:
            append(f"{specFn}:skipped\n")

        lines.sort(key=str.lower)

        outFile = f"{constants.stagePath}/pkg_info.pkg_map.txt"
        with open(outFile, "w", encoding="utf-8") as f:
            f.writelines(lines)

            self.logger.info(f"Spec to packages map written to: {outFile}")

    def _getListSpecFiles(self, paths):
        listSpecFiles = []
        for path in paths:
            for dirEntry in sorted(os.listdir(path)):
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
                if not obj.epoch:
                    verrel = obj.version
                else:
                    verrel = f"{obj.epoch}:{obj.version}"
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

        availableVersions = []
        for obj in specObjs:
            availableVersions.append(f"{obj.name}-{obj.version}")
        self.logger.info(
            "Could not find package: "
            f"{depPkg.package}{depPkg.compare}{depPkg.version}"
            " available specs: " + " ".join(availableVersions)
        )

        return None

    def _getSpecObjField(self, package, version, field):
        for specObj in self.getSpecObjects(package):
            if specObj.version == version:
                return field(specObj)
        self.logger.error(
            f"Could not find {package}-{version} package from specs"
        )
        raise Exception(f"Invalid package: {package}-{version}")

    def getBuildRequiresForPackage(self, package, version):
        buildRequiresList = []
        for pkg in self._getSpecObjField(
            package, version, field=lambda x: x.buildRequires
        ):
            properVersion = self._getProperVersion(pkg)
            if not properVersion:
                raise Exception(f"Could not find proper version for {pkg}")
            buildRequiresList.append(f"{pkg.package}-{properVersion}")
        return buildRequiresList

    def getExtraBuildRequiresForPackage(self, package, version):
        packages = []
        for pkg in self._getSpecObjField(
            package, version, field=lambda x: x.extraBuildRequires
        ):
            if pkg.compare and pkg.compare == "=":
                packages.append(f"{pkg.package}-{pkg.version}")
            else:
                # if no version deps for publishrpms - use just name
                packages.append(pkg.package)
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
            if not properVersion:
                raise Exception(f"Could not find proper version for {pkg}")
            requiresList.append(f"{pkg.package}-{properVersion}")
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
        requires = self.getBuildRequiresForPkg(pkg) + self.getRequiresForPkg(pkg)
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
                        if not properVersion:
                            raise Exception(f"Could not find proper version for {pkg}")
                        requiresList.append(f"{pkg.package}-{properVersion}")
                return requiresList
        self.logger.error(
            f"Could not find {package}-{version} package from specs"
        )
        raise Exception(f"Invalid package: {package}-{version}")

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
            if not properVersion:
                raise Exception(f"Could not find proper version for {pkg}")
            checkBuildRequiresList.append(pkg.package + "-" + properVersion)
        return checkBuildRequiresList

    # Returns list of SpecObjects for given subpackage name, merged
    # across every default package that provides it.
    def getSpecObjects(self, package):
        specNames = self.mapPackageToSpec.get(package, set())
        if not specNames:
            self.logger.error(f"Could not find {package} package from specs")
            raise Exception(f"Invalid package: {package}")
        merged = [
            obj
            for specName in specNames
            for obj in self.mapSpecObjects[specName]
        ]
        return sorted(merged, key=lambda x: self.compareVersions(x), reverse=True)

    def getPkgNamesFromObj(self, objlist):
        listPkgName = []
        for name in objlist:
            listPkgName.append(name.package)
        return listPkgName

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
        return self._getSpecObjField(package, version, field=lambda x: x.specFile)

    def getPatches(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.listPatches)

    def getSources(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.listSources)

    # returns list of package names (no versions)
    def getPackages(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.listPackages)

    def getEpoch(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.epoch)

    def getPackagesForPkg(self, pkg):
        pkgs = []
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        for p in self.getPackages(package, version):
            pkgs.append(f"{p}-{version}")
        return pkgs

    def getRPMPackages(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.listRPMPackages
        )

    @staticmethod
    def compareVersions(p):
        return LooseVersion(p.version)

    # Returns every spec name that provides package, since a subpackage
    # name can be provided by more than one spec.
    def getSpecNames(self, package):
        if self.isRPMPackage(package):
            return list(self.mapPackageToSpec[package])
        self.logger.error(f"Could not find {package} package from specs")
        raise Exception(f"Invalid package: {package}")

    # Disambiguates getSpecNames() using the exact version being built.
    def getSpecNameForVersion(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.name)

    def isRPMPackage(self, package):
        if package in self.mapPackageToSpec:
            return any(
                specName in self.mapSpecObjects
                for specName in self.mapPackageToSpec[package]
            )
        return False

    def getSecurityHardeningOption(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.securityHardening
        )

    def isNetworkRequired(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.networkRequired
        )

    def isCheckAvailable(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.isCheckAvailable
        )

    def getListPackages(self):
        return list(self.mapSpecObjects.keys())

    def getURL(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.url)

    def getSourceURL(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.sourceurl)

    def getLicense(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.license)

    def getSummary(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x: x.summary)

    def getDescription(self, package, version):
        return self._getSpecObjField(
            package, version, field=lambda x: x.descriptions[package]
        )

    # Converts "glibc-devel-2.28" into "glibc-2.28"
    def getBasePkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getSpecNameForVersion(package, version) + f"-{version}"


class SPECS(object):
    __instance = None
    specData = {}

    @staticmethod
    def getData(arch=None):
        if not arch:
            arch = constants.buildArch

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
        defPkg = None

        # linux.spec can live under SPECS/linux/ or SPECS/<dir>/linux/
        # (e.g. SPECS/91/linux/ for kernels pinned to older subreleases).
        # The active one is the first that is not skipped (via build_if).
        for specDir in constants.specPaths:
            if defPkg:
                break
            linuxDirs = sorted(
                glob.glob(f"{specDir}/linux") + glob.glob(f"{specDir}/*/linux")
            )
            for linuxDir in linuxDirs:
                if defPkg:
                    break
                for root, _, files in os.walk(linuxDir):
                    if "linux.spec" in files:
                        spec = SpecParser(f"{root}/linux.spec", constants.buildArch)
                        if spec.skipSpec:
                            continue
                        defPkg = spec.packages.get("default")
                        break

        kernelversion = defPkg.version
        kernelrelease = defPkg.release

        # adding kernelversion rpm macro
        constants.addMacro("KERNEL_VERSION", kernelversion)

        # adding kernelrelease rpm macro
        kernelrelease_comp = kernelrelease.split('.')
        if re.fullmatch(r'rc\d+', kernelrelease_comp[0]):
            kernelrelease_comp.pop(0)
        constants.addMacro("KERNEL_RELEASE", kernelrelease)

        # adding kernelsubrelease rpm macro
        a, b, c = kernelversion.split(".")
        kernelsubrelease = ('%02d%02d%03d%03d' % (int(a),
                                                  int(b), int(c),
                                                  int(kernelrelease_comp[0])))

        if kernelsubrelease:
            constants.addMacro("kernelsubrelease", f".{kernelsubrelease}")

        # Full parsing
        self.specData[constants.buildArch] = SpecData(
            constants.buildArch, constants.logPath, constants.specPaths
        )

if __name__ == "__main__":
    import sys
    import platform

    if len(sys.argv) < 2:
        print("Usage: %prog <specFilesPath>")
        sys.exit(1)

    specFilesPath = [sys.argv[1]]
    arch = platform.machine()
    logPath = "/tmp"
    constants.stagePath = "/tmp"

    constants.addMacro("photon_subrelease", "92")

    spec_data = SpecData(arch, logPath, specFilesPath)
    listSpecs = spec_data.mapSpecObjects.keys()

    for spec in listSpecs:
        for specObj in spec_data.mapSpecObjects[spec]:
            print(f"-----------Spec: {specObj.name}--------------")
            print(f"Version: {specObj.version}")
            print(f"Release: {specObj.release}")
            print(f"SpecFile: {specObj.specFile}")
            print("Source Files")
            print(specObj.listSources)
            print("Patch Files")
            print(specObj.listPatches)
            print("List RPM packages")
            print(specObj.listPackages)
            print("Build require packages")
            print(spec_data.getPkgNamesFromObj(specObj.buildRequires))
            print("install require packages")
            print(spec_data.getPkgNamesFromObj(specObj.installRequires))
            print(specObj.installRequiresPackages)
            print(f"security_hardening: {specObj.securityHardening}")
            print(f"BuildArch: {specObj.buildarch}")
            print("------------------------------------------------")
