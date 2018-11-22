from PackageBuildDataGenerator import PackageBuildDataGenerator
from Logger import Logger
import threading
from constants import constants
import docker
import os
from ChrootUtils import ChrootUtils
from CommandUtils import CommandUtils
from PackageUtils import PackageUtils
from ToolChainUtils import ToolChainUtils
from Scheduler import Scheduler
from ThreadPool import ThreadPool
from SpecData import SPECS
from StringUtils import StringUtils

class PackageManager(object):

    def __init__(self,logName=None,logPath=None,pkgBuildType="chroot"):
        if logName is None:
            logName = "PackageManager"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.mapCyclesToPackageList={}
        self.mapPackageToCycle={}
        self.sortedPackageList=[]
        self.listOfPackagesAlreadyBuilt = []
        self.listThreads={}
        self.mapOutputThread={}
        self.mapThreadsLaunchTime={}
        self.listAvailableCyclicPackages=[]
        self.listBuildOptionPackages=[]
        self.pkgBuildOptionFile=""
        self.pkgBuildType=pkgBuildType
        if self.pkgBuildType == "container":
            self.dockerClient = docker.from_env(version="auto")

    def readPackageBuildData(self, listPackages):
        try:
            pkgBuildDataGen = PackageBuildDataGenerator(self.logName,self.logPath)
            self.mapCyclesToPackageList,self.mapPackageToCycle,self.sortedPackageList = pkgBuildDataGen.getPackageBuildData(listPackages)
        except:
            self.logger.error("unable to get sorted list")
            return False
        return True

    def readAlreadyAvailablePackages(self):
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

        self.logger.info(listAvailablePackages)
        return listAvailablePackages

    def calculateParams(self,listPackages):
        self.listThreads.clear()
        self.mapOutputThread.clear()
        self.mapThreadsLaunchTime.clear()
        self.listAvailableCyclicPackages=[]
        self.mapCyclesToPackageList.clear()
        self.mapPackageToCycle.clear()
        self.sortedPackageList=[]

        listOfPackagesAlreadyBuilt = []
        listOfPackagesAlreadyBuilt = list(self.readAlreadyAvailablePackages())
        self.listOfPackagesAlreadyBuilt = listOfPackagesAlreadyBuilt[:]

        updateBuiltRPMSList = False
        while not updateBuiltRPMSList:
            updateBuiltRPMSList = True
            listOfPackagesAlreadyBuilt = self.listOfPackagesAlreadyBuilt[:]
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

        listPackagesToBuild=listPackages[:]
        for pkg in listPackages:
            if pkg in self.listOfPackagesAlreadyBuilt and not constants.rpmCheck:
                listPackagesToBuild.remove(pkg)
        if not self.readPackageBuildData(listPackagesToBuild):
            return False
        return True

    def buildToolChain(self):
        pkgCount = 0
        try:
            tUtils=ToolChainUtils()
            pkgCount = tUtils.buildCoreToolChainPackages(self.listBuildOptionPackages, self.pkgBuildOptionFile)
        except Exception as e:
            self.logger.error("Unable to build tool chain")
            self.logger.error(e)
            raise e
        return pkgCount

    def buildToolChainPackages(self, listBuildOptionPackages, pkgBuildOptionFile, buildThreads):
        pkgCount = self.buildToolChain()
        if self.pkgBuildType == "container":
            # Stage 1 build container
            #TODO image name constants.buildContainerImageName
            if pkgCount > 0 or not self.dockerClient.images.list("photon_build_container:latest"):
                self.createBuildContainer()
        self.buildGivenPackages(constants.listToolChainPackages, buildThreads)
        if self.pkgBuildType == "container":
            # Stage 2 build container
            #TODO: rebuild container only if anything in listToolChainPackages was built
            self.createBuildContainer()

    def buildTestPackages(self, listBuildOptionPackages, pkgBuildOptionFile, buildThreads):
        self.buildToolChain()
        self.buildGivenPackages(constants.listMakeCheckRPMPkgtoInstall, buildThreads)

    def buildPackages(self,listPackages, listBuildOptionPackages, pkgBuildOptionFile, buildThreads, pkgBuildType):
        self.listBuildOptionPackages = listBuildOptionPackages
        self.pkgBuildOptionFile = pkgBuildOptionFile
        self.pkgBuildType = pkgBuildType
        if constants.rpmCheck:
            constants.rpmCheck=False
            self.buildToolChainPackages(listBuildOptionPackages, pkgBuildOptionFile, buildThreads)
            self.buildTestPackages(listBuildOptionPackages, pkgBuildOptionFile, buildThreads)
            constants.rpmCheck=True
            self.buildGivenPackages(listPackages, buildThreads)
        else:
            self.buildToolChainPackages(listBuildOptionPackages, pkgBuildOptionFile, buildThreads)
            self.buildGivenPackages(listPackages, buildThreads)

    def initializeThreadPool(self,statusEvent):
        ThreadPool.clear()
        ThreadPool.mapPackageToCycle=self.mapPackageToCycle
        ThreadPool.listAvailableCyclicPackages=self.listAvailableCyclicPackages
        ThreadPool.listBuildOptionPackages=self.listBuildOptionPackages
        ThreadPool.pkgBuildOptionFile=self.pkgBuildOptionFile
        ThreadPool.logger=self.logger
        ThreadPool.statusEvent=statusEvent
        ThreadPool.pkgBuildType=self.pkgBuildType

    def initializeScheduler(self,statusEvent):
        Scheduler.setLog(self.logName, self.logPath)
        Scheduler.setParams(self.sortedPackageList, self.listOfPackagesAlreadyBuilt)
        Scheduler.setEvent(statusEvent)
        Scheduler.stopScheduling=False

    def buildGivenPackages (self, listPackages, buildThreads):
        # Extend listPackages from ["name1", "name2",..] to ["name1-vers1", "name2-vers2",..]
        listPackageNamesAndVersions=[]
        for pkg in listPackages:
            for version in SPECS.getData().getVersions(pkg):
                listPackageNamesAndVersions.append(pkg+"-"+version)
        if constants.rpmCheck:
            alreadyBuiltRPMS=self.readAlreadyAvailablePackages()
            listMakeCheckPackages=set()
            for pkg in listPackages:
                version = SPECS.getData().getHighestVersion(pkg)
                listMakeCheckPackages.add(pkg+"-"+version)
            listPackageNamesAndVersions = (list(set(listPackageNamesAndVersions)|(listMakeCheckPackages-alreadyBuiltRPMS)))

        returnVal=self.calculateParams(listPackageNamesAndVersions)
        if not returnVal:
            self.logger.error("Unable to set paramaters. Terminating the package manager.")
            raise Exception("Unable to set paramaters")

        statusEvent=threading.Event()
        self.initializeScheduler(statusEvent)
        self.initializeThreadPool(statusEvent)

        i=0
        while i < buildThreads:
            workerName="WorkerThread"+str(i)
            ThreadPool.addWorkerThread(workerName)
            ThreadPool.startWorkerThread(workerName)
            i = i + 1

        statusEvent.wait()
        Scheduler.stopScheduling=True
        self.logger.info("Waiting for all remaining worker threads")
        listWorkerObjs=ThreadPool.getAllWorkerObjects()
        for w in listWorkerObjs:
            w.join()

        setFailFlag=False
        allPackagesBuilt=False
        if Scheduler.isAnyPackagesFailedToBuild():
            setFailFlag=True

        if Scheduler.isAllPackagesBuilt():
            allPackagesBuilt=True

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

    def createBuildContainer(self):
        self.logger.info("Generating photon build container..")
        try:
            #TODO image name constants.buildContainerImageName
            self.dockerClient.images.remove("photon_build_container:latest", force=True)
        except Exception as e:
            #TODO - better handling
            self.logger.debug("Photon build container image not found.")

        # Create toolchain chroot and install toolchain RPMs
        chrootID=None
        try:
            #TODO: constants.tcrootname
            chrUtils = ChrootUtils("toolchain-chroot", self.logPath)
            returnVal, chrootID = chrUtils.createChroot("toolchain-chroot")
            self.logger.debug("Created tool-chain chroot: " + chrootID)
            if not returnVal:
                raise Exception("Unable to prepare tool-chain chroot")
            tcUtils = ToolChainUtils("toolchain-chroot", self.logPath)
            tcUtils.installToolChainRPMS(chrootID, "dummy",self.listBuildOptionPackages,self.pkgBuildOptionFile)
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
