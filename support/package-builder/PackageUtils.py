#!/usr/bin/env python3

import os
import shutil
import re
import random
import string
import PullSources

from CommandUtils import CommandUtils
from Logger import Logger
from constants import constants
from SpecData import SPECS


class PackageUtils(object):
    def __init__(self, logName=None, logPath=None):
        if logName is None:
            logName = "PackageUtils"
        if logPath is None:
            logPath = constants.logPath
        self.scriptDir = os.path.dirname(__file__)
        self.logName = logName
        self.logPath = logPath
        self.logger = Logger.getLogger(logName, logPath, constants.logLevel)
        self.rpmBinary = "rpm"
        self.installRPMPackageOptions = ["-Uv"]
        self.nodepsRPMPackageOptions = ["--nodeps"]

        self.rpmbuildBinary = "rpmbuild"
        self.rpmbuildBuildallOptions = ["--clean"]

        if constants.buildSrcRpm:
            self.rpmbuildBuildallOptions = ["-ba"] + self.rpmbuildBuildallOptions
        else:
            self.rpmbuildBuildallOptions = ["-bb"] + self.rpmbuildBuildallOptions

        self.rpmbuildNocheckOptions = ["--nocheck"]
        self.rpmbuildCheckOptions = ["-bi", "--clean"]
        self.queryRpmPackageOptions = ["-qa"]
        self.forceRpmPackageOptions = ["--force"]
        self.replaceRpmPackageOptions = ["--replacepkgs"]
        self.rpmFilesToInstallInAOneShot = []
        self.packagesToInstallInAOneShot = []
        self.noDepsRPMFilesToInstallInAOneShot = []
        self.noDepsPackagesToInstallInAOneShot = []
        self.logfnvalue = None

    def prepRPMforInstall(
        self, package, version, noDeps=False, destLogPath=None, arch=None
    ):
        if not arch:
            arch = constants.currentArch
        rpmfile = self.findRPMFile(package, version, arch)
        if rpmfile is None:
            self.logger.error(f"No rpm file found for package: {package}")
            raise Exception("Missing rpm file")

        rpmName = os.path.basename(rpmfile)
        # TODO: path from constants
        if "PUBLISHRPMS" in rpmfile:
            rpmDestFile = "/publishrpms/"
        elif "PUBLISHXRPMS" in rpmfile:
            rpmDestFile = "/publishxrpms/"
        elif constants.inputRPMSPath and constants.inputRPMSPath in rpmfile:
            rpmDestFile = "/inputrpms/"
        else:
            rpmDestFile = os.path.join(
                constants.topDirPath,
                "RPMS",
                arch if "noarch" not in rpmfile else "noarch",
                rpmName,
            )

        if noDeps:
            self.noDepsRPMFilesToInstallInAOneShot.append(rpmDestFile)
            self.noDepsPackagesToInstallInAOneShot.append(package)
        else:
            self.rpmFilesToInstallInAOneShot.append(rpmDestFile)
            self.packagesToInstallInAOneShot.append(package)

    def installRPMSInOneShot(self, sandbox, arch):
        rpmInstallcmd = [self.rpmBinary] + self.installRPMPackageOptions
        if constants.crossCompiling and arch == constants.targetArch:
            rpmInstallcmd += [
                "--ignorearch",
                "--noscripts",
                "--root",
                "/target-{constants.targetArch}",
            ]

        # TODO: Container sandbox might need  + self.forceRpmPackageOptions
        if self.noDepsRPMFilesToInstallInAOneShot:
            self.logger.debug(
                f"Installing nodeps rpms: {self.noDepsPackagesToInstallInAOneShot}"
            )
            cmd = (
                rpmInstallcmd
                + self.nodepsRPMPackageOptions
                + self.noDepsRPMFilesToInstallInAOneShot
            )
            self.logger.debug(f"Command: {cmd}")
            try:
                sandbox.runCmd(cmd, logfn=self.logger.debug)
            except Exception as e:
                self.logger.error("Unable to install nodeps rpms")
                self.logger.exception(e)
                raise
        if self.rpmFilesToInstallInAOneShot:
            self.logger.debug(f"Installing rpms: {self.packagesToInstallInAOneShot}")
            cmd = rpmInstallcmd + self.rpmFilesToInstallInAOneShot
            self.logger.debug(f"Command: {cmd}")
            try:
                sandbox.runCmd(cmd, logfn=self.logger.debug)
            except Exception as e:
                self.logger.error("Unable to install rpms")
                self.logger.exception(e)
                raise

    def buildRPMSForGivenPackage(self, sandbox, package, version, destLogPath):
        self.logger.info(f"Building package: {package}")

        listSourcesFiles = SPECS.getData().getSources(package, version)
        listPatchFiles = SPECS.getData().getPatches(package, version)
        specFile = SPECS.getData().getSpecFile(package, version)
        specName = SPECS.getData().getSpecName(package) + ".spec"
        sourcePath = os.path.join(constants.topDirPath, "SOURCES")
        sandboxSpecPath = os.path.join(constants.topDirPath, "SPECS", specName)
        if (
            constants.rpmCheck
            and package in constants.testForceRPMS
            and SPECS.getData().isCheckAvailable(package, version)
        ):
            logFilePath = os.path.join(destLogPath, f"{package}-test.log")
        else:
            logFilePath = os.path.join(destLogPath, f"{package}.log")
        sandbox.putFiles(specFile, sandboxSpecPath)

        sources_urls, macros = self._getAdditionalBuildOptions(package)
        self.logger.debug(f"Extra macros for {package}: " + str(macros))
        self.logger.debug(f"Extra source URLs for {package}: " + str(sources_urls))
        constants.setExtraSourcesURLs(package, sources_urls)

        self._copySources(sandbox, listSourcesFiles, package, version, sourcePath)
        self._copySources(sandbox, listPatchFiles, package, version, sourcePath)

        # Adding rpm macros
        listRPMMacros = constants.userDefinedMacros
        for macroName, value in listRPMMacros.items():
            macros.append(f"{macroName} {value}")

        listRPMFiles = []
        listSRPMFiles = []
        try:
            listRPMFiles, listSRPMFiles = self._buildRPM(
                sandbox, sandboxSpecPath, logFilePath, package, version, macros
            )

            if constants.rpmCheck:
                return listRPMFiles, listSRPMFiles

            logmsg = ""
            RpmsToCheck = []
            self.logger.debug(f"Checking for debug symbols in built rpms of: {package}")
            for f in listRPMFiles:
                f = os.path.basename(f)
                logmsg += f"{f} "
                if f.find("-debuginfo-") < 0:
                    RpmsToCheck.append(f)

            if self.CheckForDbgSymbols(RpmsToCheck):
                raise Exception("Rpm sanity check error")

            logmsg = f"{package} build done - RPMs: [ {logmsg}]\n"
            self.logger.info(logmsg)
        except Exception as e:
            self.logger.error(f"Failed while building rpm: {package}")
            raise e
        self.logger.debug("RPM build is successful")
        return listRPMFiles, listSRPMFiles

    """
    Check for unintended debug symbols in rpm. If present, stop the build.
    Upon rerun rpm won't be rebuilt but devs should carefully examine the faulty rpms.
    """

    def CheckForDbgSymbols(self, RpmsToCheck):
        dbg_symbols_found = False
        faulty_rpms = set()
        prohibited_files = []

        for rpm in RpmsToCheck:
            arch = rpm.split(".")[-2]
            rpm_full_path = os.path.join(constants.rpmPath, arch, rpm)
            cmd = [self.rpmBinary, "-qlp", rpm_full_path]
            out, _, _ = CommandUtils.runCmd(cmd, capture=True)
            for fn in CommandUtils.splitlines(out):
                if fn.startswith("/usr/lib/debug/.build-id"):
                    faulty_rpms.add(rpm_full_path)
                    prohibited_files.append(fn)

        if faulty_rpms:
            self.logger.error("Debug symbols found in following rpms:")
            self.logger.error("\n".join(faulty_rpms))
            self.logger.error("\n".join(prohibited_files))
            self.logger.error("Use 'rpm -qlp <rpm>' to know more on the issue\n")

        return dbg_symbols_found

    def findRPMFile(self, package, version="*", arch=None, throw=False):
        if not arch:
            arch = constants.currentArch

        if version == "*":
            version = SPECS.getData(arch).getHighestVersion(package)
        buildarch = SPECS.getData(arch).getBuildArch(package, version)
        filename = f"{package}-{version}.{buildarch}.rpm"

        fullpath = os.path.join(constants.rpmPath, buildarch, filename)
        if os.path.isfile(fullpath):
            return fullpath

        if constants.inputRPMSPath is not None:
            fullpath = os.path.join(constants.inputRPMSPath, buildarch, filename)
        if os.path.isfile(fullpath):
            return fullpath

        if throw:
            raise Exception(f"RPM {filename} not found")
        return None

    def findSourceRPMFile(self, package, version="*"):
        if version == "*":
            version = SPECS.getData().getHighestVersion(package)
        filename = f"{package}-{version}.src.rpm"

        fullpath = os.path.join(constants.sourceRpmPath, filename)
        if os.path.isfile(fullpath):
            return fullpath
        return None

    def findDebugRPMFile(self, package, version="*", arch=None):
        if not arch:
            arch = constants.currentArch

        if version == "*":
            version = SPECS.getData(arch).getHighestVersion(package)
        filename = f"{package}-debuginfo-{version}.{arch}.rpm"

        fullpath = os.path.join(constants.rpmPath, arch, filename)
        if os.path.isfile(fullpath):
            return fullpath
        return None

    def findInstalledRPMPackages(self, sandbox, arch):
        cmd = [self.rpmBinary] + self.queryRpmPackageOptions
        if constants.crossCompiling and arch == constants.targetArch:
            cmd += ["--root", f"/target-{constants.targetArch}"]
        out, _, _ = sandbox.runCmd(cmd, capture=True)
        return CommandUtils.splitlines(out)

    def adjustGCCSpecs(self, sandbox, package, version):
        if constants.adjustGCCSpecScript is None:
            self.logger.warning("adjust-gcc-specs script not specified, skipping...")
            return
        opt = SPECS.getData().getSecurityHardeningOption(package, version)
        if not opt:
            return
        cmd = [constants.adjustGCCSpecScript, opt]
        try:
            sandbox.runCmd(cmd, logfn=self.logger.debug)
        except Exception as e:
            # in debugging ...
            sandbox.runCmd(
                ["ls", "-la", constants.adjustGCCSpecScript],
                logfn=self.logger.debug,
                ignore_rc=True,
            )
            sandbox.runCmd(
                ["lsof", constants.adjustGCCSpecScript],
                logfn=self.logger.debug,
                ignore_rc=True,
            )
            sandbox.runCmd(["ps", "ax"], logfn=self.logger.debug, ignore_rc=True)

            self.logger.error("Failed while adjusting gcc specs")
            self.logger.exception(e)
            raise

    def copyFileToSandbox(self, sandbox, src, dest):
        if not os.path.isfile(src):
            raise Exception(f"'{src}' is not present ...")

        if not os.path.isabs(src):
            src = os.path.join(constants.photonDir, src)

        self.logger.debug(f"Copying {src} to {dest} in sandbox {sandbox.name}")
        sandbox.putFiles(src, dest)

    def _verifyShaAndGetSourcePath(self, source, package, version):
        # Fetch/verify sources if checksum not None.
        checksum = SPECS.getData().getChecksum(package, version, source)
        if checksum is not None:
            PullSources.get(
                package,
                source,
                checksum,
                constants.sourcePath,
                constants.getPullSourcesURLs(package),
                self.logger,
            )

        sourcePath = CommandUtils.findFile(source, constants.sourcePath)
        if not sourcePath:
            sourcePath = CommandUtils.findFile(
                source, os.path.dirname(SPECS.getData().getSpecFile(package, version))
            )
            if not sourcePath:
                if checksum is None:
                    msg = f"No checksum found or missing source for {source}"
                else:
                    msg = f"Missing source: {source}. Cannot find sources for package: {package}"
                self.logger.error(msg)
                raise Exception(msg)
        else:
            if checksum is None:
                msg = f"No checksum found for {source}"
                self.logger.error(msg)
                raise Exception(msg)
        if len(sourcePath) > 1:
            self.logger.error(
                f"Multiple sources found for source: {source}\n"
                + ",".join(sourcePath)
                + "\nUnable to determine one."
            )
            raise Exception("Multiple sources found")
        return sourcePath

    def _copySources(self, sandbox, listSourceFiles, package, version, destDir):
        files_to_copy = []
        # Fetch and verify checksum if missing
        for source in listSourceFiles:
            sourcePath = self._verifyShaAndGetSourcePath(source, package, version)
            files_to_copy.extend(sourcePath)

        sandbox.putFiles(files_to_copy, destDir)

    def _getAdditionalBuildOptions(self, package):
        pullsources_urls = []
        macros = []
        if package in constants.buildOptions.keys():
            pkg = constants.buildOptions[package]
            pullsources_urls.extend(pkg["pullsources"])
            macros.extend(pkg["macros"])
        return pullsources_urls, macros

    def _buildRPM(self, sandbox, specFile, logFile, package, version, macros):
        make_check_na = False
        rpmBuildcmd = [self.rpmbuildBinary] + self.rpmbuildBuildallOptions

        if constants.resume_build:
            rpmBuildcmd += ["-D", "__spec_prep_cmd /bin/true"]

        if (
            not constants.buildDbgInfoRpm
            and package not in constants.buildDbgInfoRpmList
        ):
            rpmBuildcmd += ["-D", "debug_package %{nil}"]

        if constants.rpmCheck and package in constants.testForceRPMS:
            pr_pounds = "#" * (68 + 2 * len(package))
            self.logger.debug(pr_pounds)
            make_check_na = not SPECS.getData().isCheckAvailable(package, version)
            if not make_check_na:
                make_check_na = package in constants.listMakeCheckPkgToSkip

            if make_check_na:
                self.logger.info(
                    f"####### {package}"
                    + f" MakeCheck is not available. Skipping MakeCheck TEST for {package} #######"
                )
                rpmBuildcmd = [self.rpmbuildBinary, "--clean"]
            else:
                self.logger.info(
                    f"####### {package}"
                    + f" MakeCheck is available. Running MakeCheck TEST for {package} #######"
                )
                rpmBuildcmd = [self.rpmbuildBinary] + self.rpmbuildCheckOptions
            self.logger.debug(pr_pounds)
        else:
            rpmBuildcmd += self.rpmbuildNocheckOptions

        for macro in macros:
            rpmBuildcmd += ["-D", macro]

        if constants.crossCompiling:
            rpmBuildcmd += [
                "-D",
                f"_build {constants.buildArch}-unknown-linux-gnu",
                "-D",
                f"_host {constants.targetArch}-unknown-linux-gnu",
                f"--target={constants.targetArch}-unknown-linux-gnu",
            ]

        rpmBuildcmd += [specFile]

        self.logger.debug(f"Building rpm....\n{rpmBuildcmd}")

        network_required = SPECS.getData().isNetworkRequired(package, version)
        if network_required:
            self.logger.debug(f"{package} requires network to build...")

        with open(logFile, "w") as logfp:
            _, _, returnVal = sandbox.runCmd(
                rpmBuildcmd,
                logfile=logfp,
                ignore_rc=True,
                network_required=network_required,
            )

        if constants.rpmCheck and package in constants.testForceRPMS:
            if make_check_na:
                constants.testLogger.info(f"{package}: N/A")
            elif returnVal == 0:
                constants.testLogger.info(f"{package}: PASS")
            else:
                constants.testLogger.info(f"{package}: FAIL")

        if constants.rpmCheck:
            if returnVal and constants.rpmCheckStopOnError:
                msg = f"RPM check is failed for {specFile}"
                self.logger.error(msg)
                raise Exception(msg)
            return [], []
        else:
            if returnVal:
                msg = f"Building rpm is failed {specFile}"
                self.logger.error(msg)
                raise Exception(msg)

        out, err, _ = CommandUtils.runCmd(
            ["sed", "-nr", "s/^Wrote: (.*)$/\\1/p", logFile], capture=True
        )
        rpmsBuilt = CommandUtils.splitlines(out)

        listRPMFiles = []
        listSRPMFiles = []
        for rpm in rpmsBuilt:
            if "/RPMS/" in rpm:
                listRPMFiles.append(rpm)
            elif "/SRPMS/" in rpm:
                listSRPMFiles.append(rpm)

        return listRPMFiles, listSRPMFiles
