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
from distutils.version import LooseVersion
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

    def buildPackageFunction(self, pkg):
        packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
        #do not build if RPM is already built
        #test only if the package is in the testForceRPMS with rpmCheck
        #build only if the package is not in the testForceRPMS with rpmCheck
        if self._checkIfPackageIsAlreadyBuilt(packageName, packageVersion):
            if not constants.rpmCheck:
                return
            elif constants.rpmCheck and self.package not in constants.testForceRPMS:
                return

        self._buildPackagePrepareFunction(packageName, packageVersion)
        try:
            self._buildPackage()
        except Exception as e:
            # TODO: self.logger might be None
            self.logger.exception(e)
            raise e

    def _buildPackagePrepareFunction(self, package, version):
        self.package = package
        self.version = version
        self.logName = "build-" + package + "-" + version
        self.logPath = constants.logPath + "/" + package + "-" + version
        if not os.path.isdir(self.logPath):
            cmdUtils = CommandUtils()
            cmdUtils.runCommandInShell("mkdir -p " + self.logPath)
        self.logger = Logger.getLogger(self.logName, self.logPath, constants.logLevel)

    def _findPackageNameAndVersionFromRPMFile(self, rpmfile):
        rpmfile = os.path.basename(rpmfile)
        releaseindex = rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:" + rpmfile)
            return None
        pkg = rpmfile[0:releaseindex]
        return pkg

    def _findInstalledPackages(self, instanceID):
        pkgUtils = PackageUtils(self.logName, self.logPath)
        if self.pkgBuildType == "chroot":
            listInstalledRPMs = pkgUtils.findInstalledRPMPackages(instanceID)
        elif self.pkgBuildType == "container":
            listInstalledRPMs = pkgUtils.findInstalledRPMPackagesInContainer(instanceID)
        listInstalledPackages = []
        for installedRPM in listInstalledRPMs:
            pkg = self._findPackageNameAndVersionFromRPMFile(installedRPM)
            if pkg is not None:
                listInstalledPackages.append(pkg)
        return listInstalledPackages, listInstalledRPMs

    def _checkIfPackageIsAlreadyBuilt(self, package, version):
        basePkg = SPECS.getData().getSpecName(package)
        listRPMPackages = SPECS.getData().getRPMPackages(basePkg, version)
        packageIsAlreadyBuilt = True
        pkgUtils = PackageUtils()
        for pkg in listRPMPackages:
            if pkgUtils.findRPMFileForGivenPackage(pkg, version) is None:
                packageIsAlreadyBuilt = False
                break
        return packageIsAlreadyBuilt

    def _findRunTimeRequiredRPMPackages(self, rpmPackage, version):
        return SPECS.getData().getRequiresForPackage(rpmPackage, version)

    def _findBuildTimeRequiredPackages(self):
        return SPECS.getData().getBuildRequiresForPackage(self.package, self.version)

    def _findBuildTimeCheckRequiredPackages(self):
        return SPECS.getData().getCheckBuildRequiresForPackage(self.package, self.version)

    def _installPackage(self, pkgUtils, package,packageVersion, instanceID, destLogPath,
                        listInstalledPackages, listInstalledRPMs):
        rpmfile = pkgUtils.findRPMFileForGivenPackage(package,packageVersion);
        if rpmfile is None:
            self.logger.error("No rpm file found for package: " + package + "-" + packageVersion)
            raise Exception("Missing rpm file")
        specificRPM = os.path.basename(rpmfile.replace(".rpm", ""))
        pkg = package+"-"+packageVersion
        if pkg in listInstalledPackages:
                return
        # mark it as installed -  to avoid cyclic recursion
        listInstalledPackages.append(pkg)
        listInstalledRPMs.append(specificRPM)
        self._installDependentRunTimePackages(pkgUtils, package, packageVersion, instanceID, destLogPath,
                                              listInstalledPackages, listInstalledRPMs)
        noDeps = False
        if (package in self.mapPackageToCycles or
                package in self.listNodepsPackages or
                package in constants.noDepsPackageList):
            noDeps = True
        if self.pkgBuildType == "chroot":
            pkgUtils.installRPM(package, packageVersion,instanceID, noDeps, destLogPath)
        elif self.pkgBuildType == "container":
            pkgUtils.prepRPMforInstallInContainer(package,packageVersion, instanceID, noDeps, destLogPath)

    def _installDependentRunTimePackages(self, pkgUtils, package, packageVersion, instanceID, destLogPath,
                                         listInstalledPackages, listInstalledRPMs):
        listRunTimeDependentPackages = self._findRunTimeRequiredRPMPackages(package, packageVersion)
        if listRunTimeDependentPackages:
            for pkg in listRunTimeDependentPackages:
                if pkg in self.mapPackageToCycles:
                    continue
                packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                latestPkgRPM = os.path.basename(
                    pkgUtils.findRPMFileForGivenPackage(packageName, packageVersion)).replace(".rpm", "")
                if pkg in listInstalledPackages and latestPkgRPM in listInstalledRPMs:
                    continue
                self._installPackage(pkgUtils, packageName,packageVersion, instanceID, destLogPath,listInstalledPackages, listInstalledRPMs)

    def _findDependentPackagesAndInstalledRPM(self, instanceID):
        listInstalledPackages, listInstalledRPMs = self._findInstalledPackages(instanceID)
        self.logger.debug(listInstalledPackages)
        listDependentPackages = self._findBuildTimeRequiredPackages()
        listTestPackages=[]
        if constants.rpmCheck and self.package in constants.testForceRPMS:
            # One time optimization
            if constants.listMakeCheckRPMPkgWithVersionstoInstall is None:
                constants.listMakeCheckRPMPkgWithVersionstoInstalli=[]
                for package in constants.listMakeCheckRPMPkgtoInstall:
                    version = SPECS.getData().getHighestVersion(package)
                    constants.listMakeCheckRPMPkgWithVersionstoInstall.append(package+"-"+version)

            listDependentPackages.extend(self._findBuildTimeCheckRequiredPackages())
            testPackages = (set(constants.listMakeCheckRPMPkgWithVersionstoInstall) -
                            set(listInstalledPackages) -
                            set([self.package+"-"+self.version]))
            listTestPackages=list(set(testPackages))
            listDependentPackages = list(set(listDependentPackages))
        return listDependentPackages, listTestPackages, listInstalledPackages, listInstalledRPMs

