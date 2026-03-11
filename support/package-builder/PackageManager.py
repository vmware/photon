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
        if not logName:
            logName = "PackageManager"
        if not logPath:
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
        self.installRootPath = f"{constants.buildImagesPath}/sandboxBase"
        self.buildStageMarkerFile = f"{self.installRootPath}/stage-marker.txt"

        if self.pkgBuildType == "container":
            self.dockerClient = docker.from_env(version="auto")

    def shouldOverwrite(self, stage, marker_file=None):
        if not marker_file:
            marker_file = self.buildStageMarkerFile
        if not os.path.isfile(marker_file):
            return True

        with open(marker_file, "r") as f:
            content = f.read().strip()

        return content != stage.value

    def getPkgListToBuild(self, pkgList):
        notBuilt = []
        pkgUtils = PackageUtils(Scheduler.buildStage, Scheduler.buildMode)
        for package in pkgList:
            flag = False
            for version in SPECS.getData().getVersions(package):
                if flag:
                    break
                # Mark package available only if all subpackages are available
                listRPMPackages = SPECS.getData().getRPMPackages(package, version)
                for rpmPkg in listRPMPackages:
                    if not pkgUtils.findRPMFile(rpmPkg, version):
                        notBuilt.append(package)
                        flag = True
                        break

        return notBuilt

    def buildToolChainPackages(self, buildThreads):
        if constants.toolchainBootstrap:
            self.logger.info("Bootstraping toolchain...")
            Scheduler.setBuildMode(BuildMode.BOOTSTRAP)

        self.logger.info("Step 1: Building core toolchain...")
        self.logger.info(constants.listCoreToolChainPackages)

        self.logger.info("\nPreparing toolchain build base image:")
        Scheduler.setBuildStage(BuildStage.CORE_TOOLCHAIN)

        toBuild = self.getPkgListToBuild(constants.listCoreToolChainPackages)

        if toBuild:
            overwrite = self.shouldOverwrite(BuildStage.CORE_TOOLCHAIN)
            self._createBuildImage(overwrite=overwrite)
            self._buildGivenPackages(toBuild, buildThreads)

        self.logger.info("Step 2: Building toolchain ...")
        self.logger.info(constants.listToolChainPackages)
        Scheduler.setBuildStage(BuildStage.TOOLCHAIN)
        toBuild = self.getPkgListToBuild(constants.listToolChainPackages)
        if toBuild:
            overwrite = self.shouldOverwrite(BuildStage.CORE_TOOLCHAIN)
            self._createBuildImage(overwrite=overwrite)
            self._buildGivenPackages(toBuild, buildThreads)

        self.logger.info("The entire toolchain is now available")
        if constants.toolchainBootstrap:
            self.logger.info("Bootstraping toolchain complete...")
            sys.exit(0)
        self.logger.info(45 * "-")
        self.logger.info("")

        Scheduler.setBuildStage(BuildStage.PACKAGES)

    def buildPackages(self, listPackages, buildThreads):
        rebuild = constants.rebuild

        def checkPackagesSandbox():
            overwrite = self.shouldOverwrite(BuildStage.PACKAGES)
            self._createBuildImage(overwrite=overwrite)

        if constants.rpmCheck:
            constants.rpmCheck = False
            constants.addMacro("with_check", "0")
            checkPackagesSandbox()
            self._buildTestPackages(buildThreads)
            constants.rpmCheck = True
            constants.addMacro("with_check", "1")
        else:
            self.buildToolChainPackages(buildThreads)
            checkPackagesSandbox()
            self.logger.info(
                "Step 3: Building the following package(s) and dependencies..."
            )
            self.logger.info(listPackages)
            self.logger.info("")

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
        pkgUtils = PackageUtils(Scheduler.buildStage, Scheduler.buildMode)
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
        self.buildToolChainPackages()
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

        # for make pkgs=a,b,c
        if Scheduler.buildStage.value == "none":
            Scheduler.setBuildStage(BuildStage.PACKAGES)

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

    def _createSandboxBase(
        self,
        baseImage=None,
        releaseVer=None,
        packagesToInstall=None,
        packagesToRemove=None,
        packagesToExcludeForUpgrade=None,
        preSteps=None,
        postSteps=None,
        overwrite=False,
    ):
        targetPath = self.installRootPath

        if os.path.isfile(self.buildStageMarkerFile):
            with open(self.buildStageMarkerFile, "r") as f:
                content = f.read().strip()
            self.logger.info(f"Current build stage: {content}")

        if os.path.exists(targetPath):
            if not overwrite:
                self.logger.info(f"Photon core sandbox {targetPath} exists")
                return
            self.cmdUtils.runCmd(["rm", "-rf", "--one-file-system", targetPath])

        self.logger.info(f"Changing build stage to: {Scheduler.buildStage.value}")
        self.logger.info(f"Generating base sandbox -> {targetPath}")

        os.makedirs(targetPath, exist_ok=True)

        if baseImage:
            cmd = [
                "tar",
                "--same-owner",
                "-p-xf",
                f"{constants.buildImagesPath}/{baseImage}"
                "-C",
                targetPath,
            ]
            self.cmdUtils.runCmd(cmd)

        if preSteps and isinstance(preSteps, list):
            for step in preSteps:
                self.logger.debug(
                    f"Executing pre step {step} for base image: {targetPath}"
                )
                self.cmdUtils.runCmd(step)

        tdnfArgs = []

        if releaseVer:
            tdnfArgs = [f"--releasever={releaseVer}"]
        elif constants.toolchainBootstrap:
            tdnfArgs = [f"--releasever={constants.releaseVersionToConsume}"]

        tdnfArgs += RepoUtil.getRepoArgs(Scheduler.buildStage, Scheduler.buildMode)

        exclusionArgs = None
        if isinstance(packagesToExcludeForUpgrade, list):
            exclusionArgs = ["--exclude"] + packagesToExcludeForUpgrade

        subCmds = [["makecache", "--refresh"], ["upgrade", "-y"]]
        if exclusionArgs:
            subCmds.append(exclusionArgs)

        if packagesToRemove and len(packagesToRemove):
            subCmds.append(["remove", "-y"] + packagesToRemove)

        if packagesToInstall and len(packagesToInstall):
            subCmds.append(["install", "-y", "--setopt=tsflags=nodocs"] + packagesToInstall)

        tdnf = TDNF(installRoot=targetPath, logger=self.logger)
        for cmd in subCmds:
            self.logger.debug(f"Executing cmd for base image {targetPath}: {cmd}")
            try:
                # No need to hold lock here
                # When sandbox is getting created, nothing is getting built
                RepoUtil.updateRepoData()
                tdnf.run(
                    args=tdnfArgs + cmd,
                    errMsg=f"Unable to call {cmd} in {targetPath}",
                )
                assert Scheduler.buildStage.value != "none"
                open(self.buildStageMarkerFile, "w").write(Scheduler.buildStage.value)
            except Exception as e:
                # make sure sandbox is cleared
                tdnf.clean()
                self.cmdUtils.runCmd(["rm", "-rf", targetPath])
                raise e

        tdnf.clean()

        # steps = [
        #     f"groupadd --root {targetPath} photon".split(),
        #     f"useradd --root {targetPath} -G photon -m {constants.photonBuilder}".split(),
        # ]

        # for step in steps:
        #     self.cmdUtils.runCmd(step)

        if postSteps and isinstance(postSteps, list):
            for step in postSteps:
                self.logger.debug(
                    f"Executing post step {step} for base image: {targetPath}"
                )
                self.cmdUtils.runCmd(step)

    def _createBuildImage(self, overwrite=False):
        releaseVer = constants.releaseVersion
        if constants.toolchainBootstrap:
            releaseVer = None
        self._createSandboxBase(
            releaseVer=releaseVer,
            overwrite=overwrite,
            packagesToInstall=[
                "coreutils-selinux",
                "shadow",
                "rpm-build",
                "build-essential",
                "photon-release",
            ],
        )
