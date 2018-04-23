import subprocess
import os

class CommandUtils(object):
    def __init__(self):
        self.findBinary = "find"
        self.sortBinary = "sort"

    def findFile (self, filename, sourcePath):
        # Perform an alphabetical sort of the output from find, to get consistent ordering.
        processFind = subprocess.Popen([self.findBinary,  "-L", sourcePath,  "-name", filename, "-not", "-type", "d"],  stdout=subprocess.PIPE)
        processSort = subprocess.Popen([self.sortBinary,  "-d"], stdin=processFind.stdout, stdout=subprocess.PIPE)
        processFind.stdout.close() # Allow processFind to receive a SIGPIPE if processSort exits.
        returnVal = processSort.wait()
        if returnVal != 0:
            return None
        result=processSort.communicate()[0]
        if result is None:
            return None
        return result.split()

    def runCommandInShell(self,cmd,logfilePath=None,chrootCmd=None):
        if chrootCmd is not None:
            cmd = chrootCmd+" "+cmd
        if logfilePath is None:
            logfilePath=os.devnull
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
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            return None
        return process.communicate()[0]

