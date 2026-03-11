#!/usr/bin/env python3

import json
import pathlib
import platform
import re
from copy import deepcopy
from enum import Enum

from Logger import Logger

PH_COMMIT_URI_PREFIX = "https://github.com/vmware/photon/commit/"


class SandboxType(str, Enum):
    CHROOT = "chroot"
    CONTAINER = "container"
    SYSTEMD_NSPAWN = "systemd-nspawn"


class BuildStage(str, Enum):
    NONE = "none"
    CORE_TOOLCHAIN = "core_toolchain"
    TOOLCHAIN = "toolchain"
    PACKAGES = "packages"


class BuildMode(str, Enum):
    BOOTSTRAP = "bootstrap"
    STANDARD = "standard"


class constants(object):
    specPaths = []
    gitSourcePaths = {}
    stagePath = ""
    sourcePath = ""
    rpmPath = ""
    logPath = ""
    logLevel = "info"
    topDirPath = ""
    buildRootPath = "/mnt"
    pullsourcesURL = ""
    extrasourcesURLs = {}
    buildPatch = False
    rpmCheck = False
    startSchedulerServer = False
    sourceRpmPath = ""
    packageWeightsPath = None
    dockerUnixSocket = "/var/run/docker.sock"
    userDefinedMacros = {}
    dist = None
    buildNumber = None
    commonBuildNumber = None
    releaseVersion = None
    subreleaseVersion = None
    photonBranch = None
    katBuild = False
    canisterBuild = False
    acvpBuild = False
    tmpDirPath = "/dev/shm"
    buildOptions = {}
    srpcli = None
    observerDockerImage = None
    observationIgnHostPatterns = []
    isolatedDockerNetwork = None
    buildArch = platform.machine()
    photonDir = ""
    buildSrcRpm = 0
    buildDbgInfoRpm = 0
    resume_build = False
    buildDbgInfoRpmList = []
    extraPackagesList = []
    releasePkgPreqPath = ""
    CopyToSandboxDict = {}
    SandboxEnv = {}
    adjustGCCSpecScript = None
    rebuild = False
    photonBuilder = "photon-builder"
    toolchainBootstrap = False
    bootstrapRepoPath = None
    packageRepoURL = None
    packageRepoPath = None
    packageRepoSnapshotURL = None
    sandboxType: SandboxType = SandboxType.CHROOT
    testLogger = None

    # These packages will be built in first order as build-core-toolchain stage
    # Put only main pakage names here. Do not add subpackages such as libgcc
    listCoreToolChainPackages = []

    # These packages will be built in a second stage to replace pre-released RPMS
    # Put only main pakage names here. Do not add subpackages such as libgcc
    listToolChainPackages = []

    # List or RPMS that will be installed in a chroot prior to build each
    # package. This list should be ordered by install order. On a stage1
    # and stage2 published rpms will/might be used after stage2 only local
    # RPMS will be used
    listToolChainRPMsToInstall = []

    """
    .spec file might contain lines such as
    Requires(post):/sbin/useradd
    Build system should interpret it as
    Requires: shadow
    """
    providedBy = {}

    @staticmethod
    def addSpecPath(specPath):
        constants.specPaths.append(specPath)

    @staticmethod
    def setReleasePkgPreqPath(releasePkgPreqPath):
        constants.releasePkgPreqPath = releasePkgPreqPath

    @staticmethod
    def setSpecPaths(specPaths):
        constants.specPaths = specPaths

    @staticmethod
    def addGitSourcePath(branch, gitSourcePath):
        constants.gitSourcePaths[branch] = gitSourcePath

    @staticmethod
    def setStagePath(stagePath):
        constants.stagePath = stagePath

    @staticmethod
    def setSourcePath(sourcePath):
        constants.sourcePath = sourcePath

    @staticmethod
    def setRpmPath(rpmPath):
        constants.rpmPath = rpmPath

    @staticmethod
    def setSourceRpmPath(sourceRpmPath):
        constants.sourceRpmPath = sourceRpmPath

    @staticmethod
    def setTopDirPath(topDirPath):
        constants.topDirPath = topDirPath

    @staticmethod
    def setLogLevel(logLevel):
        constants.logLevel = logLevel

    @staticmethod
    def setLogPath(logPath):
        constants.logPath = logPath

    @staticmethod
    def setBuildRootPath(buildRootPath):
        constants.buildRootPath = buildRootPath

    @staticmethod
    def setPullSourcesURL(url):
        constants.pullsourcesURL = url

    @staticmethod
    def setExtraSourcesURLs(packageName, urls):
        constants.extrasourcesURLs[packageName] = urls

    @staticmethod
    def getPullSourcesURLs(packageName):
        urls = []
        urls.append(constants.pullsourcesURL)
        if packageName in constants.extrasourcesURLs:
            urls.extend(constants.extrasourcesURLs[packageName])
        return urls

    @staticmethod
    def setRPMCheck(rpmCheck):
        constants.rpmCheck = rpmCheck

    @staticmethod
    def setRpmCheckStopOnError(rpmCheckStopOnError):
        constants.rpmCheckStopOnError = rpmCheckStopOnError

    @staticmethod
    def setStartSchedulerServer(startSchedulerServer):
        constants.startSchedulerServer = startSchedulerServer

    @staticmethod
    def setPackageWeightsPath(packageWeightsPath):
        constants.packageWeightsPath = packageWeightsPath

    @staticmethod
    def setDist(dist):
        constants.dist = dist

    @staticmethod
    def setBuildNumber(buildNumber):
        constants.buildNumber = buildNumber

    @staticmethod
    def setCommonBuildNumber(commonBuildNumber):
        constants.commonBuildNumber = commonBuildNumber

    @staticmethod
    def setReleaseVersion(releaseVersion):
        constants.releaseVersion = releaseVersion

    @staticmethod
    def setSubreleaseVersion(subreleaseVersion):
        constants.subreleaseVersion = subreleaseVersion

    @staticmethod
    def setPhotonBranch(photonBranch):
        constants.photonBranch = photonBranch

    @staticmethod
    def setKatBuild(katBuild):
        constants.katBuild = katBuild

    @staticmethod
    def setCanisterBuild(canisterBuild):
        constants.canisterBuild = canisterBuild

    @staticmethod
    def setAcvpBuild(acvpBuild):
        constants.acvpBuild = acvpBuild

    @staticmethod
    def setCompressionMacro(compressionMacro):
        constants.addMacro("_source_payload", compressionMacro)
        constants.addMacro("_binary_payload", compressionMacro)

    @staticmethod
    def initialize():
        if constants.rpmCheck:
            constants.testLogger = Logger.getLogger(
                "MakeCheckTest", constants.logPath, constants.logLevel
            )
            constants.addMacro("with_check", "1")
        else:
            constants.addMacro("with_check", "0")

        # adding distribution rpm macro
        if constants.dist is not None:
            constants.addMacro("dist", constants.dist)

        # adding buildnumber rpm macro
        if constants.buildNumber is not None:
            constants.addMacro("photon_build_number", constants.buildNumber)

        if (
            constants.buildNumber is not None
            and constants.commonBuildNumber is not None
        ):
            constants.addMacro(
                "phvcs",
                f"{PH_COMMIT_URI_PREFIX}{constants.buildNumber};{PH_COMMIT_URI_PREFIX}{constants.commonBuildNumber}",
            )

        # adding releasenumber rpm macro
        if constants.releaseVersion is not None:
            constants.addMacro("photon_release_version", constants.releaseVersion)

        # adding releasenumber rpm macro
        if constants.subreleaseVersion is None:
            raise Exception("Photon subrelease version must be set")
        constants.addMacro("photon_subrelease", constants.subreleaseVersion)

        if constants.katBuild:
            constants.addMacro("kat_build", "1")

        if constants.canisterBuild:
            constants.addMacro("canister_build", "1")

        if constants.acvpBuild:
            constants.addMacro("acvp_build", "1")

        if constants.releasePkgPreqPath:
            with open(constants.releasePkgPreqPath, "r") as file:
                pkgPreq = json.load(file)

            constants.listCoreToolChainPackages.extend(
                pkgPreq["listCoreToolChainPackages"]
            )
            constants.listToolChainPackages.extend(pkgPreq["listToolChainPackages"])
            # Mandate coreutils-selinux in toolchain
            constants.listToolChainPackages.append("coreutils-selinux")
            constants.listToolChainRPMsToInstall.extend(
                pkgPreq["listToolChainRPMsToInstall"]
            )
            constants.providedBy = pkgPreq["providedBy"]

        from signing import addSigningMacros

        addSigningMacros()

    @staticmethod
    def setPhotonDir(phDir):
        constants.photonDir = phDir

    @staticmethod
    def addMacro(macroName, macroValue):
        constants.userDefinedMacros[macroName] = macroValue

    @staticmethod
    def setBuildOptions(options):
        constants.buildOptions = options

    @staticmethod
    def getAdditionalMacros(package):
        macros = {}
        if package in constants.buildOptions.keys():
            pkg = constants.buildOptions[package]
            for m in pkg["macros"]:
                k, v = m.split(" ", 1)
                macros[k] = v
        return macros

    @staticmethod
    def storeScriptsToCopy(key, val):
        dest = val.get("dest")
        if not dest:
            print("Empty dest value, return ...")
            return
        constants.CopyToSandboxDict[key] = deepcopy(val)

        if key == "adjust-gcc-specs":
            constants.adjustGCCSpecScript = dest
            return
        from signing import setScriptToCopy, signingMap

        if key in signingMap:
            setScriptToCopy(key, val)
            return

    @staticmethod
    def addSandboxEnv(key, val):
        constants.SandboxEnv[key] = val

    @staticmethod
    def enable_fips_in_make_check():
        # TODO: sshedi
        # install fips-proivder in sandbox during rpmcheck
        pass

    @staticmethod
    def set_resume_build(val):
        if val:
            constants.resume_build = True

    @staticmethod
    def set_rebuild(val):
        if val:
            constants.rebuild = True

    @staticmethod
    def set_observer_rules(ruleset):
        constants.observationIgnHostPatterns = [
            re.compile(patt) for patt in ruleset.get("ignored-hosts", [])
        ]

    @staticmethod
    def setPackageRepoURL(url):
        constants.packageRepoURL = url

    @staticmethod
    def setPackageRepoPath(path):
        constants.packageRepoPath = path

    @staticmethod
    def setPackageRepoSnapshotURL(path):
        constants.packageRepoSnapshotURL = path

    @staticmethod
    def setBootstrapPackageRepoPath(path):
        constants.bootstrapRepoPath = path

    @staticmethod
    def setReleaseVersionToConsume(releaseVersionToConsume):
        constants.releaseVersionToConsume = releaseVersionToConsume

    @staticmethod
    def enableToolchainBootstrap():
        constants.toolchainBootstrap = True

    @staticmethod
    def setBaseImageTarballPath(baseImagePath):
        constants.baseImagePath = baseImagePath
        constants.baseImageTarball = pathlib.PurePath(baseImagePath).name

    @staticmethod
    def setBuildImagesPath(buildImagesPath):
        constants.buildImagesPath = buildImagesPath

    @staticmethod
    def setSandboxType(sandboxType: SandboxType):
        constants.sandboxType = sandboxType
