from CommandUtils import CommandUtils
from ChrootUtils import ChrootUtils
from Logger import Logger
from PackageUtils import PackageUtils
from constants import constants
import subprocess

class ToolChainUtils(object):
    __built_successfull=False
    
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
        
    #Tool chain should be built before calling this method
    def installToolChain(self,chrootID):
        self.logger.info("Installing toolchain.....")
        self.logger.info("Preparing build environment")
        previousVersionRPMSPath="/workspace1/testTP1RPMS/RPMS"
        cmdUtils = CommandUtils()
        prepareChrootCmd=self.prepareBuildRootCmd+" "+chrootID+" "+constants.specPath+" "+constants.rpmPath+" "+constants.logPath
        logFile=constants.logPath+"/prepareBuildRoot.log"
        returnVal=cmdUtils.runCommandInShell(prepareChrootCmd,logFile)
        if not returnVal:
            self.logger.error("Prepare build root script failed.Unable to prepare chroot.")
            raise Exception("Prepare build root script failed")
        
        for package in constants.listToolChainRPMPkgsToInstall:
            pkgUtils=PackageUtils(self.logName,self.logPath)
            rpmFile=pkgUtils.findRPMFileForGivenPackage(package)
            if rpmFile is None:
                rpmFile=self.findRPMFileInGivenLocation(package, previousVersionRPMSPath)
                if rpmFile is None:
                    self.logger.error("Unable to find rpm "+ package +" in current and previous versions")
                    raise "Input Error"
            self.logger.debug("Installing rpm:"+rpmFile)
            cmd="rpm -i --nodeps --root "+chrootID+" --define \'_dbpath /var/lib/rpm\' "+ rpmFile
            process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
            retval = process.wait()
            if retval != 0:
                self.logger.error("Installing tool chain package "+package+" failed")
                raise "RPM installation failed"
        
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/x86_64")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/noarch")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SOURCES")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SPECS")
        self.logger.info("Successfully prepared chroot:"+chrootID)
        self.logger.info("Installed tool chain successfully on chroot:"+chrootID)
    
    def installCoreToolChainPackages(self,chrootID):
        self.logger.info("Installing toolchain.....")
        self.prepareBuildEnvironmentChroot(chrootID)
        #cmdUtils=CommandUtils()
        #cmdUtils.runCommandInShell("rm "+ chrootID+"/"+constants.topDirPath+"/RPMS/x86_64/*")
        #cmdUtils.runCommandInShell("rm "+ chrootID+"/"+constants.topDirPath+"/RPMS/noarch/*")
        self.logger.info("Installed core tool chain packages successfully on chroot:"+chrootID)    
    
    
    
    def findRPMFileInGivenLocation(self,package,rpmdirPath):
        cmdUtils = CommandUtils()
        listFoundRPMFiles = cmdUtils.findFile(package+"-*.rpm",rpmdirPath)
        listFilterRPMFiles=[]
        for f in listFoundRPMFiles:
            f1=f.replace(package,"")
            print f1
            l = f1.split("-")
            print l
            if len(l) == 3:
                listFilterRPMFiles.append(f)
        if len(listFilterRPMFiles) == 1 :
            return listFilterRPMFiles[0]
        if len(listFilterRPMFiles) == 0 :
            return None
        if len(listFilterRPMFiles) > 1 :
            print("Found multiple rpm files for given package in rpm directory.Unable to determine the rpm file for package:"+package)
            return None
    
    def buildCoreToolChainPackages(self):
        self.logger.info("Building core tool chain packages.....")
        chrootID=None
        try:
            pkgUtils=PackageUtils(self.logName,self.logPath)
            for package in constants.listCoreToolChainRPMPackages:
                chrUtils = ChrootUtils(self.logName,self.logPath)
                chrootName="build-core-toolchain"
                returnVal,chrootID = chrUtils.createChroot(chrootName)
                if not returnVal:
                    self.logger.error("Creating chroot failed")
                    raise Exception("creating chroot failed")
                self.prepareBuildEnvironmentChroot(chrootID)
                rpmPkg=pkgUtils.findRPMFileForGivenPackage(package)
                if rpmPkg is None:
                    pkgUtils.buildRPMSForGivenPackage(package, chrootID)
                chrUtils.destroyChroot(chrootID)
                chrootID=None
            self.logger.info("Successfully built toolchain")
        except Exception as e:
            self.logger.error("Unable to build tool chain.")
            raise e
        finally:
            if chrootID is not None:
                chrUtils.destroyChroot(chrootID)
                
    def prepareBuildEnvironmentChroot(self,chrootID):
        self.logger.info("Preparing build environment")
        previousVersionRPMSPath="/workspace1/testTP1RPMS/RPMS"
        cmdUtils = CommandUtils()
        prepareChrootCmd=self.prepareBuildRootCmd+" "+chrootID+" "+constants.specPath+" "+constants.rpmPath+" "+constants.logPath
        logFile=constants.logPath+"/prepareBuildRoot.log"
        returnVal=cmdUtils.runCommandInShell(prepareChrootCmd,logFile)
        if not returnVal:
            self.logger.error("Prepare build root script failed.Unable to prepare chroot.")
            raise Exception("Prepare build root script failed")
        
        for package in constants.listToolChainRPMPkgsToBuild:
            pkgUtils=PackageUtils(self.logName,self.logPath)
            rpmFile=pkgUtils.findRPMFileForGivenPackage(package)
            if rpmFile is None:
                rpmFile=self.findRPMFileInGivenLocation(package, previousVersionRPMSPath)
                if rpmFile is None:
                    self.logger.error("Unable to find rpm "+ package +" in current and previous versions")
                    raise "Input Error"
            self.logger.debug("Installing rpm:"+rpmFile)
            cmd="rpm -i --nodeps --root "+chrootID+" --define \'_dbpath /var/lib/rpm\' "+ rpmFile
            process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
            retval = process.wait()
            if retval != 0:
                self.logger.error("Installing tool chain package "+package+" failed")
                raise "RPM installation failed"
        
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/x86_64")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/noarch")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SOURCES")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SPECS")
        self.logger.info("Successfully prepared chroot:"+chrootID)    
    