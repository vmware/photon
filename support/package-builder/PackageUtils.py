from CommandUtils import CommandUtils
from Logger import Logger
import os
import shutil
from constants import constants


class PackageUtils(object):
    
    def __init__(self,logName=None,logPath=None):
        if logName is None:
            self.logName = "PackageUtils"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.runInChrootCommand="./run-in-chroot.sh"
        
    
    def getRPMDestDir(self,rpmName,rpmDir):
        arch=""
        if rpmName.find("x86_64") != -1:
            arch='x86_64'
        elif rpmName.find("noarch") != -1:
            arch="noarch"
        #else: Todo throw an exeption
        rpmDestDir=rpmDir+"/"+arch
        return rpmDestDir
    
    def copyRPM(self,rpmFile,destDir):
        cmdUtils = CommandUtils()
        rpmName=os.path.basename(rpmFile)
        rpmDestDir=self.getRPMDestDir(rpmName,destDir)
        if not os.path.isdir(rpmDestDir):
            cmdUtils.run_command("mkdir -p "+rpmDestDir)
        rpmDestPath=rpmDestDir+"/"+rpmName
        shutil.copyfile(rpmFile,  rpmDestPath)
        return rpmDestPath
    
    def installRPM(self,package,chrootID,noDeps=False,destLogPath=None):
        rpmfile=self.findRPMFileForGivenPackage(package)
        if rpmfile is None:
            self.logger.error("unexpected error")
            self.logger.error("Stopping installing package:"+package)
            return False

        rpmDestFile = self.copyRPM(rpmfile, chrootID+constants.topDirPath+"/RPMS")
        rpmFile=rpmDestFile.replace(chrootID,"")
        chrootCmd=self.runInChrootCommand+" "+chrootID
        logFile=chrootID+constants.topDirPath+"/LOGS"+"/"+package+".completed"

        cmdUtils = CommandUtils()
        returnVal = cmdUtils.installRPM(rpmFile,logFile,chrootCmd,noDeps)
        if destLogPath is not None:
            shutil.copy2(logFile, destLogPath)
        if not returnVal:
            self.logger.error("Installing " + rpmFile+" rpm is failed")
            return False
        return True   
    
    def copySourcesTobuildroot(self,listSourceFiles,package,destDir):
        cmdUtils = CommandUtils()
        for source in listSourceFiles:
            sourcePath = cmdUtils.find_file(source,constants.sourcePath)
            if sourcePath is None or len(sourcePath) == 0:
                sourcePath = cmdUtils.find_file(source,constants.specPath)
            if sourcePath is None or len(sourcePath) == 0:
                self.logger.error("Missing source: "+source+". Cannot find sources for package: "+package)
                self.logger.error("Stopping building toolchain")
                return False
            if len(sourcePath) > 1:
                self.logger.error("Multiple sources found: Unable to determine one. ")
                self.logger.error("Stopping building toolchain")
                return False
            self.logger.info("Source path :" + source + " Source filename: " + sourcePath[0])
            shutil.copyfile(sourcePath[0],  destDir+source)
    
    def buildRPMSForGivenPackage(self,package, chrootID,destLogPath=None):
        self.logger.info("Building package......"+package)
        #self.adjust_gcc_specs(package)

        listSourcesFiles = constants.specData.getSources(package)
        listPatchFiles =  constants.specData.getPatches(package)
        specFile = constants.specData.getSpecFile(package)
        specName = constants.specData.getSpecName(package) + ".spec"
        
        chrootSourcePath=chrootID+constants.topDirPath+"/SOURCES/"
        chrootSpecPath=constants.topDirPath+"/SPECS/"
        chrootLogsFilePath=chrootID+constants.topDirPath+"/LOGS/"+package+".log"
        chrootCmd=self.runInChrootCommand+" "+chrootID
        shutil.copyfile(specFile, chrootID+chrootSpecPath+specName )
        
        self.copySourcesTobuildroot(listSourcesFiles,package,chrootSourcePath)
        self.copySourcesTobuildroot(listPatchFiles,package,chrootSourcePath)
        
        returnVal,listRPMFiles = self.buildRPM(chrootSpecPath+"/"+specName,chrootLogsFilePath, chrootCmd)
        if destLogPath is not None:
            shutil.copy2(chrootLogsFilePath, destLogPath)
        
        if not returnVal:
            return False
        
        for rpmFile in listRPMFiles:
            self.copyRPM(chrootID+"/"+rpmFile, constants.rpmPath)
        return True

    def buildRPM(self,specFile,logFile,chrootCmd):
        cmdUtils = CommandUtils()
        returnVal,listRPMFiles = cmdUtils.buildRPM(specFile,logFile,chrootCmd)
        if not returnVal:
            self.logger.error("Building rpm is failed "+specFile)
            return False,None
        return True,listRPMFiles    
    
    def findRPMFileForGivenPackage(self,package):
        cmdUtils = CommandUtils()
        version = constants.specData.getVersion(package)
        release = constants.specData.getRelease(package)
        listFoundRPMFiles = cmdUtils.find_file(package+"-"+version+"-"+release+"*.rpm",constants.rpmPath)
        if len(listFoundRPMFiles) == 1 :
            return listFoundRPMFiles[0]
        if len(listFoundRPMFiles) == 0 :
            return None
        if len(listFoundRPMFiles) > 1 :
            self.logger.error("Unable to determine the rpm file for package. Found multiple rpm files for given package in rpm directory")
            return None
        return None
    
    def findPackageNameFromRPMFile(self,rpmfile):
        rpmfile=os.path.basename(rpmfile)
        releaseindex=rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:"+rpmfile)
            return None
        versionindex=rpmfile[0:releaseindex].rfind("-")
        if versionindex == -1:
            self.logger.error("Invalid rpm file:"+rpmfile)
            return None
        packageName=rpmfile[0:versionindex]
        return packageName 
