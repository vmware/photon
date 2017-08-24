from CommandUtils import CommandUtils
from ChrootUtils import ChrootUtils
from Logger import Logger
from PackageUtils import PackageUtils
from constants import constants
import subprocess
import os.path
import traceback
import shutil

class ToolChainUtils(object):

    def __init__(self,logName=None,logPath=None):
        if logName is None:
            logName = "Toolchain Utils"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.adjustToolChainScript = "adjust-tool-chain.sh"
        self.localegenScript = "./locale-gen.sh"
        self.localegenConfig = "./locale-gen.conf"
        self.prepareBuildRootCmd="./prepare-build-root.sh"
        self.rpmbuildCommand = "rpmbuild"
        if os.geteuid()==0:
            self.rpmCommand="rpm"
        else:
            self.rpmCommand="fakeroot-ng rpm"

    def prepareBuildRoot(self,chrootID):
        self.logger.info("Preparing build environment")
        cmdUtils = CommandUtils()
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+"/dev")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+"/etc")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+"/proc")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+"/run")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+"/sys")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+"/tmp")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath)
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/x86_64")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/noarch")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SOURCES")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SPECS")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/LOGS")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/BUILD")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/BUILDROOT")

        prepareChrootCmd=self.prepareBuildRootCmd+" "+chrootID
        logFile=constants.logPath+"/prepareBuildRoot.log"
        returnVal=cmdUtils.runCommandInShell(prepareChrootCmd,logFile)
        if not returnVal:
            self.logger.error("Prepare build root script failed.Unable to prepare chroot.")
            raise Exception("Prepare build root script failed")

        self.logger.info("Successfully prepared chroot:"+chrootID)

    def findRPMFileInGivenLocation(self,package,rpmdirPath):
        cmdUtils = CommandUtils()
        listFoundRPMFiles = cmdUtils.findFile(package+"-*.rpm",rpmdirPath)
        listFilterRPMFiles=[]
        for f in listFoundRPMFiles:
            rpmFileName=os.path.basename(f)
            checkRPMName=rpmFileName.replace(package,"")
            rpmNameSplit = checkRPMName.split("-")
            if len(rpmNameSplit) == 3:
                listFilterRPMFiles.append(f)
        if len(listFilterRPMFiles) == 1 :
            return listFilterRPMFiles[0]
        if len(listFilterRPMFiles) == 0 :
            return None
        if len(listFilterRPMFiles) > 1 :
            self.logger.error("Found multiple rpm files for given package in rpm directory.Unable to determine the rpm file for package:"+package)
            return None

    def buildCoreToolChainPackages(self, listBuildOptionPackages, pkgBuildOptionFile):
        self.logger.info("Building core tool chain packages.....")
        chrootID=None
        pkgCount = 0
        try:
            pkgUtils=PackageUtils(self.logName,self.logPath)
            for package in constants.listCoreToolChainPackages:
                rpmPkg=pkgUtils.findRPMFileForGivenPackage(package)
                if rpmPkg is not None:
                    continue
                chrUtils = ChrootUtils(self.logName,self.logPath)
                chrootName="build-core-toolchain"
                destLogPath=constants.logPath+"/build-"+package
                if not os.path.isdir(destLogPath):
                    cmdUtils = CommandUtils()
                    cmdUtils.runCommandInShell("mkdir -p "+destLogPath)
                returnVal,chrootID = chrUtils.createChroot(chrootName)
                if not returnVal:
                    self.logger.error("Creating chroot failed")
                    raise Exception("creating chroot failed")
                self.installToolChainRPMS(chrootID, package)
                pkgUtils.adjustGCCSpecs(package, chrootID, destLogPath)
                pkgUtils.buildRPMSForGivenPackage(package, chrootID, listBuildOptionPackages, pkgBuildOptionFile, destLogPath)
                pkgCount += 1
                chrUtils.destroyChroot(chrootID)
                chrootID=None
            self.logger.info("Successfully built toolchain")
            if chrootID is not None:
                chrUtils.destroyChroot(chrootID)
        except Exception as e:
            self.logger.error("Unable to build tool chain.")
            # print stacktrace
            traceback.print_exc()
            raise e
        return pkgCount

    def installToolChainRPMS(self,chrootID, packageName):
        cmdUtils = CommandUtils()
        self.prepareBuildRoot(chrootID)
        self.logger.info("Installing Tool Chain RPMS.......")
        rpmFiles = ""
        packages = ""
        for package in constants.listToolChainRPMsToInstall:
            pkgUtils=PackageUtils(self.logName,self.logPath)
            rpmFile = None
            if constants.rpmCheck:
                rpmFile=pkgUtils.findRPMFileForGivenPackage(package)
            else:
                if (packageName not in constants.listToolChainRPMsToInstall or
                        constants.listToolChainRPMsToInstall.index(packageName) > constants.listToolChainRPMsToInstall.index(package)):
                    rpmFile=pkgUtils.findRPMFileForGivenPackage(package)
            if rpmFile is None:
                # sqlite-autoconf package was renamed, but it still published as sqlite-autoconf
                if package == "sqlite":
                    package = "sqlite-autoconf"
                rpmFile=self.findRPMFileInGivenLocation(package, constants.prevPublishRPMRepo)
                if rpmFile is None:
                    if package in constants.listOfRPMsProvidedAfterBuild:
                        self.logger.info("No old version of "+package+" exists, skip until the new version is built")
                        continue
                    self.logger.error("Unable to find rpm "+ package +" in current and previous versions")
                    raise Exception("Input Error")
            rpmFiles += " " + rpmFile
            packages += " " + package

        self.logger.debug("Installing rpms:"+packages)
        cmd=self.rpmCommand + " -i --nodeps --force --root "+chrootID+" --define \'_dbpath /var/lib/rpm\' "+ rpmFiles
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            self.logger.error("Installing tool chain  failed")
            raise Exception("RPM installation failed")
        self.logger.info("Successfully installed default Tool Chain RPMS in Chroot:"+chrootID)
        print "Building Package:"+ packageName
        print constants.perPackageToolChain
        if packageName in constants.perPackageToolChain:
            print constants.perPackageToolChain[packageName]
            self.installCustomToolChainRPMS(chrootID, constants.perPackageToolChain[packageName], packageName);
   
    def installCustomToolChainRPMS(self, chrootID, listOfToolChainPkgs, packageName):
        self.logger.info("Installing package specific tool chain RPMs for " + packageName + ".......")
        rpmFiles = ""
        packages = ""
        for package in listOfToolChainPkgs:
            pkgUtils=PackageUtils(self.logName,self.logPath)
            print "DEBUG:" + package
            if "openjre8" in packageName or "openjdk8" in packageName:
                rpmFile=self.findRPMFileInGivenLocation(package, constants.prevPublishXRPMRepo)
            else:
                rpmFile=self.findRPMFileInGivenLocation(package, constants.prevPublishRPMRepo)
            if rpmFile is None:
                self.logger.error("Unable to find rpm "+ package +" in current and previous versions")
                raise Exception("Input Error")
            rpmFiles += " " + rpmFile
            packages += " " + package

        self.logger.debug("Installing rpms:"+packages)
        cmd=self.rpmCommand + " -i --nodeps --force --root "+chrootID+" --define \'_dbpath /var/lib/rpm\' "+ rpmFiles
        print "Command Executed:" + cmd
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            self.logger.error("Installing tool chain  failed")
            raise Exception("RPM installation failed")
        self.logger.info("Successfully installed all Tool Chain X RPMS")

    def installToolChainRPMSinContainer(self, containerID):
        self.logger.info("Installing tool-chain RPMS in container: " + containerID.short_id)
        rpmFiles = ""
        packages = ""
        pkgUtils = PackageUtils(self.logName, self.logPath)
        for package in constants.listToolChainRPMPkgsToInstall:
            rpmFile = pkgUtils.findRPMFileForGivenPackage(package)
            if rpmFile is None:
                # sqlite-autoconf package was renamed, but it still published as sqlite-autoconf
                if package == "sqlite":
                    package = "sqlite-autoconf"
                rpmFile = self.findRPMFileInGivenLocation(package, constants.prevPublishRPMRepo)
                if rpmFile is None:
                    if package in constants.listOfRPMsProvidedAfterBuild:
                        self.logger.info("No old version of " + package + " exists, skip until the new version is built")
                        continue
                    self.logger.error("Unable to find rpm " + package + " in current and previous versions")
                    raise Exception("Input Error")
            if rpmFile.find("stage/PUBLISHRPMS"):
                rpmFile = rpmFile.replace(constants.prevPublishRPMRepo, "/publishrpms")
            if rpmFile.find("stage/PUBLISHXRPMS"):
                rpmFile = rpmFile.replace(constants.prevPublishXRPMRepo, "/publishxrpms")
            if rpmFile.find("stage/RPMS"):
                rpmFile = rpmFile.replace(constants.rpmPath, constants.topDirPath + "/RPMS")
            rpmFiles += " " + rpmFile
            packages += " " + package

        self.logger.debug("Installing tool-chain rpms: " + packages)

        cmd = "/usr/bin/bash -l -c '/usr/bin/rpm -Uvh --force --nodeps " + rpmFiles + "'"
        self.logger.info("VDBG-TCU-installToolChainRPMSinContainer: Installing rpms cmd: " + cmd)
        tcInstallLog = containerID.exec_run(cmd)
        # TODO: Find a way to collect exit status of the command that was run.
        if not tcInstallLog:
            self.logger.error("Installing tool chain in container failed")
            raise Exception("RPM installation in container failed")
        self.logger.info(tcInstallLog)
        self.logger.info("Successfully installed default tool-chain RPMS in container: " + containerID.short_id)

    def installCustomToolChainRPMSinContainer(self, containerID, listOfToolChainPkgs, packageName):
        self.logger.info("Installing package specific tool chain RPMs for " + packageName)
        rpmFiles = ""
        packages = ""
        for package in listOfToolChainPkgs:
            if "openjre8" in packageName or "openjdk8" in packageName:
                rpmFile=self.findRPMFileInGivenLocation(package, constants.prevPublishXRPMRepo)
            else:
                rpmFile=self.findRPMFileInGivenLocation(package, constants.prevPublishRPMRepo)
            if rpmFile is None:
                self.logger.error("Unable to find rpm " + package + " in current and previous versions")
                raise Exception("Input Error")
            if rpmFile.find("stage/PUBLISHRPMS"):
                rpmFile = rpmFile.replace(constants.prevPublishRPMRepo, "/publishrpms")
            if rpmFile.find("stage/PUBLISHXRPMS"):
                rpmFile = rpmFile.replace(constants.prevPublishXRPMRepo, "/publishxrpms")
            if rpmFile.find("stage/RPMS"):
                rpmFile = rpmFile.replace(constants.rpmPath, constants.topDirPath + "/RPMS")
            rpmFiles += " " + rpmFile
            packages += " " + package

        self.logger.debug("Installing rpms: " + packages)
        cmd = "rpm -Uvh --nodeps --force " + rpmFiles
        self.logger.debug("VDBG-TCU-installCustomToolChainRPMSinContainer: Installing rpms cmd: " + cmd)
        tcInstallLog = containerID.exec_run(cmd)
        # TODO: Find a way to collect exit status of the command that was run.
        if not tcInstallLog:
            self.logger.error("Installing tool chain in container failed")
            raise Exception("RPM installation in container failed")
        self.logger.info(tcInstallLog)
        self.logger.info("Successfully installed all tool-chain XRPMS in container: " + containerID.short_id)
