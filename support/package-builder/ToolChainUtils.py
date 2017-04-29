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
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+"/tmp")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath)
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/x86_64")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/noarch")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SOURCES")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SPECS")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/LOGS")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/BUILD")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/BUILDROOT")

        package="filesystem"
        pkgUtils=PackageUtils(self.logName,self.logPath)
        rpmFile=pkgUtils.findRPMFileForGivenPackage(package)
        if rpmFile is None:
            specFile=constants.specData.getSpecFile(package)
            cmd=self.rpmbuildCommand+" -ba --nocheck --define \'_topdir "+chrootID+constants.topDirPath+"\' --define \'_dbpath "+chrootID+"/var/lib/rpm\' --define \'dist "+constants.dist+"\' "+specFile
            self.logger.info(cmd)
            cmdUtils.runCommandInShell(cmd,self.logPath+"/filesystem.log")
            filesystemrpmFile = cmdUtils.findFile(package+"-[0-9]*.rpm", chrootID+constants.topDirPath+"/RPMS")
            filesystemsrpmFile = cmdUtils.findFile(package+"-[0-9]*.src.rpm", chrootID+constants.topDirPath+"/SRPMS")
            if len(filesystemrpmFile) > 0:
                shutil.copy2(filesystemrpmFile[0],constants.rpmPath+"/x86_64/")
            if len(filesystemsrpmFile) > 0:
                shutil.copy2(filesystemsrpmFile[0],constants.sourceRpmPath+"/")
            rpmFile=pkgUtils.findRPMFileForGivenPackage(package)
            if rpmFile is None:
                self.logger.error("Cannot find filesystem rpm")
                raise Exception("Cannot find filesystem rpm")
        
        self.logger.debug("Installing filesystem rpms:" + package)
        if os.geteuid()==0:
            cmd=self.rpmCommand + " -i --nodeps --root "+chrootID+" --define '_dbpath /var/lib/rpm' "+ rpmFile
        else:
            cmd=self.rpmCommand + " -i --nodeps --badreloc --relocate /="+chrootID+" --define '_dbpath "+chrootID+"/var/lib/rpm' "+ rpmFile
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            self.logger.error("Installing filesystem rpm failed")
            raise Exception("RPM installation failed")
        
        prepareChrootCmd=self.prepareBuildRootCmd+" "+chrootID
        logFile=constants.logPath+"/prepareBuildRoot.log"
        returnVal=cmdUtils.runCommandInShell(prepareChrootCmd,logFile)
        if not returnVal:
            self.logger.error("Prepare build root script failed.Unable to prepare chroot.")
            raise Exception("Prepare build root script failed")

        self.logger.info("Successfully prepared chroot:"+chrootID)

    def installToolChain(self,chrootID):
        self.logger.info("Installing toolchain.....")
        self.prepareBuildRoot(chrootID)
        cmdUtils = CommandUtils()

        rpmFiles = ""
        packages = ""
        for package in constants.listToolChainRPMPkgsToInstall:
            pkgUtils=PackageUtils(self.logName,self.logPath)
            rpmFile=pkgUtils.findRPMFileForGivenPackage(package)
            if rpmFile is None:
                rpmFile=self.findRPMFileInGivenLocation(package, constants.prevPublishRPMRepo)
                if rpmFile is None:
                    if package == "util-linux-devel":
                        self.logger.info("No old version of util-linux-devel exists, skip until the new version is built")
                        continue
                    if package == "flex-devel":
                        self.logger.info("No old version of flex-devel exists, skip until the new version is built")
                        continue

                    self.logger.error("Unable to find rpm "+ package +" in current and previous versions")
                    raise Exception("Input Error")
            rpmFiles += " " + rpmFile
            packages += " " + package

        self.logger.debug("Installing toolchain rpms:" + packages)
        cmd=self.rpmCommand + " -i --nodeps --force --root "+chrootID+" --define \'_dbpath /var/lib/rpm\' "+ rpmFiles
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            self.logger.error("Installing toolchain rpms failed")
            raise Exception("RPM installation failed")
        
        self.logger.info("Installed toolchain successfully on chroot:"+chrootID)
    
    def installCoreToolChainPackages(self,chrootID):
        self.logger.info("Installing toolchain.....")
        cmdUtils = CommandUtils()
        self.prepareBuildRoot(chrootID)

        rpmFiles = ""
        packages = ""
        for package in constants.listToolChainRPMPkgsToBuild:
            pkgUtils=PackageUtils(self.logName,self.logPath)
            rpmFile = None
            if package in constants.listCoreToolChainRPMPackages:
                rpmFile=pkgUtils.findRPMFileForGivenPackage(package)
            else:
                rpmFile=self.findRPMFileInGivenLocation(package, constants.prevPublishRPMRepo)
            if rpmFile is None:
                self.logger.error("Unable to find rpm "+ package)
                raise Exception("Input Error")
            rpmFiles += " " + rpmFile
            packages += " " + package

        self.logger.debug("Installing core toolchain rpms:" + packages)
        cmd=self.rpmCommand + " -i --nodeps --force --root "+chrootID+" --define \'_dbpath /var/lib/rpm\' "+ rpmFiles
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            self.logger.error("Installing toolchain rpms failed")
            raise Exception("RPM installation failed")
            
        self.logger.info("Installed core tool chain packages successfully on chroot:"+chrootID)    
    
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
        try:
            pkgUtils=PackageUtils(self.logName,self.logPath)
            for package in constants.listCoreToolChainRPMPackages:
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
                
    def installToolChainRPMS(self,chrootID, packageName):
        cmdUtils = CommandUtils()
        self.prepareBuildRoot(chrootID)
        self.logger.info("Installing Tool Chain RPMS.......")
        rpmFiles = ""
        packages = ""
        for package in constants.listToolChainRPMPkgsToBuild:
            pkgUtils=PackageUtils(self.logName,self.logPath)
            rpmFile=pkgUtils.findRPMFileForGivenPackage(package)
            if rpmFile is None:
                rpmFile=self.findRPMFileInGivenLocation(package, constants.prevPublishRPMRepo)
                if rpmFile is None:
                    if package == "util-linux-devel":
                        self.logger.info("No old version of util-linux-devel exists, skip until the new version is built")
                        continue
                    if package == "flex-devel":
                        self.logger.info("No old version of flex-devel exists, skip until the new version is built")
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
        if "openjdk" in packageName or "openjre" in packageName:
            self.installToolChainXRPMS(chrootID);
   
    def installToolChainXRPMS(self, chrootID):
        self.logger.info("Installing Tool Chain X package RPMS.......")
        rpmFiles = ""
        packages = ""
        for package in constants.listToolChainXRPMsToInstall:
            pkgUtils=PackageUtils(self.logName,self.logPath)
	    print "DEBUG:" + package
            rpmFile=self.findRPMFileInGivenLocation(package, constants.prevPublishXRPMRepo)
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
 