class PackageBuilderContainer(PackageBuilderBase):
    def __init__(self, mapPackageToCycles, pkgBuildType):
        self.buildContainerImage = "photon_build_container:latest"
        self.dockerClient = docker.from_env(version="auto")

        PackageBuilderBase.__init__(self, mapPackageToCycles, pkgBuildType)

    def _prepareBuildContainer(self, containerTaskName, packageName, packageVersion,
                               isToolChainPackage=False):
        # Prepare an empty chroot environment to let docker use the BUILD folder.
        # This avoids docker using overlayFS which will cause make check failure.
        chrootName = packageName + "-" + packageVersion
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
            self.logger.debug("BuildContainer-prepareBuildContainer: " +
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

    def _buildPackage(self):
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
                containerTaskName, self.package, self.version, isToolChainPackage)

            tcUtils = ToolChainUtils(self.logName, self.logPath)
            if self.package in constants.perPackageToolChain:
                self.logger.debug(constants.perPackageToolChain[self.package])
                tcUtils.installCustomToolChainRPMSinContainer(
                    containerID,
                    constants.perPackageToolChain[self.package].get(platform.machine(), []),
                    self.package)

            listDependentPackages, listTestPackages, listInstalledPackages, listInstalledRPMs = (
                self._findDependentPackagesAndInstalledRPM(containerID))

            pkgUtils = PackageUtils(self.logName, self.logPath)
            if listDependentPackages:
                self.logger.debug("BuildContainer-buildPackage: " +
                                 "Installing dependent packages..")
                self.logger.debug(listDependentPackages)
                for pkg in listDependentPackages:
                    packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                    self._installPackage(pkgUtils, packageName, packageVersion, containerID, destLogPath,listInstalledPackages, listInstalledRPMs)
                for pkg in listTestPackages:
                    packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                    flag = False
                    for depPkg in listDependentPackages:
                        depPackageName, depPackageVersion = StringUtils.splitPackageNameAndVersion(depPkg)
                        if depPackageName == packageName:
                            flag = True
                            break;
                    if flag == False:
                        self._installPackage(pkgUtils, packageName,packageVersion, containerID, destLogPath,listInstalledPackages, listInstalledRPMs)
                pkgUtils.installRPMSInAOneShotInContainer(containerID, destLogPath)
                self.logger.debug("Finished installing the build time dependent packages....")

            self.logger.debug("BuildContainer-buildPackage: Start building the package: " +
                             self.package)
            pkgUtils.adjustGCCSpecsInContainer(self.package, self.version, containerID, destLogPath)
            pkgUtils.buildRPMSForGivenPackageInContainer(
                self.package,
                self.version,
                containerID,
                destLogPath)
            self.logger.debug("BuildContainer-buildPackage: Successfully built the package: " +
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
        chrootName = self.package + "-" + self.version
        try:
            chrUtils = ChrootUtils(self.logName, self.logPath)
            returnVal, chrootID = chrUtils.createChroot(chrootName)
            self.logger.debug("Created new chroot: " + chrootID)
            if not returnVal:
                raise Exception("Unable to prepare build root")
            tUtils = ToolChainUtils(self.logName, self.logPath)
            tUtils.installToolChainRPMS(self.package, self.version, chrootID, self.logPath)
        except Exception as e:
            if chrootID is not None:
                self.logger.debug("Deleting chroot: " + chrootID)
                chrUtils.destroyChroot(chrootID)
            raise e
        return chrootID

    def _buildPackage(self):
        chrUtils = ChrootUtils(self.logName, self.logPath)
        chrootID = None
        try:
            chrootID = self._prepareBuildRoot()
            listDependentPackages, listTestPackages, listInstalledPackages, listInstalledRPMs = (
                self._findDependentPackagesAndInstalledRPM(chrootID))

            pkgUtils = PackageUtils(self.logName, self.logPath)

            if listDependentPackages:
                self.logger.debug("Installing the build time dependent packages......")
                for pkg in listDependentPackages:
                    packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                    self._installPackage(pkgUtils, packageName, packageVersion, chrootID, self.logPath,listInstalledPackages, listInstalledRPMs)
                for pkg in listTestPackages:
                    flag = False
                    packageName, packageVersion = StringUtils.splitPackageNameAndVersion(pkg)
                    for depPkg in listDependentPackages:
                        depPackageName, depPackageVersion = StringUtils.splitPackageNameAndVersion(depPkg)
                        if depPackageName == packageName:
                                flag = True
                                break;
                    if flag == False:
                        self._installPackage(pkgUtils, packageName,packageVersion, chrootID, self.logPath,listInstalledPackages, listInstalledRPMs)
                pkgUtils.installRPMSInAOneShot(chrootID, self.logPath)
                self.logger.debug("Finished installing the build time dependent packages....")

            pkgUtils.adjustGCCSpecs(self.package, self.version, chrootID, self.logPath)
            pkgUtils.buildRPMSForGivenPackage(self.package, self.version, chrootID,
                                              self.logPath)
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
