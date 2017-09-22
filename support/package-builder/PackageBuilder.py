from PackageUtils import PackageUtils
from Logger import Logger
from ChrootUtils import ChrootUtils
from ToolChainUtils import ToolChainUtils
from CommandUtils import CommandUtils
import os.path
from constants import constants
import shutil
from SpecData import SPECS

class PackageBuilder(object):

    def __init__(self,mapPackageToCycles,listAvailableCyclicPackages,listBuildOptionPackages,pkgBuildOptionFile):
        # will be initialized in buildPackageThreadAPI()
        self.logName=None
        self.logPath=None
        self.logger=None
        self.package=None
        self.mapPackageToCycles = mapPackageToCycles
        self.listAvailableCyclicPackages = listAvailableCyclicPackages
        self.listNodepsPackages = ["glibc","gmp","zlib","file","binutils","mpfr","mpc","gcc","ncurses","util-linux","groff","perl","texinfo","rpm","openssl","go"]
        self.listBuildOptionPackages=listBuildOptionPackages
        self.pkgBuildOptionFile=pkgBuildOptionFile

    def prepareBuildRoot(self):
        chrootID=None
        chrootName="build-"+self.package
        try:
            chrUtils = ChrootUtils(self.logName,self.logPath)
            returnVal,chrootID = chrUtils.createChroot(chrootName)
            self.logger.debug("Created new chroot: " + chrootID)
            if not returnVal:
                raise Exception("Unable to prepare build root")
            tUtils=ToolChainUtils(self.logName,self.logPath)
            tUtils.installToolChainRPMS(chrootID, self.package, self.logPath)
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
        self.package=package
        self.logName="build-"+package
        self.logPath=constants.logPath+"/build-"+package
        if not os.path.isdir(self.logPath):
            cmdUtils = CommandUtils()
            cmdUtils.runCommandInShell("mkdir -p "+self.logPath)
        self.logger=Logger.getLogger(self.logName,self.logPath)

        try:
            self.buildPackage()
            outputMap[threadName]=True
        except Exception as e:
            # TODO: self.logger might be None
            self.logger.error(e)
            outputMap[threadName]=False

    def checkIfPackageIsAlreadyBuilt(self):
        basePkg=SPECS.getData().getSpecName(self.package)
        listRPMPackages=SPECS.getData().getRPMPackages(basePkg)
        packageIsAlreadyBuilt=True
        pkgUtils = PackageUtils(self.logName,self.logPath)
        for pkg in listRPMPackages:
            if pkgUtils.findRPMFileForGivenPackage(pkg) is None:
                packageIsAlreadyBuilt=False
                break
        return packageIsAlreadyBuilt

    def buildPackage(self):
        #do not build if RPM is already built
        #test only if the package is in the testForceRPMS with rpmCheck
        #build only if the package is not in the testForceRPMS with rpmCheck
        if self.checkIfPackageIsAlreadyBuilt():
            if not constants.rpmCheck:
                self.logger.info("Skipping building the package:"+self.package)
                return
            elif constants.rpmCheck and self.package not in constants.testForceRPMS:
                self.logger.info("Skipping testing the package:"+self.package)
                return

        chrUtils = ChrootUtils(self.logName,self.logPath)
        chrootID=None
        try:
            chrootID = self.prepareBuildRoot()
            listInstalledPackages=self.findInstalledPackages(chrootID)
            listDependentPackages=self.findBuildTimeRequiredPackages()
            if constants.rpmCheck and self.package in constants.testForceRPMS:
                listDependentPackages.extend(self.findBuildTimeCheckRequiredPackages())
                testPackages=set(constants.listMakeCheckRPMPkgtoInstall)-set(listInstalledPackages)-set([self.package])
                listDependentPackages.extend(testPackages)
                listDependentPackages=list(set(listDependentPackages))

            pkgUtils = PackageUtils(self.logName,self.logPath)
            if len(listDependentPackages) != 0:
                self.logger.info("Installing the build time dependent packages......")
                for pkg in listDependentPackages:
                    self.installPackage(pkgUtils, pkg,chrootID,self.logPath,listInstalledPackages)
                pkgUtils.installRPMSInAOneShot(chrootID,self.logPath)
                self.logger.info("Finished installing the build time dependent packages......")

            pkgUtils.adjustGCCSpecs(self.package, chrootID, self.logPath)
            pkgUtils.buildRPMSForGivenPackage(self.package,chrootID,self.listBuildOptionPackages,self.pkgBuildOptionFile,self.logPath)
            self.logger.info("Successfully built the package:"+self.package)
        except Exception as e:
            self.logger.error("Failed while building package:" + self.package)
            self.logger.debug("Chroot with ID: " + chrootID + " not deleted for debugging.")
            logFileName = os.path.join(self.logPath, self.package + ".log")
            fileLog = os.popen('tail -n 100 ' + logFileName).read()
            self.logger.debug(fileLog)
            raise e
        if chrootID is not None:
            chrUtils.destroyChroot(chrootID)


    def findRunTimeRequiredRPMPackages(self,rpmPackage):
        listRequiredPackages=SPECS.getData().getRequiresForPackage(rpmPackage)
        return listRequiredPackages

    def findBuildTimeRequiredPackages(self):
        listRequiredPackages=SPECS.getData().getBuildRequiresForPackage(self.package)
        return listRequiredPackages

    def findBuildTimeCheckRequiredPackages(self):
        listRequiredPackages=SPECS.getData().getCheckBuildRequiresForPackage(self.package)
        return listRequiredPackages

    def installPackage(self,pkgUtils,package,chrootID,destLogPath,listInstalledPackages):
        if package in listInstalledPackages:
            return
        self.installDependentRunTimePackages(pkgUtils,package,chrootID,destLogPath,listInstalledPackages)
        noDeps=False
        if self.mapPackageToCycles.has_key(package):
            noDeps = True
        if package in self.listNodepsPackages:
            noDeps=True
        if package in constants.noDepsPackageList:
            noDeps=True
        pkgUtils.installRPM(package,chrootID,noDeps,destLogPath)
        listInstalledPackages.append(package)

    def installDependentRunTimePackages(self,pkgUtils,package,chrootID,destLogPath,listInstalledPackages):
        listRunTimeDependentPackages=self.findRunTimeRequiredRPMPackages(package)
        if len(listRunTimeDependentPackages) != 0:
            for pkg in listRunTimeDependentPackages:
                if self.mapPackageToCycles.has_key(pkg) and pkg not in self.listAvailableCyclicPackages:
                    continue
                if pkg in listInstalledPackages:
                    continue
                self.installPackage(pkgUtils,pkg,chrootID,destLogPath,listInstalledPackages)

