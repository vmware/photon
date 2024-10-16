#!/usr/bin/env/ python3

import platform

from copy import deepcopy
from Logger import Logger
from CommandUtils import CommandUtils as cmdUtils


class constants(object):
    specPath = ""
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
    releaseVersion = None
    katBuild = False
    canisterBuild = False
    acvpBuild = False
    testForceRPMS = []
    tmpDirPath = "/dev/shm"
    buildOptions = {}
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
    CopyToSandboxDict = {}

    noDepsPackageList = [
        "texinfo",
        "bzip2",
        "bzip2-libs",
        "gettext",
        "gettext-libs",
        "gettext-devel",
        "nspr",
        "bison",
        "go",
        "sqlite",
        "sqlite-devel",
        "sqlite-libs",
    ]

    # These packages will be built in first order as build-core-toolchain stage
    # Put only main pakage names here. Do not add subpackages such as libgcc
    listCoreToolChainPackages = [
        "filesystem",
        "linux-api-headers",
        "glibc",
        "glibc-libs",
        "libxcrypt",
        "zlib",
        "file",
        "binutils",
        "gmp",
        "mpfr",
        "mpc",
        "mpc-devel",
        "gcc",
        "pkg-config",
        "ncurses",
        "readline",
        "bash",
    ]

    # These packages will be built in a second stage to replace publish RPMS
    # Put only main pakage names here. Do not add subpackages such as libgcc
    listToolChainPackages = [
        "filesystem",
        "linux-api-headers",
        "glibc",
        "zlib",
        "file",
        "binutils",
        "gmp",
        "libselinux",
        "mpfr",
        "mpc",
        "gcc",
        "pkg-config",
        "ncurses",
        "bash",
        "bzip2",
        "sed",
        "procps-ng",
        "coreutils",
        "m4",
        "grep",
        "readline",
        "diffutils",
        "gawk",
        "findutils",
        "gettext",
        "gzip",
        "make",
        "patch",
        "util-linux",
        "attr",
        "libacl",
        "tar",
        "xz",
        "libtool",
        "flex",
        "bison",
        "popt",
        "nspr",
        "sqlite",
        "nss",
        "elfutils",
        "expat",
        "libffi",
        "libpipeline",
        "gdbm",
        "perl",
        "texinfo",
        "autoconf",
        "automake",
        "openssl",
        "zstd",
        "rpm",
        "dwz",
        "debugedit",
        "pandoc-bin",
        "help2man",
        "pcre",
        "pcre2",
    ]

    # List or RPMS that will be installed in a chroot prior to build each
    # package. This list should be ordered by install order. On a stage1
    # and stage2 published rpms will/might be used after stage2 only local
    # RPMS will be used
    listToolChainRPMsToInstall = [
        "filesystem",
        "linux-api-headers",
        "glibc",
        "glibc-libs",
        "glibc-devel",
        "glibc-iconv",
        "glibc-tools",
        "libxcrypt",
        "libxcrypt-devel",
        "zlib",
        "zlib-devel",
        "file-libs",
        "file",
        "binutils",
        "binutils-libs",
        "binutils-devel",
        "gmp",
        "gmp-devel",
        "libselinux",
        "mpfr",
        "mpfr-devel",
        "mpc",
        "mpc-devel",
        "libgcc",
        "libgcc-devel",
        "libgcc-atomic",
        "libstdc++",
        "libstdc++-devel",
        "libgomp",
        "libgomp-devel",
        "gcc",
        "pkg-config",
        "ncurses",
        "ncurses-libs",
        "ncurses-devel",
        "ncurses-terminfo",
        "bash",
        "bzip2",
        "bzip2-libs",
        "bzip2-devel",
        "sed",
        "procps-ng",
        "coreutils",
        "m4",
        "grep",
        "readline",
        "diffutils",
        "gawk",
        "findutils",
        "gettext",
        "gettext-libs",
        "gettext-devel",
        "gzip",
        "make",
        "patch",
        "util-linux",
        "util-linux-libs",
        "util-linux-devel",
        "attr",
        "libacl",
        "tar",
        "xz",
        "xz-libs",
        "libtool",
        "flex",
        "flex-devel",
        "readline-devel",
        "popt",
        "popt-devel",
        "nspr",
        "nspr-devel",
        "sqlite",
        "sqlite-libs",
        "nss",
        "nss-libs",
        "nss-devel",
        "elfutils-libelf",
        "elfutils",
        "elfutils-libelf-devel",
        "elfutils-devel",
        "expat",
        "expat-libs",
        "libffi",
        "libpipeline",
        "gdbm",
        "perl",
        "texinfo",
        "autoconf",
        "automake",
        "openssl",
        "openssl-libs",
        "openssl-devel",
        "libcap",
        "zstd",
        "zstd-libs",
        "zstd-devel",
        "lua",
        "lua-libs",
        "lua-devel",
        "rpm",
        "rpm-build",
        "rpm-devel",
        "rpm-libs",
        "rpm-build-libs",
        "rpm-sign-libs",
        "cpio",
        "debugedit",
        "pcre-libs",
        "pcre2",
        "pcre2-libs",
        "pcre2-devel",
    ]

    # List of packages that will be installed in addition for each
    # package to make check
    listMakeCheckRPMPkgtoInstall = [
        "python3",
        "python3-devel",
        "python3-libs",
        "python3-tools",
        "python3-PyYAML",
        "libyaml",
        "libffi",
        "python3-setuptools",
        "ca-certificates",
        "linux",
        "createrepo_c",
        "sudo",
        "ruby",
        "curl",
        "pcre-devel",
        "boost-devel",
        "which",
        "go",
        "e2fsprogs-devel",
        "shadow",
        "check",
        "libacl-devel",
        "device-mapper",
        "wget",
        "attr",
        "libacl",
        "tar",
        "pkg-config",
        "git",
        "openssl",
        "openssl-libs",
        "openssl-devel",
        "net-tools",
        "less",
        "iana-etc",
        "rpm-devel",
        "rpm",
        "libxml2",
        "python3-xml",
        "libacl",
        "tzdata",
        "Linux-PAM",
        "unzip",
        "systemd-devel",
        "gnupg",
        "ncurses-terminfo",
    ]

    """
    List of packages that requires privileged docker
    to run make check.
    """
    listReqPrivilegedDockerForTest = [
        "elfutils",  # SYS_PTRACE
        "gdb",
        "glibc",
        "glibc-libs",
        "attr",
        "libacl",
        "tar",
    ]

    """
    List of Packages which causes "Makecheck" job
    to stuck indefinately or getting failed.
    Until these pkgs %check is fixed, these pkgs will be
    skip to run makecheck.
    """
    listMakeCheckPkgToSkip = [
        "gtk-doc",
        "libmspack",
        "socat",
        "bash",
        "libical",
    ]

    """
    .spec file might contain lines such as
    Requires(post):/sbin/useradd
    Build system should interpret it as
    Requires: shadow
    """
    providedBy = {
        "/usr/sbin/useradd": "shadow",
        "/usr/sbin/userdel": "shadow",
        "/usr/sbin/groupadd": "shadow",
        "/sbin/service": "initscripts",
        "/usr/bin/which": "which",
        "/usr/bin/python": "python3",
        "/bin/python": "python3",
        "/bin/python3": "python3",
        "/bin/awk": "gawk",
        "/bin/gawk": "gawk",
        "/bin/sed": "sed",
        "/bin/grep": "grep",
        "/bin/sh": "bash",
        "/bin/bash": "bash",
        "/bin/zsh": "zsh",
        "/bin/tcsh": "tcsh",
        "/bin/csh": "csh",
        "/bin/perl": "perl",
        "/bin/mergerepo": "createrepo_c",
        "/bin/modifyrepo": "createrepo_c",
        "/usr/bin/false": "coreutils",
        "/usr/bin/ln": "coreutils",
        "/usr/bin/chown": "coreutils",
        "/usr/bin/cp": "coreutils",
        "/usr/bin/rm": "coreutils",
        "/usr/bin/mv": "coreutils",
        "/sbin/ldconfig": "glibc",
        "/usr/bin/containerd-shim-runc-v2": "containerd-extras",
        "jre":"openjdk11"
    }

    @staticmethod
    def setSpecPath(specPath):
        constants.specPath = specPath

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

        # adding releasenumber rpm macro
        if constants.releaseVersion is not None:
            constants.addMacro(
                "photon_release_version", constants.releaseVersion
            )

        if constants.katBuild:
            constants.addMacro("kat_build", "1")

        if constants.canisterBuild:
            constants.addMacro("canister_build", "1")

        if constants.acvpBuild:
            constants.addMacro("acvp_build", "1")

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
            _, _, retval = cmdUtils.runBashCmd(cmd, ignore_rc=True)
            if retval:
                constants.hostRpmIsNotUsable = 1
                break

        if constants.hostRpmIsNotUsable < 0:
            constants.hostRpmIsNotUsable = 0

        return constants.hostRpmIsNotUsable

    def enable_fips_in_make_check():
        constants.listMakeCheckRPMPkgtoInstall.append("openssl-fips-provider")

    def set_resume_build(val):
        if val:
            constants.resume_build = True
