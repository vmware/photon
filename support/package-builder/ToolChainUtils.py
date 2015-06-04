from CommandUtils import CommandUtils
from ChrootUtils import ChrootUtils
from Logger import Logger
from PackageUtils import PackageUtils
import shutil
from constants import constants

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
        
    def prepareChroot(self,chrootID,toolsArchive=None):
        cmdUtils=CommandUtils()
        prepareChrootCmd=self.prepareBuildRootCmd+" "+chrootID+" "+constants.specPath+" "+constants.rpmPath+" "+constants.toolsPath
        if toolsArchive is not None:
            prepareChrootCmd=prepareChrootCmd+" "+toolsArchive
        returnVal=cmdUtils.runCommandInShell(prepareChrootCmd)
        if not returnVal:
            self.logger.error("Prepare build root script failed.Unable to prepare chroot.")
            raise Exception("Prepare build root script failed")

        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/x86_64")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/RPMS/noarch")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SOURCES")
        cmdUtils.runCommandInShell("mkdir -p "+chrootID+constants.topDirPath+"/SPECS")
        self.logger.info("Successfully prepared chroot:"+chrootID)
    
    def buildCoreToolChainPackages(self):
        self.logger.info("Building core tool chain packages.....")
        chrootID=None
        chrUtils = ChrootUtils(self.logName,self.logPath)
        try:
            chrootName="build-core-toolchain"
            returnVal,chrootID = chrUtils.createChroot(chrootName)
            if not returnVal:
                raise Exception("creating chroot failed")
            self.prepareChroot(chrootID)
            pkgUtils=PackageUtils(self.logName,self.logPath)
            for package in constants.listCoreToolChainRPMPackages:
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
    
    #Tool chain should be built before calling this method
    def installToolChain(self,chrootID):
        self.logger.info("Installing toolchain.....")
        self.prepareChroot(chrootID,"minimal")
        pkgUtils= PackageUtils(self.logName,self.logPath)
        for package in constants.listToolChainRPMPkgs:
            pkgUtils.installRPM(package, chrootID, True)
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

        
    def installCoreToolChainPackages(self,chrootID):
        self.logger.info("Installing toolchain.....")
        self.prepareChroot(chrootID)
        pkgUtils= PackageUtils(self.logName,self.logPath)
        for package in constants.listCoreToolChainRPMPackages:
            pkgUtils.installRPM(package, chrootID, True)
            if package == "glibc":
                self.adjustToolChain(chrootID)
        cmdUtils=CommandUtils()
        cmdUtils.runCommandInShell("rm "+ chrootID+"/"+constants.topDirPath+"/RPMS/x86_64/*")
        cmdUtils.runCommandInShell("rm "+ chrootID+"/"+constants.topDirPath+"/RPMS/noarch/*")
        self.logger.info("Installed core tool chain packages successfully on chroot:"+chrootID)    
    
    
        
    
    
    
    

    
        
        
            
        
        
    
      

