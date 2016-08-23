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

    listMakeCheckRPMPkgtoInstall=[
        "python-setuptools",
        "which",
        "go",
        "e2fsprogs",
        "shadow",
        "check",
        "libacl-devel",
        "device-mapper",
        "wget",
        "tar",
        "pkg-config",
        "git"]

    listMakeCheckPackages=[
       "apr-util","apr","asciidoc","atftp","attr","audit","autoconf","autogen","automake","bash","bc","binutils","bison",
       "btrfs-progs","bzip2","c-ares","cgroup-utils","check","cifs-utils","coreutils","cpio","cracklib","createrepo",
       "cronie","curl","cve-check-tool","cyrus-sasl","cython","db","dbus-glib","dbus","dhcp","diffutils","e2fsprogs",
       "ecdsa","elfutils","ethtool","eventlog","expat","fakeroot-ng","file","findutils","flannel","flex","gawk","gc",
       "gdbm","gettext","git","gmp","gnome-common","gnutls","gperf","gpgme","gptfdisk","gtk-doc","gzip","haveged","iana-etc",
       "inotify-tools","intltool","iperf","json-c","kbd","kubernetes","libaio","libarchive","libassuan","libcap-ng",
       "libconfig","libgcrypt","libgpg-error","libgsystem","liblogging","libmspack","libnl","libnss-ato","libpipeline",
       "libsigc++","libsolv","libsoup","libtasn1","libtool","libunistring","libxml2","libxslt","libyaml","Linux-PAM",
       "ltrace","lzo","make","man-db","mpc","mpfr","msr-tools","nano","ncurses","net-snmp","nettle","newt","nicstat",
       "nspr","nss-altfiles","nss","openjdk","openldap","openssh","openssl","pcre","pcstat","perl-CGI","perl-common-sense",
       "perl-Config-IniFiles","perl-DBD-SQLite","perl-DBI","perl-DBIx-Simple","perl-Exporter-Tiny","perl-JSON-XS",
       "perl-libintl","perl-List-MoreUtils","perl-Module-Build","perl-Module-Install","perl-Module-ScanDeps",
       "perl-Object-Accessor","perl-Types-Serialiser","perl-WWW-Curl","perl-YAML-Tiny","perl-YAML","photon-release",
       "pkg-config","popt","postgresql","procmail","procps-ng","psmisc","pycrypto","python-cffi","python-configobj",
       "python-cryptography","python-ipaddr","python-jsonpatch","python-jsonpointer","python-lxml","python-prettytable",
       "python-pyasn1","python-pycparser","python-requests","python-zope.inetrface","PyYAML","readline","rocket",
       "rpcbind","rpm-ostree","rpm","rsync","rsyslog","rubygem-builder","rubygem-rbvmomi","rubygem-zip","runit",
       "sed","shadow","slang","sqlite-autoconf","sudo","swig","syslog-ng","systemtap","tcpdump","texinfo","unzip",
       "userspace-rcu","vim","WALinuxAgent","xerces-c","XML-Parser","xz","zlib"]


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
        
        #adding kernelsubrelease rpm macro
        kernelversion = kernelversion.replace(".","")
        if kernelversion.isdigit():
            kernelversion = int(kernelversion) << 8
        kernelsubrelease = str(kernelversion)+kernelrelease
        kernelsubrelease = kernelsubrelease.replace(constants.dist,"")
        if kernelsubrelease:
            kernelsubrelease = "."+kernelsubrelease
            constants.specData.addMacro("kernelsubrelease",kernelsubrelease) 
