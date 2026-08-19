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
                strictBRs = SPECS.getData(
                    constants.buildArch
                ).getStrictBRsForPkg(packageName, packageVersion)
                exactStrictBRs = [p for p in strictBRs if " " not in p]
                if exactStrictBRs:
                    missingBRs = self._findMissingFromRepo(
                        tdnf, exactStrictBRs, repoArgs
                    )
                    if missingBRs:
                        self._reinstallIfVersionMismatch(tdnf, missingBRs)
                self._installExtraToolchainRPMS(
                    tdnf, packageName, packageVersion
                )
                self._installExtraToolchainRPMS(
                    tdnf, packageName, packageVersion, sansSnapshot=True
                )

            if constants.listOptionalToolChainRPMsToInstall:
                available_pkgs = []

                for pkg in constants.listOptionalToolChainRPMsToInstall:
                    try:
                        out = tdnf.run(
                                args=["repoquery", pkg] + repoArgs,
                                errMsg=f"Checking availability of {pkg}",
                              )
                        if out and pkg in out:
                            available_pkgs.append(pkg)
                    except Exception as e:
                        self.logger.debug(f"Optional RPM {pkg} not available, skipping: {e}")

                if available_pkgs:
                    subCmd = ["install", "-y", "--setopt=tsflags=nodocs"] + available_pkgs
                    tdnf.run(
                        args=subCmd + repoArgs,
                        errMsg="Unable to install optional toolchain rpms",
                    )
                    self.logger.debug(
                        f"Installed optional toolchain RPMs: {available_pkgs}"
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

    def _installExtraToolchainRPMS(self, tdnf, packageName, packageVersion, sansSnapshot=False):
        if sansSnapshot:
            listOfToolChainPkgs = SPECS.getData(
                constants.buildArch
            ).getExtraBuildRequiresSansSnapshotForPackage(packageName, packageVersion)
            label = " (sans snapshot)"
            errMsg = "Extra BuildRequires (sans snapshot) RPM installation failed"
            repoName = "packages"
            tdnf.createPackagesRepoFile()
        else:
            listOfToolChainPkgs = SPECS.getData(
                constants.buildArch
            ).getExtraBuildRequiresForPackage(packageName, packageVersion)
            label = ""
            errMsg = "Extra BuildRequires RPM installation failed"
            repoName = "packages-snapshot"

        if not listOfToolChainPkgs:
            return []

        self.logger.debug(
            f"Installing package specific toolchain RPMs{label} for {packageName}: "
            + str(listOfToolChainPkgs)
        )

        repoArgs = [
            f"--releasever={constants.releaseVersionToConsume}",
            "--disablerepo=*",
            f"--enablerepo={repoName}",
        ]

        subCmd = ["install", "-y", "--nogpgcheck", "--setopt=tsflags=nodocs"]

        if sansSnapshot:
            tdnf.run(args=subCmd + listOfToolChainPkgs + repoArgs, errMsg=errMsg)
        else:
            # Only install from snapshot what is actually there; fall back to packages for the rest
            missingFromSnapshot = self._findMissingFromRepo(tdnf, listOfToolChainPkgs, repoArgs)
            pkgsInSnapshot = [p for p in listOfToolChainPkgs if p not in set(missingFromSnapshot)]
            if pkgsInSnapshot:
                tdnf.run(args=subCmd + pkgsInSnapshot + repoArgs, errMsg=errMsg)
            strictExtraBRs = SPECS.getData(
                constants.buildArch
            ).getStrictExtraBRsForPackage(packageName, packageVersion)
            # strict ExtraBRs installed from snapshot + packages missing from snapshot
            strictInSnapshot = [p for p in strictExtraBRs if p not in set(missingFromSnapshot)]
            toReinstall = missingFromSnapshot + strictInSnapshot
            if toReinstall:
                self._reinstallIfVersionMismatch(tdnf, toReinstall)

    def _findMissingFromRepo(self, tdnf, packages, repoArgs):
        missing = []
        for pkg in packages:
            try:
                out = tdnf.run(
                    args=["repoquery", pkg] + repoArgs,
                    errMsg=f"Checking availability of {pkg}",
                )
                if not out or pkg not in out:
                    missing.append(pkg)
            except Exception as e:
                self.logger.debug(
                    f"Package {pkg} not available locally, will try packages repo: {e}"
                )
                missing.append(pkg)
        return missing

    def _reinstallIfVersionMismatch(self, tdnf, packages):
        self.logger.debug(f"Reinstalling rpms: {packages}")
        subCmd = [
            "install", "-y", "--nogpgcheck", "--setopt=tsflags=nodocs",
            "--setopt=reposdir=/etc/yum.repos.d",
        ] + packages
        tdnf.createPackagesRepoFile()
        tdnf.run(
            args=subCmd + RepoUtil.getPackagesRepoArgs(),
            errMsg="Unable to install desired version of BRs/ExtraBRs",
        )
