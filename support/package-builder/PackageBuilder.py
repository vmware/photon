#!/usr/bin/env python3

import os

from CommandUtils import CommandUtils
from constants import BuildStage, constants
from Logger import Logger
from PackageUtils import PackageUtils
from Sandbox import init_sandbox
from SourceConfigData import SOURCES
from SpecData import SPECS
from SRP import SRP
from StringUtils import StringUtils
from ToolChainUtils import ToolChainUtils


class PackageBuilder(object):
    def __init__(self, pkg, mapPackageToCycles, sandboxType, buildStage, buildMode):
        # will be initialized in buildPackageFunction()
        self.package, self.version = StringUtils.splitPackageNameAndVersion(pkg)
        self.buildStage = buildStage
        self.buildMode = buildMode
        self.mapPackageToCycles = mapPackageToCycles
        self.logName = f"build-{pkg}"
        self.logPath = os.path.join(constants.logPath, f"{pkg}.{constants.currentArch}")
        # Cleanup the log directory
        os.makedirs(self.logPath, exist_ok=True)
        CommandUtils.runCmd(["find", self.logPath, "-name", "*.log", "-delete"])
        self.logger = Logger.getLogger(self.logName, self.logPath, constants.logLevel)

        self.srp = SRP(pkg, self.logger)

        baseImageTarball = constants.buildBaseImageTarball[buildStage]

        self.sandbox = init_sandbox(
            name=pkg,
            sandboxType=sandboxType,
            baseImagePath=os.path.join(constants.buildImagesPath, baseImageTarball),
            optionalMounts={
                "bindsrw": [
                    [
                        f"{constants.stagePath}/LOGS/{pkg}.{constants.buildArch}",
                        f"{constants.topDirPath}/LOGS/{pkg}.{constants.buildArch}",
                    ]
                ],
            },
            logger=self.logger,
            cmdAudit=self.srpLogCommand,
        )

    def build(self, doneList):
        # do not build if RPM is already built
        # test only if the package is in the testForceRPMS with rpmCheck
        # build only if the package is not in the testForceRPMS with rpmCheck
        if not (constants.rpmCheck or self.package in constants.testForceRPMS):
            if self._checkIfPackageIsAlreadyBuilt(self.package, self.version, doneList):
                return

        try:
            self._buildPackage(doneList)
        except Exception as e:
            # TODO: self.logger might be None
            self.logger.exception(e)
            raise e

    def _buildPackage(self, doneList):
        listRPMFiles = []
        listSRPMFiles = []
        try:
            self.srp.initialize()
            self.sandbox.create()

            tUtils = ToolChainUtils(
                self.buildStage,
                self.buildMode,
                self.logName,
                self.logPath,
                self.srpLogCommand,
            )
            inputRPMS = tUtils.installToolchainRPMS(
                self.sandbox,
                self.package,
                self.version,
            )

            if (self.package not in constants.listCoreToolChainPackages) or (
                constants.rpmCheck and self.package in constants.testForceRPMS
            ):
                self._installDependencies(constants.buildArch)

            pkgUtils = PackageUtils(
                self.buildStage, self.buildMode, self.logName, self.logPath
            )
            for _, v in constants.CopyToSandboxDict.items():
                pkgUtils.copyFileToSandbox(self.sandbox, v["src"], v["dest"])
            pkgUtils.adjustGCCSpecs(self.sandbox, self.package, self.version)
            listRPMFiles, listSRPMFiles = pkgUtils.buildRPMSForGivenPackage(
                self.sandbox, self.package, self.version, self.logPath
            )

            # SRP: Remove the names of generated RPMs from the list of inputRPMs.
            # There are some RPMs in outputs which by current design
            # end up as inputs causing infinite loops during report generation.
            inputRPMS = list(set(inputRPMS) - set(listRPMFiles))
            self.srp.addInputRPMS(inputRPMS)

            # SRP: Add input sources only after pkgUtils.buildRPMSForGivenPackage() as it
            # also fetches any missing ones.
            if self.srp.isEnabled():
                specDir = os.path.dirname(
                    SPECS.getData().getSpecFile(self.package, self.version)
                )
                if not os.path.isdir(specDir):
                    raise Exception(
                        f"ERROR: {package}-{version}, '{specDir}' does not exist ..."
                    )

                for source in SPECS.getData().getSources(self.package, self.version):
                    checksum = SOURCES(specDir).getData().getChecksum(source)
                    # If checksum present - report this source tarball.
                    if checksum:
                        self.srp.addInputSource(source, checksum)

            self.srp.addObservation(self.sandbox.getObservation())
            self.srp.addOutputRPMS(listRPMFiles + listSRPMFiles)
            if self.sandbox:
                self.sandbox.destroy()
            self.srp.finalize()
            self.logger.debug(
                f"Successfully built the package: {self.package}-{self.version}"
            )
        except Exception as e:
            self.logger.error(
                f"Failed while building package: {self.package}-{self.version}"
            )
            self.logger.debug(
                f"Sandbox: {self.sandbox.name} not deleted for debugging."
            )
            if constants.rpmCheck and self.package in constants.testForceRPMS:
                logFileName = os.path.join(self.logPath, f"{self.package}-test.log")
            else:
                logFileName = os.path.join(self.logPath, f"{self.package}.log")
            CommandUtils.runCmd(
                ["tail", "-n", "100", logFileName],
                ignore_rc=True,
                logfn=self.logger.info,
            )
            # Removing just built RPM files if any
            for f in listRPMFiles + listSRPMFiles:
                self.logger.info(f"Removing {f}")
                self.sandbox.runCmd(["rm", "-f", f], logfn=self.logger.debug)
            self.logger.exception(e)
            raise

    def _installDependencies(self, arch, deps=[]):
        (
            listDependentPackages,
            listTestPackages,
            listInstalledPackages,
            listInstalledRPMs,
        ) = self._findDependentPackagesAndInstalledRPM(self.sandbox, arch)

        # PackageUtils should be initialized here - as per arch basis
        # Do not move it to __init__
        pkgUtils = PackageUtils(
            self.buildStage, self.buildMode, self.logName, self.logPath
        )

        if listDependentPackages:
            self.logger.debug(
                f"Installing the build time dependent packages for {arch} {self.package} ..."
            )
            for pkg in listDependentPackages:
                pkgName, pkgVer = StringUtils.splitPackageNameAndVersion(pkg)
                pkgUtils.prepRPMforInstall(
                    pkgName
                    if self.buildStage is BuildStage.CORE_TOOLCHAIN
                    else f"{pkgName}-{pkgVer}"
                )
            for pkg in listTestPackages:
                flag = False
                pkgName, pkgVer = StringUtils.splitPackageNameAndVersion(pkg)
                for depPkg in listDependentPackages:
                    depPackageName, depPackageVersion = (
                        StringUtils.splitPackageNameAndVersion(depPkg)
                    )
                    if depPackageName == pkgName:
                        flag = True
                        break
                if not flag:
                    pkgUtils.prepRPMforInstall(
                        pkgName
                        if self.buildStage is BuildStage.CORE_TOOLCHAIN
                        else f"{pkgName}-{pkgVer}"
                    )
            pkgUtils.installRPMSInOneShot(self.sandbox, arch)
            self.logger.debug(f"Finished installing the build dependencies for {arch}")

    def srpLogCommand(self, cmd, env={}):
        self.srp.addCommand(cmd, env)

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
        deps = SPECS.getData(arch).getBuildRequiresForPackage(
            self.package, self.version
        )

        return deps

    def _findBuildTimeCheckRequiredPackages(self):
        return SPECS.getData().getCheckBuildRequiresForPackage(
            self.package, self.version
        )

    def _findDependentPackagesAndInstalledRPM(self, sandbox, arch):
        listInstalledPackages, listInstalledRPMs = self._findInstalledPackages(
            sandbox, arch
        )
        self.logger.debug(listInstalledPackages)
        listDependentPackages = self._findBuildTimeRequiredPackages(arch)
        listTestPackages = []
        if constants.rpmCheck and self.package in constants.testForceRPMS:
            # One time optimization
            if len(constants.listMakeCheckRPMPkgWithVersionstoInstall) == 0:
                for package in constants.listMakeCheckRPMPkgtoInstall:
                    version = SPECS.getData(arch).getHighestVersion(package)
                    constants.listMakeCheckRPMPkgWithVersionstoInstall.append(
                        package + "-" + version
                    )

            listDependentPackages.extend(self._findBuildTimeCheckRequiredPackages())
            testPackages = (
                set(constants.listMakeCheckRPMPkgWithVersionstoInstall)
                - set(listInstalledPackages)
                - set([self.package + "-" + self.version])
            )
            listTestPackages = list(set(testPackages))
            listDependentPackages = list(set(listDependentPackages))
        return (
            listDependentPackages,
            listTestPackages,
            listInstalledPackages,
            listInstalledRPMs,
        )
