from PackageUtils import PackageUtils
from Logger import Logger
from ChrootUtils import ChrootUtils
from ToolChainUtils import ToolChainUtils
from CommandUtils import CommandUtils
import os.path
from constants import constants
import shutil
from SpecData import SPECS
import docker
import sys

class PackageBuilderBase(object):
    def __init__(self,mapPackageToCycles,listAvailableCyclicPackages,listBuildOptionPackages,pkgBuildOptionFile, pkgBuildType):
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
        self.pkgBuildType = pkgBuildType

    def buildPackageThreadAPIPrepare(self,package,outputMap, threadName):
        self.package=package
        self.logName="build-"+package
        self.logPath=constants.logPath+"/build-"+package
        if not os.path.isdir(self.logPath):
            cmdUtils = CommandUtils()
            cmdUtils.runCommandInShell("mkdir -p "+self.logPath)
        self.logger=Logger.getLogger(self.logName,self.logPath)

    def findPackageNameFromRPMFile(self,rpmfile):
        rpmfile = os.path.basename(rpmfile).decode()
        releaseindex = rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:" + rpmfile)
            return None
        versionindex = rpmfile[0:releaseindex].rfind("-")
        if versionindex == -1:
            self.logger.error("Invalid rpm file:" + rpmfile)
            return None
        packageName=rpmfile[0:versionindex]
        return packageName

    def findInstalledPackages(self, instanceID):
        pkgUtils = PackageUtils(self.logName, self.logPath)
        if self.pkgBuildType == "chroot":
            listInstalledRPMs = pkgUtils.findInstalledRPMPackages(instanceID)
        elif self.pkgBuildType == "container":
            listInstalledRPMs = pkgUtils.findInstalledRPMPackagesInContainer(instanceID)
        listInstalledPackages=[]
        for installedRPM in listInstalledRPMs:
            packageName=self.findPackageNameFromRPMFile(installedRPM)
            if packageName is not None:
                listInstalledPackages.append(packageName)
        return listInstalledPackages, listInstalledRPMs

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

    def findRunTimeRequiredRPMPackages(self,rpmPackage):
        listRequiredPackages=SPECS.getData().getRequiresForPackage(rpmPackage)
        return listRequiredPackages

    def findBuildTimeRequiredPackages(self):
        listRequiredPackages=SPECS.getData().getBuildRequiresForPackage(self.package)
        return listRequiredPackages

    def findBuildTimeCheckRequiredPackages(self):
        listRequiredPackages=SPECS.getData().getCheckBuildRequiresForPackage(self.package)
        return listRequiredPackages

    def installPackage(self, pkgUtils, package, instanceID, destLogPath, listInstalledPackages, listInstalledRPMs):
        latestRPM = os.path.basename(pkgUtils.findRPMFileForGivenPackage(package)).replace(".rpm", "")
        if package in listInstalledPackages and latestRPM in listInstalledRPMs:
            return
        # mark it as installed -  to avoid cyclic recursion
        listInstalledPackages.append(package)
        listInstalledRPMs.append(latestRPM)
        self.installDependentRunTimePackages(pkgUtils,package,instanceID,destLogPath,listInstalledPackages, listInstalledRPMs)
        noDeps=False
        if package in self.mapPackageToCycles:
            noDeps = True
        if package in self.listNodepsPackages:
            noDeps=True
        if package in constants.noDepsPackageList:
            noDeps=True
        if self.pkgBuildType == "chroot":
            pkgUtils.installRPM(package,instanceID,noDeps,destLogPath)
        elif self.pkgBuildType == "container":
            pkgUtils.prepRPMforInstallInContainer(package, instanceID, noDeps, destLogPath)

    def installDependentRunTimePackages(self,pkgUtils,package,instanceID,destLogPath,listInstalledPackages, listInstalledRPMs):
        listRunTimeDependentPackages=self.findRunTimeRequiredRPMPackages(package)
        if len(listRunTimeDependentPackages) != 0:
            for pkg in listRunTimeDependentPackages:
                if pkg in self.mapPackageToCycles and pkg not in self.listAvailableCyclicPackages:
                    continue
                latestPkgRPM = os.path.basename(pkgUtils.findRPMFileForGivenPackage(pkg)).replace(".rpm", "") 
                if pkg in listInstalledPackages and latestPkgRPM in listInstalledRPMs:
                    continue
                self.installPackage(pkgUtils, pkg, instanceID, destLogPath, listInstalledPackages, listInstalledRPMs)

