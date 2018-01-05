import os
import ctypes
import ctypes.util
import json
import collections
import subprocess
import fileinput
import re
import shutil

class Utils(object):
    def __init__(self):
        self.filesystems = []
        with open('/proc/filesystems') as fs:
            for line in fs:
                self.filesystems.append(line.rstrip('\n').split('\t')[1])

        self.libcloader = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)

    def mount(self, source, destination, filesystem, flags):
        if not os.access(source, os.R_OK):
            raise Exception("Could not find path " + source)
        if not os.access(destination, os.F_OK):
            os.mkdir(destination)
        if not os.access(destination, os.W_OK):
            raise Exception("Could not write to path " + destination)
        if filesystem not in self.filesystems:
            raise ValueError("Filesystem unknown")
        ret = self.libcloader.mount(ctypes.c_char_p(source),
                                    ctypes.c_char_p(destination),
                                    ctypes.c_char_p(filesystem),
                                    ctypes.c_char_p(flags),
                                    0)
        if ret != 0:
            raise RuntimeError(
                "Cannot mount {} : {}".format(source, os.strerror(ctypes.get_errno())))

    def umount(self, destination):
        ret = self.libcloader.umount(ctypes.c_char_p(destination))
        if ret != 0:
            raise RuntimeError(
                "Cannot umount {} : {}".format(destination, os.strerror(ctypes.get_errno())))
    @staticmethod
    def jsonread(filename):
        json_data = open(filename)
        data = json.load(json_data, object_pairs_hook=collections.OrderedDict)
        json_data.close()
        return data

    @staticmethod
    def runshellcommand(cmd, ignore_errors=False):
        print(cmd)
        command = cmd.split()
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if not ignore_errors:
            if rc != 0:
                print(err)
                raise RuntimeError("Cannot run command {}".format(cmd))
        return output.decode()

    @staticmethod
    def replaceinfile(filename, pattern, sub):
        for line in fileinput.input(filename, inplace=True):
            line = re.sub(pattern, sub, line)
            print(line)

    @staticmethod
    def replaceandsaveasnewfile(old_file, new_file, pattern, sub):
        with open(old_file, "r") as old, open(new_file, "w") as new:
            for line in old:
                line = re.sub(pattern, sub, line)
                new.write(line)

    @staticmethod
    def copyallfiles(src, target):
        files = os.listdir(src)
        for file in files:
            filename = os.path.join(src, file)
            if os.path.isfile(filename):
                shutil.copy(filename, target)
