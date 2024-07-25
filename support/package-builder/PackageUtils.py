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
        self.cmdUtils = CommandUtils()
        self.rpmBinary = "rpm"
        self.installRPMPackageOptions = "-Uv"
        self.nodepsRPMPackageOptions = "--nodeps"

        self.rpmbuildBinary = "rpmbuild"
        self.rpmbuildBuildallOption = "--clean"

        if constants.buildSrcRpm:
            self.rpmbuildBuildallOption = f"-ba {self.rpmbuildBuildallOption}"
        else:
            self.rpmbuildBuildallOption = f"-bb {self.rpmbuildBuildallOption}"

        self.rpmbuildNocheckOption = "--nocheck"
        self.rpmbuildCheckOption = "-bi --clean"
        self.queryRpmPackageOptions = "-qa"
        self.forceRpmPackageOptions = "--force"
        self.replaceRpmPackageOptions = "--replacepkgs"
        self.adjustGCCSpecScript = "adjust-gcc-specs.sh"
        self.rpmFilesToInstallInAOneShot = ""
        self.packagesToInstallInAOneShot = ""
        self.noDepsRPMFilesToInstallInAOneShot = ""
        self.noDepsPackagesToInstallInAOneShot = ""
        self.logfnvalue = None

    def prepRPMforInstall(self, package, version, noDeps=False, destLogPath=None, arch=None):
        if not arch:
            arch=constants.currentArch
        rpmfile = self.findRPMFile(package, version, arch)
        if rpmfile is None:
            self.logger.error(f"No rpm file found for package: {package}")
            raise Exception("Missing rpm file")

        rpmName = os.path.basename(rpmfile)
        #TODO: path from constants
        if "PUBLISHRPMS" in rpmfile:
            rpmDestFile = "/publishrpms/"
        elif "PUBLISHXRPMS" in rpmfile:
            rpmDestFile = "/publishxrpms/"
        elif constants.inputRPMSPath and constants.inputRPMSPath in rpmfile:
            rpmDestFile = "/inputrpms/"
        else:
            rpmDestFile = f"{constants.topDirPath}/RPMS/"

        if "noarch" in rpmfile:
            rpmDestFile += "noarch/"
        else:
            rpmDestFile += f"{arch}/"
        rpmDestFile += rpmName

        if noDeps:
            self.noDepsRPMFilesToInstallInAOneShot += f" {rpmDestFile}"
            self.noDepsPackagesToInstallInAOneShot += f" {package}"
        else:
            self.rpmFilesToInstallInAOneShot += f" {rpmDestFile}"
            self.packagesToInstallInAOneShot += f" {package}"

    def installRPMSInOneShot(self, sandbox, arch):
        rpmInstallcmd = f"{self.rpmBinary} {self.installRPMPackageOptions}"
        if constants.crossCompiling and arch == constants.targetArch:
            rpmInstallcmd += f" --ignorearch --noscripts --root /target-{constants.targetArch}"

        # TODO: Container sandbox might need  + self.forceRpmPackageOptions
        if self.noDepsRPMFilesToInstallInAOneShot != "":
            self.logger.debug(f"Installing nodeps rpms: {self.noDepsPackagesToInstallInAOneShot}")
            cmd = f"{rpmInstallcmd} {self.nodepsRPMPackageOptions} {self.noDepsRPMFilesToInstallInAOneShot}"
            if sandbox.run(cmd, logfn=self.logger.debug):
                self.logger.debug(f"Command Executed: {cmd}")
                self.logger.error("Unable to install rpms. Error {}".format(returnVal))
                raise Exception("RPM installation failed")
        if self.rpmFilesToInstallInAOneShot != "":
            self.logger.debug(f"Installing rpms: {self.packagesToInstallInAOneShot}")
            cmd = f"{rpmInstallcmd} {self.rpmFilesToInstallInAOneShot}"
            if sandbox.run(cmd, logfn=self.logger.debug):
                self.logger.debug(f"Command Executed: {cmd}")
                self.logger.error("Unable to install rpms")
                raise Exception("RPM installation failed")

    def buildRPMSForGivenPackage(self, sandbox, package, version, destLogPath):
        self.logger.info(f"Building package: {package}")

        listSourcesFiles = SPECS.getData().getSources(package, version)
        listPatchFiles = SPECS.getData().getPatches(package, version)
        specFile = SPECS.getData().getSpecFile(package, version)
        specName = SPECS.getData().getSpecName(package) + ".spec"
        sourcePath = f"{constants.topDirPath}/SOURCES/"
        specPath = f"{constants.topDirPath}/SPECS/"
        if (constants.rpmCheck and
            package in constants.testForceRPMS and
            SPECS.getData().isCheckAvailable(package, version)):
            logFilePath = f"{destLogPath}/{package}-test.log"
        else:
            logFilePath = f"{destLogPath}/{package}.log"
        sandbox.put(specFile, specPath + specName)

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
            listRPMFiles, listSRPMFiles = self._buildRPM(sandbox, f"{specPath}{specName}",
                                                         logFilePath, package, version, macros)

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
        logs = []
        result_logs = []
        faulty_rpms = []
        dbg_symbols_found = False
        look_for = "/usr/lib/debug/.build-id"

        def HandleLogs(log):
            nonlocal logs
            logs += log.split("\n")

        for fn in RpmsToCheck:
            logs = []
            rpm_full_path = f"{constants.rpmPath}/" + fn.split(".")[-2] + f"/{fn}"
            cmd = f"{self.rpmBinary} -qlp {rpm_full_path}"
            self.cmdUtils.runBashCmd(cmd, logfn=HandleLogs)
            if look_for in logs:
                result_logs += logs
                faulty_rpms.append(rpm_full_path)
                if not dbg_symbols_found:
                    dbg_symbols_found = True

        if dbg_symbols_found:
            self.logger.error("Debug symbols found in following rpms:")
            self.logger.error("\n".join(faulty_rpms))
            self.logger.error("\n".join(result_logs))
            self.logger.error("Use 'rpm -qlp <rpm>' to know more on the issue\n")

        return dbg_symbols_found

    def findRPMFile(self, package,version="*",arch=None, throw=False):
        if not arch:
            arch=constants.currentArch

        if version == "*":
            version = SPECS.getData(arch).getHighestVersion(package)
        buildarch=SPECS.getData(arch).getBuildArch(package, version)
        filename= f"{package}-{version}.{buildarch}.rpm"

        fullpath = f"{constants.rpmPath}/{buildarch}/{filename}"
        if os.path.isfile(fullpath):
            return fullpath

        if constants.inputRPMSPath is not None:
            fullpath = f"{constants.inputRPMSPath}/{buildarch}/{filename}"
        if os.path.isfile(fullpath):
            return fullpath

        if throw:
            raise Exception(f"RPM {filename} not found")
        return None

    def findSourceRPMFile(self, package,version="*"):
        if version == "*":
            version = SPECS.getData().getHighestVersion(package)
        filename= f"{package}-{version}.src.rpm"

        fullpath = f"{constants.sourceRpmPath}/{filename}"
        if os.path.isfile(fullpath):
            return fullpath
        return None

    def findDebugRPMFile(self, package,version="*",arch=None):
        if not arch:
            arch=constants.currentArch

        if version == "*":
            version = SPECS.getData(arch).getHighestVersion(package)
        filename= f"{package}-debuginfo-{version}.{arch}.rpm"

        fullpath = f"{constants.rpmPath}/{arch}/{filename}"
        if os.path.isfile(fullpath):
            return fullpath
        return None

    def findInstalledRPMPackages(self, sandbox, arch):
        rpms = None
        def setOutValue(data):
            nonlocal rpms
            rpms = data
        cmd = f"{self.rpmBinary} {self.queryRpmPackageOptions}"
        if constants.crossCompiling and arch == constants.targetArch:
            cmd += f" --root /target-{constants.targetArch}"
        sandbox.run(cmd, logfn=setOutValue)
        return rpms.split()

    def adjustGCCSpecs(self, sandbox, package, version):
        opt = " " + SPECS.getData().getSecurityHardeningOption(package, version)
        cmd = f"/tmp/{self.adjustGCCSpecScript}{opt}"
        if not sandbox.run(cmd, logfn=self.logger.debug):
            return

        # in debugging ...
        sandbox.run(f"ls -la /tmp/{self.adjustGCCSpecScript}", logfn=self.logger.debug)
        sandbox.run(f"lsof /tmp/{self.adjustGCCSpecScript}", logfn=self.logger.debug)
        sandbox.run("ps ax", logfn=self.logger.debug)

        self.logger.error("Failed while adjusting gcc specs")
        raise Exception("Failed while adjusting gcc specs")

    def copyFileToSandbox(self, sandbox, src, dest):
        if not os.path.isfile(src):
            raise Exception(f"'{src}' is not present ...")

        if not os.path.isabs(src):
            src = f"{constants.photonDir}/{src}"

        sandbox.put(src, dest)

    def _verifyShaAndGetSourcePath(self, source, package, version):
        # Fetch/verify sources if checksum not None.
        checksum = SPECS.getData().getChecksum(package, version, source)
        if checksum is not None:
            PullSources.get(package, source, checksum, constants.sourcePath,
                            constants.getPullSourcesURLs(package), self.logger)

        sourcePath = self.cmdUtils.findFile(source, constants.sourcePath)
        if not sourcePath:
            sourcePath = self.cmdUtils.findFile(source, os.path.dirname(SPECS.getData().getSpecFile(package, version)))
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
            self.logger.error(f"Multiple sources found for source: {source}\n" +
                              ",".join(sourcePath) +"\nUnable to determine one.")
            raise Exception("Multiple sources found")
        return sourcePath

    def _copySources(self, sandbox, listSourceFiles, package, version, destDir):
        files_to_copy = []
        # Fetch and verify checksum if missing
        for source in listSourceFiles:
            sourcePath = self._verifyShaAndGetSourcePath(source, package, version)
            files_to_copy.extend(sourcePath)

        if files_to_copy:
            sandbox.put_list_of_files(files_to_copy, destDir)

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
        rpmBuildcmd = f"{self.rpmbuildBinary} {self.rpmbuildBuildallOption}"

        if constants.resume_build:
            rpmBuildcmd += f" -D \"__spec_prep_cmd /bin/true\" "

        if not constants.buildDbgInfoRpm and package not in constants.buildDbgInfoRpmList:
            rpmBuildcmd += " -D \"debug_package %{nil}\" "

        if constants.rpmCheck and package in constants.testForceRPMS:
            pr_pounds = "#" * (68 + 2 * len(package))
            self.logger.debug(pr_pounds)
            make_check_na = not SPECS.getData().isCheckAvailable(package, version)
            if not make_check_na:
                make_check_na = package in constants.listMakeCheckPkgToSkip

            if make_check_na:
                self.logger.info(f"####### {package}" +
                                 f" MakeCheck is not available. Skipping MakeCheck TEST for {package} #######")
                rpmBuildcmd = f"{self.rpmbuildBinary} --clean"
            else:
                self.logger.info(f"####### {package}" +
                                 f" MakeCheck is available. Running MakeCheck TEST for {package} #######")
                rpmBuildcmd = f"{self.rpmbuildBinary} {self.rpmbuildCheckOption}"
            self.logger.debug(pr_pounds)
        else:
            rpmBuildcmd += f" {self.rpmbuildNocheckOption}"

        for macro in macros:
            rpmBuildcmd += f" -D \"{macro}\""

        if constants.crossCompiling:
            rpmBuildcmd += (
                f" -D \"_build {constants.buildArch}-unknown-linux-gnu\""
                f" -D \"_host {constants.targetArch}-unknown-linux-gnu\""
                f" --target={constants.targetArch}-unknown-linux-gnu"
            )

        rpmBuildcmd += f" {specFile}"

        self.logger.debug(f"Building rpm....\n{rpmBuildcmd}")

        network_required = SPECS.getData().isNetworkRequired(package, version)
        if network_required:
            self.logger.debug(f"{package} requires network to build...")

        returnVal = sandbox.run(rpmBuildcmd, logfile=logFile, network_required=network_required)

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

        # Fetch built rpm names from log file
        fileContents = []
        stageLogFile = logFile.replace(f"{constants.topDirPath}/LOGS", constants.logPath)

        def HandleLogs(log):
            nonlocal fileContents
            fileContents += log.split("\n")

        cmd = f"grep -aw \"^Wrote: \" {stageLogFile}"
        (_, _, returnVal) = self.cmdUtils.runBashCmd(cmd, logfn=HandleLogs)

        if returnVal or not fileContents:
            msg = f"{stageLogFile} doesn't have 'Wrote: ' entries"
            self.logger.error(msg)
            raise Exception(msg)

        listRPMFiles = []
        listSRPMFiles = []
        for line in fileContents:
            if line:
                listcontents = line.split()
                if "/RPMS/" in listcontents[1]:
                    listRPMFiles.append(listcontents[1])
                elif "/SRPMS/" in listcontents[1]:
                    listSRPMFiles.append(listcontents[1])

        return listRPMFiles, listSRPMFiles
