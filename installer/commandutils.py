# pylint: disable=invalid-name,missing-docstring
import subprocess
import os
import crypt
import string
import random

class CommandUtils(object):
    def __init__(self, logger):
        self.logger = logger

    def run(self, cmd):
        self.logger.debug(cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = process.communicate()
        retval = process.returncode
        if out != b'':
            self.logger.info(out.decode())
        if retval != 0:
            self.logger.info("Command failed: {}".format(cmd))
            self.logger.info("Error code: {}".format(retval))
            self.logger.error(err.decode())
        return retval

    @staticmethod
    def is_vmware_virtualization():
        """Detect vmware vm"""
        process = subprocess.Popen(['systemd-detect-virt'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err is not None and err != 0:
            return False
        return out.decode() == 'vmware\n'

    @staticmethod
    def generate_password_hash(password):
        """Generate hash for the password"""
        shadow_password = crypt.crypt(
            password, "$6$" + "".join(
                [random.choice(
                    string.ascii_letters + string.digits) for _ in range(16)]))
        return shadow_password

