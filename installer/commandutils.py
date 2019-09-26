# pylint: disable=invalid-name,missing-docstring
import subprocess
import os

class CommandUtils(object):
    def __init__(self, logger):
        self.logger = logger

    def run(self, cmd):
        self.logger.debug(cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = process.communicate()
        retval = process.returncode
        self.logger.info(out.decode())
        if retval != 0:
            self.logger.debug(err.decode())
        return retval

