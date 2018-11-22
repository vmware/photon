from Logger import Logger

class constants(object):
    specPath=""
    sourcePath=""
    rpmPath=""
    logPath=""
    topDirPath=""
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
    userDefinedMacros={}

    noDepsPackageList=[
        "texinfo",
        "bzip2",
        "bzip2-libs",
        "gettext",
        "nspr",
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
    # package. This list should be ordered by install order. On a stage1
    # and stage2 published rpms will/might be used after stage2 only local
    # RPMS will be used
    listToolChainRPMsToInstall=[
        "filesystem",
        "linux-api-headers",
        "glibc",
        "glibc-devel",
        "glibc-iconv",
        "glibc-tools",
        "zlib",
        "zlib-devel",
        "file-libs",
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

    perPackageToolChain = dict.fromkeys(["openjdk8", "openjdk8-doc", "openjdk8-src", "openjdk8-sample", "openjre8", "openjdk9", "openjdk9-doc", "openjdk9-src", "openjdk9-sample", "openjre9", "openjdk10", "openjdk10-doc", "openjdk10-src", "openjdk10-sample", "openjre10" ], [
        "glib-devel",
        "icu-devel",
        "openjdk",
        "openjre",
        "icu",
        "cups",
        "cups-devel",
        "xorg-proto-devel",
        "libXtst",
        "libXtst-devel",
        "libXfixes",
        "libXfixes-devel",
        "libXi",
        "libXi-devel",
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
        "file-libs",
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

    # List of packages that requires privileged docker
    # to run make check.
    listReqPrivilegedDockerForTest=[
        "elfutils", # SYS_PTRACE
        "gdb",
        "glibc",
        "tar"]

    # .spec file might contain lines such as
    # Requires(post):/sbin/useradd
    # Build system should interpret it as
    # Requires: shadow
    providedBy={
        "/usr/sbin/useradd":"shadow",
        "/usr/sbin/groupadd":"shadow",
        "/usr/bin/which":"which",
        "/bin/sed":"sed"
    }

    # list of spec files to skip for parsing for given arch
    skipSpecsForArch={
        "x86_64":[
            "docker-volume-vsphere.spec"
        ],
        "aarch64":[
            "docker-volume-vsphere.spec",
            # fakeroot-ng does not support aarch64
            "fakeroot-ng.spec",
            # ipxe does not support aarch64
            "ipxe.spec",
            # kexec-tools for arm64 does not support fpic
            "kexec-tools.spec",
            # no TXT/tboot on arm64
            "tboot.spec",
            # backward-cpp does not support amd64
            "backward-cpp.spec",
            "envoy.spec",
            # only generic linux is for arm64
            "linux-esx.spec",
            "linux-secure.spec",
            "linux-aws.spec",
            # only linux-secure supports aufs
            "aufs-util.spec",
            # open-vm-tools does not support aarch64
            "open-vm-tools.spec",
            # TODO: mariadb build hangs on amd64
            "mariadb.spec",
            # TODO: mysql fails on amd64 with fpic
            "mysql.spec",
            # irqbalance for arm64 ?
            "irqbalance.spec",
            # no X rpms to build openjdk, skip all java packages
            "openjdk8.spec",
            "ant-contrib.spec",
            "apache-ant.spec",
            "apache-maven.spec",
            "apache-tomcat.spec",
            "cassandra.spec",
            "commons-daemon.spec",
            "jna.spec",
            "kubernetes-dashboard.spec",
            "lightwave.spec",
            "mesos.spec",
            "protobuf.spec",
            "wavefront-proxy.spec",
            "zookeeper.spec",
            # requires lightwave
            "pmd.spec",
            # requires protobuf
            "calico-felix.spec",
            "lightstep-tracer-cpp.spec",
            "protobuf-c.spec",
            "runc.spec",
            # requires cassandra
            "python-cqlsh.spec",
            # requires python-pyinstaller, but it has unresolved glibc deps
            "calico-k8s-policy.spec",
            "libcalico.spec",
            # pcstat requires patching for aarch64
            "pcstat.spec",
            # sysdig for aarch64 requires luajit, skip it and falco
            # https://github.com/draios/sysdig/issues/833
            "sysdig.spec",
            "falco.spec"
        ]
    }

    @staticmethod
    def initialize(options):
        constants.specPath = options.specPath
        constants.sourcePath = options.sourcePath
        constants.rpmPath = options.rpmPath
        constants.sourceRpmPath = options.sourceRpmPath
        constants.topDirPath = options.topDirPath
        constants.logPath = options.logPath
        constants.prevPublishRPMRepo = options.publishRPMSPath
        constants.prevPublishXRPMRepo = options.publishXRPMSPath
        constants.buildRootPath=options.buildRootPath
        constants.pullsourcesConfig = options.pullsourcesConfig
        constants.inputRPMSPath=options.inputRPMSPath
        constants.testForceRPMS=[]
        constants.rpmCheck = options.rpmCheck
        constants.rpmCheckStopOnError = options.rpmCheckStopOnError
        constants.publishBuildDependencies=options.publishBuildDependencies
        constants.packageWeightsPath=options.packageWeightsPath
        constants.tmpDirPath = "/dev/shm"
        if constants.rpmCheck:
            constants.testLogger=Logger.getLogger("MakeCheckTest",constants.logPath)
            constants.addMacro("with_check","1")
        else:
            constants.addMacro("with_check","0")

        #adding distribution rpm macro
        constants.addMacro("dist",options.dist)

        #adding buildnumber rpm macro
        constants.addMacro("photon_build_number",options.buildNumber)

        #adding releasenumber rpm macro
        constants.addMacro("photon_release_version",options.releaseVersion)

        if options.katBuild != None:
            constants.addMacro("kat_build", options.katBuild)

    @staticmethod
    def setTestForceRPMS(listsPackages):
        constants.testForceRPMS=listsPackages

    @staticmethod
    def addMacro(macroName, macroValue):
        constants.userDefinedMacros[macroName]=macroValue

    @staticmethod
    def setLogLevel(logLevel):
        constants.logLevel = logLevel

    @staticmethod
    def setLogPath(logPath):
        constants.logPath = logPath

    @staticmethod
    def setSpecPath(specPath):
        constants.specPath = specPath
