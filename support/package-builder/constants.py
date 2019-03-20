from SpecData import SerializableSpecObjectsUtils
from SpecUtils import Specutils

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
    noDepsPackageList=["texinfo","bzip2","gettext","nspr","xz","bison","go"]
    publishBuildDependencies=False
    packageWeightsPath=None
    listToolChainPackages=[
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
        "util-linux-devel",
        "tar",
        "xz",
        "libtool",
        "flex",
        "flex-devel",
        "bison",
        "lua",
        "popt",
        "nspr",
        "sqlite-autoconf",
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

    listCoreToolChainRPMPackages=[
        "linux-api-headers",
        "glibc",
        "glibc-devel",
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
        "libgcc-atomic",
        "libstdc++",
        "libstdc++-devel",
        "libgomp",
        "libgomp-devel",
        "gcc",
        "pkg-config",
        "ncurses",
        "readline",
        "bash",
        "vim"]

    # List of X library RPMS that will be installed in a chroot prior to build openjdk & openjre package. 
    listToolChainXRPMsToInstall=[
        "glib-devel",
        "icu-devel",
        "openjdk",
        "openjre",
        "icu",
        "cups",
        "cups-devel",
        "freetype2",
        "freetype2-devel",
        "xorg-proto-devel",
        "libXtst",
        "libXtst-devel",
        "libXfixes",
        "libXfixes-devel",
        "libXi",
        "libXi-devel",
        "harfbuzz",
        "harfbuzz-devel",
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
        "libXrender-devel"]

    listToolChainRPMPkgsToInstall=[
        "linux-api-headers",
        "glibc",
        "glibc-devel",
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
        "libgcc-atomic",
        "libstdc++",
        "libstdc++-devel",
        "libgomp",
        "libgomp-devel",
        "gcc",
        "pkg-config",
        "ncurses",
        "bash",
        "bzip2",
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
        "util-linux-devel",
        "tar",
        "xz",
        "libtool",
        "flex",
        "flex-devel",
        "bison",
        "lua",
        "popt",
        "nspr",
        "sqlite-autoconf",
        "nss",
        "elfutils-libelf",
        "libpipeline",
        "gdbm",
        "perl",
        "texinfo",
        "libcap",
        "rpm",
        "rpm-build",
        "rpm-devel",
        "autoconf",
        "automake",
        "groff",
        "man-pages",
        "elfutils",
        "cpio",
        "go",
        "expat",
        "libffi",
        "openssl",
        "openssl-devel",
        "python2",
        "python2-libs",
        "python2-devel"]

    listToolChainRPMPkgsToBuild=[
        "linux-api-headers",
        "glibc",
        "glibc-devel",
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
        "libgcc-atomic",
        "libstdc++",
        "libstdc++-devel",
        "libgomp",
        "libgomp-devel",
        "gcc",
        "pkg-config",
        "ncurses",
        "bash",
        "bzip2",
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
        "sqlite-autoconf",
        "nss",
        "nss-devel",
        "bzip2-devel",
        "elfutils-libelf",
        "elfutils",
        "elfutils-libelf-devel",
        "elfutils-devel",
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
        "python2-libs",
        "python2-devel",
        "libcap",
        "rpm",
        "rpm-build",
        "rpm-devel",
        "groff",
        "man-pages",
        "cpio"]


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
        constants.prevPublishXRPMRepo = options.publishXRPMSPath
        constants.buildRootPath=options.buildRootPath
        constants.pullsourcesConfig = options.pullsourcesConfig
        constants.inputRPMSPath=options.inputRPMSPath
        constants.rpmCheck = options.rpmCheck
        constants.packageWeightsPath=options.packageWeightsPath
        constants.publishBuildDependencies=options.publishBuildDependencies
        constants.specData = SerializableSpecObjectsUtils(constants.logPath)
        constants.updateRPMMacros(options)
        # Perform full parsing now
        constants.specData.readSpecsAndConvertToSerializableObjects(constants.specPath)
        
    @staticmethod
    def updateRPMMacros(options):
        if options.katBuild != None:
            constants.specData.addMacro("kat_build", options.katBuild)

        #adding distribution rpm macro
        constants.specData.addMacro("dist",constants.dist)

        #adding buildnumber rpm macro
        constants.specData.addMacro("photon_build_number",constants.buildNumber)

        #adding releasenumber rpm macro
        constants.specData.addMacro("photon_release_version",constants.releaseVersion)

        #adding check rpm macro
        constants.specData.addMacro("with_check","0")

	#adding openjre version rpm macro
        spec = Specutils(constants.specPath + "/openjdk/openjdk.spec")
        javaversion = spec.getVersion()
        constants.specData.addMacro("JAVA_VERSION",javaversion)

	#adding openjre 9 version rpm macro
        spec = Specutils(constants.specPath + "/openjdk9/openjdk9.spec")
        javaversion9 = spec.getVersion()
        constants.specData.addMacro("JAVA_VERSION_9",javaversion9)

	#adding openjre 10 version rpm macro
        spec = Specutils(constants.specPath + "/openjdk10/openjdk10.spec")
        javaversion10 = spec.getVersion()
        constants.specData.addMacro("JAVA_VERSION_10",javaversion10)
        
        #adding kernelversion rpm macro
        spec = Specutils(constants.specPath + "/linux/linux.spec")
        kernelversion = spec.getVersion()
        constants.specData.addMacro("KERNEL_VERSION",kernelversion)

        #adding kernelrelease rpm macro
        kernelrelease = spec.getRelease()
        constants.specData.addMacro("KERNEL_RELEASE",kernelrelease)
       
        #adding kernelsubrelease rpm macro
        kernelversion = kernelversion.replace(".","")
        if kernelversion.isdigit():
            kernelversion = int(kernelversion) << 8
        kernelsubrelease = str(kernelversion)+kernelrelease.split('.')[0]
        if kernelsubrelease:
            kernelsubrelease = "."+kernelsubrelease
            constants.specData.addMacro("kernelsubrelease",kernelsubrelease) 

