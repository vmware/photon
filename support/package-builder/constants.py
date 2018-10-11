from Logger import Logger

class constants(object):
    specPath = ""
    sourcePath = ""
    rpmPath = ""
    logPath = ""
    topDirPath = ""
    buildRootPath = "/mnt"
    prevPublishRPMRepo = ""
    prevPublishXRPMRepo = ""
    pullsourcesConfig = ""
    buildPatch = False
    inputRPMSPath = ""
    rpmCheck = False
    sourceRpmPath = ""
    publishBuildDependencies = False
    packageWeightsPath = None
    dockerUnixSocket = "/var/run/docker.sock"
    userDefinedMacros = {}
    dist = None
    buildNumber = None
    releaseVersion = None
    katBuild = None
    testForceRPMS = []
    tmpDirPath = "/dev/shm"
    buildOptions = {}
    # will be extended later from listMakeCheckRPMPkgtoInstall
    listMakeCheckRPMPkgWithVersionstoInstall = None

    noDepsPackageList = [
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
    listCoreToolChainPackages = [
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
    listToolChainPackages = [
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
    listToolChainRPMsToInstall = [
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

    perPackageToolChain = dict.fromkeys(
        ["openjdk8",
         "openjdk8-doc",
         "openjdk8-src",
         "openjdk8-sample",
         "openjre8",
         "openjdk9",
         "openjdk9-doc",
         "openjdk9-src",
         "openjre9",
         "openjdk10",
         "openjdk10-doc",
         "openjdk10-src",
         "openjre10"],
          {
          "x86_64":[
            "icu-devel",
            "cups",
            "cups-devel",
            "xorg-proto-devel",
            "libXtst",
            "libXtst-devel",
            "libXfixes",
            "libXfixes-devel",
            "libXi",
            "libXi-devel",
            "openjdk",
            "openjre",
            "icu",
            "alsa-lib",
            "alsa-lib-devel",
            "xcb-proto",
            "libXdmcp-devel",
            "libXau-devel",
            "util-macros",
            "xtrans",
            "libxcb-devel",
            "proto",
            "libXdmcp",
            "libxcb",
            "libXau",
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
            "libXrender-devel"],
         "aarch64":[
            "icu-devel",
            "openjdk",
            "openjre",
            "icu",
            "alsa-lib",
            "alsa-lib-devel",
            "xcb-proto",
            "libXdmcp-devel",
            "libXau-devel",
            "util-macros",
            "xtrans",
            "libxcb-devel",
            "proto",
            "libXdmcp",
            "libxcb",
            "libXau",
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
          })

    perPackageToolChain["apache-maven"] = {
          "x86_64":["apache-maven"],
          "aarch64":["apache-maven"]
          }

    # List of RPMs which are not published. They will be created during the
    # build process
    listOfRPMsProvidedAfterBuild = [
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
    listMakeCheckRPMPkgtoInstall = [
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
        "ncurses-terminfo"]

    listReInstallPackages = [
        "go"]

    # List of packages that requires privileged docker
    # to run make check.
    listReqPrivilegedDockerForTest = [
        "elfutils", # SYS_PTRACE
        "gdb",
        "glibc",
        "tar"]

    # .spec file might contain lines such as
    # Requires(post):/sbin/useradd
    # Build system should interpret it as
    # Requires: shadow
    providedBy = {
        "/usr/sbin/useradd":"shadow",
        "/usr/sbin/groupadd":"shadow",
        "/usr/bin/which":"which",
        "/bin/sed":"sed"
    }

    # list of spec files to skip for parsing for given arch
    skipSpecsForArch = {
        "x86_64":[
            "u-boot-rpi3.spec",
            "openjdk8_aarch64.spec",
            "librpcsecgss.spec"
            ],
        "aarch64":[
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
            # syslinux does not support aarch64
            "syslinux.spec",
            # TODO: mariadb build hangs on amd64
            "mariadb.spec",
            # TODO: mysql fails on amd64 with fpic
            "mysql.spec",
            # irqbalance for arm64 ?
            "irqbalance.spec",
            # openjdk8.spec is for x86_64 arch
            "openjdk8.spec",
            "openjdk9.spec",
            "openjdk10.spec",
            "elasticsearch.spec",
            # dotnet-runtime source has dep on libcurl.so.4(CURL_OPENSSL_3)(64bit)
            "dotnet-runtime.spec",
            "powershell.spec",
            # dashboard failed to build libxslt during `npm install`
            "kubernetes-dashboard.spec",
            # test issue (java null pointer exception) before compilation
            "wavefront-proxy.spec",
            # sysdig for aarch64 requires luajit, skip it and falco
            # https://github.com/draios/sysdig/issues/833
            "sysdig.spec",
            "falco.spec",
            # one more fail, not investigated yet
            "log4cpp.spec",

            # VIVACE packages
            # need to update to mono-4.5
            "mono.spec",
            "banshee.spec",
            "dbus-sharp.spec",
            "dbus-sharp-glib.spec",
            "gnome-keyring-sharp.spec",
            "gnome-sharp.spec",
            "gtk-sharp2.spec",
            "mono-addins.spec",
            "monodevelop.spec",
            "nuget.spec",
            "nunit.spec",
            "pinta.spec",
            "taglib-sharp.spec",
            "tomboy.spec",
            "totem.spec",
            "webkit-sharp.spec",
            # compilation issues with libwebkit
            "libwebkit.spec",
            "xf86-video-vmware.spec",
            "xf86-video-intel.spec",
            "xf86-input-vmmouse.spec",
            # does not recognize aarch64
            "thunderbird.spec",
            #
            "open-vm-tools-vivace.spec",
            "librpcsecgss.spec"
        ]
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
    def setLogPath(logPath):
        constants.logPath = logPath

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
    def setPullSourcesConfig(pullSourcesConfig):
        constants.pullsourcesConfig = pullSourcesConfig

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
    def initialize():
        if constants.rpmCheck:
            constants.testLogger = Logger.getLogger("MakeCheckTest", constants.logPath)
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
            constants.addMacro("photon_release_version", constants.releaseVersion)

        if constants.katBuild is not None:
            constants.addMacro("kat_build", constants.katBuild)

    @staticmethod
    def setTestForceRPMS(listsPackages):
        constants.testForceRPMS = listsPackages

    @staticmethod
    def addMacro(macroName, macroValue):
        constants.userDefinedMacros[macroName] = macroValue

    @staticmethod
    def setBuidOptions(options):
        constants.buildOptions = options
