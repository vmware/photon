import sys
import os.path
from PackageUtils import PackageUtils
from Logger import Logger
from ChrootUtils import ChrootUtils
from ToolChainUtils import ToolChainUtils
from CommandUtils import CommandUtils
from constants import constants
from SpecData import SPECS
import docker

class PackageBuilderBase(object):
    def __init__(self, mapPackageToCycles, pkgBuildType):
        # will be initialized in buildPackageFunction()
        self.logName = None
        self.logPath = None
        self.logger = None
        self.package = None
        self.mapPackageToCycles = mapPackageToCycles
        self.listNodepsPackages = ["glibc", "gmp", "zlib", "file", "binutils", "mpfr",
                                   "mpc", "gcc", "ncurses", "util-linux", "groff", "perl",
                                   "texinfo", "rpm", "openssl", "go"]
        self.pkgBuildType = pkgBuildType

    def buildPackageFunction(self, package):
        self._buildPackagePrepareFunction(package)
        versions = self.getNumOfVersions(package)
        if(versions < 1):
            raise Exception("No package exists")
        for version in range(0, versions):
            try:
                self._buildPackage(version)
            except Exception as e:
                # TODO: self.logger might be None
                self.logger.exception(e)
                raise e

    def _buildPackagePrepareFunction(self, package):
        self.package = package
        self.logName = "build-" + package
        self.logPath = constants.logPath + "/build-" + package
        if not os.path.isdir(self.logPath):
            cmdUtils = CommandUtils()
            cmdUtils.runCommandInShell("mkdir -p " + self.logPath)
        self.logger = Logger.getLogger(self.logName, self.logPath)

    def _findPackageNameFromRPMFile(self, rpmfile):
        rpmfile = os.path.basename(rpmfile)
        releaseindex = rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:" + rpmfile)
            return None
        versionindex = rpmfile[0:releaseindex].rfind("-")
        if versionindex == -1:
            self.logger.error("Invalid rpm file:" + rpmfile)
            return None
        packageName = rpmfile[0:versionindex]
        return packageName

    def _findInstalledPackages(self, instanceID):
        pkgUtils = PackageUtils(self.logName, self.logPath)
        if self.pkgBuildType == "chroot":
            listInstalledRPMs = pkgUtils.findInstalledRPMPackages(instanceID)
        elif self.pkgBuildType == "container":
            listInstalledRPMs = pkgUtils.findInstalledRPMPackagesInContainer(instanceID)
        listInstalledPackages = []
        for installedRPM in listInstalledRPMs:
            packageName = self._findPackageNameFromRPMFile(installedRPM)
            if packageName is not None:
                listInstalledPackages.append(packageName)
        return listInstalledPackages, listInstalledRPMs

    def _checkIfPackageIsAlreadyBuilt(self, index=0):
        basePkg = SPECS.getData().getSpecName(self.package)
        listRPMPackages = SPECS.getData().getRPMPackages(basePkg, index)
        packageIsAlreadyBuilt = True
        pkgUtils = PackageUtils(self.logName, self.logPath)
        for pkg in listRPMPackages:
            if pkgUtils.findRPMFileForGivenPackage(pkg, index) is None:
                packageIsAlreadyBuilt = False
                break
        return packageIsAlreadyBuilt

    def _findRunTimeRequiredRPMPackages(self, rpmPackage, index=0):
        return SPECS.getData().getRequiresForPackage(rpmPackage, index)

    def _findBuildTimeRequiredPackages(self, index=0):
        return SPECS.getData().getBuildRequiresForPackage(self.package, index)

    def _findBuildTimeCheckRequiredPackages(self, index=0):
        return SPECS.getData().getCheckBuildRequiresForPackage(self.package, index)

    def _installPackage(self, pkgUtils, package, instanceID, destLogPath,
                        listInstalledPackages, listInstalledRPMs):
        latestRPM = os.path.basename(
            pkgUtils.findRPMFileForGivenPackage(package)).replace(".rpm", "")
        if package in listInstalledPackages and latestRPM in listInstalledRPMs:
            return
        # mark it as installed -  to avoid cyclic recursion
        listInstalledPackages.append(package)
        listInstalledRPMs.append(latestRPM)
        self._installDependentRunTimePackages(pkgUtils, package, instanceID, destLogPath,
                                              listInstalledPackages, listInstalledRPMs)
        noDeps = False
        if (package in self.mapPackageToCycles or
                package in self.listNodepsPackages or
                package in constants.noDepsPackageList):
            noDeps = True
        if self.pkgBuildType == "chroot":
            pkgUtils.installRPM(package, instanceID, noDeps, destLogPath)
        elif self.pkgBuildType == "container":
            pkgUtils.prepRPMforInstallInContainer(package, instanceID, noDeps, destLogPath)

    def _installDependentRunTimePackages(self, pkgUtils, package, instanceID, destLogPath,
                                         listInstalledPackages, listInstalledRPMs):
        listRunTimeDependentPackages = self._findRunTimeRequiredRPMPackages(package)
        if listRunTimeDependentPackages:
            for pkg in listRunTimeDependentPackages:
                if pkg in self.mapPackageToCycles:
                    continue
                latestPkgRPM = os.path.basename(
                    pkgUtils.findRPMFileForGivenPackage(pkg)).replace(".rpm", "")
                if pkg in listInstalledPackages and latestPkgRPM in listInstalledRPMs:
                    continue
                self._installPackage(pkgUtils, pkg, instanceID, destLogPath,
                                     listInstalledPackages, listInstalledRPMs)

    def _findDependentPackagesAndInstalledRPM(self, instanceID, index=0):
        listInstalledPackages, listInstalledRPMs = self._findInstalledPackages(instanceID)
        self.logger.info(listInstalledPackages)
        listDependentPackages = self._findBuildTimeRequiredPackages(index)
        if constants.rpmCheck and self.package in constants.testForceRPMS:
            listDependentPackages.extend(self._findBuildTimeCheckRequiredPackages(index))
            testPackages = (set(constants.listMakeCheckRPMPkgtoInstall) -
                            set(listInstalledPackages) -
                            set([self.package]))
            listDependentPackages.extend(testPackages)
            listDependentPackages = list(set(listDependentPackages))
        return listDependentPackages, listInstalledPackages, listInstalledRPMs

    @staticmethod
    def getNumOfVersions(package):
        return SPECS.getData().getNumberOfVersions(package)

