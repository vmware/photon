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
    pullsourcesConfig=""
    buildPatch=False
    inputRPMSPath=""
    rpmCheck=False
    sourceRpmPath=""
    noDepsPackageList=["texinfo","bzip2","gettext","nspr","xz","bison","openjdk","go"]

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
        "python2",
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
        "bash",
        "bzip2",
        "bzip2-libs",
        "bzip2-devel",
        "sed",
        "ncurses-devel",
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
        "rpm",
        "rpm-build",
        "rpm-devel",
        "rpm-libs",
        "groff",
        "man-pages",
        "cpio",
        "go"]

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
        "libffi",
        "python-setuptools",
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
        "rpm-devel",
        "rpm",
        "libxml2",
        "python-xml",
        "libacl",
        "tzdata",
        "libgcrypt-devel",
        "Linux-PAM",
        "unzip"]

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
        constants.prevPublishRPMRepo=options.publishRPMSPath
        constants.buildRootPath=options.buildRootPath
        constants.specData = SerializableSpecObjectsUtils(constants.logPath)
        constants.specData.readSpecsAndConvertToSerializableObjects(constants.specPath)
        constants.pullsourcesConfig = options.pullsourcesConfig
        constants.inputRPMSPath=options.inputRPMSPath
        constants.updateRPMMacros()
        constants.testForceRPMS=[]
        constants.rpmCheck = options.rpmCheck
        constants.rpmCheckStopOnError = options.rpmCheckStopOnError
        if constants.rpmCheck:
            constants.testLogger=Logger.getLogger("MakeCheckTest",constants.logPath)

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

        #adding kernelrelease rpm macro
        kernelrelease = constants.specData.getRelease("linux")
        constants.specData.addMacro("KERNEL_RELEASE",kernelrelease)
        
        #adding kernelsubrelease rpm macro
        kernelversion = kernelversion.replace(".","")
        if kernelversion.isdigit():
            kernelversion = int(kernelversion) << 8
        kernelsubrelease = str(kernelversion)+kernelrelease
        kernelsubrelease = kernelsubrelease.replace(constants.dist,"")
        if kernelsubrelease:
            kernelsubrelease = "."+kernelsubrelease
            constants.specData.addMacro("kernelsubrelease",kernelsubrelease)

    @staticmethod
    def setTestForceRPMS(listsPackages):
         constants.testForceRPMS=listsPackages