class PackageBuilderContainer(object):
    def __init__(self, mapPackageToCycles, listAvailableCyclicPackages, listBuildOptionPackages, pkgBuildOptionFile, pkgBuildType):
        self.buildContainerImage = "photon_build_container:latest"
        self.dockerClient = docker.from_env(version="auto")

        self.base = PackageBuilderBase(mapPackageToCycles, listAvailableCyclicPackages,
                                       listBuildOptionPackages, pkgBuildOptionFile, pkgBuildType)

    def buildPackageThreadAPI(self, package, outputMap, threadName):
        self.base.buildPackageThreadAPIPrepare(package, outputMap, threadName)
        try:
            self.buildPackage()
            outputMap[threadName]=True
        except Exception as e:
            # TODO: self.logger might be None
            self.base.logger.exception(e)
            outputMap[threadName]=False
            raise e

    def prepareBuildContainer(self, containerTaskName, packageName, isToolChainPackage=False):
        # Prepare an empty chroot environment to let docker use the BUILD folder.
        # This avoids docker using overlayFS which will cause make check failure.
        chrootName="build-"+packageName
        chrUtils = ChrootUtils(self.base.logName, self.base.logPath)
        returnVal,chrootID = chrUtils.createChroot(chrootName)
        if not returnVal:
            raise Exception("Unable to prepare build root")
        cmdUtils = CommandUtils()
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + constants.topDirPath)
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + constants.topDirPath + "/BUILD")

        containerID = None
        mountVols = {
                        constants.prevPublishRPMRepo: {'bind': '/publishrpms', 'mode': 'ro'},
                        constants.prevPublishXRPMRepo: {'bind': '/publishxrpms', 'mode': 'ro'},
                        constants.tmpDirPath: {'bind': '/tmp', 'mode': 'rw'},
                        constants.rpmPath: {'bind': constants.topDirPath + "/RPMS", 'mode': 'rw'},
                        constants.sourceRpmPath: {'bind': constants.topDirPath + "/SRPMS", 'mode': 'rw'},
                        constants.logPath + "/" + self.base.logName: {'bind': constants.topDirPath + "/LOGS", 'mode': 'rw'},
                        chrootID + constants.topDirPath + "/BUILD": {'bind': constants.topDirPath + "/BUILD", 'mode': 'rw'},
                        constants.dockerUnixSocket: {'bind': constants.dockerUnixSocket, 'mode': 'rw'}
                    }

        containerName = containerTaskName
        containerName = containerName.replace("+", "p")
        try:
            oldContainerID = self.dockerClient.containers.get(containerName)
            if oldContainerID is not None:
                oldContainerID.remove(force=True)
        except docker.errors.NotFound:
            sys.exc_clear()

        try:
            self.base.logger.info("BuildContainer-prepareBuildContainer: Starting build container: " + containerName)
            #TODO: Is init=True equivalent of --sig-proxy?
            privilegedDocker = False
            cap_list = ['SYS_PTRACE']
            if packageName in constants.listReqPrivilegedDockerForTest:
                privilegedDocker = True

            containerID = self.dockerClient.containers.run(self.buildContainerImage,
                                                               detach=True,
                                                               cap_add=cap_list,
                                                               privileged=privilegedDocker,
                                                               name=containerName,
                                                               network_mode="host",
                                                               volumes=mountVols,
                                                               command="/bin/bash -l -c /wait.sh")

            self.base.logger.debug("Started Photon build container for task " + containerTaskName
                               + " ID: " + containerID.short_id)
            if not containerID:
                raise Exception("Unable to start Photon build container for task " + containerTaskName)
        except Exception as e:
            self.base.logger.debug("Unable to start Photon build container for task " + containerTaskName)
            raise e
        return containerID, chrootID

    def buildPackage(self):
        #do not build if RPM is already built
        #test only if the package is in the testForceRPMS with rpmCheck
        #build only if the package is not in the testForceRPMS with rpmCheck
        if self.base.checkIfPackageIsAlreadyBuilt():
            if not constants.rpmCheck:
                self.base.logger.info("Skipping building the package:" + self.base.package)
                return
            elif constants.rpmCheck and self.base.package not in constants.testForceRPMS:
                self.base.logger.info("Skipping testing the package:" + self.base.package)
                return

        #should initialize a logger based on package name
        containerTaskName = "build-" + self.base.package
        containerID = None
        chrootID = None
        isToolChainPackage = False
        if self.base.package in constants.listToolChainPackages:
            isToolChainPackage = True
        destLogPath = constants.logPath + "/build-" + self.base.package
        try:
            containerID, chrootID = self.prepareBuildContainer(containerTaskName, self.base.package, isToolChainPackage)

            tcUtils = ToolChainUtils(self.base.logName, self.base.logPath)
            if self.base.package in constants.perPackageToolChain:
                self.base.logger.debug(constants.perPackageToolChain[self.base.package])
                tcUtils.installCustomToolChainRPMSinContainer(containerID,
                                                              constants.perPackageToolChain[self.base.package],
                                                              self.base.package);

            listInstalledPackages, listInstalledRPMs = self.base.findInstalledPackages(containerID)
            self.base.logger.info(listInstalledPackages)
            listDependentPackages = self.base.findBuildTimeRequiredPackages()
            if constants.rpmCheck and self.base.package in constants.testForceRPMS:
                listDependentPackages.extend(self.base.findBuildTimeCheckRequiredPackages())
                testPackages=set(constants.listMakeCheckRPMPkgtoInstall)-set(listInstalledPackages)-set([self.base.package])
                listDependentPackages.extend(testPackages)
                listDependentPackages=list(set(listDependentPackages))

            pkgUtils = PackageUtils(self.base.logName, self.base.logPath)
            if len(listDependentPackages) != 0:
                self.base.logger.info("BuildContainer-buildPackage: Installing dependent packages..")
                self.base.logger.info(listDependentPackages)
                for pkg in listDependentPackages:
                    self.base.installPackage(pkgUtils, pkg, containerID, destLogPath, listInstalledPackages, listInstalledRPMs)
                pkgUtils.installRPMSInAOneShotInContainer(containerID, destLogPath)
                self.base.logger.info("Finished installing the build time dependent packages......")

            self.base.logger.info("BuildContainer-buildPackage: Start building the package: " + self.base.package)
            pkgUtils.adjustGCCSpecsInContainer(self.base.package, containerID, destLogPath)
            pkgUtils.buildRPMSForGivenPackageInContainer(
                                               self.base.package,
                                               containerID,
                                               self.base.listBuildOptionPackages,
                                               self.base.pkgBuildOptionFile,
                                               destLogPath)
            self.base.logger.info("BuildContainer-buildPackage: Successfully built the package: " + self.base.package)
        except Exception as e:
            self.base.logger.error("Failed while building package:" + self.base.package)
            if containerID is not None:
                self.base.logger.debug("Container " + containerID.short_id + " retained for debugging.")
            logFileName = os.path.join(destLogPath, self.base.package + ".log")
            fileLog = os.popen('tail -n 20 ' + logFileName).read()
            self.base.logger.debug(fileLog)
            raise e

        # Remove the container
        if containerID is not None:
            containerID.remove(force=True)
        # Remove the dummy chroot
        if chrootID is not None:
            chrUtils = ChrootUtils(self.base.logName, self.base.logPath)
            chrUtils.destroyChroot(chrootID)

