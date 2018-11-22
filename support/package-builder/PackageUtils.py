from CommandUtils import CommandUtils
from Logger import Logger
import os
import platform
import shutil
from constants import constants
import re
from time import sleep
import PullSources
import json
import collections
from SpecData import SPECS
from distutils.version import LooseVersion

class PackageUtils(object):

    def __init__(self,logName=None,logPath=None):
        if logName is None:
            logName = "PackageUtils"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.runInChrootCommand="./run-in-chroot.sh " + constants.sourcePath + " " + constants.rpmPath;
        self.rpmBinary = "rpm"
        self.installRPMPackageOptions = "-Uvh"
        self.nodepsRPMPackageOptions = "--nodeps"

        self.rpmbuildBinary = "rpmbuild"
        self.rpmbuildBuildallOption = "-ba --clean"
        self.rpmbuildNocheckOption = "--nocheck"
        self.rpmbuildCheckOption ="-bi --clean"
        self.queryRpmPackageOptions = "-qa"
        self.forceRpmPackageOptions = "--force"
        self.replaceRpmPackageOptions = "--replacepkgs"
        self.adjustGCCSpecScript="adjust-gcc-specs.sh"
        self.rpmFilesToInstallInAOneShot=""
        self.packagesToInstallInAOneShot=""
        self.noDepsRPMFilesToInstallInAOneShot=""
        self.noDepsPackagesToInstallInAOneShot=""
        self.rpmFilesToReInstallInAOneShot=""
        self.noDepsRPMFilesToReInstallInAOneShot=""

    def getRPMArch(self,rpmName):
        arch=""
        if rpmName.find("x86_64") != -1:
            arch="x86_64"
        elif rpmName.find("aarch64") != -1:
            arch="aarch64"
        elif rpmName.find("noarch") != -1:
            arch="noarch"
        return arch

    def getRPMDestDir(self,rpmName,rpmDir):
        arch = self.getRPMArch(rpmName)
        rpmDestDir=rpmDir+"/"+arch
        return rpmDestDir

    def copyRPM(self,rpmFile,destDir):
        cmdUtils = CommandUtils()
        rpmName=os.path.basename(rpmFile)
        rpmDestDir=self.getRPMDestDir(rpmName,destDir)
        rpmDestPath=rpmDestDir+"/"+rpmName
        if os.geteuid()==0:
            if not os.path.isdir(rpmDestDir):
                cmdUtils.runCommandInShell("mkdir -p "+rpmDestDir)
            shutil.copyfile(rpmFile,  rpmDestPath)
        return rpmDestPath

    def installRPM(self,package,version,chrootID,noDeps=False,destLogPath=None):
