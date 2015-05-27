from CommandUtils import CommandUtils
from ChrootUtils import ChrootUtils
from Logger import Logger
from PackageUtils import PackageUtils
import shutil
from constants import constants
import subprocess

class ToolChainUtils(object):
    __built_successfull=False
    
    def __init__(self,logName=None,logPath=None):
        if logName is None:
            logName = "Toolchain Utils"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.adjustToolChainScript = "adjust-tool-chain.sh"
        self.localegenScript = "./locale-gen.sh"
        self.localegenConfig = "./locale-gen.conf"
        self.prepareBuildRootCmd="./prepare-build-root.sh"
        
        self.listPkgsRequiredToBuildToolchain=["linux-api-headers", "glibc","glibc-devel",  "zlib","zlib-devel",  "file",
            "binutils","binutils-devel",  "gmp","gmp-devel", "mpfr", "mpfr-devel", "mpc",
            "libgcc","libgcc-devel","libstdc++","libstdc++-devel","libgomp","libgomp-devel","gcc",
            "pkg-config", "ncurses", "bash", "bzip2", "sed","ncurses-devel","procps-ng","coreutils", "m4","grep",
            "readline", "diffutils","gawk", "findutils", "gettext", "gzip","make",  "patch",
            "util-linux", "tar", "xz","libtool", "flex",  "bison",
            "readline-devel", "lua","lua-devel","popt","popt-devel","nspr","sqlite-autoconf","nss","nss-devel",
            "bzip2-devel","elfutils-libelf","elfutils","elfutils-libelf-devel","elfutils-devel",
            "expat","libffi","libpipeline", "gdbm","perl","texinfo","autoconf","automake",
            "openssl","openssl-devel","python2","python2-libs","python2-devel","rpm",
            "groff", "man-db", "man-pages","cpio"]

        self.listPkgsToInstallToolChain=["linux-api-headers", "glibc","glibc-devel",  "zlib","zlib-devel",  "file",
            "binutils","binutils-devel",  "gmp","gmp-devel", "mpfr", "mpfr-devel", "mpc",
            "libgcc","libgcc-devel","libstdc++","libstdc++-devel","libgomp","libgomp-devel","gcc",
            "pkg-config", "ncurses", "bash", "bzip2", "sed","procps-ng","coreutils", "m4","grep",
            "readline","diffutils","gawk", "findutils", "gettext", "gzip","make",  "patch",
            "util-linux", "tar", "xz","libtool", "flex",  "bison",
            "lua","popt","nspr","sqlite-autoconf","nss","elfutils-libelf",
            "libpipeline", "gdbm","perl","texinfo","rpm",
            "autoconf","automake", "groff", "man-db", "man-pages","elfutils","cpio"]
    
    def prepareChroot(self,chrootID,toolsArchive=""):
        process = subprocess.Popen([self.prepareBuildRootCmd, chrootID,  constants.specPath,  constants.rpmPath, constants.toolsPath,toolsArchive])
        returnVal = process.wait()
        if returnVal != 0:
            self.logger.error("Prepare build root script failed.Unable to prepare chroot.")
            raise Exception("Prepare build root script failed")

        cmdUtils=CommandUtils()
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/x86_64")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/noarch")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SOURCES")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SPECS")
        self.logger.info("Successfully prepared chroot:"+chrootID)
    
    def buildToolChain(self):
        self.logger.info("Building Tool Chain .....")
        chrootID=None
        chrUtils = ChrootUtils(self.logName,self.logPath)
        try:
            returnVal,chrootID = chrUtils.createChroot()
            if not returnVal:
                raise Exception("creating chroot failed")
            self.prepareChroot(chrootID)
            pkgUtils=PackageUtils(self.logName,self.logPath)
            for package in self.listPkgsRequiredToBuildToolchain:
                rpmPkg=pkgUtils.findRPMFileForGivenPackage(package)
                if rpmPkg is None:
                    pkgUtils.buildRPMSForGivenPackage(package, chrootID)
                pkgUtils.installRPM(package, chrootID, True)
                if package == "glibc":
                    self.adjustToolChain(chrootID)
            self.logger.info("Successfully built toolchain")
        except Exception as e:
            self.logger.error("Unable to build tool chain.")
            raise e
        finally:
            if chrootID is not None:
                chrUtils.destroyChroot(chrootID)
    
    #tool chain should be updated before calling this method
    def installToolChain(self,chrootID):
        self.logger.info("Installing toolchain.....")
        self.prepareChroot(chrootID,"minimal")
        pkgUtils= PackageUtils(self.logName,self.logPath)
        for package in self.listPkgsToInstallToolChain:
            pkgUtils.installRPM(package, chrootID, True)
            if package == "glibc":
                self.adjustToolChain(chrootID)
        cmdUtils=CommandUtils()
        cmdUtils.runCommandInShell("rm -rf "+ chrootID+"/tools")
        cmdUtils.runCommandInShell("rm "+ chrootID+"/"+constants.topDirPath+"/RPMS/x86_64/*")
        cmdUtils.runCommandInShell("rm "+ chrootID+"/"+constants.topDirPath+"/RPMS/noarch/*")
        self.logger.info("Installed tool chain successfully on chroot:"+chrootID)
    
    def adjustToolChain(self,chrootID):
        shutil.copy2(self.adjustToolChainScript,  chrootID+"/tmp")
        shutil.copy2(self.localegenScript,  chrootID+"/sbin")
        shutil.copy2(self.localegenConfig,  chrootID+"/etc")
        cmdUtils=CommandUtils()
        logFile=constants.logPath+"/adjustToolChainScript.log"
        returnVal = cmdUtils.runCommandInShell("/tmp/"+self.adjustToolChainScript,logFile, "./run-in-chroot.sh "+chrootID)
        if not returnVal:
            self.logger.error("Adjust tool chain script failed.")
            raise Exception("Adjust tool chain script failed")

        
        
    
        
    
    
    
    

    
        
        
            
        
        
    
      

