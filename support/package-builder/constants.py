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
    pullsourcesConfig=""
    buildPatch=False
    inputRPMSPath=""
    rpmCheck=False
    noDepsPackageList=["texinfo","bzip2","gettext","man-db","nspr", "nspr-devel","xz","bison","openjdk","go"]
    listToolChainPackages=["linux-api-headers", "glibc","zlib", "file", "file-devel",
        "binutils","gmp","mpfr", "mpc","gcc", "pkg-config", "ncurses", "bash", "bzip2", "sed","procps-ng","coreutils", "m4","grep",
        "readline", "diffutils","gawk", "findutils", "gettext", "gzip","make",  "patch","util-linux", "util-linux-devel",
        "tar", "xz","libtool", "flex",  "flex-devel","bison", "lua","popt","nspr","nspr-devel","sqlite-autoconf","nss",
        "elfutils", "expat","libffi","libpipeline", "gdbm","perl","texinfo","autoconf","automake",
        "openssl","python2","rpm", "groff", "man-db", "man-pages","cpio"]
    
    listCoreToolChainRPMPackages=["linux-api-headers", "glibc","glibc-devel",  "zlib","zlib-devel",  "file", "file-devel",
        "binutils","binutils-devel",  "gmp","gmp-devel", "mpfr", "mpfr-devel", "mpc",
        "libgcc","libgcc-devel","libstdc++","libstdc++-devel","libgomp","libgomp-devel","gcc",
        "pkg-config","bash"]
    
    listToolChainRPMPkgsToInstall=["linux-api-headers", "glibc","glibc-devel",  "zlib","zlib-devel",  "file", "file-devel",
        "binutils","binutils-devel",  "gmp","gmp-devel", "mpfr", "mpfr-devel", "mpc",
        "libgcc","libgcc-devel","libstdc++","libstdc++-devel","libgomp","libgomp-devel","gcc",
        "pkg-config", "ncurses", "bash", "bzip2", "sed","procps-ng","coreutils", "m4","grep",
        "readline","diffutils","gawk", "findutils", "gettext", "gzip","make",  "patch",
        "util-linux", "util-linux-devel", "tar", "xz","libtool", "flex", "flex-devel",  "bison",
        "lua","popt","nspr", "nspr-devel","sqlite-autoconf","nss","elfutils-libelf",
        "libpipeline", "gdbm","perl","texinfo","rpm","rpm-build", "rpm-devel",
        "autoconf","automake", "groff", "man-db", "man-pages","elfutils","cpio"]

    listToolChainRPMPkgsToBuild=["linux-api-headers", "glibc","glibc-devel",  "zlib","zlib-devel",  "file", "file-devel",
            "binutils","binutils-devel",  "gmp","gmp-devel", "mpfr", "mpfr-devel", "mpc",
            "libgcc","libgcc-devel","libstdc++","libstdc++-devel","libgomp","libgomp-devel","gcc",
            "pkg-config", "ncurses", "bash", "bzip2", "sed","ncurses-devel","procps-ng","coreutils", "m4","grep",
            "readline", "diffutils","gawk", "findutils", "gettext", "gzip","make",  "patch",
            "util-linux", "util-linux-devel", "tar", "xz","libtool", "flex",  "flex-devel","bison",
            "readline-devel", "lua","lua-devel","popt","popt-devel","nspr","nspr-devel","sqlite-autoconf","nss","nss-devel",
            "bzip2-devel","elfutils-libelf","elfutils","elfutils-libelf-devel","elfutils-devel",
            "expat","libffi","libpipeline", "gdbm","perl","texinfo","autoconf","automake",
            "openssl","openssl-devel","python2","python2-libs","python2-devel","rpm","rpm-build", "rpm-devel",
            "groff", "man-db", "man-pages","cpio"]
    
    
    @staticmethod
    def initialize(options):
        constants.dist = options.dist
        constants.buildNumber = options.buildNumber
        constants.releaseVersion = options.releaseVersion
        constants.specPath = options.specPath
        constants.sourcePath = options.sourcePath
        constants.rpmPath = options.rpmPath
        constants.topDirPath = options.topDirPath
        constants.logPath = options.logPath
        constants.prevPublishRPMRepo=options.publishRPMSPath
        constants.buildRootPath=options.buildRootPath
        constants.specData = SerializableSpecObjectsUtils(constants.logPath)
        constants.specData.readSpecsAndConvertToSerializableObjects(constants.specPath)
        constants.pullsourcesConfig = options.pullsourcesConfig
        constants.inputRPMSPath=options.inputRPMSPath
        constants.rpmCheck = options.rpmCheck
        

        
        
    
