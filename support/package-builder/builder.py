#!/usr/bin/env python

from optparse import OptionParser
import os.path
from CommandUtils import CommandUtils
from Logger import Logger
from constants import constants
from PackageManager import PackageManager 
import json
import sys
from SpecUtils import Specutils
from StringUtils import StringUtils
import collections
import traceback

def main():
    usage = "Usage: %prog [options] <package name>"
    parser = OptionParser(usage)
    parser.add_option("-s",  "--spec-path",  dest="specPath",  default="../../SPECS")
    parser.add_option("-x",  "--source-path",  dest="sourcePath",  default="../../stage/SOURCES")
    parser.add_option("-r",  "--rpm-path",  dest="rpmPath",  default="../../stage/RPMS")
    parser.add_option("-i",  "--install-package", dest="installPackage",  default=False,  action ="store_true")
    parser.add_option("-p",  "--publish-RPMS-path", dest="publishRPMSPath",  default="../../stage/PUBLISHRPMS")
    parser.add_option("-l",  "--log-path", dest="logPath",  default="../../stage/LOGS")
    parser.add_option("-o",  "--build-option", dest="buildOption",  default="full")
    parser.add_option("-z",  "--top-dir-path", dest="topDirPath",  default="/usr/src/photon")
    parser.add_option("-j",  "--json-file", dest="inputJSONFile",  default="../../common/data/build_install_options_all.json")
    parser.add_option("-b",  "--build-root-path", dest="buildRootPath",  default="/mnt")
    parser.add_option("-t",  "--threads", dest="buildThreads",  default=1, type="int", help="Numbeer of working threads")
    parser.add_option("-m",  "--tool-chain-stage", dest="toolChainStage",  default="None")
    parser.add_option("-c",  "--pullsources-config", dest="pullsourcesConfig",  default="pullsources.conf")
    parser.add_option("-d",  "--dist", dest="dist",  default="")

    (options,  args) = parser.parse_args()
    cmdUtils=CommandUtils()
    if not os.path.isdir(options.logPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.logPath)
    
    logger=Logger.getLogger(options.logPath+"/Main")
    
    errorFlag=False
    package = None
    if not os.path.isdir(options.sourcePath):
        logger.error("Given Sources Path is not a directory:"+options.sourcePath)
        errorFlag = True
    if not os.path.isdir(options.specPath):
        logger.error("Given Specs Path is not a directory:"+options.specPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath):
        logger.error("Given RPMS Path is not a directory:"+options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath+"/x86_64"):
        logger.error("Given RPMS Path is missing x86_64 sub-directory:"+options.publishRPMSPath)
        errorFlag = True
    if not os.path.isdir(options.publishRPMSPath+"/noarch"):
        logger.error("Given RPMS Path is missing noarch sub-directory:"+options.publishRPMSPath)
        errorFlag = True
    
    if not os.path.isfile(options.inputJSONFile) and not options.installPackage:
        logger.error("Given JSON File is not a file:"+options.inputJSONFile)
        errorFlag = True
        
    if options.installPackage :
        if len(args) != 1:
            logger.error("Please provide package name")
            errorFlag = True
        else:
            package=args[0]
        
    if errorFlag:
        logger.error("Found some errors. Please fix input options and re-run it.")
        return False
    
    
    if not os.path.isdir(options.rpmPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/x86_64")
        cmdUtils.runCommandInShell("mkdir -p "+options.rpmPath+"/noarch")
    
    if not os.path.isdir(options.buildRootPath):
        cmdUtils.runCommandInShell("mkdir -p "+options.buildRootPath)
    
    logger.info("Source Path :"+options.sourcePath)
    logger.info("Spec Path :" + options.specPath)
    logger.info("Rpm Path :" + options.rpmPath)
    logger.info("Log Path :" + options.logPath)
    logger.info("Top Dir Path :" + options.topDirPath)
    logger.info("Publish RPMS Path :" + options.publishRPMSPath)
    if not options.installPackage:
        logger.info("JSON File :" + options.inputJSONFile)
    else:
        logger.info("Package to build:"+package)

    '''    
    listPackages=["acl","attr","autoconf","automake","bash","bc","bindutils","binutils","bison","boost","btrfs-progs","bzip2","ca-certificates","cdrkit","check",
                  "cloud-init","cmake","coreutils","cpio","cracklib","createrepo","curl","cyrus-sasl","db","dbus","deltarpm","diffutils","docbook-xml","docbook-xsl",
                  "docker","dracut","e2fsprogs","elfutils","etcd","expat","file","filesystem","findutils","flex","gawk","gcc","gdb","gdbm","gettext","git",
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
    '''
    try:
        constants.initialize(options)
        if package == "packages_list":
            buildPackagesList(options.specPath, options.buildRootPath+"/../packages_list.csv")
        elif package == "sources_list":
            buildSourcesList(options.specPath, options.buildRootPath+"/../")
        elif options.toolChainStage == "stage1":
            pkgManager = PackageManager()
            pkgManager.buildToolChain()
        elif options.toolChainStage == "stage2":
            pkgManager = PackageManager()
            pkgManager.buildToolChainPackages(options.buildThreads)
        elif options.installPackage:
            buildAPackage(package, options.buildThreads)
        else:
            buildPackagesFromGivenJSONFile(options.inputJSONFile, options.buildOption,logger, options.buildThreads)
    except Exception as e:
        logger.error("Caught an exception")
        logger.error(str(e))
        # print stacktrace
        traceback.print_exc()
        sys.exit(1)
    
    sys.exit(0)

def buildToolChain(buildThreads):
    pkgManager = PackageManager()
    pkgManager.buildToolChainPackages(buildThreads)

def buildPackagesList(specPath, csvFilename):
    csvFile = open(csvFilename, "w")
    csvFile.write("Package,Version,License,URL,Sources,Patches\n")
    lst = os.listdir(specPath)
    lst.sort()
    for dirEntry in lst:
        specDir = os.path.join(specPath, dirEntry)
        if os.path.isdir(specDir):
            for specEntry in os.listdir(specDir):
                specFile = os.path.join(specDir, specEntry)
                if os.path.isfile(specFile) and specFile.endswith(".spec"):
                    spec=Specutils(specFile)
                    name=spec.getBasePackageName()
                    version=spec.getRPMVersion(name)
                    license=spec.getLicense(name)
                    url=spec.getURL(name)
                    ss=spec.getSourceURLs()
                    sources=""
                    for s in ss:
                        if (s.startswith("http") or s.startswith("ftp")):
                            if sources != "":
                                sources += " "
                            sources += s
                    patches=""
                    ps=spec.getPatchNames()
                    for p in ps:
                        if patches != "":
                            patches += " "
                        patches += p
                    csvFile.write(name+","+version+","+license+","+url+","+sources+","+patches+"\n")
    csvFile.close()

def buildSourcesList(specPath, yamlDir, singleFile=False):
    strUtils = StringUtils()
    if singleFile:
        yamlFile = open(yamlDir+"sources_list.yaml", "w")
    lst = os.listdir(specPath)
    lst.sort()
    for dirEntry in lst:
        specDir = os.path.join(specPath, dirEntry)
        if os.path.isdir(specDir):
            for specEntry in os.listdir(specDir):
                specFile = os.path.join(specDir, specEntry)
                if os.path.isfile(specFile) and specFile.endswith(".spec"):
                    spec=Specutils(specFile)
                    modified = len(spec.getPatchNames()) > 0
                    ss=spec.getSourceURLs()
                    for s in ss:
                        if (s.startswith("http") or s.startswith("ftp")):
                            ossname=strUtils.getPackageNameFromURL(s)
                            ossversion=strUtils.getPackageVersionFromURL(s)
                            if not singleFile:
                                yamlFile = open(yamlDir+ossname+"-"+ossversion+".yaml", "w")
                            yamlFile.write("vmwsource:"+ossname+":"+ossversion+":\n")
                            yamlFile.write("  repository: VMWsource\n")
                            yamlFile.write("  name: '"+ossname+"'\n")
                            yamlFile.write("  version: '"+ossversion+"'\n")
                            yamlFile.write("  url: "+s+"\n")
                            yamlFile.write("  license: UNKNOWN\n")
                            if modified:
                                yamlFile.write("  modified: true\n")
                            yamlFile.write("\n")
                            if not singleFile:
                                yamlFile.close()
    if singleFile:
        yamlFile.close()

def buildAPackage(package, buildThreads):
    listPackages=[]
    listPackages.append(package)
    pkgManager = PackageManager()
    pkgManager.buildPackages(listPackages, buildThreads)

def buildPackagesFromGivenJSONFile(inputJSONFile,buildOption,logger, buildThreads):
    listPackages = get_all_package_names(inputJSONFile)

    listPackagesToBuild=[]
    for pkg in listPackages:
        p =  pkg.encode('utf-8')
        listPackagesToBuild.append(str(p))
    logger.info("List of packages to build:")
    logger.info(listPackagesToBuild)
    pkgManager = PackageManager()
    pkgManager.buildPackages(listPackagesToBuild, buildThreads)
    
def get_all_package_names(build_install_option):
    base_path = os.path.dirname(build_install_option)
    jsonData = open(build_install_option)
    option_list_json = json.load(jsonData, object_pairs_hook=collections.OrderedDict)
    jsonData.close()
    options_sorted = option_list_json.items()
    packages = []

    for install_option in options_sorted:
        filename = os.path.join(base_path, install_option[1]["file"])
        jsonData=open(filename)
        package_list_json = json.load(jsonData)
        jsonData.close()
        packages = packages + package_list_json["packages"]

    return packages

if __name__=="__main__":
    main()
