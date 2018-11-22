from PackageUtils import PackageUtils
from Logger import Logger
from ChrootUtils import ChrootUtils
from ToolChainUtils import ToolChainUtils
from CommandUtils import CommandUtils
import os.path
from constants import constants
import shutil
from SpecData import SPECS
from StringUtils import StringUtils

class PackageBuilderBase(object):
    def __init__(self, mapPackageToCycles, pkgBuildType):
        # will be initialized in buildPackageFunction()
        self.logName = None
        self.logPath = None
        self.logger = None
        self.package = None
        self.version = None
        self.mapPackageToCycles = mapPackageToCycles
        self.listNodepsPackages = ["glibc", "gmp", "zlib", "file", "binutils", "mpfr",
                                   "mpc", "gcc", "ncurses", "util-linux", "groff", "perl",
                                   "texinfo", "rpm", "openssl", "go"]
        self.pkgBuildType = pkgBuildType

    def _findPackageNameAndVersionFromRPMFile(self, rpmfile):
        rpmfile = os.path.basename(rpmfile)
        releaseindex = rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:" + rpmfile)
            return None
        pkg = rpmfile[0:releaseindex]
        return pkg

    def checkIfPackageIsAlreadyBuilt(self, package, version):
        basePkg=SPECS.getData().getSpecName(package)
        listRPMPackages=SPECS.getData().getRPMPackages(basePkg, version)
        packageIsAlreadyBuilt=True
        pkgUtils = PackageUtils(self.logName,self.logPath)
        for pkg in listRPMPackages:
            if pkgUtils.findRPMFileForGivenPackage(pkg, version) is None:
                packageIsAlreadyBuilt=False
                break
        return packageIsAlreadyBuilt

    def findRunTimeRequiredRPMPackages(self,rpmPackage, version):
        listRequiredPackages=SPECS.getData().getRequiresForPackage(rpmPackage, version)
        return listRequiredPackages

    def findBuildTimeRequiredPackages(self):
        listRequiredPackages=SPECS.getData().getBuildRequiresForPackage(self.package, self.version)
        return listRequiredPackages

    def findBuildTimeCheckRequiredPackages(self):
        listRequiredPackages=SPECS.getData().getCheckBuildRequiresForPackage(self.package, self.version)
        return listRequiredPackages

