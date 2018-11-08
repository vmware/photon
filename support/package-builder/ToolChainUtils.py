import os.path
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
        self.logger.info("Step 1 : Building the core toolchain packages for " + constants.currentArch)
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
                destLogPath = constants.logPath + "/" + package + "-" + version + "." + constants.currentArch
                if not os.path.isdir(destLogPath):
                    CommandUtils.runCommandInShell("mkdir -p " + destLogPath)
                chroot = Chroot(self.logger)
                chroot.create(package + "-" + version)
                self.installToolchainRPMS(chroot, package, version)
                pkgUtils.adjustGCCSpecs(chroot, package, version)
                pkgUtils.buildRPMSForGivenPackage(chroot, package, version, destLogPath)
                pkgCount += 1
                chroot.destroy()
            self.logger.debug("Successfully built toolchain")
            self.logger.info("-" * 45 + "\n")
        except Exception as e:
            self.logger.error("Unable to build toolchain.")
            # print stacktrace
            traceback.print_exc()
            raise e
        return pkgCount

    def getListDependentPackages(self, package, version):
        listBuildRequiresPkg=SPECS.getData(constants.buildArch).getBuildRequiresForPackage(package, version)
        listBuildRequiresPkg.extend(SPECS.getData(constants.buildArch).getCheckBuildRequiresForPackage(package, version))
        return listBuildRequiresPkg

    def installToolchainRPMS(self, chroot, packageName=None, packageVersion=None, usePublishedRPMS=True, availablePackages=None):
        self.logger.debug("Installing toolchain RPMS.......")
        rpmFiles = ""
        packages = ""
        listBuildRequiresPackages = []

        listRPMsToInstall=list(constants.listToolChainRPMsToInstall)
        if constants.crossCompiling:
            targetPackageName = packageName
            packageName = None
            packageVersion = None
            listRPMsToInstall.extend(['cross-'+constants.targetArch+'-binutils',
                                      'cross-'+constants.targetArch+'-gcc'])
        if packageName:
            listBuildRequiresPackages = self.getListDependentPackages(packageName, packageVersion)
        for package in listRPMsToInstall:
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
                version = SPECS.getData(constants.buildArch).getHighestVersion(package)

            basePkg = SPECS.getData(constants.buildArch).getSpecName(package)+"-"+version
            isAvailable = (availablePackages and basePkg in availablePackages)

            if constants.rpmCheck:
                rpmFile = pkgUtils.findRPMFile(package, version, constants.buildArch)

            if rpmFile is None:
                # Honor the toolchain list order.
                # if index of depended package ('package') is more
                # then index of the current package that we are
                # building ('packageName'), then we _must_ use published
                # `package` rpm.
                if (packageName and
                    packageName in listRPMsToInstall and
                    listRPMsToInstall.index(packageName) <
                        listRPMsToInstall.index(package)):
                    isAvailable = False
                else:
                    rpmFile = pkgUtils.findRPMFile(package, version, constants.buildArch)

            if rpmFile is None:
                if not usePublishedRPMS or isAvailable or constants.crossCompiling:
                    raise Exception("%s-%s.%s not found in available packages" % (package, version, constants.buildArch))

                # Safe to use published RPM

                # sqlite-autoconf package was renamed, but it still published as sqlite-autoconf
                if (package == "sqlite") and (constants.buildArch == "x86_64"):
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

        self.logger.debug(rpmFiles)
        self.logger.debug(packages)
        cmd = (self.rpmCommand + " -i -v --nodeps --noorder --force --root " +
               chroot.getID() +" --define \'_dbpath /var/lib/rpm\' "+ rpmFiles)
        retVal = CommandUtils.runCommandInShell(cmd, logfn=self.logger.debug)
        if retVal != 0:
            self.logger.debug("Command Executed:" + cmd)
            self.logger.error("Installing toolchain failed")
            raise Exception("RPM installation failed")
        self.logger.debug("Successfully installed default toolchain RPMS in Chroot:" + chroot.getID())

        if packageName:
            self.installExtraToolChainRPMS(chroot, packageName, packageVersion)

        if constants.crossCompiling:
            self.installTargetToolchain(chroot, targetPackageName)

    def installExtraToolChainRPMS(self, sandbox, packageName, packageVersion):
        listOfToolChainPkgs = SPECS.getData(constants.buildArch).getExtraBuildRequiresForPackage(packageName, packageVersion)
        if not listOfToolChainPkgs:
            return
        self.logger.debug("Installing package specific toolchain RPMs for " + packageName +
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

    def installTargetToolchain(self, chroot, stopAtPackage=None):
        self.logger.debug("Installing target toolchain RPMS.......")
        pkgUtils = PackageUtils(self.logName, self.logPath)
        rpmFiles = ""
        packages = ""
        for package in constants.listCoreToolChainPackages:
            if stopAtPackage and package == stopAtPackage:
                break
            version = SPECS.getData().getHighestVersion(package)
            basePkg = SPECS.getData().getSpecName(package)
            # install all subpackages of given package
            # for instance: for 'glibc' we want glibc-devel, glibc-tools,
            #               glibc-i18n, etc also to be installed
            subpackages = SPECS.getData().getRPMPackages(basePkg, version)
            for p in subpackages:
                rpmFile = pkgUtils.findRPMFile(p, version, constants.targetArch)
                rpmFiles += " " + rpmFile
                packages += " " + package+"-"+version

        self.logger.debug(packages)

        cmd = "mkdir -p " + chroot.getID() +"/target-"+ constants.targetArch+"/var/lib/rpm"
        CommandUtils.runCommandInShell(cmd, logfn=self.logger.debug)

        if rpmFiles != "":
            cmd = (self.rpmCommand+" -Uvh --nodeps --ignorearch --noscripts --root "+
                   chroot.getID() +"/target-"+ constants.targetArch+
                   " --define \'_dbpath /var/lib/rpm\' "+rpmFiles)
            retVal = CommandUtils.runCommandInShell(cmd, logfn=self.logger.debug)
            if retVal != 0:
                self.logger.debug("Command Executed:" + cmd)
                self.logger.error("Installing toolchain failed")
                raise Exception("RPM installation failed")
        self.logger.debug("Successfully installed target toolchain RPMS in chroot:" + chroot.getID())