class PackageBuilderContainer(PackageBuilderBase):
    def __init__(self, mapPackageToCycles, pkgBuildType):
        self.buildContainerImage = "photon_build_container:latest"
        self.dockerClient = docker.from_env(version="auto")

        PackageBuilderBase.__init__(self, mapPackageToCycles, pkgBuildType)

    def _prepareBuildContainer(self, containerTaskName, packageName,
                               isToolChainPackage=False):
        # Prepare an empty chroot environment to let docker use the BUILD folder.
        # This avoids docker using overlayFS which will cause make check failure.
        chrootName = "build-" + packageName
        chrUtils = ChrootUtils(self.logName, self.logPath)
        returnVal, chrootID = chrUtils.createChroot(chrootName)
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
            constants.logPath + "/" + self.logName: {'bind': constants.topDirPath + "/LOGS",
                                                     'mode': 'rw'},
            chrootID + constants.topDirPath + "/BUILD": {'bind': constants.topDirPath + "/BUILD",
                                                         'mode': 'rw'},
            constants.dockerUnixSocket: {'bind': constants.dockerUnixSocket, 'mode': 'rw'}
            }

        containerName = containerTaskName
        containerName = containerName.replace("+", "p")
        try:
            oldContainerID = self.dockerClient.containers.get(containerName)
            if oldContainerID is not None:
                oldContainerID.remove(force=True)
        except docker.errors.NotFound:
            try:
                sys.exc_clear()
            except:
                pass

        try:
            self.logger.info("BuildContainer-prepareBuildContainer: " +
                             "Starting build container: " + containerName)
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

            self.logger.debug("Started Photon build container for task " + containerTaskName +
                              " ID: " + containerID.short_id)
            if not containerID:
                raise Exception("Unable to start Photon build container for task " +
                                containerTaskName)
        except Exception as e:
            self.logger.debug("Unable to start Photon build container for task " +
                              containerTaskName)
            raise e
        return containerID, chrootID

    def _buildPackage(self, index=0):
        #do not build if RPM is already built
        #test only if the package is in the testForceRPMS with rpmCheck
        #build only if the package is not in the testForceRPMS with rpmCheck
        if self._checkIfPackageIsAlreadyBuilt(index):
            if not constants.rpmCheck:
                self.logger.info("Skipping building the package:" + self.package)
                return
            elif constants.rpmCheck and self.package not in constants.testForceRPMS:
                self.logger.info("Skipping testing the package:" + self.package)
                return

        #should initialize a logger based on package name
        containerTaskName = "build-" + self.package
        containerID = None
        chrootID = None
        isToolChainPackage = False
        if self.package in constants.listToolChainPackages:
            isToolChainPackage = True
        destLogPath = constants.logPath + "/build-" + self.package
        try:
            containerID, chrootID = self._prepareBuildContainer(
                containerTaskName, self.package, isToolChainPackage)

            tcUtils = ToolChainUtils(self.logName, self.logPath)
            if self.package in constants.perPackageToolChain:
                self.logger.debug(constants.perPackageToolChain[self.package])
                tcUtils.installCustomToolChainRPMSinContainer(
                    containerID,
                    constants.perPackageToolChain[self.package],
                    self.package)

            listDependentPackages, listInstalledPackages, listInstalledRPMs = (
                self._findDependentPackagesAndInstalledRPM(containerID, index))

            pkgUtils = PackageUtils(self.logName, self.logPath)
            if listDependentPackages:
                self.logger.info("BuildContainer-buildPackage: " +
                                 "Installing dependent packages..")
                self.logger.info(listDependentPackages)
                for pkg in listDependentPackages:
                    self._installPackage(pkgUtils, pkg, containerID, destLogPath,
                                         listInstalledPackages, listInstalledRPMs)
                pkgUtils.installRPMSInAOneShotInContainer(containerID, destLogPath)
                self.logger.info("Finished installing the build time dependent packages....")

            self.logger.info("BuildContainer-buildPackage: Start building the package: " +
                             self.package)
            pkgUtils.adjustGCCSpecsInContainer(self.package, containerID, destLogPath, index)
            pkgUtils.buildRPMSForGivenPackageInContainer(
                self.package,
                containerID,
                destLogPath,
                index)
            self.logger.info("BuildContainer-buildPackage: Successfully built the package: " +
                             self.package)
        except Exception as e:
            self.logger.error("Failed while building package:" + self.package)
            if containerID is not None:
                self.logger.debug("Container " + containerID.short_id +
                                  " retained for debugging.")
            logFileName = os.path.join(destLogPath, self.package + ".log")
            fileLog = os.popen('tail -n 20 ' + logFileName).read()
            self.logger.debug(fileLog)
            raise e

        # Remove the container
        if containerID is not None:
            containerID.remove(force=True)
        # Remove the dummy chroot
        if chrootID is not None:
            chrUtils = ChrootUtils(self.logName, self.logPath)
            chrUtils.destroyChroot(chrootID)

