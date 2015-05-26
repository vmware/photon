from PackageUtils import PackageUtils
from Logger import Logger
from ChrootUtils import ChrootUtils
from ToolChainUtils import ToolChainUtils
from CommandUtils import CommandUtils
import os.path
from constants import constants

class PackageBuilder(object):
    
    #logger=None
    
    #@staticmethod
    #def setLog(logPath):
    #   PackageBuilder.logger=Logger.getLogger(logPath+"/PackageBuilder")
    
    def __init__(self,mapPackageToCycles,listAvailableCyclicPackages,logName=None,logPath=None):
        if logName is None:
            logName = "PackageBuilder"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.runInChrootCommand="./run-in-chroot.sh"
        self.mapPackageToCycles = mapPackageToCycles
        self.listAvailableCyclicPackages = listAvailableCyclicPackages
        self.listNodepsPackages = ["glibc","gmp","zlib","file","binutils","mpfr","mpc","gcc","ncurses","util-linux","groff","perl","texinfo","rpm","openssl","go"]
    
    #assumes tool chain is already built
    def prepareBuildRoot(self):
        chrUtils = ChrootUtils(self.logName,self.logPath)
        returnVal,chrootID = chrUtils.createChroot()
        if not returnVal:
            self.logger.error("Unable to build tool chain.")
            chrUtils.destroyChroot(chrootID)
            return False 
        tUtils=ToolChainUtils(self.logName,self.logPath)
        returnVal = tUtils.installToolChain(chrootID)
        return returnVal,chrootID
    
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
        cmdUtils = CommandUtils()
        listInstalledRPMs=cmdUtils.find_installed_rpm_packages(self.runInChrootCommand+" "+chrootID)
        listInstalledPackages=[]
        for installedRPM in listInstalledRPMs:
            packageName=self.findPackageNameFromRPMFile(installedRPM)
            if packageName is not None:
                listInstalledPackages.append(packageName)
        return listInstalledPackages
    
    def buildPackageThreadAPI(self,package,outputMap, threadName):
        returnVal=self.buildPackage(package)
        outputMap[threadName]=returnVal
        
    def buildPackage(self,package):
        #should initialize a logger based on package name
        chrUtils = ChrootUtils(self.logName,self.logPath)
        returnVal,chrootID = self.prepareBuildRoot()
        if not returnVal:
            return False
        
        destLogPath=constants.logPath+"/build-"+package
        if not os.path.isdir(destLogPath):
            cmdUtils = CommandUtils()
            cmdUtils.run_command("mkdir -p "+destLogPath)
        
        listInstalledPackages=self.findInstalledPackages(chrootID)
        self.logger.info("List of installed packages")
        self.logger.info(listInstalledPackages)
        returnVal,listDependentPackages=self.findBuildTimeRequiredPackages(package)
        if not returnVal:
            chrUtils.destroyChroot(chrootID)
            self.logger.error ("Failed during building the package"+package)
            return False
        
        if len(listDependentPackages) != 0:
            self.logger.info("Installing the build time dependent packages......")
            for pkg in listDependentPackages:
                returnVal = self.installPackage(pkg,chrootID,destLogPath,listInstalledPackages)
                if not returnVal:
                    self.logger.error("Failed while installing the build time dependent package"+pkg)
                    chrUtils.destroyChroot(chrootID)
                    return False
            self.logger.info("Finished installing the build time dependent packages......")

        pkgUtils = PackageUtils(self.logName,self.logPath)
        returnVal = pkgUtils.buildRPMSForGivenPackage(package,chrootID,destLogPath)
        if not returnVal:
            self.logger.error("Failed while building the package"+package)
            chrUtils.destroyChroot(chrootID)
            return False
        self.logger.info("Successfully built the package:"+package)
        chrUtils.destroyChroot(chrootID)
        return True
        
    def findRunTimeRequiredRPMPackages(self,rpmPackage):
        listRequiredPackages=constants.specData.getRequiresForPackage(rpmPackage)
        return True,listRequiredPackages
    
    def findBuildTimeRequiredPackages(self,package):
        listRequiredPackages=constants.specData.getBuildRequiresForPackage(package)
        return True,listRequiredPackages
    
    def installPackage(self,package,chrootID,destLogPath,listInstalledPackages):
        #if toolchain package called this method, preventing from installing again
        if package in listInstalledPackages:
            return True
        returnVal = self.installDependentRunTimePackages(package,chrootID,destLogPath,listInstalledPackages)
        if not returnVal:
            return False
        pkgUtils = PackageUtils(self.logName,self.logPath)
        noDeps=False
        if self.mapPackageToCycles.has_key(package):
            noDeps = True
        if package in self.listNodepsPackages:
            noDeps=True
        returnVal = pkgUtils.installRPM(package,chrootID,noDeps,destLogPath)
        if not returnVal:
            self.logger.error("Stop installing package"+package)
            return False
        listInstalledPackages.append(package)
        self.logger.info("Installed the package:"+package)
        return True

    def installDependentRunTimePackages(self,package,chrootID,destLogPath,listInstalledPackages):
        returnVal,listRunTimeDependentPackages=self.findRunTimeRequiredRPMPackages(package)
        if not returnVal:
            return False
        if len(listRunTimeDependentPackages) != 0:
            for pkg in listRunTimeDependentPackages:
                if self.mapPackageToCycles.has_key(pkg) and pkg not in self.listAvailableCyclicPackages:
                    continue
                if pkg in listInstalledPackages:
                    continue
                returnVal = self.installPackage(pkg,chrootID,destLogPath,listInstalledPackages)
                if not returnVal:
                    return False
        return True
