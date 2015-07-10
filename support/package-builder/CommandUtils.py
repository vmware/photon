import subprocess
import os
from Logger import Logger
from constants import constants

class CommandUtils(object):
    def __init__(self,logName=None,logPath=None):
        if logName is None:
            logName = "CommandUtils"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.findBinary = "find"

    def findFile (self, filename, sourcePath):
        process = subprocess.Popen([self.findBinary,  "-L", sourcePath,  "-name", filename],  stdout=subprocess.PIPE)
        returnVal = process.wait()
        if returnVal != 0:
            return None
        result=process.communicate()[0]
        if result is None:
            return None
        return result.split()

    def runCommandInShell(self,cmd,logfilePath=None,chrootCmd=None):
        if chrootCmd is not None:
            cmd = chrootCmd+" "+cmd
        if logfilePath is None:
            logfilePath=os.devnull
        self.logger.debug(cmd)
        logfile=open(logfilePath,"w")
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=logfile,stderr=logfile)
        retval = process.wait()
        logfile.close()
        if retval==0:
            return True
        return False
    
    def runCommandInShell2(self,cmd,chrootCmd=None):
        if chrootCmd is not None:
            cmd = chrootCmd+" "+cmd
        self.logger.debug(cmd)
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            return None
        result = process.communicate()[0]
        if result is None:
            return None
        return result.split()

