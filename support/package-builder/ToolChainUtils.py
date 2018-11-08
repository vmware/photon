import os.path
import platform
import traceback
import re
from CommandUtils import CommandUtils
from Logger import Logger
from PackageUtils import PackageUtils
from constants import constants
from SpecData import SPECS
from StringUtils import StringUtils
from Sandbox import Chroot, Container

class ToolChainUtils(object):

    def __init__(self, logName=None, logPath=None):
        if logName is None:
            logName = "Toolchain Utils"
        if logPath is None:
            logPath = constants.logPath
        self.logName = logName
        self.logPath = logPath
        self.logger = Logger.getLogger(logName, logPath, constants.logLevel)
        self.rpmbuildCommand = "rpmbuild"
        if os.geteuid() == 0:
            self.rpmCommand = "rpm"
        else:
            self.rpmCommand = "fakeroot-ng rpm"

    def _findPublishedRPM(self, package, rpmdirPath):
        listFoundRPMFiles = CommandUtils.findFile(package + "-*.rpm", rpmdirPath)
        listFilterRPMFiles = []
        for f in listFoundRPMFiles:
            rpmFileName = os.path.basename(f)
            checkRPMName = rpmFileName.replace(package, "")
            rpmNameSplit = checkRPMName.split("-")
            if len(rpmNameSplit) == 3:
                listFilterRPMFiles.append(f)
        if len(listFilterRPMFiles) == 1:
            return listFilterRPMFiles[0]
        if len(listFilterRPMFiles) == 0:
            return None
        if len(listFilterRPMFiles) > 1:
            self.logger.error("Found multiple rpm files for given package in rpm directory." +
                              "Unable to determine the rpm file for package:" + package)
            return None

    def buildCoreToolChainPackages(self):
        self.logger.info("Step 1 : Building the core toolchain packages.....")
        self.logger.info(constants.listCoreToolChainPackages)
        self.logger.info("")
        chroot = None
        pkgCount = 0
        try:
            pkgUtils = PackageUtils(self.logName, self.logPath)
            coreToolChainYetToBuild = []
            for package in constants.listCoreToolChainPackages:
                version = SPECS.getData().getHighestVersion(package)
                rpmPkg = pkgUtils.findRPMFile(package, version)
                if rpmPkg is not None:
                    continue
                else:
                    coreToolChainYetToBuild.append(package)
            if coreToolChainYetToBuild:
                self.logger.info("The following core toolchain packages need to be built :")
                self.logger.info(coreToolChainYetToBuild)
            else:
                self.logger.info("Core toolchain packages are already available")

            for package in coreToolChainYetToBuild:
                self.logger.debug("Building core toolchain package : " + package)
                version = SPECS.getData().getHighestVersion(package)
                destLogPath = constants.logPath + "/" + package + "-" + version
                if not os.path.isdir(destLogPath):
                    CommandUtils.runCommandInShell("mkdir -p " + destLogPath)
                chroot = Chroot(self.logger)
                chroot.create(package + "-" + version)
                self.installToolChainRPMS(chroot, package, version, destLogPath)
                pkgUtils.adjustGCCSpecs(chroot, package, version)
                pkgUtils.buildRPMSForGivenPackage(chroot, package, version, destLogPath)
                pkgCount += 1
                chroot.destroy()
            self.logger.debug("Successfully built toolchain")
            self.logger.info("-" * 45 + "\n")
        except Exception as e:
            self.logger.error("Unable to build tool chain.")
            # print stacktrace
            traceback.print_exc()
            raise e
        return pkgCount

    def getListDependentPackages(self, package, version):
        listBuildRequiresPkg=SPECS.getData().getBuildRequiresForPackage(package, version)
        listBuildRequiresPkg.extend(SPECS.getData().getCheckBuildRequiresForPackage(package, version))
        return listBuildRequiresPkg

    def installToolChainRPMS(self, chroot, packageName=None, packageVersion=None, logPath=None, usePublishedRPMS=True, availablePackages=None):
        if logPath is None:
            logPath = self.logPath
        self.logger.debug("Installing Tool Chain RPMS.......")
        rpmFiles = ""
        packages = ""
        listBuildRequiresPackages = []
        if packageName:
            listBuildRequiresPackages = self.getListDependentPackages(packageName, packageVersion)
        for package in constants.listToolChainRPMsToInstall:
            pkgUtils = PackageUtils(self.logName, self.logPath)
            rpmFile = None
            version = None

            # Get proper package version
            for depPkg in listBuildRequiresPackages:
                depPkgName, depPkgVersion = StringUtils.splitPackageNameAndVersion(depPkg)
                if depPkgName == package:
                        version=depPkgVersion
                        break
            if not version:
                version = SPECS.getData().getHighestVersion(package)

            basePkg = SPECS.getData().getSpecName(package)+"-"+version
            isAvailable = (availablePackages and basePkg in availablePackages)

            if constants.rpmCheck:
                rpmFile = pkgUtils.findRPMFile(package, version)

            if rpmFile is None:
                # Honor the toolchain list order.
                # if index of depended package ('package') is more
                # then index of the current package that we are
                # building ('packageName'), then we _must_ use published
                # `package` rpm.
                if (packageName and
                    packageName in constants.listToolChainRPMsToInstall and
                    constants.listToolChainRPMsToInstall.index(packageName) <
                        constants.listToolChainRPMsToInstall.index(package)):
                    isAvailable = False
                else:
                    rpmFile = pkgUtils.findRPMFile(package, version)

            if rpmFile is None:
                if not usePublishedRPMS or isAvailable:
                    raise Exception("%s-%s not found in available packages" % (package, version))

                # sqlite-autoconf package was renamed, but it still published as sqlite-autoconf
                if (package == "sqlite") and (platform.machine() == "x86_64"):
                    package = "sqlite-autoconf"
                rpmFile = self._findPublishedRPM(package, constants.prevPublishRPMRepo)
                if rpmFile is None:
                    if package in constants.listOfRPMsProvidedAfterBuild:
                        self.logger.debug("No old version of " + package +
                                         " exists, skip until the new version is built")
                        continue
                    self.logger.error("Unable to find published rpm " + package)
                    raise Exception("Input Error")
            rpmFiles += " " + rpmFile
            packages += " " + package+"-"+version

        self.logger.debug(packages)
        cmd = (self.rpmCommand + " -i -v --nodeps --noorder --force --root " +
               chroot.getPath() +" --define \'_dbpath /var/lib/rpm\' "+ rpmFiles)
        retVal = CommandUtils.runCommandInShell(cmd, logfn=self.logger.debug)
        if retVal != 0:
            self.logger.debug("Command Executed:" + cmd)
            self.logger.error("Installing tool chain  failed")
            raise Exception("RPM installation failed")
        self.logger.debug("Successfully installed default Tool Chain RPMS in Chroot:" + chroot.getPath())
        if packageName:
            self.installCustomToolChainRPMS(chroot, packageName, packageVersion)

    def installCustomToolChainRPMS(self, sandbox, packageName, packageVersion):
        listOfToolChainPkgs = SPECS.getData().getExtraBuildRequiresForPackage(packageName, packageVersion)
        if not listOfToolChainPkgs:
            return
        self.logger.debug("Installing package specific tool chain RPMs for " + packageName +
                         ": " + str(listOfToolChainPkgs))
        rpmFiles = ""
        packages = ""
        for package in listOfToolChainPkgs:
            pkgUtils = PackageUtils(self.logName, self.logPath)
            if re.match("openjre*", packageName) is not None or re.match("openjdk*", packageName):
                path = constants.prevPublishXRPMRepo
                sandboxPath = "/publishxrpms"
            else:
                path = constants.prevPublishRPMRepo
                sandboxPath = "/publishrpms"
            rpmFile = self._findPublishedRPM(package, path)
            if rpmFile is None:
                self.logger.error("Unable to find rpm "+ package +
                                  " in current and previous versions")
                raise Exception("Input Error")
            rpmFiles += " " + rpmFile.replace(path, sandboxPath)
            packages += " " + package

        self.logger.debug("Installing custom rpms:" + packages)
        cmd = (self.rpmCommand + " -i -v --nodeps --noorder --force " + rpmFiles)
        retVal = sandbox.run(cmd, logfn=self.logger.debug)
        if retVal != 0:
            self.logger.debug("Command Executed:" + cmd)
            self.logger.error("Installing custom toolchains failed")
            raise Exception("RPM installation failed")

