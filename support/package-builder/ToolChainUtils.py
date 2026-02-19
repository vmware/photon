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
        if logName is None:
            logName = "ToolchainUtils"
        if logPath is None:
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
        tdnf = TDNF(
            installRoot=chroot.getRootPath(), repoArgs=repoArgs, logger=self.logger
        )
        try:
            response = tdnf.run(
                subCmd=["upgrade", "--refresh", "--exclude=photon-release"],
                errMsg="Unable to upgrade",
            )
            response = tdnf.run(
                subCmd=["install"] + packages,
                errMsg="Unable to install rpms",
            )
            self.logger.debug(
                f"Successfully installed default toolchain RPMS in sandbox {chroot.getRootPath()} {rpmFiles}"  # noqa: E501
            )
            if packageName:
                self.installExtraToolchainRPMS(
                    tdnf, chroot, packageName, packageVersion
                )
            response = tdnf.run(
                subCmd=["list"],
                repoArgs=[],
                args=["--installed", "-j"],
                errMsg="Listing installed RPMs",
            )
            rpmFiles = tdnf.processInstalled(response)
        except Exception as e:
            raise Exception(f"Failed installing/processing rpmFiles {str(e)}")
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
        tdnf.run(
            subCmd=["install", "--nogpgcheck"] + listOfToolChainPkgs,
            repoArgs=repoArgs,
            errMsg="Extra BuildRequires RPM installation failed",
        )