class PackageBuilder(PackageBuilderBase):

    def __init__(self,mapPackageToCycles,listAvailableCyclicPackages,listBuildOptionPackages,pkgBuildOptionFile):
        PackageBuilderBase.__init__(self, mapPackageToCycles, "chroot")
        # will be initialized in buildPackageThreadAPI()
        self.listAvailableCyclicPackages = listAvailableCyclicPackages

        self.listBuildOptionPackages=listBuildOptionPackages
        self.pkgBuildOptionFile=pkgBuildOptionFile

    def prepareBuildRoot(self):
        chrootID=None
        chrootName="build-"+self.package + "-" + self.version
        try:
            chrUtils = ChrootUtils(self.logName,self.logPath)
            returnVal,chrootID = chrUtils.createChroot(chrootName)
            self.logger.debug("Created new chroot: " + chrootID)
            if not returnVal:
                raise Exception("Unable to prepare build root")
            tUtils=ToolChainUtils(self.logName,self.logPath)
            tUtils.installToolChainRPMS(chrootID, self.package,self.version, self.listBuildOptionPackages, self.pkgBuildOptionFile, self.logPath)
        except Exception as e:
            if chrootID is not None:
                self.logger.debug("Deleting chroot: " + chrootID)
                chrUtils.destroyChroot(chrootID)
            raise e
        return chrootID

    def findInstalledPackages(self, instanceID):
        pkgUtils = PackageUtils(self.logName, self.logPath)
        if self.pkgBuildType == "chroot":
            listInstalledRPMs = pkgUtils.findInstalledRPMPackages(instanceID)
        listInstalledPackages = []
        for installedRPM in listInstalledRPMs:
            pkg = self._findPackageNameAndVersionFromRPMFile(installedRPM)
            if pkg is not None:
                listInstalledPackages.append(pkg)
        return listInstalledPackages, listInstalledRPMs

    def buildPackageThreadAPI(self,package,outputMap, threadName,):
        packageName, packageVersion = StringUtils.splitPackageNameAndVersion(package)
        #do not build if RPM is already built
        #test only if the package is in the testForceRPMS with rpmCheck
        #build only if the package is not in the testForceRPMS with rpmCheck
        if self.checkIfPackageIsAlreadyBuilt(packageName, packageVersion):
            if not constants.rpmCheck:
                outputMap[threadName]=True
                return
            elif constants.rpmCheck and packageName not in constants.testForceRPMS:
                outputMap[threadName]=True
                return

        self.package=packageName
        self.version=packageVersion
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
            self.logger.exception(e)
            outputMap[threadName]=False
            raise e

    def buildPackage(self):
        chrUtils = ChrootUtils(self.logName,self.logPath)
        chrootID=None
        try:
            chrootID = self.prepareBuildRoot()
            listInstalledPackages, listInstalledRPMs=self.findInstalledPackages(chrootID)
            listDependentPackages=self.findBuildTimeRequiredPackages()
            listTestPackages=[]
            if constants.rpmCheck and self.package in constants.testForceRPMS:
                listDependentPackages.extend(self.findBuildTimeCheckRequiredPackages())
                testPackages=set(constants.listMakeCheckRPMPkgtoInstall)-set(listInstalledPackages)-set([self.package])
                listTestPackages = list(set(testPackages))
                listDependentPackages=list(set(listDependentPackages))
            pkgUtils = PackageUtils(self.logName,self.logPath)
            if len(listDependentPackages) != 0:
                self.logger.info("Installing the build time dependent packages......")
                for pkg in listDependentPackages:
                    packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                    self.installPackage(pkgUtils,packageName,packageVersion,chrootID,self.logPath,listInstalledPackages,listInstalledRPMs)
                for pkg in listTestPackages:
                    flag=False
                    packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                    for depPkg in listDependentPackages:
                        depPackageName, depPackageVersion = StringUtils.splitPackageNameAndVersion(depPkg)
                        if depPackageName == packageName:
                                flag = True
                                break;
                    if flag == False:
                        self.installPackage(pkgUtils,packageName,packageVersion,chrootID,self.logPath,listInstalledPackages,listInstalledRPMs)
                pkgUtils.installRPMSInAOneShot(chrootID,self.logPath)
                self.logger.info("Finished installing the build time dependent packages......")

            pkgUtils.adjustGCCSpecs(self.package, chrootID, self.logPath, self.version)
            pkgUtils.buildRPMSForGivenPackage(self.package,self.version,chrootID,self.listBuildOptionPackages,self.pkgBuildOptionFile,self.logPath)
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

    def installPackage(self,pkgUtils,package,packageVersion,chrootID,destLogPath,listInstalledPackages,listInstalledRPMs):
        rpmfile = pkgUtils.findRPMFileForGivenPackage(package,packageVersion);
        if rpmfile is None:
            self.logger.error("No rpm file found for package: " + package + "-" + packageVersion)
            raise Exception("Missing rpm file")
        specificRPM = os.path.basename(rpmfile.replace(".rpm", ""))
        pkg = package+"-"+packageVersion
        if pkg in listInstalledPackages:
            return
        # For linux packages, install the gcc dependencies from publish rpms
        if self.package in self.listBuildOptionPackages:
            if SPECS.getData().getSpecName(package) == "gcc":
                tUtils=ToolChainUtils(self.logName,self.logPath)
                overridenPkgVer = tUtils.getOverridenPackageVersion(self.package, package, self.listBuildOptionPackages, self.pkgBuildOptionFile)
                overridenPkg = package+"-"+overridenPkgVer
                if overridenPkg in listInstalledPackages:
                    return

        # mark it as installed -  to avoid cyclic recursion
        listInstalledPackages.append(pkg)
        listInstalledRPMs.append(specificRPM)
        self.installDependentRunTimePackages(pkgUtils,package,packageVersion, chrootID,destLogPath,listInstalledPackages,listInstalledRPMs)
        noDeps=False
        if self.mapPackageToCycles.has_key(package):
            noDeps = True
        if package in self.listNodepsPackages:
            noDeps=True
        if package in constants.noDepsPackageList:
            noDeps=True

        pkgUtils.installRPM(package,packageVersion,chrootID,noDeps,destLogPath)

    def installDependentRunTimePackages(self,pkgUtils,package,packageVersion,chrootID,destLogPath,listInstalledPackages,listInstalledRPMs):
        listRunTimeDependentPackages=self.findRunTimeRequiredRPMPackages(package,packageVersion)
        if len(listRunTimeDependentPackages) != 0:
            for pkg in listRunTimeDependentPackages:
                if self.mapPackageToCycles.has_key(pkg):
                    continue
                packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                latestPkgRPM = os.path.basename(
                    pkgUtils.findRPMFileForGivenPackage(packageName, packageVersion)).replace(".rpm", "")
                if pkg in listInstalledPackages and latestPkgRPM in listInstalledRPMs:
                    continue
                self.installPackage(pkgUtils,packageName,packageVersion,chrootID,destLogPath,listInstalledPackages,listInstalledRPMs)


