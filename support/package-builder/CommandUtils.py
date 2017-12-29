import subprocess
import os

class CommandUtils(object):
    def __init__(self):
        self.findBinary = "find"

    def findFile (self, filename, sourcePath):
        process = subprocess.Popen([self.findBinary, "-L", sourcePath, "-name", filename, "-not", "-type", "d"],  stdout=subprocess.PIPE)
        # We don't check the return val here because find could return 1 but still be able to find
        # the result. We shouldn't blindly return None without even checking the result.
        # The reason we want to suppress this is because for built RPMs, we first copy it to
        # the location with a random name and move it to the real name. find will complain our
        # action and return 1.
        # find's flag ignore_readdir_race can suppress this but it isn't working.
        # https://bugs.centos.org/view.php?id=13685

        #if returnVal != 0:
        #    return None
        result=process.communicate()[0]
        if result is None:
            return None
        return result.decode().split()

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

