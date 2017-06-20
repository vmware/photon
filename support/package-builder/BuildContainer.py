from PackageUtils import PackageUtils
from Logger import Logger
from ToolChainUtils import ToolChainUtils
from CommandUtils import CommandUtils
import os.path
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
        containerID = None
        mountVols = {
                        constants.prevPublishRPMRepo: {'bind': '/publishrpms', 'mode': 'ro'},
                        constants.prevPublishXRPMRepo: {'bind': '/publishxrpms', 'mode': 'ro'},
                        constants.rpmPath: {'bind': '/toolchainrpms', 'mode': 'ro'},
                    }
        # TODO: Check photon_build_container image exists
        try:
            containerName = containerTaskName
            containerName = containerName.replace("+", "p")
            self.logger.info("VDBG-BC-prepareBuildContainer: Starting build container: " + containerName)
            containerID = self.dockerClient.containers.run(self.buildContainerImage,
                                                           detach=True,
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
        return containerID

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
            #self.logger.info("VDBG-BC-findInstalledPackages: rpm=" + installedRPM + " pkg=" + packageName)
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
        if self.checkIfPackageIsAlreadyBuilt(package):
            self.logger.info("Skipping building the package:"+package)
            return

        #should initialize a logger based on package name
        containerTaskName = "build-" + package
        containerID = None
        isToolChainPackage = False
        if package in constants.listToolChainPackages:
            isToolChainPackage = True
        destLogPath = constants.logPath + "/build-"+package
        try:
            containerID = self.prepareBuildContainer(containerTaskName, package, isToolChainPackage)
            if not os.path.isdir(destLogPath):
                cmdUtils = CommandUtils()
                cmdUtils.runCommandInShell("mkdir -p "+destLogPath)

            if package in constants.perPackageToolChain:
                self.logger.debug("VDBG-BC-buildPackage: perPackageToolChain list for package " + package + ": ")
                self.logger.debug(constants.perPackageToolChain[package])
                self.installCustomToolChainRPMS(containerID, constants.perPackageToolChain[package], package);

            listInstalledPackages, listInstalledRPMs = self.findInstalledPackages(containerID)
            self.logger.debug("VDBG-BC-buildPackage: List of installed package RPMs: ")
            self.logger.debug(listInstalledRPMs)
            self.logger.info(listInstalledPackages)
            listDependentPackages = self.findBuildTimeRequiredPackages(package)

            pkgUtils = PackageUtils(self.logName,self.logPath)
            #self.logger.info("VDBG-BC-buildPackage: Checking len(dependentpkg)")
            if len(listDependentPackages) != 0:
                self.logger.info("VDBG-BC-buildPackage: Installing dependent packages..")
                for pkg in listDependentPackages:
                    #self.logger.info("VDBG-BC-buildPackage: Calling installPackage for: " + pkg)
                    self.installPackage(pkgUtils, pkg, containerID, destLogPath, listInstalledPackages, listInstalledRPMs)
                #self.logger.info("VDBG-BC-buildPackage: Finished installPackage")
                pkgUtils.installRPMSInAOneShotInContainer(containerID, destLogPath)
                #self.logger.info("VDBG-BC-buildPackage: Finished installRPMSIn 1shot")
            #self.logger.info("VDBG-BC-buildPackage: Calling adjustGCC")
            pkgUtils.adjustGCCSpecsInContainer(package, containerID, destLogPath)
            pkgUtils.buildRPMSForGivenPackageInContainer(
                                               package,
                                               containerID,
                                               self.listBuildOptionPackages,
                                               self.pkgBuildOptionFile,
                                               destLogPath)
            self.logger.info("VDBG-BC-buildPackage: Successfully built the package: " + package)
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

    def findRunTimeRequiredRPMPackages(self, rpmPackage):
        listRequiredPackages = constants.specData.getRequiresForPackage(rpmPackage)
        return listRequiredPackages

    def findBuildTimeRequiredPackages(self, package):
        listRequiredPackages = constants.specData.getBuildRequiresForPackage(package)
        return listRequiredPackages

    def installPackage(self, pkgUtils, package, containerID, destLogPath, listInstalledPackages, listInstalledRPMs):
        latestRPM = os.path.basename(pkgUtils.findRPMFileForGivenPackage(package)).replace(".rpm", "")
        self.logger.info("VDBG-BC-installPackage: package: " + package + ", latestRPM: " + latestRPM)
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
        #self.logger.info("VDBG-BC-installDependentRunTimePackages: package: " + package + ", latestRPM: " + latestRPM)
        listRunTimeDependentPackages = self.findRunTimeRequiredRPMPackages(package)
        if len(listRunTimeDependentPackages) != 0:
            for pkg in listRunTimeDependentPackages:
                if self.mapPackageToCycles.has_key(pkg) and pkg not in self.listAvailableCyclicPackages:
                    continue
                latestPkgRPM = os.path.basename(pkgUtils.findRPMFileForGivenPackage(pkg)).replace(".rpm", "")
                if pkg in listInstalledPackages and latestPkgRPM in listInstalledRPMs:
                    continue
                self.installPackage(pkgUtils, pkg, containerID, destLogPath, listInstalledPackages, listInstalledRPMs)
