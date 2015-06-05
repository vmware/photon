#!/usr/bin/env python

from optparse import OptionParser
import os.path
from CommandUtils import CommandUtils
from Logger import Logger
from constants import constants
from PackageManager import PackageManager 
from ChrootUtils import ChrootUtils

def main():
    usage = "Usage: %prog [options] <package name>"
    parser = OptionParser(usage)
    parser.add_option("-s",  "--spec-path",  dest="specPath",  default="/workspace1/myrepos/photon/SPECS")
    parser.add_option("-o",  "--source-path",  dest="sourcePath",  default="/workspace1/mysources")
    parser.add_option("-r",  "--rpm-path",  dest="rpmPath",  default="/workspace1/mystage/RPMS")
    parser.add_option("-t",  "--install-tool-chain",  dest="installToolChain",  default=False,  action ="store_true")
    parser.add_option("-i",  "--install-package", dest="installPackage",  default=False,  action ="store_true")
    parser.add_option("-c",  "--clean-build", dest="cleanBuild",  default=False,  action ="store_true")
    parser.add_option("-p",  "--tools-path", dest="toolsPath",  default="/workspace1/mystage")
    parser.add_option("-l",  "--log-path", dest="logPath",  default="/workspace1/LOGS")
    parser.add_option("-a",  "--build-all", dest="buildAll",  default=False,  action ="store_true")
    parser.add_option("-f",  "--force", dest="forceBuild",  default=False,  action ="store_true")
    parser.add_option("-x",  "--incremental-build", dest="incrementalBuild",  default=True,  action ="store_true")
    parser.add_option("-z",  "--top-dir-path", dest="topDirPath",  default="/usr/src/photon")
    
    
    (options,  args) = parser.parse_args()
    
    cmdUtils=CommandUtils()
    if not os.path.isdir(options.logPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.logPath)
    
    if not os.path.isdir(options.rpmPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/x86_64")
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/noarch")
    
    logger=Logger.getLogger(options.logPath+"/Main")
    logger.info("Source Path :"+options.sourcePath)
    logger.info("Spec Path :" + options.specPath)
    logger.info("Rpm Path :" + options.rpmPath)
    logger.info("Tools Path :" + options.toolsPath)
    logger.info("Log Path :" + options.logPath)
    logger.info("Top Dir Path :" + options.topDirPath)
    
        
    listPackages=["acl","attr","autoconf","automake","bash","bc","bindutils","binutils","bison","boost","btrfs-progs","bzip2","ca-certificates","cdrkit","check",
                  "cloud-init","cmake","coreutils","cpio","cracklib","createrepo","curl","cyrus-sasl","db","dbus","deltarpm","diffutils","docbook-xml","docbook-xsl",
                  "docker","dparted","dracut","e2fsprogs","elfutils","etcd","expat","file","filesystem","findutils","flex","gawk","gcc","gdb","gdbm","gettext","git",
                  "glib","glibc","glibmm","gmp","go","gobject-introspection","google-daemon","google-startup-scripts","gperf","gpgme","gptfdisk","grep","groff",
                  "grub","gtk-doc","gzip","haveged","hawkey","iana-etc","inetutils","intltool","iproute2","iptables","itstool","json-glib","kbd","kmod","krb5",
                  "kubernetes","less","libaio","libassuan","libcap","libdnet","libffi","libgpg-error","libgsystem","libhif","libmspack","libpcap","libpipeline",
                  "librepo","libselinux","libsepol","libsigc++","libsolv","libtool","libxml2","libxslt","libyaml","linux","linux-api-headers","Linux-PAM","lua",
                  "lvm2","lzo","m4","make","man-db","man-pages","mercurial","mpc","mpfr","nano","ncurses","nspr","nss","ntp","openldap","openssh","openssl",
                  "open-vm-tools","ostree","parted","patch","pcre","perl","perl-common-sense","perl-Config-IniFiles","perl-DBD-SQLite","perl-DBI","perl-DBIx-Simple",
                  "perl-Exporter-Tiny","perl-JSON-XS","perl-libintl","perl-List-MoreUtils","perl-Module-Install","perl-Module-ScanDeps","perl-Types-Serialiser",
                  "perl-WWW-Curl","perl-YAML","perl-YAML-Tiny","photon-release","pkg-config","popt","procps-ng","psmisc","pycurl","pygobject","python2",
                  "python-configobj","python-iniparse","python-jsonpatch","python-jsonpointer","python-prettytable","python-requests","python-setuptools",
                  "python-six","PyYAML","readline","rocket","rpm","rpm-ostree","rpm-ostree-toolbox","ruby","sed","shadow","sqlite-autoconf","strace","sudo",
                  "swig","systemd","tar","tcpdump","tcsh","tdnf","texinfo","thin-provisioning-tools","tzdata","unzip","urlgrabber","util-linux","vim","wget",
                  "which","xerces-c","XML-Parser","xml-security-c","xz","yum","yum-metadata-parser","zlib"]
    
    constants.initialize(options)
    
    pkgManager = PackageManager()
    pkgManager.buildPackages(listPackages)
    
 
if __name__=="__main__":
    main()