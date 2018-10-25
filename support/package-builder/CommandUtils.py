# pylint: disable=invalid-name,missing-docstring
import subprocess
import os

class CommandUtils:

    @staticmethod
    def findFile(filename, sourcePath):
        process = subprocess.Popen(["find", "-L", sourcePath, "-name", filename,
                                    "-not", "-type", "d"], stdout=subprocess.PIPE)
        # We don't check the return val here because find could return 1 but still be
        # able to find
        # the result. We shouldn't blindly return None without even checking the result.
        # The reason we want to suppress this is because for built RPMs, we first copy it to
        # the location with a random name and move it to the real name. find will complain our
        # action and return 1.
        # find's flag ignore_readdir_race can suppress this but it isn't working.
        # https://bugs.centos.org/view.php?id=13685

        #if returnVal != 0:
        #    return None
        result = process.communicate()[0]
        if result is None:
            return None
        return result.decode().split()

    @staticmethod
    def runCommandInShell(cmd, logfile=None, logfn=None):
        retval = 0
        if logfn:
            process = subprocess.Popen("%s" %cmd, shell=True, stdout=subprocess.PIPE)
            retval = process.wait()
            logfn(process.communicate()[0].decode())
        else:
            if logfile is None:
                logfile = os.devnull
            with open(logfile, "w") as f:
                process = subprocess.Popen("%s" %cmd, shell=True, stdout=f, stderr=f)
            retval = process.wait()
        return retval

