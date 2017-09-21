from PackageUtils import PackageUtils
from Logger import Logger
from ToolChainUtils import ToolChainUtils
from CommandUtils import CommandUtils
from ChrootUtils import ChrootUtils
import os.path
import sys
from constants import constants
import shutil
import docker

class BuildContainer(object):

    def __init__(self, mapPackageToCycles, listAvailableCyclicPackages, listBuildOptionPackages, pkgBuildOptionFile, logName=None, logPath=None):
        if logName is None:
            logName = "BuildContainer"
        if logPath is None:
            logPath = constants.logPath
        self.logName = logName
        self.logPath = logPath
        self.logger = Logger.getLogger(logName, logPath, True)
        self.buildContainerImage = "photon_build_container:latest"
        self.dockerClient = docker.from_env(version="auto")
        self.mapPackageToCycles = mapPackageToCycles
        self.listAvailableCyclicPackages = listAvailableCyclicPackages
        self.listNodepsPackages = ["glibc","gmp","zlib","file","binutils","mpfr","mpc","gcc","ncurses","util-linux","groff","perl","texinfo","rpm","openssl","openssl-devel","go"]
        self.listBuildOptionPackages = listBuildOptionPackages
        self.pkgBuildOptionFile = pkgBuildOptionFile

    def prepareBuildContainer(self, containerTaskName, packageName, isToolChainPackage=False):
        # Prepare an empty chroot environment to let docker use the BUILD folder
        chrootName="build-"+packageName
        chrUtils = ChrootUtils(self.logName,self.logPath)
        returnVal,chrootID = chrUtils.createChroot(chrootName)
        self.logger.debug("Created new chroot for docker: " + chrootID)
        if not returnVal:
            raise Exception("Unable to prepare build root")
        tUtils=ToolChainUtils(self.logName,self.logPath)
        tUtils.prepareDummyBuildRoot(chrootID)

        containerID = None
        mountVols = {
                        constants.prevPublishRPMRepo: {'bind': '/publishrpms', 'mode': 'ro'},
                        constants.prevPublishXRPMRepo: {'bind': '/publishxrpms', 'mode': 'ro'},
                        constants.tmpDirPath: {'bind': '/tmp', 'mode': 'rw'},
                        constants.rpmPath: {'bind': constants.topDirPath + "/RPMS", 'mode': 'rw'},
                        constants.sourceRpmPath: {'bind': constants.topDirPath + "/SRPMS", 'mode': 'rw'},
                        constants.logPath + "/" + self.logName: {'bind': constants.topDirPath + "/LOGS", 'mode': 'rw'},
                        chrootID + constants.topDirPath + "/BUILD": {'bind': constants.topDirPath + "/BUILD", 'mode': 'rw'}
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
            self.logger.info("BuildContainer-prepareBuildContainer: Starting build container: " + containerName)
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

            self.logger.debug("Started Photon build container for task " + containerTaskName
                               + " ID: " + containerID.short_id)
            if not containerID:
                raise Exception("Unable to start Photon build container for task " + containerTaskName)
        except Exception as e:
            self.logger.debug("Unable to start Photon build container for task " + containerTaskName)
            raise e
        return containerID, chrootID

    def findPackageNameFromRPMFile(self, rpmfile):
        rpmfile = os.path.basename(rpmfile)
        releaseindex = rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:" + rpmfile)
            return None
        versionindex=rpmfile[0:releaseindex].rfind("-")
        if versionindex == -1:
            self.logger.error("Invalid rpm file:" + rpmfile)
            return None
        packageName = rpmfile[0:versionindex]
        return packageName

    def findInstalledPackages(self, containerID):
        pkgUtils = PackageUtils(self.logName, self.logPath)
        listInstalledRPMs = pkgUtils.findInstalledRPMPackagesInContainer(containerID)
        listInstalledPackages = []
        for installedRPM in listInstalledRPMs:
            packageName = self.findPackageNameFromRPMFile(installedRPM)
            if packageName is not None:
                listInstalledPackages.append(packageName)
        return listInstalledPackages, listInstalledRPMs

    def buildPackageThreadAPI(self, package, outputMap, threadName,):
        try:
            self.buildPackage(package)
            outputMap[threadName] = True
        except Exception as e:
            self.logger.error(e)
            outputMap[threadName] = False

    def checkIfPackageIsAlreadyBuilt(self, package):
        basePkg = constants.specData.getSpecName(package)
        listRPMPackages = constants.specData.getRPMPackages(basePkg)
        packageIsAlreadyBuilt = True
        pkgUtils = PackageUtils(self.logName,self.logPath)
        for pkg in listRPMPackages:
            if pkgUtils.findRPMFileForGivenPackage(pkg) is None:
                packageIsAlreadyBuilt = False
                break
        return packageIsAlreadyBuilt

    def buildPackage(self, package):
        #do not build if RPM is already built
        #test only if the package is in the testForceRPMS with rpmCheck
        #build only if the package is not in the testForceRPMS with rpmCheck
        if self.checkIfPackageIsAlreadyBuilt(package):
            if not constants.rpmCheck:
                self.logger.info("Skipping building the package:"+package)
                return
            elif constants.rpmCheck and package not in constants.testForceRPMS:
                self.logger.info("Skipping testing the package:"+package)
                return

        #should initialize a logger based on package name
        containerTaskName = "build-" + package
        containerID = None
        chrootID = None
        isToolChainPackage = False
        if package in constants.listToolChainPackages:
            isToolChainPackage = True
        destLogPath = constants.logPath + "/build-"+package
        try:
            containerID, chrootID = self.prepareBuildContainer(containerTaskName, package, isToolChainPackage)
            if not os.path.isdir(destLogPath):
                cmdUtils = CommandUtils()
                cmdUtils.runCommandInShell("mkdir -p "+destLogPath)

            tcUtils = ToolChainUtils(self.logName, self.logPath)
            if package in constants.perPackageToolChain:
                self.logger.debug(constants.perPackageToolChain[package])
                tcUtils.installCustomToolChainRPMSinContainer(containerID, constants.perPackageToolChain[package], package);

            listInstalledPackages, listInstalledRPMs = self.findInstalledPackages(containerID)
            self.logger.info(listInstalledPackages)
            listDependentPackages = self.findBuildTimeRequiredPackages(package)
            if constants.rpmCheck and package in constants.testForceRPMS:
                listDependentPackages.extend(self.findBuildTimeCheckRequiredPackages(package))
                testPackages=set(constants.listMakeCheckRPMPkgtoInstall)-set(listInstalledPackages)-set([package])
                listDependentPackages.extend(testPackages)
                listDependentPackages=list(set(listDependentPackages))

            pkgUtils = PackageUtils(self.logName,self.logPath)
            if len(listDependentPackages) != 0:
                self.logger.info("BuildContainer-buildPackage: Installing dependent packages..")
                self.logger.info(listDependentPackages)
                for pkg in listDependentPackages:
                    self.installPackage(pkgUtils, pkg, containerID, destLogPath, listInstalledPackages, listInstalledRPMs)
                # Special case sqlite due to package renamed from sqlite-autoconf to sqlite
                if "sqlite" in listInstalledPackages or "sqlite-devel" in listInstalledPackages or "sqlite-libs" in listInstalledPackages:
                    if "sqlite" not in listInstalledPackages:
                        self.installPackage(pkgUtils, "sqlite", containerID, destLogPath, listInstalledPackages, listInstalledRPMs)
                    if "sqlite-devel" not in listInstalledPackages:
                        self.installPackage(pkgUtils, "sqlite-devel", containerID, destLogPath, listInstalledPackages, listInstalledRPMs)
                    if "sqlite-libs" not in listInstalledPackages:
                        self.installPackage(pkgUtils, "sqlite-libs", containerID, destLogPath, listInstalledPackages, listInstalledRPMs)
                pkgUtils.installRPMSInAOneShotInContainer(containerID, destLogPath)

            pkgUtils.adjustGCCSpecsInContainer(package, containerID, destLogPath)

            pkgUtils.buildRPMSForGivenPackageInContainer(
                                               package,
                                               containerID,
                                               self.listBuildOptionPackages,
                                               self.pkgBuildOptionFile,
                                               destLogPath)
            self.logger.info("BuildContainer-buildPackage: Successfully built the package: " + package)
        except Exception as e:
            self.logger.error("Failed while building package:" + package)
            if containerID is not None:
                self.logger.debug("Container " + containerID.short_id + " retained for debugging.")
            logFileName = os.path.join(destLogPath, package + ".log")
            fileLog = os.popen('tail -n 20 ' + logFileName).read()
            self.logger.debug(fileLog)
            raise e

        # Remove the container
        if containerID is not None:
            containerID.remove(force=True)
        # Remove the dummy chroot
        if chrootID is not None:
            chrUtils = ChrootUtils(self.logName,self.logPath)
            chrUtils.destroyChroot(chrootID)

    def findRunTimeRequiredRPMPackages(self, rpmPackage):
        listRequiredPackages = constants.specData.getRequiresForPackage(rpmPackage)
        return listRequiredPackages

    def findBuildTimeRequiredPackages(self, package):
        listRequiredPackages = constants.specData.getBuildRequiresForPackage(package)
        return listRequiredPackages

    def findBuildTimeCheckRequiredPackages(self,package):
        listRequiredPackages=constants.specData.getCheckBuildRequiresForPackage(package)
        return listRequiredPackages

    def installPackage(self, pkgUtils, package, containerID, destLogPath, listInstalledPackages, listInstalledRPMs):
        latestRPM = os.path.basename(pkgUtils.findRPMFileForGivenPackage(package)).replace(".rpm", "")
        if package in listInstalledPackages and latestRPM in listInstalledRPMs:
            return
        self.installDependentRunTimePackages(pkgUtils, package, containerID, destLogPath, listInstalledPackages, listInstalledRPMs)
        noDeps = False
        if self.mapPackageToCycles.has_key(package):
            noDeps = True
        if package in self.listNodepsPackages:
            noDeps = True
        if package in constants.noDepsPackageList:
            noDeps = True
        pkgUtils.prepRPMforInstallInContainer(package, containerID, noDeps, destLogPath)
        listInstalledPackages.append(package)
        listInstalledRPMs.append(latestRPM)

    def installDependentRunTimePackages(self, pkgUtils, package, containerID, destLogPath, listInstalledPackages, listInstalledRPMs):
        listRunTimeDependentPackages = self.findRunTimeRequiredRPMPackages(package)
        if len(listRunTimeDependentPackages) != 0:
            for pkg in listRunTimeDependentPackages:
                if self.mapPackageToCycles.has_key(pkg) and pkg not in self.listAvailableCyclicPackages:
                    continue
                latestPkgRPM = os.path.basename(pkgUtils.findRPMFileForGivenPackage(pkg)).replace(".rpm", "")
                if pkg in listInstalledPackages and latestPkgRPM in listInstalledRPMs:
                    continue
                self.installPackage(pkgUtils, pkg, containerID, destLogPath, listInstalledPackages, listInstalledRPMs)
