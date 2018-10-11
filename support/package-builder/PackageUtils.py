import os
import platform
import shutil
import re
import random
import string
from CommandUtils import CommandUtils
from Logger import Logger
from constants import constants
import PullSources
from SpecData import SPECS
from distutils.version import LooseVersion

class PackageUtils(object):

    def __init__(self, logName=None, logPath=None):
        if logName is None:
            logName = "PackageUtils"
        if logPath is None:
            logPath = constants.logPath
        self.logName = logName
        self.logPath = logPath
        self.logger = Logger.getLogger(logName, logPath, constants.logLevel)
        self.runInChrootCommand = ("./run-in-chroot.sh " + constants.sourcePath +
                                   " " + constants.rpmPath)
        self.rpmBinary = "rpm"
        self.installRPMPackageOptions = "-Uvh"
        self.nodepsRPMPackageOptions = "--nodeps"

        self.rpmbuildBinary = "rpmbuild"
        self.rpmbuildBuildallOption = "-ba --clean"
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
        self.rpmFilesToReInstallInAOneShot = ""
        self.noDepsRPMFilesToReInstallInAOneShot = ""

    def installRPM(self, package,version, chrootID, noDeps=False, destLogPath=None):

        rpmfile = self.findRPMFileForGivenPackage(package,version)
        if rpmfile is None:
            self.logger.error("No rpm file found for package:" + package)
            raise Exception("Missing rpm file: " + package)

        rpmDestFile = self._copyRPM(rpmfile, chrootID + constants.topDirPath + "/RPMS")
        rpmFile = rpmDestFile.replace(chrootID, "")
        if noDeps:
            self.noDepsRPMFilesToInstallInAOneShot += " " + rpmFile
            self.noDepsPackagesToInstallInAOneShot += " " + package
        else:
            self.rpmFilesToInstallInAOneShot += " " + rpmFile
            self.packagesToInstallInAOneShot += " " + package

    def installRPMSInAOneShot(self, chrootID, destLogPath):
        chrootCmd = self.runInChrootCommand + " " + chrootID
        rpmInstallcmd = self.rpmBinary + " " + self.installRPMPackageOptions
        cmdUtils = CommandUtils()
        if self.noDepsRPMFilesToInstallInAOneShot != "":
            self.logger.debug("Installing nodeps rpms: " +
                             self.noDepsPackagesToInstallInAOneShot)
            logFile = destLogPath + "/install_rpms_nodeps.log"
            cmd = (rpmInstallcmd+" "+self.nodepsRPMPackageOptions + " " +
                   self.noDepsRPMFilesToInstallInAOneShot)
            returnVal = cmdUtils.runCommandInShell(cmd, logFile, chrootCmd)
            if not returnVal:
                self.logger.debug("Command Executed:" + cmd)
                self.logger.error("Unable to install rpms")
                raise Exception("RPM installation failed")
        if self.rpmFilesToInstallInAOneShot != "":
            self.logger.debug("Installing rpms: " + self.packagesToInstallInAOneShot)
            logFile = destLogPath+"/install_rpms.log"
            cmd = rpmInstallcmd+" "+self.rpmFilesToInstallInAOneShot
            returnVal = cmdUtils.runCommandInShell(cmd, logFile, chrootCmd)
            if not returnVal:
                self.logger.debug("Command Executed:" + cmd)
                self.logger.error("Unable to install rpms")
                raise Exception("RPM installation failed")

    def buildRPMSForGivenPackage(self, package, version, chrootID, destLogPath=None):
        self.logger.info("Building package : " + package)

        listSourcesFiles = SPECS.getData().getSources(package, version)
        listPatchFiles = SPECS.getData().getPatches(package, version)
        specFile = SPECS.getData().getSpecFile(package, version)
        specName = SPECS.getData().getSpecName(package) + ".spec"

        chrootSourcePath = chrootID + constants.topDirPath + "/SOURCES/"
        chrootSpecPath = constants.topDirPath + "/SPECS/"
        chrootLogsFilePath = chrootID + constants.topDirPath + "/LOGS/" + package + ".log"
        chrootCmd = self.runInChrootCommand + " " + chrootID
        shutil.copyfile(specFile, chrootID + chrootSpecPath + specName)

        sources_urls, macros = self._getAdditionalBuildOptions(package)
        self.logger.debug("Extra macros for " + package + ": " + str(macros))
        self.logger.debug("Extra source URLs for " + package + ": " + str(sources_urls))
        constants.setExtraSourcesURLs(sources_urls)

        # FIXME: some sources are located in SPECS/.. how to mount?
        #        if os.geteuid()==0:
        self._copySourcesTobuildroot(listSourcesFiles, package, version, chrootSourcePath)
        self._copySourcesTobuildroot(listPatchFiles, package, version, chrootSourcePath)

        #Adding rpm macros
        listRPMMacros = constants.userDefinedMacros
        for macroName, value in listRPMMacros.items():
            macros.append(macroName + " " + value)

        listRPMFiles = []
        listSRPMFiles = []
        try:
            listRPMFiles, listSRPMFiles = self._buildRPM(chrootSpecPath + specName,
                                                         chrootLogsFilePath, chrootCmd,
                                                         package, macros)
            logmsg = package + " build done - RPMs : [ "
            for f in listRPMFiles:
                logmsg += (os.path.basename(f) + " ")
            logmsg += "]\n"
            self.logger.info(logmsg)
        except Exception as e:
            self.logger.error("Failed while building rpm:" + package)
            raise e
        finally:
            if destLogPath is not None:
                if (constants.rpmCheck and
                        package in constants.testForceRPMS and
                        SPECS.getData().isCheckAvailable(package)):
                    cmd = ("sed -i '/^Executing(%check):/,/^Processing files:/{//!b};d' " +
                           chrootLogsFilePath)
                    logFile = destLogPath + "/adjustTestFile.log"
                    returnVal = CommandUtils().runCommandInShell(cmd, logFile)
                    testLogFile = destLogPath + "/" + package + "-test.log"
                    shutil.copyfile(chrootLogsFilePath, testLogFile)
                else:
                    shutil.copy2(chrootLogsFilePath, destLogPath)
        self.logger.debug("RPM build is successful")

        for rpmFile in listRPMFiles:
            self._copyRPM(chrootID + "/" + rpmFile, constants.rpmPath)

        for srpmFile in listSRPMFiles:
            srpmDestFile = self._copyRPM(chrootID + "/" + srpmFile, constants.sourceRpmPath)

    def findRPMFileForGivenPackage(self, package,version="*"):
        cmdUtils = CommandUtils()
        if version == "*":
                version = SPECS.getData().getHighestVersion(package)
        release = SPECS.getData().getRelease(package, version)
        buildarch=SPECS.getData().getBuildArch(package, version)
        listFoundRPMFiles = sum([cmdUtils.findFile(package + "-" + version + "-" + release + "." +
                                                   buildarch+".rpm",
                                                   constants.rpmPath)], [])
        if constants.inputRPMSPath is not None:
            listFoundRPMFiles = sum([cmdUtils.findFile(package + "-" + version + "-" + release +
                                                       "." + buildarch+".rpm",
                                                       constants.inputRPMSPath)],
                                    listFoundRPMFiles)
        if len(listFoundRPMFiles) == 1:
            return listFoundRPMFiles[0]
        if len(listFoundRPMFiles) == 0:
            return None
        if len(listFoundRPMFiles) > 1:
            self.logger.error("Found multiple rpm files for given package in rpm directory." +
                              "Unable to determine the rpm file for package:" + package +
                              " : " + str(listFoundRPMFiles))
            raise Exception("Multiple rpm files found")

    def findInstalledRPMPackages(self, chrootID):
        cmd = self.rpmBinary + " " + self.queryRpmPackageOptions
        chrootCmd = self.runInChrootCommand + " " + chrootID
        cmdUtils = CommandUtils()
        result = cmdUtils.runCommandInShell2(cmd, chrootCmd)
        if result is not None:
            return result.decode().split()
        return result

    def adjustGCCSpecs(self, package, version, chrootID, logPath):
        opt = " " + SPECS.getData().getSecurityHardeningOption(package, version)
        cmdUtils = CommandUtils()
        cpcmd = ("cp " + self.adjustGCCSpecScript + " " + chrootID +
                 "/tmp/" + self.adjustGCCSpecScript)
        cmd = "/tmp/" + self.adjustGCCSpecScript + opt
        logFile = logPath + "/adjustGCCSpecScript.log"
        chrootCmd = self.runInChrootCommand + " " + chrootID
        returnVal = cmdUtils.runCommandInShell(cpcmd, logFile)
        if not returnVal:
            self.logger.error("Error during copying the file adjust gcc spec")
            raise Exception("Failed while copying adjust gcc spec file")
        returnVal = cmdUtils.runCommandInShell(cmd, logFile, chrootCmd)
        if returnVal:
            return

        self.logger.debug(cmdUtils.runCommandInShell2("ls -la " + chrootID +
                                                      "/tmp/" + self.adjustGCCSpecScript))
        self.logger.debug(cmdUtils.runCommandInShell2("lsof " + chrootID + "/tmp/" +
                                                      self.adjustGCCSpecScript))
        self.logger.debug(cmdUtils.runCommandInShell2("ps ax"))

        self.logger.error("Failed while adjusting gcc specs")
        raise Exception("Failed while adjusting gcc specs")

    def prepRPMforInstallInContainer(self, package,version, containerID, noDeps=False, destLogPath=None):
        rpmfile = self.findRPMFileForGivenPackage(package,version)
        if rpmfile is None:
            self.logger.error("No rpm file found for package: " + package)
            raise Exception("Missing rpm file")

        rpmDestFile = self._getRPMPathInContainer(rpmfile, containerID)
        if noDeps:
            self.noDepsRPMFilesToInstallInAOneShot += " " + rpmDestFile
            self.noDepsPackagesToInstallInAOneShot += " " + package
            if package in constants.listReInstallPackages:
                self.noDepsRPMFilesToReInstallInAOneShot += " " + rpmDestFile
        else:
            self.rpmFilesToInstallInAOneShot += " " + rpmDestFile
            self.packagesToInstallInAOneShot += " " + package
            if package in constants.listReInstallPackages:
                self.rmpFilesToReInstallInAOneShot += " " + rpmDestFile

    def installRPMSInAOneShotInContainer(self, containerID, destLogPath):
        rpmInstallcmd = (self.rpmBinary + " " + self.installRPMPackageOptions + " " +
                         self.forceRpmPackageOptions)

        if self.noDepsRPMFilesToInstallInAOneShot != "":
            self.logger.debug("PackageUtils-installRPMSInAOneShotInContainer: " +
                             "Installing nodeps rpms: " +
                             self.noDepsPackagesToInstallInAOneShot)
            logFile = destLogPath + "/install_rpms_nodeps.log"
            cmd = (rpmInstallcmd + " " + self.nodepsRPMPackageOptions + " " +
                   self.noDepsRPMFilesToInstallInAOneShot)
            cmd = "/bin/bash -l -c '" + cmd + "'"
            #self.logger.debug("VDBG-PU-installRPMSInAOneShotInContainer: " +
            #                  "Install nodeps cmd: " + cmd)
            #TODO: Error code from exec_run
            installLog = containerID.exec_run(cmd)
            if not installLog:
                self.logger.error("Unable to install nodeps rpms")
                raise Exception("nodeps RPM installation failed")
            with open(logFile, 'w') as logfile:
                logfile.write(installLog.decode())

            if self.noDepsRPMFilesToReInstallInAOneShot != "":
                cmd = (rpmInstallcmd + " " + self.nodepsRPMPackageOptions + " " +
                       self.forceRpmPackageOptions + " " +
                       self.noDepsRPMFilesToReInstallInAOneShot)
                cmd = "/bin/bash -l -c '" + cmd + "'"
                #self.logger.debug("VDBG-PU-installRPMSInAOneShotInContainer: " +
                #                  "ReInstall nodeps cmd: " + cmd)
                #TODO: Error code from exec_run
                installLog = containerID.exec_run(cmd)
                if not installLog:
                    self.logger.error("Unable to re-install nodeps rpms")
                    raise Exception("nodeps RPM re-installation failed")
                with open(logFile, 'a') as logfile:
                    logfile.write(installLog.decode())

        if self.rpmFilesToInstallInAOneShot != "":
            self.logger.debug("PackageUtils-installRPMSInAOneShotInContainer: Installing rpms: " +
                             self.packagesToInstallInAOneShot)
            logFile = destLogPath + "/install_rpms.log"
            cmd = rpmInstallcmd + " " + self.rpmFilesToInstallInAOneShot
            cmd = "/bin/bash -l -c '" + cmd + "'"
            #self.logger.debug("VDBG-PU-installRPMSInAOneShotInContainer: Install cmd: " + cmd)
            #TODO: Error code from exec_run
            installLog = containerID.exec_run(cmd)
            if not installLog:
                self.logger.error("Unable to install rpms")
                raise Exception("RPM installation failed")
            with open(logFile, 'w') as logfile:
                logfile.write(installLog.decode())

            if self.rpmFilesToReInstallInAOneShot != "":
                cmd = (rpmInstallcmd + " " + self.forceRpmPackageOptions + " " +
                       self.rpmFilesToReInstallInAOneShot)
                cmd = "/bin/bash -l -c '" + cmd + "'"
                #self.logger.debug("VDBG-PU-installRPMSInAOneShotInContainer: " +
                #                  "ReInstall cmd: " + cmd)
                #TODO: Error code from exec_run
                installLog = containerID.exec_run(cmd)
                if not installLog:
                    self.logger.error("Unable to re-install rpms")
                    raise Exception("RPM re-installation failed")
                with open(logFile, 'a') as logfile:
                    logfile.write(installLog.decode())

    def findInstalledRPMPackagesInContainer(self, containerID):
        cmd = self.rpmBinary + " " + self.queryRpmPackageOptions
        cmd = "/bin/bash -l -c '" + cmd + "'"
        #TODO: Error code from exec_run
        result = containerID.exec_run(cmd)
        if result is not None:
            return result.decode().split()
        return result

    def adjustGCCSpecsInContainer(self, package, version, containerID, logPath):
        opt = " " + SPECS.getData().getSecurityHardeningOption(package, version)
        adjustCmd = "/" + self.adjustGCCSpecScript + opt
        adjustCmd = "/bin/bash -l -c '" + adjustCmd + "'"
        logFile = logPath + "/adjustGCCSpecScript.log"

        #TODO: Error code from exec_run
        scriptLog = containerID.exec_run(adjustCmd)
        if scriptLog:
            with open(logFile, 'w') as logfile:
                logfile.write(scriptLog.decode())
            return

        self.logger.debug(containerID.exec_run("ls -la /tmp/" + self.adjustGCCSpecScript))
        self.logger.debug(containerID.exec_run("lsof /tmp/" + self.adjustGCCSpecScript))
        self.logger.debug(containerID.exec_run("ps ax"))
        self.logger.error("Failed while adjusting gcc specs")
        raise Exception("Failed while adjusting gcc specs")

    def buildRPMSForGivenPackageInContainer(self, package, version, containerID, destLogPath=None):
        self.logger.debug("Building rpms for package " + package + " in container " +
                         containerID.short_id)

        listSourcesFiles = SPECS.getData().getSources(package, version)
        listPatchFiles = SPECS.getData().getPatches(package, version)
        specFile = SPECS.getData().getSpecFile(package, version)
        specName = SPECS.getData().getSpecName(package) + ".spec"
        sourcePath = constants.topDirPath + "/SOURCES/"
        specPath = constants.topDirPath + "/SPECS/"
        rpmLogFile = constants.topDirPath + "/LOGS/" + package + ".log"
        destLogFile = destLogPath + "/" + package + ".log"
        cmdUtils = CommandUtils()

        #TODO: mount it in, don't copy
        cpSpecCmd = "docker cp " + specFile + " " + containerID.short_id \
                        + ":" + specPath + specName
        returnVal = cmdUtils.runCommandInShell(cpSpecCmd)
        if not returnVal:
            self.logger.error("Error copying source SPEC file to container")
            raise Exception("Failed copying source SPEC to container")

        macros = []
        sources_urls, macros = self._getAdditionalBuildOptions(package)
        constants.setExtraSourcesURLs(sources_urls)

        #FIXME: some sources are located in SPECS/.. how to mount?
        #        if os.geteuid()==0:
        #TODO: mount it in, don't copy
        self._copySourcesToContainer(listSourcesFiles, package, version, containerID, sourcePath)
        #TODO: mount it in, don't copy
        self._copySourcesToContainer(listPatchFiles, package, version, containerID, sourcePath)

        # Add rpm macros
        listRPMMacros = constants.userDefinedMacros
        for macroName, value in listRPMMacros.items():
            macros.append(macroName + " " + value)

        # Build RPMs
        listRPMFiles = []
        listSRPMFiles = []
        try:
            listRPMFiles, listSRPMFiles = self._buildRPMinContainer(
                specPath + specName,
                rpmLogFile,
                destLogFile,
                containerID,
                package,
                version,
                macros)
            logmsg = "Successfully built " + package + " - RPMs : [" + "".join(os.path.basename(listRPMFiles)) + "]"
            self.logger.info(logmsg)
        except Exception as e:
            self.logger.error("Failed while building rpm: " + package)
            raise e
        finally:
            if destLogPath is not None:
                rpmLog = destLogPath + "/" + package + ".log"
                if (constants.rpmCheck and
                        package in constants.testForceRPMS and
                        SPECS.getData().isCheckAvailable(package, version)):
                    cmd = "sed -i '/^Executing(%check):/,/^Processing files:/{//!b};d' " + rpmLog
                    logFile = destLogPath + "/adjustTestFile.log"
                    returnVal = CommandUtils().runCommandInShell(cmd, logFile)
                    testLogFile = destLogPath + "/" + package + "-test.log"
                    shutil.copyfile(rpmLog, testLogFile)
        self.logger.debug("RPM build is successful")

        # Verify RPM and SRPM files exist as success criteria
        for rpmFile in listRPMFiles:
            rpmName = os.path.basename(rpmFile)
            rpmDestDir = self._getRPMDestDir(rpmName, constants.rpmPath)
            rpmDestFile = rpmDestDir + "/" + rpmName
            if not os.path.isfile(rpmDestFile):
                self.logger.error("Could not find RPM file: " + rpmDestFile)
                raise Exception("Built RPM file not found.")

        for srpmFile in listSRPMFiles:
            srpmName = os.path.basename(srpmFile)
            srpmDestDir = self._getRPMDestDir(os.path.basename(srpmFile), constants.sourceRpmPath)
            srpmDestFile = srpmDestDir + "/" + srpmName
            if not os.path.isfile(srpmDestFile):
                self.logger.error("Could not find RPM file: " + srpmDestFile)
                raise Exception("Built SRPM file not found.")

    def _getRPMArch(self, rpmName):
        arch = ""
        if "x86_64" in rpmName:
            arch = "x86_64"
        elif "aarch64" in rpmName:
            arch = "aarch64"
        elif "noarch" in rpmName:
            arch = "noarch"
        return arch

    def _getRPMDestDir(self, rpmName, rpmDir):
        arch = self._getRPMArch(rpmName)
        rpmDestDir = rpmDir + "/" + arch
        return rpmDestDir

    def _copyRPM(self, rpmFile, destDir):
        cmdUtils = CommandUtils()
        rpmName = os.path.basename(rpmFile)
        rpmDestDir = self._getRPMDestDir(rpmName, destDir)
        # shutil is not atomic. copy & move to ensure atomicity.
        rpmDestPath = rpmDestDir + "/" + rpmName
        rpmDestPathTemp = (rpmDestDir + "/." +
                           ''.join([random.choice(string.ascii_letters +
                                                  string.digits) for n in range(10)]))
        if os.geteuid() == 0:
            if not os.path.isdir(rpmDestDir):
                cmdUtils.runCommandInShell("mkdir -p " + rpmDestDir)
            shutil.copyfile(rpmFile, rpmDestPathTemp)
            shutil.move(rpmDestPathTemp, rpmDestPath)
        return rpmDestPath

    def _verifyShaAndGetSourcePath(self, source, package, version):
        cmdUtils = CommandUtils()
        # Fetch/verify sources if sha1 not None.
        sha1 = SPECS.getData().getSHA1(package, version, source)
        if sha1 is not None:
            PullSources.get(package, source, sha1, constants.sourcePath,
                            constants.getPullSourcesURLs(), self.logger)

        sourcePath = cmdUtils.findFile(source, constants.sourcePath)
        if not sourcePath:
            sourcePath = cmdUtils.findFile(source, constants.specPath)
            if not sourcePath:
                if sha1 is None:
                    self.logger.error("No sha1 found or missing source for " + source)
                    raise Exception("No sha1 found or missing source for " + source)
                else:
                    self.logger.error("Missing source: " + source +
                                      ". Cannot find sources for package: " + package)
                    raise Exception("Missing source")
        else:
            if sha1 is None:
                self.logger.error("No sha1 found for "+source)
                raise Exception("No sha1 found")
        if len(sourcePath) > 1:
            self.logger.error("Multiple sources found for source:" + source + "\n" +
                              ",".join(sourcePath) +"\nUnable to determine one.")
            raise Exception("Multiple sources found")
        return sourcePath

    def _copySourcesTobuildroot(self, listSourceFiles, package, version, destDir):
        for source in listSourceFiles:
            sourcePath = self._verifyShaAndGetSourcePath(source, package, version)
            self.logger.debug("Copying... Source path :" + source +
                             " Source filename: " + sourcePath[0])
            shutil.copy2(sourcePath[0], destDir)

    def _getAdditionalBuildOptions(self, package):
        pullsources_urls = []
        macros = []
        if package in constants.buildOptions.keys():
            pkg = constants.buildOptions[package]
            pullsources_urls.extend(pkg["pullsources"])
            macros.extend(pkg["macros"])
        return pullsources_urls, macros


    def _buildRPM(self, specFile, logFile, chrootCmd, package, macros):

        rpmBuildcmd = self.rpmbuildBinary + " " + self.rpmbuildBuildallOption

        if constants.rpmCheck and package in constants.testForceRPMS:
            self.logger.debug("#" * (68 + 2 * len(package)))
            if not SPECS.getData().isCheckAvailable(package):
                self.logger.debug("####### " + package +
                                 " MakeCheck is not available. Skipping MakeCheck TEST for " +
                                 package + " #######")
                rpmBuildcmd = self.rpmbuildBinary + " --clean"
            else:
                self.logger.debug("####### " + package +
                                 " MakeCheck is available. Running MakeCheck TEST for " +
                                 package + " #######")
                rpmBuildcmd = self.rpmbuildBinary + " " + self.rpmbuildCheckOption
            self.logger.debug("#" * (68 + 2 * len(package)))
        else:
            rpmBuildcmd += " " + self.rpmbuildNocheckOption

        for macro in macros:
            rpmBuildcmd += ' --define \\\"%s\\\"' % macro
        rpmBuildcmd += " " + specFile

        cmdUtils = CommandUtils()
        self.logger.debug("Building rpm....")
        self.logger.debug(rpmBuildcmd)
        returnVal = cmdUtils.runCommandInShell(rpmBuildcmd, logFile, chrootCmd)
        if constants.rpmCheck and package in constants.testForceRPMS:
            if not SPECS.getData().isCheckAvailable(package):
                constants.testLogger.debug(package + " : N/A")
            elif returnVal:
                constants.testLogger.debug(package + " : PASS")
            else:
                constants.testLogger.debug(package + " : FAIL")

        if constants.rpmCheck:
            if not returnVal and constants.rpmCheckStopOnError:
                self.logger.error("Checking rpm is failed " + specFile)
                raise Exception("RPM check failed")
        else:
            if not returnVal:
                self.logger.error("Building rpm is failed " + specFile)
                raise Exception("RPM build failed")

        #Extracting rpms created from log file
        listRPMFiles = []
        listSRPMFiles = []
        with open(logFile, 'r') as logfile:
            fileContents = logfile.readlines()
            for i in range(0, len(fileContents)):
                if re.search("^Wrote:", fileContents[i]):
                    listcontents = fileContents[i].split()
                    if ((len(listcontents) == 2) and
                            listcontents[1].strip().endswith(".rpm") and
                            "/RPMS/" in listcontents[1]):
                        listRPMFiles.append(listcontents[1])
                    if ((len(listcontents) == 2) and
                            listcontents[1].strip().endswith(".src.rpm") and
                            "/SRPMS/" in listcontents[1]):
                        listSRPMFiles.append(listcontents[1])
        return listRPMFiles, listSRPMFiles


    def _copySourcesToContainer(self, listSourceFiles, package, version, containerID, destDir):
        cmdUtils = CommandUtils()
        for source in listSourceFiles:
            sourcePath = self._verifyShaAndGetSourcePath(source, package, version)
            self.logger.debug("Copying source file: " + sourcePath[0])
            copyCmd = "docker cp " + sourcePath[0] + " " + containerID.short_id + ":" + destDir
            cmdUtils.runCommandInShell(copyCmd)

    def _getRPMPathInContainer(self, rpmFile, containerID):
        rpmName = os.path.basename(rpmFile)
        #TODO: Container path from constants
        if "PUBLISHRPMS" in rpmFile:
            rpmPath = "/publishrpms/"
        elif "PUBLISHXRPMS" in rpmFile:
            rpmPath = "/publishxrpms/"
        else:
            rpmPath = constants.topDirPath + "/RPMS/"
        if "noarch" in rpmFile:
            rpmPath += "noarch/"
        else:
            rpmPath += platform.machine()+"/"
        rpmPath += rpmName
        return rpmPath


    def _buildRPMinContainer(self, specFile, rpmLogFile, destLogFile, containerID, package, version, macros):

        rpmBuildCmd = self.rpmbuildBinary + " " + self.rpmbuildBuildallOption

        if constants.rpmCheck and package in constants.testForceRPMS:
            self.logger.debug("#" * (68 + 2 * len(package)))
            if not SPECS.getData().isCheckAvailable(package, version):
                self.logger.debug("####### " + package +
                                 " MakeCheck is not available. Skipping MakeCheck TEST for " +
                                 package + " #######")
                rpmBuildCmd = self.rpmbuildBinary + " --clean"
            else:
                self.logger.debug("####### " + package +
                                 " MakeCheck is available. Running MakeCheck TEST for " +
                                 package + " #######")
                rpmBuildCmd = self.rpmbuildBinary + " " + self.rpmbuildCheckOption
            self.logger.debug("#" * (68 + 2 * len(package)))
        else:
            rpmBuildCmd += " "+self.rpmbuildNocheckOption

        for macro in macros:
            rpmBuildCmd += ' --define \"%s\"' % macro
        rpmBuildCmd += " " + specFile
        rpmBuildCmd = "/bin/bash -l -c '" + rpmBuildCmd + " > " + rpmLogFile + " 2>&1'"
        rpmBuildCmd = "docker exec -t " + str(containerID.short_id) + " " + rpmBuildCmd

        cmdUtils = CommandUtils()
        self.logger.debug("Building rpm for package: " + package)
        #TODO: Show running log of rpmbuildcmd
        #TODO: Get exit status of rpmBuildCmd
        #containerID.exec_run(rpmBuildCmd)
        returnVal = cmdUtils.runCommandInShell(rpmBuildCmd)

        if not os.path.isfile(destLogFile):
            self.logger.error("RPM build not file not found. Building rpm failed for: " + specFile)
            raise Exception("RPM Build failed")

        if constants.rpmCheck and package in constants.testForceRPMS:
            if not SPECS.getData().isCheckAvailable(package, version):
                constants.testLogger.info(package + " : N/A")
            elif returnVal:
                constants.testLogger.info(package + " : PASS")
            else:
                constants.testLogger.error(package + " : FAIL")

        if constants.rpmCheck:
            if not returnVal and constants.rpmCheckStopOnError:
                self.logger.error("Checking rpm is failed " + specFile)
                raise Exception("RPM check failed")
        else:
            if not returnVal:
                self.logger.error("Building rpm is failed " + specFile)
                raise Exception("RPM build failed")

        #Extracting rpms created from log file
        listRPMFiles = []
        listSRPMFiles = []
        with open(destLogFile, 'r') as logfile:
            rpmBuildLogLines = logfile.readlines()
            for i in range(0, len(rpmBuildLogLines)):
                if re.search("^Wrote:", rpmBuildLogLines[i]):
                    listcontents = rpmBuildLogLines[i].split()
                    if ((len(listcontents) == 2) and
                            listcontents[1].strip().endswith(".rpm") and
                            "/RPMS/" in listcontents[1]):
                        listRPMFiles.append(listcontents[1])
                    if ((len(listcontents) == 2) and
                            listcontents[1].strip().endswith(".src.rpm") and
                            "/SRPMS/" in listcontents[1]):
                        listSRPMFiles.append(listcontents[1])
        #if not listRPMFiles:
        #    self.logger.error("Building rpm failed for " + specFile)
        #    raise Exception("RPM Build failed")
        return listRPMFiles, listSRPMFiles