#        self.logger.info("Installing rpm for package:"+package)
#        self.logger.debug("No deps:"+str(noDeps))

        rpmfile=self.findRPMFileForGivenPackage(package,version)
        if rpmfile is None:
            self.logger.error("No rpm file found for package:"+package)
            raise Exception("Missing rpm file: "+package)

        rpmDestFile = self.copyRPM(rpmfile, chrootID+constants.topDirPath+"/RPMS")
        rpmFile=rpmDestFile.replace(chrootID,"")
        if noDeps:
            self.noDepsRPMFilesToInstallInAOneShot += " " + rpmFile
            self.noDepsPackagesToInstallInAOneShot += " " + package
        else:
            self.rpmFilesToInstallInAOneShot += " " + rpmFile
            self.packagesToInstallInAOneShot += " " + package

    def installRPMSInAOneShot(self,chrootID,destLogPath):
        chrootCmd=self.runInChrootCommand+" "+chrootID
        rpmInstallcmd=self.rpmBinary+" "+ self.installRPMPackageOptions
        cmdUtils = CommandUtils()
        if self.noDepsRPMFilesToInstallInAOneShot != "":
            self.logger.info("Installing nodeps rpms: " + self.noDepsPackagesToInstallInAOneShot)
            logFile=destLogPath+"/install_rpms_nodeps.log"
            cmd = rpmInstallcmd+" "+self.nodepsRPMPackageOptions + " " + self.noDepsRPMFilesToInstallInAOneShot
            returnVal = cmdUtils.runCommandInShell(cmd, logFile, chrootCmd)
            if not returnVal:
                self.logger.debug("Command Executed:" + cmd)
                self.logger.error("Unable to install rpms")
                raise Exception("RPM installation failed")
        if self.rpmFilesToInstallInAOneShot != "":
            self.logger.info("Installing rpms: " + self.packagesToInstallInAOneShot)
            logFile=destLogPath+"/install_rpms.log"
            cmd=rpmInstallcmd+" "+self.rpmFilesToInstallInAOneShot
            returnVal = cmdUtils.runCommandInShell(cmd, logFile, chrootCmd)
            if not returnVal:
                self.logger.debug("Command Executed:" + cmd)
                self.logger.error("Unable to install rpms")
                raise Exception("RPM installation failed")

    def verifyShaAndGetSourcePath(self, source, package, version):
        cmdUtils = CommandUtils()
        # Fetch/verify sources if sha1 not None.
        sha1 = SPECS.getData().getSHA1(package, source, version)
        if sha1 is not None:
            PullSources.get(package, source, sha1, constants.sourcePath, constants.pullsourcesConfig, self.logger)

        sourcePath = cmdUtils.findFile(source,constants.sourcePath)
        if sourcePath is None or len(sourcePath) == 0:
            sourcePath = cmdUtils.findFile(source,constants.specPath)
            if sourcePath is None or len(sourcePath) == 0:
                if sha1 is None:
                    self.logger.error("No sha1 found or missing source for "+source)
                    raise Exception("No sha1 found or missing source for "+source)
                else:
                    self.logger.error("Missing source: "+source+". Cannot find sources for package: "+package)
                    raise Exception("Missing source")
        else:
            if sha1 is None:
                self.logger.error("No sha1 found for "+source)
                raise Exception("No sha1 found")
        if len(sourcePath) > 1:
            self.logger.error("Multiple sources found for source:"+source+"\n"+ ",".join(sourcePath) +"\nUnable to determine one.")
            raise Exception("Multiple sources found")
        return sourcePath

    def copySourcesTobuildroot(
            self,
            listSourceFiles,
            package,
            destDir,
            version):
        for source in listSourceFiles:
            sourcePath = self.verifyShaAndGetSourcePath(source, package, version)
            self.logger.info("Copying... Source path :" + source + " Source filename: " + sourcePath[0])
            shutil.copy2(sourcePath[0], destDir)

    def copyAdditionalBuildFiles(self,listAdditionalFiles,chrootID):
        cmdUtils = CommandUtils()
        for additionalFile in listAdditionalFiles:
            source = additionalFile["src"].encode('utf-8')
            destDir = chrootID + additionalFile["dst"].encode('utf-8')
            if os.path.exists(source):
                if os.path.isfile(source):
                    shutil.copy(source, destDir)
                else:
                    shutil.copytree(source, destDir)

    def getAdditionalBuildFiles(self, package, pkgBuildOptionFile):
        listAdditionalFiles = []
        macros = []
        jsonData = open(pkgBuildOptionFile)
        pkg_build_option_json = json.load(jsonData, object_pairs_hook=collections.OrderedDict)
        jsonData.close()
        pkgs_sorted = pkg_build_option_json.items()
        for pkg in pkgs_sorted:
            p = str(pkg[0].encode('utf-8'))
            if p == package:
                filelist = pkg[1]["files"]
                for f in filelist:
                    listAdditionalFiles.append(f)
                macrolist = pkg[1]["macros"]
                for macro in macrolist:
                    macros.append(str(macro.encode('utf-8')))
        return listAdditionalFiles, macros

    def buildRPMSForGivenPackage(
            self,
            package,
            version,
            chrootID,
            listBuildOptionPackages,
            pkgBuildOptionFile,
            destLogPath=None):
        self.logger.info("Building rpm's for package:"+package)

        listSourcesFiles = SPECS.getData().getSources(package, version)
        listPatchFiles =  SPECS.getData().getPatches(package, version)
        specFile = SPECS.getData().getSpecFile(package, version)
        specName = SPECS.getData().getSpecName(package) + ".spec"
        chrootSourcePath=chrootID+constants.topDirPath+"/SOURCES/"
        chrootSpecPath=constants.topDirPath+"/SPECS/"
        chrootLogsFilePath=chrootID+constants.topDirPath+"/LOGS/"+package+".log"
        chrootCmd=self.runInChrootCommand+" "+chrootID
        shutil.copyfile(specFile, chrootID+chrootSpecPath+specName )

