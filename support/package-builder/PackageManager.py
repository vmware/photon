import os
import threading
import copy
from PackageBuildDataGenerator import PackageBuildDataGenerator
from Logger import Logger
from constants import constants
import docker
from CommandUtils import CommandUtils
from PackageUtils import PackageUtils
from ToolChainUtils import ToolChainUtils
from Scheduler import Scheduler
from ThreadPool import ThreadPool
from SpecData import SPECS
from StringUtils import StringUtils
from Sandbox import Chroot, Container

class PackageManager(object):

    def __init__(self, logName=None, logPath=None, pkgBuildType="chroot"):
        if logName is None:
            logName = "PackageManager"
        if logPath is None:
            logPath = constants.logPath
        self.logName = logName
        self.logPath = logPath
        self.logLevel = constants.logLevel
        self.logger = Logger.getLogger(logName, logPath, constants.logLevel)
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
            if pkgCount > 0 or not self.dockerClient.images.list(constants.buildContainerImage):
                self._createBuildContainer()
        self.logger.info("Step 2 : Building stage 2 of the toolchain...")
        self.logger.info(constants.listToolChainPackages)
        self.logger.info("")
        self._buildGivenPackages(constants.listToolChainPackages, buildThreads)
        self.logger.info("The entire toolchain is now available")
        self.logger.info(45 * '-')
        self.logger.info("")
        if self.pkgBuildType == "container":
            # Stage 2 build container
            #TODO: rebuild container only if anything in listToolChainPackages was built
            self._createBuildContainer()

    def buildPackages(self, listPackages, buildThreads):
        if constants.rpmCheck:
            constants.rpmCheck = False
            self.buildToolChainPackages(buildThreads)
            self._buildTestPackages(buildThreads)
            constants.rpmCheck = True
            self._buildGivenPackages(listPackages, buildThreads)
        else:
            self.buildToolChainPackages(buildThreads)
            self.logger.info("Step 3 : Building the following package(s) and dependencies...")
            self.logger.info(listPackages)
            self.logger.info("")
            self._buildGivenPackages(listPackages, buildThreads)
        self.logger.info("Package build has been completed")
        self.logger.info("")

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

    # Returns list of package names which spec file has all subpackages built
    # Returns set of package name and version like
    # ["name1-vers1", "name2-vers2",..]
    def _readAlreadyAvailablePackages(self):
        listAvailablePackages = set()
        pkgUtils = PackageUtils(self.logName, self.logPath)
        listPackages = SPECS.getData().getListPackages()
        for package in listPackages:
            for version in SPECS.getData().getVersions(package):
                # Mark package available only if all subpackages are available
                packageIsAlreadyBuilt=True
                listRPMPackages = SPECS.getData().getRPMPackages(package, version)
                for rpmPkg in listRPMPackages:
                    if pkgUtils.findRPMFileForGivenPackage(rpmPkg, version) is None:
                        packageIsAlreadyBuilt=False
                        break;
                if packageIsAlreadyBuilt:
                    listAvailablePackages.add(package+"-"+version)

        self.logger.debug("List of Already built packages")
        self.logger.debug(listAvailablePackages)
        return listAvailablePackages

    def _calculateParams(self, listPackages):
        self.mapCyclesToPackageList.clear()
        self.mapPackageToCycle.clear()
        self.sortedPackageList = []

        self.listOfPackagesAlreadyBuilt = list(self._readAlreadyAvailablePackages())

        updateBuiltRPMSList = False
        while not updateBuiltRPMSList:
            updateBuiltRPMSList = True
            listOfPackagesAlreadyBuilt = self.listOfPackagesAlreadyBuilt
            for pkg in listOfPackagesAlreadyBuilt:
                packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                listDependentRpmPackages = SPECS.getData().getRequiresAllForPackage(packageName, packageVersion)
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
        Scheduler.setLog(self.logName, self.logPath, self.logLevel)
        Scheduler.setParams(self.sortedPackageList, set(self.listOfPackagesAlreadyBuilt))
        Scheduler.setEvent(statusEvent)
        Scheduler.stopScheduling = False

    def _buildGivenPackages(self, listPackages, buildThreads):
        # Extend listPackages from ["name1", "name2",..] to ["name1-vers1", "name2-vers2",..]
        listPackageNamesAndVersions=[]
        for pkg in listPackages:
            for version in SPECS.getData().getVersions(pkg):
                listPackageNamesAndVersions.append(pkg+"-"+version)
        alreadyBuiltRPMS = self._readAlreadyAvailablePackages()
        if alreadyBuiltRPMS:
            self.logger.debug("List of already available packages:")
            self.logger.debug(alreadyBuiltRPMS)

        if constants.rpmCheck:
            listMakeCheckPackages=set()
            for pkg in listPackages:
                version = SPECS.getData().getHighestVersion(pkg)
                listMakeCheckPackages.add(pkg+"-"+version)
            listPackageNamesAndVersions = (list(set(listPackageNamesAndVersions)|(listMakeCheckPackages-alreadyBuiltRPMS)))

        returnVal = self._calculateParams(listPackageNamesAndVersions)
        if not returnVal:
            self.logger.error("Unable to set paramaters. Terminating the package manager.")
            raise Exception("Unable to set paramaters")

        listBasePackageNamesAndVersions = list(map(lambda x:SPECS.getData().getBasePkg(x), listPackageNamesAndVersions))
        listPackagesToBuild = list((set(listBasePackageNamesAndVersions) - set(alreadyBuiltRPMS)))
        if listPackagesToBuild:
            self.logger.info("List of packages yet to be built...")
            self.logger.info(listPackagesToBuild)
            self.logger.info("")
        statusEvent = threading.Event()
        self._initializeScheduler(statusEvent)
        self._initializeThreadPool(statusEvent)

        for i in range(0, buildThreads):
            workerName = "WorkerThread" + str(i)
            ThreadPool.addWorkerThread(workerName)
            ThreadPool.startWorkerThread(workerName)

        statusEvent.wait()
        Scheduler.stopScheduling = True
        self.logger.debug("Waiting for all remaining worker threads")
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
                self.logger.debug("All packages built successfully")
            else:
                self.logger.error("Build stopped unexpectedly.Unknown error.")
                raise Exception("Unknown error")

    def _createBuildContainer(self):
        self.logger.debug("Generating photon build container..")
        try:
            #TODO image name constants.buildContainerImageName
            self.dockerClient.images.remove(constants.buildContainerImage, force=True)
        except Exception as e:
            #TODO - better handling
            self.logger.debug("Photon build container image not found.")

        # Create toolchain chroot and install toolchain RPMs
        chroot = None
        try:
            #TODO: constants.tcrootname
            chroot = Chroot(self.logger)
            chroot.create("toolchain-chroot")
            tcUtils = ToolChainUtils("toolchain-chroot", self.logPath)
            tcUtils.installToolChainRPMS(chroot)
        except Exception as e:
            if chroot:
                chroot.destroy()
            raise e
        self.logger.debug("createBuildContainer: " + chroot.getPath())

        # Create photon build container using toolchain chroot
        chroot.unmountAll()
        #TODO: Coalesce logging
        cmdUtils = CommandUtils()
        cmd = "cd " + chroot.getPath() + " && tar -czf ../tcroot.tar.gz ."
        cmdUtils.runCommandInShell(cmd, logfn=self.logger.debug)
        cmd = "mv " + chroot.getPath() + "/../tcroot.tar.gz ."
        cmdUtils.runCommandInShell(cmd, logfn=self.logger.debug)
        #TODO: Container name, docker file name from constants.
        self.dockerClient.images.build(tag=constants.buildContainerImage,
                                       path=".",
                                       rm=True,
                                       dockerfile="Dockerfile.photon_build_container")

        # Cleanup
        cmd = "rm -f ./tcroot.tar.gz"
        cmdUtils.runCommandInShell(cmd, logfn=self.logger.debug)
        chroot.destroy()
        self.logger.debug("Photon build container successfully created.")
