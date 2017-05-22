from SpecData import SerializableSpecObjectsUtils

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
    noDepsPackageList=["texinfo","bzip2","gettext","nspr","xz","bison","openjdk","go"]
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
        "libstdc++",
        "libstdc++-devel",
        "libgomp",
        "libgomp-devel",
        "gcc",
        "pkg-config",
        "ncurses",
        "readline",
        "bash"]

    # List of X library RPMS that will be installed in a chroot prior to build openjdk & openjre package. 
    listToolChainXRPMsToInstall=[
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
        "libXrender-devel"
	]

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
		"go"]

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
        constants.specData = SerializableSpecObjectsUtils(constants.logPath)
        constants.specData.readSpecsAndConvertToSerializableObjects(constants.specPath)
        constants.pullsourcesConfig = options.pullsourcesConfig
        constants.inputRPMSPath=options.inputRPMSPath
        constants.rpmCheck = options.rpmCheck
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

        #adding kernelrelease rpm macro
        kernelrelease = constants.specData.getRelease("linux")
        constants.specData.addMacro("KERNEL_RELEASE",kernelrelease)
       
	#adding openjre8 version rpm macro
        java8version = constants.specData.getVersion("openjre8")
        constants.specData.addMacro("JAVA_VERSION",java8version)

        #adding kernelsubrelease rpm macro
        kernelversion = kernelversion.replace(".","")
        if kernelversion.isdigit():
            kernelversion = int(kernelversion) << 8
        kernelsubrelease = str(kernelversion)+kernelrelease
        kernelsubrelease = kernelsubrelease.replace(constants.dist,"")
        if kernelsubrelease:
            kernelsubrelease = "."+kernelsubrelease
            constants.specData.addMacro("kernelsubrelease",kernelsubrelease) 