# FIXME: some sources are located in SPECS/.. how to mount?
#        if os.geteuid()==0:
        self.copySourcesTobuildroot(listSourcesFiles,package,chrootSourcePath, version)
        self.copySourcesTobuildroot(listPatchFiles,package,chrootSourcePath, version)

        macros = []
        if package in listBuildOptionPackages:
            listAdditionalFiles, macros = self.getAdditionalBuildFiles(package, pkgBuildOptionFile)
            self.copyAdditionalBuildFiles(listAdditionalFiles,chrootID)

        #Adding rpm macros
        listRPMMacros = constants.userDefinedMacros
        for macroName in listRPMMacros.keys():
            macros.append(macroName+" "+listRPMMacros[macroName])

        listRPMFiles=[]
        listSRPMFiles=[]
        try:
            listRPMFiles,listSRPMFiles = self.buildRPM(chrootSpecPath +specName,chrootLogsFilePath,chrootCmd,package,macros)
            self.logger.info("Successfully built rpm:"+package)
        except Exception as e:
            self.logger.error("Failed while building rpm:"+package)
            raise e
        finally:
            if destLogPath is not None:
                if constants.rpmCheck and package in constants.testForceRPMS and SPECS.getData().isCheckAvailable(package):
                    cmd="sed -i '/^Executing(%check):/,/^Processing files:/{//!b};d' "+ chrootLogsFilePath
                    logFile = destLogPath+"/adjustTestFile.log"
                    returnVal = CommandUtils().runCommandInShell(cmd, logFile)
                    testLogFile = destLogPath+"/"+package+"-test.log"
                    shutil.copyfile(chrootLogsFilePath, testLogFile)
                else:
                    shutil.copy2(chrootLogsFilePath, destLogPath)
        self.logger.info("RPM build is successful")

        for rpmFile in listRPMFiles:
            self.copyRPM(chrootID+"/"+rpmFile, constants.rpmPath)

        for srpmFile in listSRPMFiles:
            srpmDestFile = self.copyRPM(chrootID+"/"+srpmFile, constants.sourceRpmPath)

    def buildRPM(self,specFile,logFile,chrootCmd,package,macros):
        rpmBuildcmd=self.rpmbuildBinary+" "+self.rpmbuildBuildallOption

        if constants.rpmCheck and package in constants.testForceRPMS:
            self.logger.info("#"*(68+2*len(package)))
            if not SPECS.getData().isCheckAvailable(package):
                self.logger.info("####### "+package+" MakeCheck is not available. Skipping MakeCheck TEST for "+package+ " #######")
                rpmBuildcmd=self.rpmbuildBinary+" --clean"
            else:
                self.logger.info("####### "+package+" MakeCheck is available. Running MakeCheck TEST for "+package+ " #######")
                rpmBuildcmd=self.rpmbuildBinary+" "+self.rpmbuildCheckOption
            self.logger.info("#"*(68+2*len(package)))
        else:
           rpmBuildcmd+=" "+self.rpmbuildNocheckOption

        for macro in macros:
            rpmBuildcmd+=' --define \\\"%s\\\"' % macro
        rpmBuildcmd+=" "+specFile

        cmdUtils = CommandUtils()
        self.logger.info("Building rpm....")
        self.logger.info(rpmBuildcmd)
        returnVal = cmdUtils.runCommandInShell(rpmBuildcmd, logFile, chrootCmd)
        if constants.rpmCheck and package in constants.testForceRPMS:
            if not SPECS.getData().isCheckAvailable(package):
                constants.testLogger.info(package+" : N/A")
            elif returnVal:
                constants.testLogger.info(package+" : PASS")
            else:
                constants.testLogger.error(package+" : FAIL" )

        if constants.rpmCheck:
            if not returnVal and constants.rpmCheckStopOnError:
                self.logger.error("Checking rpm is failed "+specFile)
                raise Exception("RPM check failed")
        else:
            if not returnVal:
                self.logger.error("Building rpm is failed "+specFile)
                raise Exception("RPM build failed")

        #Extracting rpms created from log file
        logfile=open(logFile,'r')
        fileContents=logfile.readlines()
        logfile.close()
        listRPMFiles=[]
        listSRPMFiles=[]
        for i in range(0,len(fileContents)):
            if re.search("^Wrote:",fileContents[i]):
                listcontents=fileContents[i].split()
                if (len(listcontents) == 2) and listcontents[1].strip()[-4:] == ".rpm" and listcontents[1].find("/RPMS/") != -1:
                    listRPMFiles.append(listcontents[1])
                if (len(listcontents) == 2) and listcontents[1].strip()[-8:] == ".src.rpm" and listcontents[1].find("/SRPMS/") != -1:
                    listSRPMFiles.append(listcontents[1])
        return listRPMFiles,listSRPMFiles

    def findRPMFileForGivenPackage(self, package, version = "*"):
        cmdUtils = CommandUtils()

        # If no version is specified, use the latest from the source
        # code.
        if version == "*":
            version = SPECS.getData().getHighestVersion(package)
        release = SPECS.getData().getRelease(package,version)
        # pkg_build_options does not specify the release and there is no spec for that
        if not release:
            release = "*"
        listFoundRPMFiles = sum([cmdUtils.findFile(package+"-"+version+"-"+release+"."+platform.machine()+".rpm",constants.rpmPath),
                            cmdUtils.findFile(package+"-"+version+"-"+release+".noarch.rpm",constants.rpmPath)], [])
        if constants.inputRPMSPath is not None:
            listFoundRPMFiles = sum([cmdUtils.findFile(package+"-"+version+"-"+release+"."+platform.machine()+".rpm",constants.inputRPMSPath),
                            cmdUtils.findFile(package+"-"+version+"-"+release+".noarch.rpm",constants.inputRPMSPath)], listFoundRPMFiles)
        if len(listFoundRPMFiles) == 1 :
            return listFoundRPMFiles[0]
        if len(listFoundRPMFiles) == 0 :
            return None
        if len(listFoundRPMFiles) > 1 :
            self.logger.error("Found multiple rpm files for given package in rpm directory.Unable to determine the rpm file for package:"+package+ " list:"+str(listFoundRPMFiles))
            raise Exception("Multiple rpm files found")

    def findPackageNameFromRPMFile(self,rpmfile):
        rpmfile=os.path.basename(rpmfile)
        releaseindex=rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:"+rpmfile)
            raise Exception("Invalid RPM")
        versionindex=rpmfile[0:releaseindex].rfind("-")
        if versionindex == -1:
            self.logger.error("Invalid rpm file:"+rpmfile)
            raise Exception("Invalid RPM")
        packageName=rpmfile[0:versionindex]
        return packageName

    def findPackageInfoFromRPMFile(self,rpmfile):
        rpmfile=os.path.basename(rpmfile)
        rpmfile=rpmfile.replace("."+platform.machine()+".rpm","")
        rpmfile=rpmfile.replace(".noarch.rpm","")
        releaseindex=rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:"+rpmfile)
            raise Exception("Invalid RPM")
        versionindex=rpmfile[0:releaseindex].rfind("-")
        if versionindex == -1:
            self.logger.error("Invalid rpm file:"+rpmfile)
            raise Exception("Invalid RPM")
        packageName=rpmfile[0:versionindex]
        version=rpmfile[versionindex+1:releaseindex]
        release=rpmfile[releaseindex+1:]
        return packageName,version,release

    def findInstalledRPMPackages(self, chrootID):
        cmd = self.rpmBinary+" "+self.queryRpmPackageOptions
        chrootCmd=self.runInChrootCommand+" "+chrootID
        cmdUtils=CommandUtils()
        result=cmdUtils.runCommandInShell2(cmd, chrootCmd)
        if result is not None:
            return result.split()
        return result

    def adjustGCCSpecs(self, package, chrootID, logPath, version):
        opt = " " + SPECS.getData().getSecurityHardeningOption(package, version)
        cmdUtils=CommandUtils()
        cpcmd="cp "+ self.adjustGCCSpecScript+" "+chrootID+"/tmp/"+self.adjustGCCSpecScript
        cmd = "/tmp/"+self.adjustGCCSpecScript+opt
        logFile = logPath+"/adjustGCCSpecScript.log"
        chrootCmd=self.runInChrootCommand+" "+chrootID
        returnVal = cmdUtils.runCommandInShell(cpcmd, logFile)
        if not returnVal:
            self.logger.error("Error during copying the file adjust gcc spec")
            raise Exception("Failed while copying adjust gcc spec file")
        returnVal = cmdUtils.runCommandInShell(cmd, logFile, chrootCmd)
        if returnVal:
            return

        self.logger.debug(cmdUtils.runCommandInShell2("ls -la " + chrootID + "/tmp/" + self.adjustGCCSpecScript))
        self.logger.debug(cmdUtils.runCommandInShell2("lsof " + chrootID + "/tmp/" + self.adjustGCCSpecScript))
        self.logger.debug(cmdUtils.runCommandInShell2("ps ax"))

        self.logger.error("Failed while adjusting gcc specs")
        raise Exception("Failed while adjusting gcc specs")

    def copySourcesToContainer(self, listSourceFiles, package, containerID, destDir, version):
        cmdUtils = CommandUtils()
        for source in listSourceFiles:
            sourcePath = self.verifyShaAndGetSourcePath(source, package, version)
            self.logger.info("Copying source file: " + sourcePath[0])
            copyCmd = "docker cp " + sourcePath[0] + " " + containerID.short_id + ":" + destDir
            cmdUtils.runCommandInShell(copyCmd)

    def copyAdditionalBuildFilesToContainer(self, listAdditionalFiles, containerID):
        cmdUtils = CommandUtils()
        #self.logger.debug("VDBG-PU-copyAdditionalBuildFilesToContainer id: " +containerID.short_id)
        #self.logger.debug(listAdditionalFiles)
        for additionalFile in listAdditionalFiles:
            source = additionalFile["src"].encode('utf-8')
            destDir = additionalFile["dst"].encode('utf-8')
            destPath = containerID.short_id + ":" + destDir
            #TODO: exit status of exec_run
            containerID.exec_run("mkdir -p " + destDir)
            if os.path.exists(source):
                copyCmd = "docker cp " + source
                if os.path.isfile(source):
                    self.logger.info("Copying addl source file: " + source)
                    copyCmd += " " + destPath
                else:
                    self.logger.info("Copying addl source file tree: " + source)
                    copyCmd +=  "/. " + destPath
                #TODO: cmd error code
                cmdUtils.runCommandInShell(copyCmd)

    def getRPMPathInContainer(self, rpmFile, containerID):
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

    def prepRPMforInstallInContainer(self, package, version, containerID, noDeps=False, destLogPath=None):
        rpmfile = self.findRPMFileForGivenPackage(package, version)
        if rpmfile is None:
            self.logger.error("No rpm file found for package: " + package)
            raise Exception("Missing rpm file")

        rpmDestFile = self.getRPMPathInContainer(rpmfile, containerID)
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
        rpmInstallcmd = self.rpmBinary + " " + self.installRPMPackageOptions + " " + self.forceRpmPackageOptions

        if self.noDepsRPMFilesToInstallInAOneShot != "":
            self.logger.info("PackageUtils-installRPMSInAOneShotInContainer: Installing nodeps rpms: " + \
                             self.noDepsPackagesToInstallInAOneShot)
            logFile = destLogPath + "/install_rpms_nodeps.log"
            cmd = rpmInstallcmd + " " + self.nodepsRPMPackageOptions + " " + self.noDepsRPMFilesToInstallInAOneShot
            cmd = "/bin/bash -l -c '" + cmd + "'"
            #self.logger.debug("VDBG-PU-installRPMSInAOneShotInContainer: Install nodeps cmd: " + cmd)
            #TODO: Error code from exec_run
            installLog = containerID.exec_run(cmd)
            if not installLog:
                self.logger.error("Unable to install nodeps rpms")
                raise Exception("nodeps RPM installation failed")
            logfile = open(logFile, 'w')
            logfile.write(installLog)
            logfile.close()

            if self.noDepsRPMFilesToReInstallInAOneShot != "":
                cmd = rpmInstallcmd + " " + self.nodepsRPMPackageOptions + " " + self.forceRpmPackageOptions + " " + self.noDepsRPMFilesToReInstallInAOneShot
                cmd = "/bin/bash -l -c '" + cmd + "'"
                #self.logger.debug("VDBG-PU-installRPMSInAOneShotInContainer: ReInstall nodeps cmd: " + cmd)
                #TODO: Error code from exec_run
                installLog = containerID.exec_run(cmd)
                if not installLog:
                    self.logger.error("Unable to re-install nodeps rpms")
                    raise Exception("nodeps RPM re-installation failed")
                logfile = open(logFile, 'a')
                logfile.write(installLog)
                logfile.close()

        if self.rpmFilesToInstallInAOneShot != "":
            self.logger.info("PackageUtils-installRPMSInAOneShotInContainer: Installing rpms: " + \
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
            logfile = open(logFile, 'w')
            logfile.write(installLog)
            logfile.close()

            if self.rpmFilesToReInstallInAOneShot != "":
                cmd = rpmInstallcmd + " " + self.forceRpmPackageOptions + " " + self.rpmFilesToReInstallInAOneShot
                cmd = "/bin/bash -l -c '" + cmd + "'"
                #self.logger.debug("VDBG-PU-installRPMSInAOneShotInContainer: ReInstall cmd: " + cmd)
                #TODO: Error code from exec_run
                installLog = containerID.exec_run(cmd)
                if not installLog:
                    self.logger.error("Unable to re-install rpms")
                    raise Exception("RPM re-installation failed")
                logfile = open(logFile, 'a')
                logfile.write(installLog)
                logfile.close()

    def findInstalledRPMPackagesInContainer(self, containerID):
        cmd = self.rpmBinary + " " + self.queryRpmPackageOptions
        cmd = "/bin/bash -l -c '" + cmd + "'"
        #TODO: Error code from exec_run
        result = containerID.exec_run(cmd)
        if result is not None:
            return result.split()
        return result

    def adjustGCCSpecsInContainer(self, package, containerID, logPath, version):
        opt = " " + SPECS.getData().getSecurityHardeningOption(package, version)
        adjustCmd = "/" + self.adjustGCCSpecScript + opt
        adjustCmd = "/bin/bash -l -c '" + adjustCmd + "'"
        logFile = logPath + "/adjustGCCSpecScript.log"

        #TODO: Error code from exec_run
        scriptLog = containerID.exec_run(adjustCmd)
        if scriptLog:
            logfile = open(logFile, 'w')
            logfile.write(scriptLog)
            logfile.close()
            return

        self.logger.debug(containerID.exec_run("ls -la /tmp/" + self.adjustGCCSpecScript))
        self.logger.debug(containerID.exec_run("lsof /tmp/" + self.adjustGCCSpecScript))
        self.logger.debug(containerID.exec_run("ps ax"))
        self.logger.error("Failed while adjusting gcc specs")
        raise Exception("Failed while adjusting gcc specs")

    def buildRPMSForGivenPackageInContainer(
            self,
            package,
            version,
            containerID,
            listBuildOptionPackages,
            pkgBuildOptionFile,
            destLogPath=None):
        self.logger.info("Building rpm's for package " + package + " in container " + containerID.short_id)

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

# FIXME: some sources are located in SPECS/.. how to mount?
#        if os.geteuid()==0:
        #TODO: mount it in, don't copy
        macros = []
        self.copySourcesToContainer(listSourcesFiles, package, containerID, sourcePath, version)
        #TODO: mount it in, don't copy
        self.copySourcesToContainer(listPatchFiles, package, containerID, sourcePath, version)
        if package in listBuildOptionPackages:
            listAdditionalFiles, macros = self.getAdditionalBuildFiles(package, pkgBuildOptionFile)
            self.copyAdditionalBuildFilesToContainer(listAdditionalFiles, containerID)

        # Add rpm macros
        listRPMMacros = constants.userDefinedMacros
        for macroName in listRPMMacros.keys():
            macros.append(macroName + " " + listRPMMacros[macroName])

        # Build RPMs
        listRPMFiles=[]
        listSRPMFiles=[]
        try:
            listRPMFiles, listSRPMFiles = self.buildRPMinContainer(
                                                    specPath + specName,
                                                    rpmLogFile,
                                                    destLogFile,
                                                    containerID,
                                                    package,
                                                    macros)
            self.logger.info("Successfully built rpm:"+package)
        except Exception as e:
            self.logger.error("Failed while building rpm: " + package)
            raise e
        finally:
            if destLogPath is not None:
                rpmLog = destLogPath + "/" + package + ".log"
                if constants.rpmCheck and package in constants.testForceRPMS and SPECS.getData().isCheckAvailable(package):
                    cmd="sed -i '/^Executing(%check):/,/^Processing files:/{//!b};d' "+ rpmLog
                    logFile = destLogPath+"/adjustTestFile.log"
                    returnVal = CommandUtils().runCommandInShell(cmd, logFile)
                    testLogFile = destLogPath+"/"+package+"-test.log"
                    shutil.copyfile(rpmLog, testLogFile)
        self.logger.info("RPM build is successful")

        # Verify RPM and SRPM files exist as success criteria
        for rpmFile in listRPMFiles:
            rpmName = os.path.basename(rpmFile)
            rpmDestDir = self.getRPMDestDir(rpmName, constants.rpmPath)
            rpmDestFile = rpmDestDir + "/" + rpmName
            if not os.path.isfile(rpmDestFile):
                self.logger.error("Could not find RPM file: " + rpmDestFile)
                raise Exception("Built RPM file not found.")

        for srpmFile in listSRPMFiles:
            srpmName = os.path.basename(srpmFile)
            srpmDestDir = self.getRPMDestDir(os.path.basename(srpmFile), constants.sourceRpmPath)
            srpmDestFile = srpmDestDir + "/" + srpmName
            if not os.path.isfile(srpmDestFile):
                self.logger.error("Could not find RPM file: " + srpmDestFile)
                raise Exception("Built SRPM file not found.")

    def buildRPMinContainer(self, specFile, rpmLogFile, destLogFile, containerID, package, macros):

        rpmBuildCmd = self.rpmbuildBinary + " " + self.rpmbuildBuildallOption

        if constants.rpmCheck and package in constants.testForceRPMS:
            self.logger.info("#"*(68+2*len(package)))
            if not SPECS.getData().isCheckAvailable(package):
                self.logger.info("####### "+package+" MakeCheck is not available. Skipping MakeCheck TEST for "+package+ " #######")
                rpmBuildCmd=self.rpmbuildBinary+" --clean"
            else:
                self.logger.info("####### "+package+" MakeCheck is available. Running MakeCheck TEST for "+package+ " #######")
                rpmBuildCmd=self.rpmbuildBinary+" "+self.rpmbuildCheckOption
            self.logger.info("#"*(68+2*len(package)))
        else:
           rpmBuildCmd+=" "+self.rpmbuildNocheckOption

        for macro in macros:
            rpmBuildCmd += ' --define \"%s\"' % macro
        rpmBuildCmd += " " + specFile
        rpmBuildCmd = "/bin/bash -l -c '" + rpmBuildCmd + " > " + rpmLogFile + " 2>&1'"
        rpmBuildCmd = "docker exec -t " + str(containerID.short_id) + " " + rpmBuildCmd

        cmdUtils = CommandUtils()
        self.logger.info("Building rpm for package: " + package)
        #TODO: Show running log of rpmbuildcmd
        #TODO: Get exit status of rpmBuildCmd
        #containerID.exec_run(rpmBuildCmd)
        returnVal = cmdUtils.runCommandInShell(rpmBuildCmd)

        if not os.path.isfile(destLogFile):
            self.logger.error("RPM build not file not found. Building rpm failed for: " + specFile)
            raise Exception("RPM Build failed")

        if constants.rpmCheck and package in constants.testForceRPMS:
            if not SPECS.getData().isCheckAvailable(package):
                constants.testLogger.info(package+" : N/A")
            elif returnVal:
                constants.testLogger.info(package+" : PASS")
            else:
                constants.testLogger.error(package+" : FAIL" )

        if constants.rpmCheck:
            if not returnVal and constants.rpmCheckStopOnError:
                self.logger.error("Checking rpm is failed "+specFile)
                raise Exception("RPM check failed")
        else:
            if not returnVal:
                self.logger.error("Building rpm is failed "+specFile)
                raise Exception("RPM build failed")

        #Extracting rpms created from log file
        listRPMFiles=[]
        listSRPMFiles=[]
        logfile = open(destLogFile, 'r')
        rpmBuildLogLines = logfile.readlines()
        logfile.close()
        for i in range(0, len(rpmBuildLogLines)):
            if re.search("^Wrote:", rpmBuildLogLines[i]):
                listcontents = rpmBuildLogLines[i].split()
                if (len(listcontents) == 2) and listcontents[1].strip()[-4:] == ".rpm" and listcontents[1].find("/RPMS/") != -1:
                    listRPMFiles.append(listcontents[1])
                if (len(listcontents) == 2) and listcontents[1].strip()[-8:] == ".src.rpm" and listcontents[1].find("/SRPMS/") != -1:
                    listSRPMFiles.append(listcontents[1])
        #if not listRPMFiles:
        #    self.logger.error("Building rpm failed for " + specFile)
        #    raise Exception("RPM Build failed")
        return listRPMFiles, listSRPMFiles
