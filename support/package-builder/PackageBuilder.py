from PackageUtils import PackageUtils
from Logger import Logger
from ChrootUtils import ChrootUtils
from ToolChainUtils import ToolChainUtils
from CommandUtils import CommandUtils
import os.path
from constants import constants
import shutil
from time import sleep

class PackageBuilder(object):
    
    def __init__(self,mapPackageToCycles,listAvailableCyclicPackages,logName=None,logPath=None):
        if logName is None:
            logName = "PackageBuilder"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.mapPackageToCycles = mapPackageToCycles
        self.listAvailableCyclicPackages = listAvailableCyclicPackages
        self.listNodepsPackages = ["glibc","gmp","zlib","file","binutils","mpfr","mpc","gcc","ncurses","util-linux","groff","perl","texinfo","rpm","openssl","go"]
        self.runInChrootCommand="./run-in-chroot.sh"
        self.adjustGCCSpecScript="adjust-gcc-specs.sh"
        
    def prepareBuildRoot(self,chrootName,isToolChainPackage=False):
        chrootID=None
        try:
            chrUtils = ChrootUtils(self.logName,self.logPath)
            returnVal,chrootID = chrUtils.createChroot(chrootName)
            self.logger.debug("Created new chroot: " + chrootID)
            if not returnVal:
                raise Exception("Unable to prepare build root")
            tUtils=ToolChainUtils(self.logName,self.logPath)
            if isToolChainPackage:
                tUtils.installCoreToolChainPackages(chrootID)
            else:
                tUtils.installToolChain(chrootID)
        except Exception as e:
            if chrootID is not None:
                self.logger.debug("Deleting chroot: " + chrootID)
                chrUtils.destroyChroot(chrootID)
            raise e
        return chrootID
    
    def findPackageNameFromRPMFile(self,rpmfile):
        rpmfile=os.path.basename(rpmfile)
        releaseindex=rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:"+rpmfile)
            return None
        versionindex=rpmfile[0:releaseindex].rfind("-")
        if versionindex == -1:
            self.logger.error("Invalid rpm file:"+rpmfile)
            return None
        packageName=rpmfile[0:versionindex]
        return packageName
    
    def findInstalledPackages(self,chrootID):
        pkgUtils = PackageUtils(self.logName,self.logPath)
        listInstalledRPMs=pkgUtils.findInstalledRPMPackages(chrootID)
        listInstalledPackages=[]
        for installedRPM in listInstalledRPMs:
            packageName=self.findPackageNameFromRPMFile(installedRPM)
            if packageName is not None:
                listInstalledPackages.append(packageName)
        return listInstalledPackages
    
    def buildPackageThreadAPI(self,package,outputMap, threadName,):
        try:
            self.buildPackage(package)
            outputMap[threadName]=True
        except Exception as e:
            self.logger.error(e)
            outputMap[threadName]=False
        
    def buildPackage(self,package):
        #should initialize a logger based on package name
        chrUtils = ChrootUtils(self.logName,self.logPath)
        chrootName="build-"+package
        chrootID=None
        isToolChainPackage=False
        if package in constants.listToolChainPackages:
            isToolChainPackage=True
        try:
            chrootID = self.prepareBuildRoot(chrootName,isToolChainPackage)
            destLogPath=constants.logPath+"/build-"+package
            if not os.path.isdir(destLogPath):
                cmdUtils = CommandUtils()
                cmdUtils.runCommandInShell("mkdir -p "+destLogPath)
            
            listInstalledPackages=self.findInstalledPackages(chrootID)
            self.logger.info("List of installed packages")
            self.logger.info(listInstalledPackages)
            listDependentPackages=self.findBuildTimeRequiredPackages(package)
            
            if len(listDependentPackages) != 0:
                self.logger.info("Installing the build time dependent packages......")
                for pkg in listDependentPackages:
                    self.installPackage(pkg,chrootID,destLogPath,listInstalledPackages)
                self.logger.info("Finished installing the build time dependent packages......")
            self.adjustGCCSpecs(package, chrootID, destLogPath)
            pkgUtils = PackageUtils(self.logName,self.logPath)
            pkgUtils.buildRPMSForGivenPackage(package,chrootID,destLogPath)
            self.logger.info("Successfully built the package:"+package)
        except Exception as e:
            self.logger.error("Failed while building package:" + package)
            self.logger.debug("Chroot with ID: " + chrootID + " not deleted for debugging.")
            raise e
        if chrootID is not None:
            chrUtils.destroyChroot(chrootID)
        
        
    def findRunTimeRequiredRPMPackages(self,rpmPackage):
        listRequiredPackages=constants.specData.getRequiresForPackage(rpmPackage)
        return listRequiredPackages
    
    def findBuildTimeRequiredPackages(self,package):
        listRequiredPackages=constants.specData.getBuildRequiresForPackage(package)
        return listRequiredPackages
    
    def installPackage(self,package,chrootID,destLogPath,listInstalledPackages):
        if package in listInstalledPackages:
            return
        self.installDependentRunTimePackages(package,chrootID,destLogPath,listInstalledPackages)
        pkgUtils = PackageUtils(self.logName,self.logPath)
        noDeps=False
        if self.mapPackageToCycles.has_key(package):
            noDeps = True
        if package in self.listNodepsPackages:
            noDeps=True
        if package in constants.noDepsPackageList:
            noDeps=True
        pkgUtils.installRPM(package,chrootID,noDeps,destLogPath)
        listInstalledPackages.append(package)
        self.logger.info("Installed the package:"+package)

    def installDependentRunTimePackages(self,package,chrootID,destLogPath,listInstalledPackages):
        listRunTimeDependentPackages=self.findRunTimeRequiredRPMPackages(package)
        if len(listRunTimeDependentPackages) != 0:
            for pkg in listRunTimeDependentPackages:
                if self.mapPackageToCycles.has_key(pkg) and pkg not in self.listAvailableCyclicPackages:
                    continue
                if pkg in listInstalledPackages:
                    continue
                self.installPackage(pkg,chrootID,destLogPath,listInstalledPackages)

    def adjustGCCSpecs(self, package, chrootID, logPath):
        opt = ""
        # TODO: reading of hardening flag from spec files
        if package == "linux" or package == "glibc":
            opt = " clean"
        elif package.startswith("xf86-") or package.startswith("xorg-server") :
            opt = " nonow"

        shutil.copy2(self.adjustGCCSpecScript,  chrootID+"/tmp/"+self.adjustGCCSpecScript)
        cmdUtils=CommandUtils()
        cmd = "/tmp/"+self.adjustGCCSpecScript+opt
        logFile = logPath+"/adjustGCCSpecScript.log"
        chrootCmd=self.runInChrootCommand+" "+chrootID
        retryCount=10
        returnVal=False
        while retryCount > 0:
            returnVal = cmdUtils.runCommandInShell(cmd, logFile, chrootCmd)
            if returnVal:
                return
            self.logger.error("Failed while adjusting gcc specs")
            self.logger.error("Retrying again .....")
            retryCount = retryCount - 1
            sleep(5)
        if not returnVal:
            self.logger.error("Failed while adjusting gcc specs")
            raise "Failed while adjusting gcc specs"
