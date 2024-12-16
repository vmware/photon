#!/usr/bin/env/ python3

import json
import os.path
import platform

from copy import deepcopy
from Logger import Logger
from CommandUtils import CommandUtils as cmdUtils

PH_COMMIT_URI_PREFIX = "https://github.com/vmware/photon/commit/"


class constants(object):
    specPaths = []
    gitSourcePath = ""
    stagePath = ""
    sourcePath = ""
    rpmPath = ""
    logPath = ""
    logLevel = "info"
    topDirPath = ""
    buildRootPath = "/mnt"
    prevPublishRPMRepo = ""
    prevPublishXRPMRepo = ""
    publishrpmurl = ""
    publishXrpmurl = ""
    pullsourcesURL = ""
    extrasourcesURLs = {}
    buildPatch = False
    inputRPMSPath = ""
    rpmCheck = False
    startSchedulerServer = False
    sourceRpmPath = ""
    publishBuildDependencies = False
    packageWeightsPath = None
    dockerUnixSocket = "/var/run/docker.sock"
    buildContainerImage = "photon_build_container:latest"
    userDefinedMacros = {}
    dist = None
    buildNumber = None
    commonBuildNumber = None
    releaseVersion = None
    katBuild = False
    canisterBuild = False
    acvpBuild = False
    testForceRPMS = []
    tmpDirPath = "/dev/shm"
    buildOptions = {}
    srpcli = None
    observerDockerImage = None
    isolatedDockerNetwork = None
    # will be extended later from listMakeCheckRPMPkgtoInstall
    listMakeCheckRPMPkgWithVersionstoInstall = None
    buildArch = platform.machine()
    targetArch = platform.machine()
    crossCompiling = False
    currentArch = buildArch
    hostRpmIsNotUsable = -1
    phBuilderTag = ""
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
    srpSigningScript = {}
    srpSigningParams = {}
    srpSigningAuth = {}

    # Update to below constants lists will be provided by release branch as pkgPreq data
    noDepsPackageList = []

    # These packages will be built in first order as build-core-toolchain stage
    # Put only main pakage names here. Do not add subpackages such as libgcc
    listCoreToolChainPackages = []

    # These packages will be built in a second stage to replace publish RPMS
    # Put only main pakage names here. Do not add subpackages such as libgcc
    listToolChainPackages = []

    # List or RPMS that will be installed in a chroot prior to build each
    # package. This list should be ordered by install order. On a stage1
    # and stage2 published rpms will/might be used after stage2 only local
    # RPMS will be used
    listToolChainRPMsToInstall = []

    # List of packages that will be installed in addition for each
    # package to make check
    listMakeCheckRPMPkgtoInstall = []

    """
    List of packages that requires privileged docker
    to run make check.
    """
    listReqPrivilegedDockerForTest = []

    """
    List of Packages which causes "Makecheck" job
    to stuck indefinately or getting failed.
    Until these pkgs %check is fixed, these pkgs will be
    skip to run makecheck.
    """
    listMakeCheckPkgToSkip = []

    """
    .spec file might contain lines such as
    Requires(post):/sbin/useradd
    Build system should interpret it as
    Requires: shadow
    """
    providedBy = ""

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
    def setGitSourcePath(gitSourcePath):
        constants.gitSourcePath = gitSourcePath

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
    def setPublishRpmURL(url):
        constants.publishrpmurl = url

    @staticmethod
    def setPublishXRpmURL(url):
        constants.publishXrpmurl = url

    @staticmethod
    def setPrevPublishRPMRepo(prevPublishRPMRepo):
        constants.prevPublishRPMRepo = prevPublishRPMRepo

    @staticmethod
    def setPrevPublishXRPMRepo(prevPublishXRPMRepo):
        constants.prevPublishXRPMRepo = prevPublishXRPMRepo

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
    def setInputRPMSPath(inputRPMSPath):
        constants.inputRPMSPath = inputRPMSPath

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
    def setPublishBuildDependencies(publishBuildDependencies):
        constants.publishBuildDependencies = publishBuildDependencies

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
                f"{PH_COMMIT_URI_PREFIX}{constants.buildNumber}\;{PH_COMMIT_URI_PREFIX}{constants.commonBuildNumber}",
            )

        # adding releasenumber rpm macro
        if constants.releaseVersion is not None:
            constants.addMacro("photon_release_version", constants.releaseVersion)

        if constants.katBuild:
            constants.addMacro("kat_build", "1")

        if constants.canisterBuild:
            constants.addMacro("canister_build", "1")

        if constants.acvpBuild:
            constants.addMacro("acvp_build", "1")

        if constants.releasePkgPreqPath:
            with open(constants.releasePkgPreqPath, "r") as file:
                pkgPreq = json.load(file)
            constants.noDepsPackageList.extend(pkgPreq["noDepsPackageList"])
            constants.listCoreToolChainPackages.extend(
                pkgPreq["listCoreToolChainPackages"]
            )
            constants.listToolChainPackages.extend(pkgPreq["listToolChainPackages"])
            constants.listToolChainRPMsToInstall.extend(
                pkgPreq["listToolChainRPMsToInstall"]
            )
            constants.listMakeCheckRPMPkgtoInstall.extend(
                pkgPreq["listMakeCheckRPMPkgtoInstall"]
            )
            constants.listReqPrivilegedDockerForTest.extend(
                pkgPreq["listReqPrivilegedDockerForTest"]
            )
            constants.listMakeCheckPkgToSkip.extend(pkgPreq["listMakeCheckPkgToSkip"])
            constants.providedBy = pkgPreq["providedBy"]

        if constants.srpSigningScript:
            constants.addMacro("signing_script", constants.srpSigningScript["dest"])
        if constants.srpSigningParams:
            constants.addMacro("signing_params", constants.srpSigningParams["dest"])
        if constants.srpSigningAuth:
            constants.addMacro("signing_auth", constants.srpSigningAuth["dest"])

    @staticmethod
    def setTestForceRPMS(listsPackages):
        constants.testForceRPMS = listsPackages

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
        constants.CopyToSandboxDict[key] = deepcopy(val)
        if key == "adjust-gcc-specs":
            constants.adjustGCCSpecScript = val["dest"]
        if key == "srp-signing-script":
            constants.srpSigningScript["src"] = val["src"]
            constants.srpSigningScript["dest"] = val["dest"]
        if key == "srp-signing-params":
            constants.srpSigningParams["src"] = val["src"]
            constants.srpSigningParams["dest"] = val["dest"]
        if key == "srp-signing-auth":
            constants.srpSigningAuth["src"] = val["src"]
            constants.srpSigningAuth["dest"] = val["dest"]

    @staticmethod
    def addSandboxEnv(key, val):
        constants.SandboxEnv[key] = val

    @staticmethod
    def checkIfHostRpmNotUsable():
        if constants.hostRpmIsNotUsable >= 0:
            return constants.hostRpmIsNotUsable

        # if rpm doesn't have zstd support
        # if host rpm doesn't support sqlite backend db
        cmds = [
            "rpm --showrc | grep -qw 'rpmlib(PayloadIsZstd)'",
            "rpm -E %{_db_backend} | grep -qw 'sqlite'",
            "rpm -E %{_dbpath} | grep -qw '/usr/lib/sysimage/rpm'",
        ]

        for cmd in cmds:
            _, _, retval = cmdUtils.runCmd(cmd, shell=True, ignore_rc=True)
            if retval != 0:
                constants.hostRpmIsNotUsable = 1
                break

        if constants.hostRpmIsNotUsable < 0:
            constants.hostRpmIsNotUsable = 0

        return constants.hostRpmIsNotUsable

    def enable_fips_in_make_check():
        constants.listMakeCheckRPMPkgtoInstall.append("openssl-fips-provider")

    @staticmethod
    def set_resume_build(val):
        if val:
            constants.resume_build = True
