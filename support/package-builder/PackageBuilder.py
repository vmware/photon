#!/usr/bin/env python3

import os.path

from PackageUtils import PackageUtils
from Logger import Logger
from ToolChainUtils import ToolChainUtils
from CommandUtils import CommandUtils
from constants import constants
from SpecData import SPECS
from StringUtils import StringUtils
from Sandbox import Chroot, Container


class PackageBuilder(object):
    def __init__(self, mapPackageToCycles, sandboxType):
        # will be initialized in buildPackageFunction()
        self.logName = None
        self.logPath = None
        self.logger = None
        self.package = None
        self.version = None
        self.doneList = None
        self.sandboxType = sandboxType
        self.sandbox = None
        self.cmdUtils = CommandUtils()
        self.mapPackageToCycles = mapPackageToCycles
        self.listNodepsPackages = ["glibc", "gmp", "zlib", "file", "binutils", "mpfr",
                                   "mpc", "gcc", "ncurses", "util-linux", "groff", "perl",
                                   "texinfo", "rpm", "openssl", "go"]

    def build(self, pkg, doneList):
        packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
        #do not build if RPM is already built
        #test only if the package is in the testForceRPMS with rpmCheck
        #build only if the package is not in the testForceRPMS with rpmCheck

        if not (constants.rpmCheck or packageName in constants.testForceRPMS):
            if self._checkIfPackageIsAlreadyBuilt(packageName, packageVersion, doneList):
                return

        self._buildPackagePrepareFunction(packageName, packageVersion, doneList)
        try:
            self._buildPackage()
        except Exception as e:
            # TODO: self.logger might be None
            self.logger.exception(e)
            raise e

    def _buildPackage(self):
        try:
            self.sandbox.create(f"{self.package}-{self.version}")

            tUtils = ToolChainUtils(self.logName, self.logPath)
            if self.sandbox.hasToolchain():
                tUtils.installExtraToolchainRPMS(self.sandbox, self.package, self.version)
            else:
                tUtils.installToolchainRPMS(self.sandbox, self.package, self.version, availablePackages=self.doneList)

            if ((self.package not in constants.listCoreToolChainPackages) or
                    (constants.rpmCheck and self.package in constants.testForceRPMS)):
                self._installDependencies(constants.buildArch)
                if constants.crossCompiling:
                    self._installDependencies(constants.targetArch)

            pkgUtils = PackageUtils(self.logName, self.logPath)
            pkgUtils.adjustGCCSpecs(self.sandbox, self.package, self.version)
            pkgUtils.buildRPMSForGivenPackage(self.sandbox, self.package, self.version,
                                              self.logPath)
            self.logger.debug(f"Successfully built the package: {self.package}")
        except Exception as e:
            self.logger.error(f"Failed while building package: {self.package}")
            self.logger.debug("Sandbox: " + self.sandbox.getID() + " not deleted for debugging.")
            if constants.rpmCheck and self.package in constants.testForceRPMS:
                logFileName = os.path.join(self.logPath, f"{self.package}-test.log")
            else:
                logFileName = os.path.join(self.logPath, f"{self.package}.log")
            fileLog, _, _ = self.cmdUtils.runBashCmd(f"tail -n 100 {logFileName}", capture=True)
            self.logger.info(fileLog)
            raise e
        if self.sandbox:
            self.sandbox.destroy()

    def _installDependencies(self, arch, deps=[]):
        listDependentPackages, listTestPackages, listInstalledPackages, listInstalledRPMs = (
            self._findDependentPackagesAndInstalledRPM(self.sandbox, arch))

        # PackageUtils should be initialized here - as per arch basis
        # Do not move it to __init__
        pkgUtils = PackageUtils(self.logName, self.logPath)

        if listDependentPackages:
            self.logger.debug("Installing the build time dependent packages for " + arch)
            for pkg in listDependentPackages:
                packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                self._installPackage(pkgUtils, packageName, packageVersion, self.sandbox, self.logPath,listInstalledPackages, listInstalledRPMs, arch)
            for pkg in listTestPackages:
                flag = False
                packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                for depPkg in listDependentPackages:
                    depPackageName, depPackageVersion = StringUtils.splitPackageNameAndVersion(depPkg)
                    if depPackageName == packageName:
                        flag = True
                        break
                if not flag:
                    self._installPackage(pkgUtils, packageName,packageVersion, self.sandbox, self.logPath,listInstalledPackages, listInstalledRPMs, arch)
            pkgUtils.installRPMSInOneShot(self.sandbox,arch)
            self.logger.debug("Finished installing the build time dependent packages for " + arch)

    def _buildPackagePrepareFunction(self, package, version, doneList):
        self.package = package
        self.version = version
        self.logName = "build-" + package + "-" + version
        self.logPath = constants.logPath + "/" + package + "-" + version + "." + constants.currentArch
        if not os.path.isdir(self.logPath):
            self.cmdUtils.runCommandInShell(f"mkdir -p {self.logPath}")
        else:
            self.cmdUtils.runCommandInShell(f"rm -f {self.logPath}/*.log")
        self.logger = Logger.getLogger(self.logName, self.logPath, constants.logLevel)
        self.doneList = doneList

        if self.sandboxType == "chroot":
            sandbox = Chroot(self.logger)
        elif self.sandboxType == "container":
            sandbox = Container(self.logger)
        else:
            raise Exception("Unknown sandbox type: " + self.sandboxType)

        self.sandbox = sandbox

    def _findPackageNameAndVersionFromRPMFile(self, rpmfile):
        rpmfile = os.path.basename(rpmfile)
        releaseindex = rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:" + rpmfile)
            return None
        pkg = rpmfile[0:releaseindex]
        return pkg

    def _findInstalledPackages(self, sandbox, arch):
        pkgUtils = PackageUtils(self.logName, self.logPath)
        listInstalledRPMs = pkgUtils.findInstalledRPMPackages(sandbox, arch)
        listInstalledPackages = []
        for installedRPM in listInstalledRPMs:
            pkg = self._findPackageNameAndVersionFromRPMFile(installedRPM)
            if pkg is not None:
                listInstalledPackages.append(pkg)
        return listInstalledPackages, listInstalledRPMs

    def _checkIfPackageIsAlreadyBuilt(self, package, version, doneList):
        basePkg = SPECS.getData().getSpecName(package) + "-" + version
        return basePkg in doneList

    def _findRunTimeRequiredRPMPackages(self, rpmPackage, version, arch):
        return SPECS.getData(arch).getRequiresForPackage(rpmPackage, version)

    def _findBuildTimeRequiredPackages(self, arch):
        deps = SPECS.getData(arch).getBuildRequiresForPackage(self.package, self.version)

        # Add BuildRequiresNative list
        if constants.crossCompiling and arch == constants.buildArch:
            deps.extend(SPECS.getData(arch).getBuildRequiresNativeForPackage(self.package, self.version))

        return deps

    def _findBuildTimeCheckRequiredPackages(self):
        return SPECS.getData().getCheckBuildRequiresForPackage(self.package, self.version)

    def _installPackage(self, pkgUtils, package, packageVersion, sandbox, destLogPath,
                        listInstalledPackages, listInstalledRPMs, arch):
        rpmfile = pkgUtils.findRPMFile(package, packageVersion, arch)
        if rpmfile is None:
            self.logger.error("No rpm file found for package: " + package + "-" + packageVersion)
            raise Exception("Missing rpm file")
        specificRPM = os.path.basename(rpmfile.replace(".rpm", ""))
        pkg = package+"-"+packageVersion
        if pkg in listInstalledPackages:
            return
        # mark it as installed -  to avoid cyclic recursion
        listInstalledPackages.append(pkg)
        listInstalledRPMs.append(specificRPM)
        self._installDependentRunTimePackages(pkgUtils, package, packageVersion, sandbox, destLogPath,
                                              listInstalledPackages, listInstalledRPMs, arch)
        noDeps = False
        if (package in self.mapPackageToCycles or
                package in self.listNodepsPackages or
                package in constants.noDepsPackageList):
            noDeps = True
        pkgUtils.prepRPMforInstall(package,packageVersion, noDeps, destLogPath, arch)

    def _installDependentRunTimePackages(self, pkgUtils, package, packageVersion, sandbox, destLogPath,
                                         listInstalledPackages, listInstalledRPMs, arch):
        listRunTimeDependentPackages = self._findRunTimeRequiredRPMPackages(package, packageVersion, arch)
        if listRunTimeDependentPackages:
            for pkg in listRunTimeDependentPackages:
                if pkg in self.mapPackageToCycles:
                    continue
                packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                rpmfile = pkgUtils.findRPMFile(packageName, packageVersion, arch, True)
                if rpmfile is None:
                    self.logger.error("No rpm file found for package: " + packageName + "-" + packageVersion)
                    raise Exception("Missing rpm file")
                latestPkgRPM = os.path.basename(rpmfile).replace(".rpm", "")
                if pkg in listInstalledPackages and latestPkgRPM in listInstalledRPMs:
                    continue
                self._installPackage(pkgUtils, packageName,packageVersion, sandbox, destLogPath,listInstalledPackages, listInstalledRPMs, arch)

    def _findDependentPackagesAndInstalledRPM(self, sandbox, arch):
        listInstalledPackages, listInstalledRPMs = self._findInstalledPackages(sandbox, arch)
        self.logger.debug(listInstalledPackages)
        if constants.crossCompiling and arch == constants.buildArch:
            listDependentPackages = self._findBuildTimeRequiredPackages(constants.targetArch)
            # TODO remove unsupported by buildArch packages from this list
        else:
            listDependentPackages = self._findBuildTimeRequiredPackages(arch)
        listTestPackages=[]
        if constants.rpmCheck and self.package in constants.testForceRPMS:
            # One time optimization
            if constants.listMakeCheckRPMPkgWithVersionstoInstall is None:
                constants.listMakeCheckRPMPkgWithVersionstoInstall=[]
                for package in constants.listMakeCheckRPMPkgtoInstall:
                    version = SPECS.getData(arch).getHighestVersion(package)
                    constants.listMakeCheckRPMPkgWithVersionstoInstall.append(package+"-"+version)

            listDependentPackages.extend(self._findBuildTimeCheckRequiredPackages())
            testPackages = (set(constants.listMakeCheckRPMPkgWithVersionstoInstall) -
                            set(listInstalledPackages) -
                            set([self.package+"-"+self.version]))
            listTestPackages=list(set(testPackages))
            listDependentPackages = list(set(listDependentPackages))
        return listDependentPackages, listTestPackages, listInstalledPackages, listInstalledRPMs
