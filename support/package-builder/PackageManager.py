#!/usr/bin/env python3

import copy
import os
import sys
import threading

import docker
import RepoUtil
from CommandUtils import CommandUtils
from constants import BuildMode, BuildStage, constants
from Logger import Logger
from PackageBuildDataGenerator import PackageBuildDataGenerator
from PackageUtils import PackageUtils
from Scheduler import Scheduler
from SpecData import SPECS
from TDNFSandbox import TDNF
from ThreadPool import ThreadPool


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
        self.cmdUtils = CommandUtils()
        if self.pkgBuildType == "container":
            self.dockerClient = docker.from_env(version="auto")

    def buildToolChainPackages(self, buildThreads):
        if constants.toolchainBootstrap:
            self.logger.info("Bootstraping toolchain...")
            Scheduler.setBuildMode(BuildMode.BOOTSTRAP)
        self.logger.info("Building toolchain...")
        self.logger.info(constants.listToolChainPackages)
        self.logger.info("\nPreparing toolchain build base image:")
        Scheduler.setBuildStage(BuildStage.CORE_TOOLCHAIN)
        self._createBuildImage(
            targetName=constants.buildBase[BuildStage.CORE_TOOLCHAIN],
            targetFile=constants.buildBaseImageTarball[BuildStage.CORE_TOOLCHAIN],
        )
        self._buildGivenPackages(constants.listCoreToolChainPackages, buildThreads)
        Scheduler.setBuildStage(BuildStage.TOOLCHAIN)
        self._createBuildImage(
            targetName=constants.buildBase[BuildStage.TOOLCHAIN],
            targetFile=constants.buildBaseImageTarball[BuildStage.TOOLCHAIN],
        )
        self._buildGivenPackages(constants.listToolChainPackages, buildThreads)
        self.logger.info("The entire toolchain is now available")
        if constants.toolchainBootstrap:
            self.logger.info("Bootstraping toolchain complete...")
            sys.exit(0)
        Scheduler.setBuildStage(BuildStage.PACKAGES)
        self.logger.info(45 * "-")
        self.logger.info("")

    def buildPackages(self, listPackages, buildThreads):
        rebuild = constants.rebuild
        if constants.rpmCheck:
            constants.rpmCheck = False
            constants.addMacro("with_check", "0")
            self.buildToolChainPackages(buildThreads)
            self._buildTestPackages(buildThreads)
            constants.rpmCheck = True
            constants.addMacro("with_check", "1")
            self._createBuildImage(
                targetName=constants.buildBase[BuildStage.PACKAGES],
                targetFile=constants.buildBaseImageTarball[BuildStage.PACKAGES],
            )
            self._buildGivenPackages(listPackages, buildThreads, rebuild)
        else:
            self.buildToolChainPackages(buildThreads)
            self.logger.info(
                "Step 3: Building the following package(s) and dependencies..."
            )
            self.logger.info(listPackages)
            self.logger.info("")
            self._createBuildImage(
                targetName=constants.buildBase[BuildStage.PACKAGES],
                targetFile=constants.buildBaseImageTarball[BuildStage.PACKAGES],
            )
            self._buildGivenPackages(listPackages, buildThreads, rebuild)
        self.logger.info("Package build has been completed")
        self.logger.info("")

    def _readPackageBuildData(self, listPackages):
        try:
            pkgBuildDataGen = PackageBuildDataGenerator(self.logName, self.logPath)
            (
                self.mapCyclesToPackageList,
                self.mapPackageToCycle,
                self.sortedPackageList,
            ) = pkgBuildDataGen.getPackageBuildData(listPackages)

        except Exception as e:
            self.logger.exception(e)
            self.logger.error("unable to get sorted list")
            return False
        return True

    """
    Returns list of base package names which spec file has all
    subpackages built
    Returns set of package name and version like
    ["name1-vers1", "name2-vers2",..]
    """

    def _readAlreadyAvailablePackages(self):
        listAvailablePackages = set()
        pkgUtils = PackageUtils(self.logName, self.logPath)
        listPackages = SPECS.getData().getListPackages()
        for package in listPackages:
            for version in SPECS.getData().getVersions(package):
                # Mark package available only if all subpackages are available
                packageIsAlreadyBuilt = True
                listRPMPackages = SPECS.getData().getRPMPackages(package, version)
                for rpmPkg in listRPMPackages:
                    if pkgUtils.findRPMFile(rpmPkg, version) is None:
                        packageIsAlreadyBuilt = False
                        break
                if packageIsAlreadyBuilt:
                    listAvailablePackages.add(f"{package}-{version}")

        return listAvailablePackages

    def _calculateParams(self, listPackages, rebuild=False):
        self.mapCyclesToPackageList.clear()
        self.mapPackageToCycle.clear()
        self.sortedPackageList = []

        self.listOfPackagesAlreadyBuilt = self._readAlreadyAvailablePackages()

        if rebuild:
            self.listOfPackagesAlreadyBuilt = set(
                self.listOfPackagesAlreadyBuilt
            ) - set(listPackages)

        if self.listOfPackagesAlreadyBuilt:
            self.logger.debug("List of already available packages:")
            self.logger.debug(self.listOfPackagesAlreadyBuilt)

        listPackagesToBuild = copy.copy(listPackages)
        for pkg in listPackages:
            if pkg in self.listOfPackagesAlreadyBuilt and not constants.rpmCheck:
                listPackagesToBuild.remove(pkg)

        if constants.rpmCheck:
            self.sortedPackageList = listPackagesToBuild
        else:
            if not self._readPackageBuildData(listPackagesToBuild):
                return False

        if self.sortedPackageList:
            self.logger.info("List of packages yet to be built...")
            self.logger.info(
                str(set(self.sortedPackageList) - set(self.listOfPackagesAlreadyBuilt))
            )
            self.logger.info("")

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
        Scheduler.setParams(self.sortedPackageList, self.listOfPackagesAlreadyBuilt)
        Scheduler.setEvent(statusEvent)
        Scheduler.stopScheduling = False

    def _buildGivenPackages(self, listPackages, buildThreads, rebuild=False):
        # Extend listPackages from ["name1", "name2",..] to
        # ["name1-vers1", "name2-vers2",..]
        listPackageNamesAndVersions = set()

        for pkg in listPackages:
            versionGiven = None
            if "@" in pkg:
                pkg, versionGiven = pkg.split("@")

            base = SPECS.getData().getSpecName(pkg)
            for version in SPECS.getData().getVersions(base):
                if versionGiven and versionGiven not in version:
                    continue
                listPackageNamesAndVersions.add(f"{base}-{version}")

        returnVal = self._calculateParams(listPackageNamesAndVersions, rebuild=rebuild)
        if not returnVal:
            self.logger.error(
                "Unable to set parameters. Terminating the package manager."
            )
            raise Exception("Unable to set parameters")
        self._buildPackages(buildThreads)

    def _buildPackages(self, buildThreads):
        if constants.startSchedulerServer:
            import SchedulerServer

            self._initializeScheduler(None)
            SchedulerServer.mapPackageToCycle = self.mapPackageToCycle
            serverThread = threading.Thread(
                target=SchedulerServer.startServer, name="serverthread"
            )
            serverThread.start()
            serverThread.join()
        else:
            statusEvent = threading.Event()
            self._initializeScheduler(statusEvent)
            self._initializeThreadPool(statusEvent)
            for i in range(0, buildThreads):
                workerName = f"WorkerThread{i}"
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

    def _createImageTarball(
        self,
        targetName=None,
        targetFile=None,
        baseImage=None,
        releaseVer=None,
        packagesToInstall=None,
        packagesToRemove=None,
        packagesToExcludeForUpgrade=None,
        preSteps=None,
        postSteps=None,
        overwrite=False,
    ):
        if targetName is None or targetFile is None:
            raise Exception("Unable to create image.targetFile or targetName is empty")

        imageTarballPath = f"{constants.buildImagesPath}/{targetFile}"

        if overwrite:
            cmd = ["rm", "-f", imageTarballPath]
            self.cmdUtils.runCmd(cmd)

        if os.path.exists(imageTarballPath) and os.path.getsize(imageTarballPath) > 0:
            self.logger.debug(f"photon build image {imageTarballPath} exists")
            return
        self.logger.debug(f"Generating build image.. {targetFile}")

        targetPath = f"{constants.buildImagesPath}/{targetName}"
        os.makedirs(targetPath, exist_ok=True)

        if baseImage is not None:
            cmd = [
                "tar",
                "--same-owner",
                "-p-xf",
                os.path.join(constants.buildImagesPath, baseImage),
                "-C",
                targetPath,
            ]
            self.cmdUtils.runCmd(cmd)

        if preSteps is not None and type(preSteps) is list:
            for step in preSteps:
                self.logger.debug(
                    f"Executing pre step {step} for base image: {targetName}"
                )
                self.cmdUtils.runCmd(step)

        repoArgs = []

        if releaseVer is not None:
            repoArgs = [f"--releasever={releaseVer}"]
        elif constants.toolchainBootstrap:
            repoArgs = [f"--releasever={constants.releaseVersionToConsume}"]

        repoArgs = repoArgs + RepoUtil.getRepoArgs(
            Scheduler.buildStage, Scheduler.buildMode
        )

        exclusionArgs = None
        if type(packagesToExcludeForUpgrade) is list:
            exclusionArgs = ["--exclude"] + packagesToExcludeForUpgrade

        subCmds: list = [["makecache"]]
        if exclusionArgs is not None:
            subCmds.append(["upgrade"] + exclusionArgs)
        else:
            subCmds.append(["upgrade"])

        if packagesToRemove is not None and len(packagesToRemove) > 0:
            subCmds.append(["remove"] + packagesToRemove)

        if packagesToInstall is not None and len(packagesToInstall) > 0:
            subCmds.append(["install"] + packagesToInstall)

        tdnf = TDNF(installRoot=targetPath, repoArgs=repoArgs, logger=self.logger)
        for cmd in subCmds:
            self.logger.debug(f"Executing cmd for base image {targetName}: {cmd}")
            try:
                tdnf.run(
                    subCmd=cmd,
                    args=[],
                    errMsg=f"Unable to call {cmd} in {targetPath}",
                )
            except Exception as e:
                # make sure sandbox is cleared
                tdnf.clean()
                raise e

        tdnf.clean()

        # steps = [
        #     f"groupadd --root {targetPath} photon".split(),
        #     f"useradd --root {targetPath} -G photon -m {constants.photonBuilder}".split(),
        # ]

        # for step in steps:
        #     self.cmdUtils.runCmd(step)

        if postSteps is not None and type(postSteps) is list:
            for step in postSteps:
                self.logger.debug(
                    f"Executing post step {step} for base image: {targetName}"
                )
                self.cmdUtils.runCmd(step)

        self.logger.debug("Compressing photon build image..")
        self.cmdUtils.runCmd(
            args=["tar", "--same-owner", "-p", "-cf", imageTarballPath, "."],
            cwd=targetPath,
        )
        self.cmdUtils.runCmd(["rm", "-rf", targetPath])

    def _createBuildImage(self, targetName, targetFile):
        releaseVer = constants.releaseVersion
        if constants.toolchainBootstrap:
            releaseVer = None
        self._createImageTarball(
            targetName=targetName,
            targetFile=targetFile,
            baseImage=None,
            releaseVer=releaseVer,
            packagesToInstall=[
                "coreutils-selinux",
                "shadow",
                "rpm-build",
                "build-essential",
                "photon-release",
            ],
            packagesToRemove=None,
            preSteps=None,
            postSteps=None,
            overwrite=False,
        )