class PackageBuilderChroot(object):
    def __init__(self, mapPackageToCycles, listAvailableCyclicPackages, listBuildOptionPackages, pkgBuildOptionFile, pkgBuildType):
        self.base = PackageBuilderBase(mapPackageToCycles, listAvailableCyclicPackages,
                                       listBuildOptionPackages, pkgBuildOptionFile, pkgBuildType)

    def buildPackageThreadAPI(self, package, outputMap, threadName):
        self.base.buildPackageThreadAPIPrepare(package,outputMap, threadName)
        try:
            self.buildPackage()
            outputMap[threadName]=True
        except Exception as e:
            # TODO: self.logger might be None
            self.base.logger.exception(e)
            outputMap[threadName]=False
            raise e

    def prepareBuildRoot(self):
        chrootID=None
        chrootName="build-"+self.base.package
        try:
            chrUtils = ChrootUtils(self.base.logName,self.base.logPath)
            returnVal,chrootID = chrUtils.createChroot(chrootName)
            self.base.logger.debug("Created new chroot: " + chrootID)
            if not returnVal:
                raise Exception("Unable to prepare build root")
            tUtils=ToolChainUtils(self.base.logName,self.base.logPath)
            tUtils.installToolChainRPMS(chrootID, self.base.package, self.base.logPath)
        except Exception as e:
            if chrootID is not None:
                self.base.logger.debug("Deleting chroot: " + chrootID)
                chrUtils.destroyChroot(chrootID)
            raise e
        return chrootID

    def buildPackage(self):
        #do not build if RPM is already built
        #test only if the package is in the testForceRPMS with rpmCheck
        #build only if the package is not in the testForceRPMS with rpmCheck
        if self.base.checkIfPackageIsAlreadyBuilt():
            if not constants.rpmCheck:
                self.base.logger.info("Skipping building the package:" + self.base.package)
                return
            elif constants.rpmCheck and self.base.package not in constants.testForceRPMS:
                self.base.logger.info("Skipping testing the package:" + self.base.package)
                return

        chrUtils = ChrootUtils(self.base.logName,self.base.logPath)
        chrootID=None
        try:
            chrootID = self.prepareBuildRoot()
            listInstalledPackages, listInstalledRPMs = self.base.findInstalledPackages(chrootID)
            listDependentPackages=self.base.findBuildTimeRequiredPackages()
            if constants.rpmCheck and self.base.package in constants.testForceRPMS:
                listDependentPackages.extend(self.base.findBuildTimeCheckRequiredPackages())
                testPackages=set(constants.listMakeCheckRPMPkgtoInstall)-set(listInstalledPackages)-set([self.base.package])
                listDependentPackages.extend(testPackages)
                listDependentPackages=list(set(listDependentPackages))

            pkgUtils = PackageUtils(self.base.logName,self.base.logPath)
            if len(listDependentPackages) != 0:
                self.base.logger.info("Installing the build time dependent packages......")
                for pkg in listDependentPackages:
                    self.base.installPackage(pkgUtils, pkg, chrootID, self.base.logPath, listInstalledPackages, listInstalledRPMs)
                pkgUtils.installRPMSInAOneShot(chrootID, self.base.logPath)
                self.base.logger.info("Finished installing the build time dependent packages......")

            pkgUtils.adjustGCCSpecs(self.base.package, chrootID, self.base.logPath)
            pkgUtils.buildRPMSForGivenPackage(self.base.package, chrootID,self.base.listBuildOptionPackages,
                                              self.base.pkgBuildOptionFile, self.base.logPath)
            self.base.logger.info("Successfully built the package:" + self.base.package)
        except Exception as e:
            self.base.logger.error("Failed while building package:" + self.base.package)
            self.base.logger.debug("Chroot with ID: " + chrootID + " not deleted for debugging.")
            logFileName = os.path.join(self.base.logPath, self.base.package + ".log")
            fileLog = os.popen('tail -n 100 ' + logFileName).read()
            self.base.logger.debug(fileLog)
            raise e
        if chrootID is not None:
            chrUtils.destroyChroot(chrootID)
