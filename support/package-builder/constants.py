from SpecData import SerializableSpecObjectsUtils
from Logger import Logger

class constants(object):
    specPath=""
    sourcePath=""
    rpmPath=""
    logPath=""
    dist=""
    buildNumber="0000000"
    releaseVersion="NNNnNNN"
    topDirPath=""
    specData=None
    buildRootPath="/mnt"
    prevPublishRPMRepo=""
    prevPublishXRPMRepo=""
    pullsourcesConfig=""
    buildPatch=False
    inputRPMSPath=""
    rpmCheck=False
    sourceRpmPath=""
    publishBuildDependencies=False
    packageWeightsPath=None

    noDepsPackageList=[
        "texinfo",
        "bzip2",
        "bzip2-libs",
        "gettext",
        "nspr",
        "xz",
        "bison",
        "go",
        "sqlite",
        "sqlite-devel",
        "sqlite-libs"]

    # These packages will be built in first order as build-core-toolchain stage
    listCoreToolChainPackages=[
        "filesystem",
        "linux-api-headers",
        "glibc",
        "zlib",
        "file",
        "binutils",
        "gmp",
        "mpfr",
        "mpc",
        "libgcc",
        "libstdc++",
        "libgomp",
        "gcc",
        "pkg-config",
        "ncurses",
        "readline",
        "bash"]

    # These packages will be built in a second stage to replace publish RPMS
    listToolChainPackages=[
        "filesystem",
        "linux-api-headers",
        "glibc",
        "zlib",
        "file",
        "binutils",
        "gmp",
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
        "tar",
        "xz",
        "libtool",
        "flex",
        "bison",
        "lua",
        "popt",
        "nspr",
        "nspr-devel",
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
        "openssl-devel",
        "python2",
        "libdb",
        "rpm",
        "groff",
        "man-pages",
        "cpio"]

    # List or RPMS that will be installed in a chroot prior to build each
    # package. On a stage1 and stage2 published rpms will/might be used
    # after stage2 only local RPMS will be used
    listToolChainRPMsToInstall=[
        "filesystem",
        "linux-api-headers",
        "glibc",
        "glibc-devel",
        "glibc-iconv",
        "glibc-tools",
        "zlib",
        "zlib-devel",
        "file",
        "binutils",
        "binutils-devel",
        "gmp",
        "gmp-devel",
        "mpfr",
        "mpfr-devel",
        "mpc",
        "libgcc",
        "libgcc-devel",
        "libstdc++",
        "libstdc++-devel",
        "libgomp",
        "libgomp-devel",
        "gcc",
        "pkg-config",
        "ncurses",
        "ncurses-libs",
        "ncurses-devel",
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
        "gzip",
        "make",
        "patch",
        "util-linux",
        "util-linux-libs",
        "util-linux-devel",
        "tar",
        "xz",
        "xz-libs",
        "libtool",
        "flex",
        "flex-devel",
        "bison",
        "readline-devel",
        "lua",
        "lua-devel",
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
        "openssl-devel",
        "python2",
        "python2-libs",
        "python2-devel",
        "libcap",
        "libdb",
        "libdb-devel",
        "rpm",
        "rpm-build",
        "rpm-devel",
        "rpm-libs",
        "groff",
        "man-pages",
        "cpio",
        "go"]

    perPackageToolChain = dict.fromkeys(["openjdk8", "openjdk8-doc", "openjdk8-src", "openjdk8-sample", "openjre8" ], [
        "glib-devel",
        "icu-devel",
        "openjdk",
        "openjre",
        "icu",
        "harfbuzz",
        "harfbuzz-devel",
        "freetype2",
        "freetype2-devel",
        "alsa-lib",
        "alsa-lib-devel",
        "xcb-proto",
        "libXdmcp-devel",
        "libXau-devel",
        "util-macros",
        "xtrans",
        "libxcb-devel",
        "fontconfig-devel",
        "proto",
        "libXdmcp",
        "libxcb",
        "libXau",
        "fontconfig",
        "xtrans-devel",
        "libX11",
        "libX11-devel",
        "libXext",
        "libXext-devel",
        "libICE-devel",
        "libSM",
        "libICE",
        "libSM-devel",
        "libXt",
        "libXmu",
        "libXt-devel",
        "libXmu-devel",
        "libXrender",
        "libXrender-devel"])
    perPackageToolChain["apache-maven"] = ["apache-maven"]
    # List of RPMs which are not published. They will be created during the
    # build process
    listOfRPMsProvidedAfterBuild=[
        "util-linux-devel",
        "flex-devel",
        "nspr-devel",
        "glibc-iconv",
        "glibc-tools",
        "bzip2-libs",
        "expat-libs",
        "ncurses-libs",
        "util-linux-libs",
        "nss-libs",
        "xz-libs",
        "sqlite",
        "sqlite-libs",
        "rpm-libs"]

    # List of packages that will be installed in addition for each
    # package to make check
    listMakeCheckRPMPkgtoInstall=[
        "python2",
        "python2-devel",
        "python2-libs",
        "python2-tools",
        "PyYAML",
        "libyaml",
        "libffi",
        "python-setuptools",
        "python3-setuptools",
        "ca-certificates",
        "linux",
        "createrepo",
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
        "tar",
        "pkg-config",
        "git",
        "openssl",
        "openssl-devel",
        "net-tools",
        "less",
        "iana-etc",
        "yum-metadata-parser",
        "yum",
        "libdb",
        "rpm-devel",
        "rpm",
        "libxml2",
        "python-xml",
        "python3-xml",
        "libacl",
        "tzdata",
        "libgcrypt-devel",
        "Linux-PAM",
        "unzip",
        "systemd-devel",
        "gnupg",
        "ncurses-terminfo" ]

    listReInstallPackages=[
        "go"]

    @staticmethod
    def initialize(options):
        constants.dist = options.dist
        constants.buildNumber = options.buildNumber
        constants.releaseVersion = options.releaseVersion
        constants.specPath = options.specPath
        constants.sourcePath = options.sourcePath
        constants.rpmPath = options.rpmPath
        constants.sourceRpmPath = options.sourceRpmPath
        constants.topDirPath = options.topDirPath
        constants.logPath = options.logPath
        constants.prevPublishRPMRepo = options.publishRPMSPath
        constants.prevPublishXRPMRepo = options.publishXRPMSPath
        constants.buildRootPath=options.buildRootPath
        constants.specData = SerializableSpecObjectsUtils(constants.logPath)
        constants.specData.readSpecsAndConvertToSerializableObjects(constants.specPath)
        constants.pullsourcesConfig = options.pullsourcesConfig
        constants.inputRPMSPath=options.inputRPMSPath
        constants.testForceRPMS=[]
        constants.rpmCheck = options.rpmCheck
        constants.rpmCheckStopOnError = options.rpmCheckStopOnError
        constants.publishBuildDependencies=options.publishBuildDependencies
        constants.packageWeightsPath=options.packageWeightsPath
        if constants.rpmCheck:
            constants.testLogger=Logger.getLogger("MakeCheckTest",constants.logPath)
        constants.updateRPMMacros()

    @staticmethod
    def updateRPMMacros():
        #adding distribution rpm macro
        constants.specData.addMacro("dist",constants.dist)

        #adding buildnumber rpm macro
        constants.specData.addMacro("photon_build_number",constants.buildNumber)

        #adding releasenumber rpm macro
        constants.specData.addMacro("photon_release_version",constants.releaseVersion)

        #adding kernelversion rpm macro
        kernelversion = constants.specData.getVersion("linux")
        constants.specData.addMacro("KERNEL_VERSION",kernelversion)

        #adding openjre8 version rpm macro
        java8version = constants.specData.getVersion("openjre8")
        constants.specData.addMacro("JAVA8_VERSION",java8version)

        #adding kernelrelease rpm macro
        kernelrelease = constants.specData.getRelease("linux")
        constants.specData.addMacro("KERNEL_RELEASE",kernelrelease)

        #adding kernelsubrelease rpm macro
        a,b,c = kernelversion.split(".")
        kernelsubrelease = '%02d%02d%03d%03d' % (int(a),int(b),int(c),int(kernelrelease.replace(constants.dist,"")))
        if kernelsubrelease:
            kernelsubrelease = "."+kernelsubrelease
            constants.specData.addMacro("kernelsubrelease",kernelsubrelease)

        #adding check rpm macro
        if constants.rpmCheck:
            constants.specData.addMacro("with_check","1")
        else:
            constants.specData.addMacro("with_check","0")

    @staticmethod
    def setTestForceRPMS(listsPackages):
         constants.testForceRPMS=listsPackages
