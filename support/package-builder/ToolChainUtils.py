#!/usr/bin/env python3

import RepoUtil

from constants import constants
from Logger import Logger
from SpecData import SPECS
from StringUtils import StringUtils
from TDNFSandbox import TDNF


class ToolChainUtils(object):
    def __init__(
        self, buildStage, buildMode, logName=None, logPath=None, cmdlog=lambda cmd: None
    ):
        self.buildStage = buildStage
        self.buildMode = buildMode
        if not logName:
            logName = "ToolchainUtils"
        if not logPath:
            logPath = constants.logPath
        self.cmdlog = cmdlog
        self.logName = logName
        self.logPath = logPath
        self.logger = Logger.getLogger(logName, logPath, constants.logLevel)

    def getListDependentPackages(self, package, version):
        listBuildRequiresPkg = SPECS.getData(
            constants.buildArch
        ).getBuildRequiresForPackage(package, version)
        listBuildRequiresPkg.extend(
            SPECS.getData(constants.buildArch).getCheckBuildRequiresForPackage(
                package, version
            )
        )
        return listBuildRequiresPkg

    def installToolchainRPMS(
        self,
        chroot,
        packageName=None,
        packageVersion=None,
    ):
        self.logger.debug("Installing toolchain RPMS ...")
        rpmFiles = []
        packages = []
        listBuildRequiresPackages = []

        listRPMsToInstall = list(constants.listToolChainRPMsToInstall)

        if packageName:
            listBuildRequiresPackages = self.getListDependentPackages(
                packageName, packageVersion
            )

        for package in listRPMsToInstall:
            version = None

            # Get proper package version
            for depPkg in listBuildRequiresPackages:
                (
                    depPkgName,
                    depPkgVersion,
                ) = StringUtils.splitPackageNameAndVersion(depPkg)
                if depPkgName == package:
                    version = depPkgVersion
                    break

            if not version:
                version = SPECS.getData(constants.buildArch).getHighestVersion(package)
            if package == "coreutils":
                package = package.replace("coreutils", "coreutils-selinux")
            packages.append(package)
        packages.append("build-essential")

        repoArgs = RepoUtil.getRepoArgs(self.buildStage, self.buildMode)
        tdnf = TDNF(installRoot=chroot.getRootPath(), logger=self.logger)
        try:
            subCmd = ["upgrade", "-y", "--exclude=photon-release"]
            response = tdnf.run(
                args=subCmd + repoArgs,
                errMsg="Unable to upgrade",
            )

            subCmd = ["install", "-y", "--setopt=tsflags=nodocs"] + packages
            response = tdnf.run(
                args=subCmd + repoArgs,
                errMsg="Unable to install rpms",
            )
            self.logger.debug(
                f"Successfully installed default toolchain RPMS in sandbox {chroot.getRootPath()} {rpmFiles}"
            )
            if packageName:
                self.installExtraToolchainRPMS(
                    tdnf, chroot, packageName, packageVersion
                )

            if constants.listOptionalToolChainRPMsToInstall:
                try:
                    subCmd = ["install", "-y", "--setopt=tsflags=nodocs"] + constants.listOptionalToolChainRPMsToInstall
                    tdnf.run(args=subCmd + repoArgs, errMsg="Unable to install optional toolchain rpms")
                    self.logger.debug(
                        f"Installed optional toolchain RPMs: {constants.listOptionalToolChainRPMsToInstall}"
                    )
                except Exception as e:
                    self.logger.warning(
                        f"Optional toolchain RPMs not available, skipping: {e}"
                    )

            response = tdnf.run(
                args=["list", "--installed", "--disablerepo=*", "-j"],
                errMsg="Listing installed RPMs",
            )
            rpmFiles = tdnf.processInstalled(response)
        except Exception as e:
            raise Exception(f"Failed installing/processing rpmFiles {e} while building {packageName}")
        finally:
            tdnf.clean()

        return rpmFiles

    def installExtraToolchainRPMS(self, tdnf, sandbox, packageName, packageVersion):
        listOfToolChainPkgs = SPECS.getData(
            constants.buildArch
        ).getExtraBuildRequiresForPackage(packageName, packageVersion)
        if not listOfToolChainPkgs:
            return []
        self.logger.debug(
            f"Installing package specific toolchain RPMs for {packageName}: "
            + str(listOfToolChainPkgs)
        )
        repoArgs = [
            f"--releasever={constants.releaseVersionToConsume}",
            "--disablerepo=*",
            "--enablerepo=packages",
        ]

        subCmd = ["install", "-y", "--nogpgcheck", "--setopt=tsflags=nodocs"] + listOfToolChainPkgs
        tdnf.run(
            args=subCmd + repoArgs,
            errMsg="Extra BuildRequires RPM installation failed",
        )
