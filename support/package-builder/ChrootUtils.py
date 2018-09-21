# pylint: disable=invalid-name,missing-docstring
import os.path
from Logger import Logger
from CommandUtils import CommandUtils
from constants import constants

class ChrootUtils(object):

    def __init__(self, logName=None, logPath=None):
        if logName is None:
            logName = "ChrootUtils"
        if logPath is None:
            logPath = constants.logPath
        self.logName = logName
        self.logPath = logPath
        self.logger = Logger.getLogger(logName, logPath)

    def createChroot(self, chrootName):
        chrootID = constants.buildRootPath + "/" + chrootName
        if os.path.isdir(chrootID):
            if not self.destroyChroot(chrootID):
                self.logger.error("Given chroot " + chrootID +
                                  " is already exists. unable to destroy it ")
                return False, None
        # need to add timeout for this step
        # http://stackoverflow.com/questions/1191374/subprocess-with-timeout
        cmdUtils = CommandUtils()
        returnVal = cmdUtils.runCommandInShell("mkdir -p " + chrootID)
        if not returnVal:
            self.logger.error("Unable to create chroot:" + chrootID + ".Unknown error.")
            return False, None
        return True, chrootID

    def destroyChroot(self, chrootID):
        # need to add timeout for this step
        # http://stackoverflow.com/questions/1191374/subprocess-with-timeout
        cmdUtils = CommandUtils()
        returnVal = cmdUtils.runCommandInShell("./clean-up-chroot.py " + chrootID)
        if not returnVal:
            self.logger.error("Unable to destroy chroot:" + chrootID + ".Unknown error.")
            return False

        returnVal = cmdUtils.runCommandInShell("rm -rf " + chrootID)
        if not returnVal:
            self.logger.error("Unable to destroy chroot:" + chrootID + ".Unknown error.")
            return False
        return True
