import os
import threading
import copy
from PackageBuildDataGenerator import PackageBuildDataGenerator
from Logger import Logger
from constants import constants
import docker
from ChrootUtils import ChrootUtils
from CommandUtils import CommandUtils
from PackageUtils import PackageUtils
from ToolChainUtils import ToolChainUtils
from Scheduler import Scheduler
from ThreadPool import ThreadPool
from SpecData import SPECS
from SpecStructures import *

class PackageManager(object):

    def __init__(self, logName=None, logPath=None, pkgBuildType="chroot"):
        if logName is None:
            logName = "PackageManager"
        if logPath is None:
            logPath = constants.logPath
        self.logName = logName
        self.logPath = logPath
        self.logger = Logger.getLogger(logName, logPath)
        self.mapCyclesToPackageList = {}
        self.mapPackageToCycle = {}
        self.sortedPackageList = []
        self.listOfPackagesAlreadyBuilt = set()
        self.pkgBuildType = pkgBuildType
        if self.pkgBuildType == "container":
            self.dockerClient = docker.from_env(version="auto")

    def buildToolChain(self):
        pkgCount = 0
        try:
            tUtils = ToolChainUtils()
            pkgCount = tUtils.buildCoreToolChainPackages()
        except Exception as e:
            self.logger.error("Unable to build tool chain")
            self.logger.error(e)
            raise e
        return pkgCount

    def buildToolChainPackages(self, buildThreads):
        pkgCount = self.buildToolChain()
        if self.pkgBuildType == "container":
            # Stage 1 build container
            #TODO image name constants.buildContainerImageName
            if pkgCount > 0 or not self.dockerClient.images.list("photon_build_container:latest"):
                self._createBuildContainer()
        self._buildGivenPackages(constants.listToolChainPackages, buildThreads)
        if self.pkgBuildType == "container":
            # Stage 2 build container
            #TODO: rebuild container only if anything in listToolChainPackages was built
            self._createBuildContainer()

    def buildPackages(self, listPackages, buildThreads, pkgBuildType):
        self.pkgBuildType = pkgBuildType
        if constants.rpmCheck:
            constants.rpmCheck = False
            self.buildToolChainPackages(buildThreads)
            self._buildTestPackages(buildThreads)
            constants.rpmCheck = True
            self._buildGivenPackages(listPackages, buildThreads)
        else:
            self.buildToolChainPackages(buildThreads)
            self._buildGivenPackages(listPackages, buildThreads)

    def _readPackageBuildData(self, listPackages):
        try:
            pkgBuildDataGen = PackageBuildDataGenerator(self.logName, self.logPath)
            self.mapCyclesToPackageList, self.mapPackageToCycle, self.sortedPackageList = (
                pkgBuildDataGen.getPackageBuildData(listPackages))

        except Exception as e:
            self.logger.exception(e)
            self.logger.error("unable to get sorted list")
            return False
        return True

    def _readAlreadyAvailablePackages(self):
        listAvailablePackages = set()
        listFoundRPMPackages = set()
        listRPMFiles = set()
        listDirectorys = set()
        mapPackageVersionRelease={}
        pkgVerRel = dependentPackageData()
        listDirectorys.add(constants.rpmPath)
        if constants.inputRPMSPath is not None:
            listDirectorys.add(constants.inputRPMSPath)

        while listDirectorys:
            dirPath = listDirectorys.pop()
            for dirEntry in os.listdir(dirPath):
                dirEntryPath = os.path.join(dirPath, dirEntry)
                if os.path.isfile(dirEntryPath) and dirEntryPath.endswith(".rpm"):
                    listRPMFiles.add(dirEntryPath)
                elif os.path.isdir(dirEntryPath):
                    listDirectorys.add(dirEntryPath)
        pkgUtils = PackageUtils(self.logName, self.logPath)
        for rpmfile in listRPMFiles:
            package, version, release = pkgUtils.findPackageInfoFromRPMFile(rpmfile)
            pkgVerRel.package = package
            pkgVerRel.version = version
            pkgVerRel.release = release
            if package in mapPackageVersionRelease:
                mapPackageVersionRelease[package].append(pkgVerRel)
            else:
                mapPackageVersionRelease[package]=[pkgVerRel]
        for package in mapPackageVersionRelease:
            if SPECS.getData().isRPMPackage(package):
                numVersions=SPECS.getData().getNumberOfVersions(package)
                for index in range(0, numVersions):
                        flag=False;
                        specVersion=SPECS.getData().getVersion(package,index)
                        specRelease=SPECS.getData().getRelease(package,index)
                        for i in range(0,len(mapPackageVersionRelease[package])):
                                if specVersion == mapPackageVersionRelease[package][i].version and specRelease == mapPackageVersionRelease[package][i].release:
                                        flag=True
                        if flag == False:
                                break
                if flag:
                        listFoundRPMPackages.add(package)
        #Mark package available only if all sub packages are available
        for package in listFoundRPMPackages:
            basePkg = SPECS.getData().getSpecName(package)
            if basePkg in listAvailablePackages:
                continue
            listRPMPackages = SPECS.getData().getRPMPackages(basePkg)
            packageIsAlreadyBuilt = True
            for rpmpkg in listRPMPackages:
                if rpmpkg not in listFoundRPMPackages:
                    packageIsAlreadyBuilt = False
            if packageIsAlreadyBuilt:
                listAvailablePackages.add(package)
        self.logger.info("List of Already built packages")
        self.logger.info(listAvailablePackages)
        return listAvailablePackages

    def _calculateParams(self, listPackages):
        self.mapCyclesToPackageList.clear()
        self.mapPackageToCycle.clear()
        self.sortedPackageList = []

        self.listOfPackagesAlreadyBuilt = self._readAlreadyAvailablePackages()

        updateBuiltRPMSList = False
        while not updateBuiltRPMSList:
            updateBuiltRPMSList = True
            listOfPackagesAlreadyBuilt = list(self.listOfPackagesAlreadyBuilt)
            for pkg in listOfPackagesAlreadyBuilt:
                listDependentRpmPackages = SPECS.getData().getRequiresAllForPackage(pkg)
                needToRebuild = False
                for dependentPkg in listDependentRpmPackages:
                    if dependentPkg not in self.listOfPackagesAlreadyBuilt:
                        needToRebuild = True
                        updateBuiltRPMSList = False
                if needToRebuild:
                    self.listOfPackagesAlreadyBuilt.remove(pkg)

        listPackagesToBuild = copy.copy(listPackages)
        for pkg in listPackages:
            if (pkg in self.listOfPackagesAlreadyBuilt and
                    not constants.rpmCheck):
                listPackagesToBuild.remove(pkg)

        if not self._readPackageBuildData(listPackagesToBuild):
            return False
        return True

    def _buildTestPackages(self, buildThreads):
        self.buildToolChain()
        self._buildGivenPackages(constants.listMakeCheckRPMPkgtoInstall, buildThreads)

    def _initializeThreadPool(self, statusEvent):
        ThreadPool.clear()
        ThreadPool.mapPackageToCycle = self.mapPackageToCycle
        ThreadPool.logger = self.logger
        ThreadPool.statusEvent = statusEvent
        ThreadPool.pkgBuildType = self.pkgBuildType

    def _initializeScheduler(self, statusEvent):
        Scheduler.setLog(self.logName, self.logPath)
        Scheduler.setParams(self.sortedPackageList, self.listOfPackagesAlreadyBuilt)
        Scheduler.setEvent(statusEvent)
        Scheduler.stopScheduling = False

    def _buildGivenPackages(self, listPackages, buildThreads):
        if constants.rpmCheck:
            alreadyBuiltRPMS = self._readAlreadyAvailablePackages()
            listPackages = (list(set(listPackages)|(set(constants.listMakeCheckRPMPkgtoInstall)-
                                                    alreadyBuiltRPMS)))

        returnVal = self._calculateParams(listPackages)
        if not returnVal:
            self.logger.error("Unable to set paramaters. Terminating the package manager.")
            raise Exception("Unable to set paramaters")

        statusEvent = threading.Event()
        self._initializeScheduler(statusEvent)
        self._initializeThreadPool(statusEvent)

        for i in range(0, buildThreads):
            workerName = "WorkerThread" + str(i)
            ThreadPool.addWorkerThread(workerName)
            ThreadPool.startWorkerThread(workerName)

        statusEvent.wait()
        Scheduler.stopScheduling = True
        self.logger.info("Waiting for all remaining worker threads")
        ThreadPool.join_all()

        setFailFlag = False
        allPackagesBuilt = False
        if Scheduler.isAnyPackagesFailedToBuild():
            setFailFlag = True

        if Scheduler.isAllPackagesBuilt():
            allPackagesBuilt = True

        if setFailFlag:
            self.logger.error("Some of the packages failed:")
            self.logger.error(Scheduler.listOfFailedPackages)
            raise Exception("Failed during building package")

        if not setFailFlag:
            if allPackagesBuilt:
                self.logger.info("All packages built successfully")
            else:
                self.logger.error("Build stopped unexpectedly.Unknown error.")
                raise Exception("Unknown error")

        self.logger.info("Terminated")

    def _createBuildContainer(self):
        self.logger.info("Generating photon build container..")
        try:
            #TODO image name constants.buildContainerImageName
            self.dockerClient.images.remove("photon_build_container:latest", force=True)
        except Exception as e:
            #TODO - better handling
            self.logger.debug("Photon build container image not found.")

        # Create toolchain chroot and install toolchain RPMs
        chrootID = None
        try:
            #TODO: constants.tcrootname
            chrUtils = ChrootUtils("toolchain-chroot", self.logPath)
            returnVal, chrootID = chrUtils.createChroot("toolchain-chroot")
            self.logger.debug("Created tool-chain chroot: " + chrootID)
            if not returnVal:
                raise Exception("Unable to prepare tool-chain chroot")
            tcUtils = ToolChainUtils("toolchain-chroot", self.logPath)
            tcUtils.installToolChainRPMS(chrootID, "dummy")
        except Exception as e:
            if chrootID is not None:
                self.logger.debug("Deleting chroot: " + chrootID)
                chrUtils.destroyChroot(chrootID)
            raise e
        self.logger.info("VDBG-PU-createBuildContainer: chrootID: " + chrootID)

        # Create photon build container using toolchain chroot
        #TODO: Coalesce logging
        cmdUtils = CommandUtils()
        cmd = "./umount-build-root.sh " + chrootID
        cmdUtils.runCommandInShell(cmd, self.logPath + "/toolchain-chroot1.log")
        cmd = "cd " + chrootID + " && tar -czvf ../tcroot.tar.gz ."
        cmdUtils.runCommandInShell(cmd, self.logPath + "/toolchain-chroot2.log")
        cmd = "mv " + chrootID + "/../tcroot.tar.gz ."
        cmdUtils.runCommandInShell(cmd, self.logPath + "/toolchain-chroot3.log")
        #TODO: Container name, docker file name from constants.
        self.dockerClient.images.build(tag="photon_build_container:latest",
                                       path=".",
                                       rm=True,
                                       dockerfile="Dockerfile.photon_build_container")

        # Cleanup
        cmd = "rm -f ./tcroot.tar.gz"
        cmdUtils.runCommandInShell(cmd, self.logPath + "/toolchain-chroot4.log")
        chrUtils.destroyChroot(chrootID)
        self.logger.info("Photon build container successfully created.")