class PackageBuilderChroot(PackageBuilderBase):
    def __init__(self, mapPackageToCycles, pkgBuildType):
        PackageBuilderBase.__init__(self, mapPackageToCycles, pkgBuildType)

    def _prepareBuildRoot(self):
        chrootID = None
        chrootName = "build-" + self.package
        try:
            chrUtils = ChrootUtils(self.logName, self.logPath)
            returnVal, chrootID = chrUtils.createChroot(chrootName)
            self.logger.debug("Created new chroot: " + chrootID)
            if not returnVal:
                raise Exception("Unable to prepare build root")
            tUtils = ToolChainUtils(self.logName, self.logPath)
            tUtils.installToolChainRPMS(chrootID, self.package, self.logPath)
        except Exception as e:
            if chrootID is not None:
                self.logger.debug("Deleting chroot: " + chrootID)
                chrUtils.destroyChroot(chrootID)
            raise e
        return chrootID

    def _buildPackage(self, index=0):
        #do not build if RPM is already built
        #test only if the package is in the testForceRPMS with rpmCheck
        #build only if the package is not in the testForceRPMS with rpmCheck
        if self._checkIfPackageIsAlreadyBuilt(index):
            if not constants.rpmCheck:
                self.logger.info("Skipping building the package:" + self.package)
                return
            elif constants.rpmCheck and self.package not in constants.testForceRPMS:
                self.logger.info("Skipping testing the package:" + self.package)
                return

        chrUtils = ChrootUtils(self.logName, self.logPath)
        chrootID = None
        try:
            chrootID = self._prepareBuildRoot()
            listDependentPackages, listInstalledPackages, listInstalledRPMs = (
                self._findDependentPackagesAndInstalledRPM(chrootID, index))

            pkgUtils = PackageUtils(self.logName, self.logPath)

            if listDependentPackages:
                self.logger.info("Installing the build time dependent packages......")
                for pkg in listDependentPackages:
                    self._installPackage(pkgUtils, pkg, chrootID, self.logPath,
                                         listInstalledPackages, listInstalledRPMs)
                pkgUtils.installRPMSInAOneShot(chrootID, self.logPath)
                self.logger.info("Finished installing the build time dependent packages....")

            pkgUtils.adjustGCCSpecs(self.package, chrootID, self.logPath, index)
            pkgUtils.buildRPMSForGivenPackage(self.package, chrootID,
                                              self.logPath, index)
            self.logger.info("Successfully built the package:" + self.package)
        except Exception as e:
            self.logger.error("Failed while building package:" + self.package)
            self.logger.debug("Chroot with ID: " + chrootID +
                              " not deleted for debugging.")
            logFileName = os.path.join(self.logPath, self.package + ".log")
            fileLog = os.popen('tail -n 100 ' + logFileName).read()
            self.logger.debug(fileLog)
            raise e
        if chrootID is not None:
            chrUtils.destroyChroot(chrootID)
