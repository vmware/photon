import sys
import os.path
import subprocess
import shutil
import docker
from constants import constants
from Logger import Logger
from CommandUtils import CommandUtils

class Sandbox(object):
    def __init__(self, logger):
        self.logger = logger

    def create(self, name):
        pass

    def destroy(self):
        pass

    def run(self, logfile, logfn):
        pass

    def put(self, src, dest):
        pass

class Chroot(Sandbox):
    def __init__(self, logger):
        Sandbox.__init__(self, logger)
        self.chrootID = None
        self.prepareBuildRootCmd = "./prepare-build-root.sh"
        self.runInChrootCommand = ("./run-in-chroot.sh " + constants.sourcePath +
                                   " " + constants.rpmPath)
        self.chrootCmdPrefix = None

    def getPath(self):
        return self.chrootID

    def create(self, chrootName):
        if self.chrootID:
            raise Exception("Unable to create: " + chrootName + ". Chroot is already active: " + self.chrootID)

        chrootID = constants.buildRootPath + "/" + chrootName
        if os.path.isdir(chrootID):
            self._destroy(chrootID)

        # need to add timeout for this step
        # http://stackoverflow.com/questions/1191374/subprocess-with-timeout
        cmdUtils = CommandUtils()
        returnVal = cmdUtils.runCommandInShell("mkdir -p " + chrootID)
        if returnVal != 0:
            raise Exception("Unable to create chroot: " + chrootID + ". Unknown error.")
        self.logger.debug("Created new chroot: " + chrootID)

        cmdUtils.runCommandInShell("mkdir -p " + chrootID + "/dev")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + "/etc")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + "/proc")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + "/run")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + "/sys")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + "/tmp")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + "/publishrpms")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + "/publishxrpms")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + constants.topDirPath)
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + constants.topDirPath + "/RPMS")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + constants.topDirPath + "/SRPMS")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + constants.topDirPath + "/SOURCES")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + constants.topDirPath + "/SPECS")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + constants.topDirPath + "/LOGS")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + constants.topDirPath + "/BUILD")
        cmdUtils.runCommandInShell("mkdir -p " + chrootID + constants.topDirPath + "/BUILDROOT")

        prepareChrootCmd = self.prepareBuildRootCmd + " " + chrootID
        returnVal = cmdUtils.runCommandInShell(prepareChrootCmd, logfn=self.logger.debug)
        if returnVal != 0:
            self.logger.error("Prepare build root script failed.Unable to prepare chroot.")
            raise Exception("Prepare build root script failed")

        if os.geteuid() == 0:
            cmdUtils.runCommandInShell("mount --bind " + constants.rpmPath + " " +
                                        chrootID + constants.topDirPath + "/RPMS")
            cmdUtils.runCommandInShell("mount --bind " + constants.sourceRpmPath + " " +
                                        chrootID + constants.topDirPath + "/SRPMS")
            cmdUtils.runCommandInShell("mount -o ro --bind " + constants.prevPublishRPMRepo + " " +
                                        chrootID + "/publishrpms")
            cmdUtils.runCommandInShell("mount -o ro --bind " + constants.prevPublishXRPMRepo + " " +
                                        chrootID + "/publishxrpms")

        self.logger.debug("Successfully created chroot:" + chrootID)

        self.chrootID = chrootID
        self.chrootCmdPrefix = self.runInChrootCommand + " " + chrootID + " "

    def destroy(self):
        self._destroy(self.chrootID)
        self.chrootID = None

    def _destroy(self, chrootID):
        if not chrootID:
            return
        self.logger.debug("Deleting chroot: " + chrootID)
        self._unmountAll(chrootID)
        self._removeChroot(chrootID)

    def run(self, cmd, logfile=None, logfn=None):
        self.logger.debug("Chroot.run() cmd: " + self.chrootCmdPrefix + cmd)
        cmd = cmd.replace('"', '\\"')
        return CommandUtils.runCommandInShell(self.chrootCmdPrefix + cmd, logfile, logfn)

    def put(self, src, dest):
        shutil.copy2(src, self.chrootID + dest)

    def _removeChroot(self, chrootPath):
        cmd = "rm -rf " + chrootPath
        process = subprocess.Popen("%s" %cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            raise Exception("Unable to remove files from chroot " + chrootPath)

    def unmountAll(self):
        self._unmountAll(self.chrootID)

    def _unmountAll(self, chrootID):
        listmountpoints = self._findmountpoints(chrootID)
        if listmountpoints is None:
            return True
        for mountpoint in listmountpoints:
            cmd = "umount " + mountpoint
            process = subprocess.Popen("%s" %cmd, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            retval = process.wait()
            if retval != 0:
                raise Exception("Unable to unmount " + mountpoint)

    def _findmountpoints(self, chrootPath):
        if not chrootPath.endswith("/"):
            chrootPath = chrootPath + "/"
        cmd = "mount | grep " + chrootPath + " | cut -d' ' -s -f3"
        process = subprocess.Popen("%s" %cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            raise Exception("Unable to find mountpoints in chroot")

        mountpoints = process.communicate()[0].decode()
        mountpoints = mountpoints.replace("\n", " ").strip()
        if mountpoints == "":
            self.logger.debug("No mount points found")
            return None
        listmountpoints = mountpoints.split(" ")
        sorted(listmountpoints)
        listmountpoints.reverse()
        return listmountpoints


class Container(Sandbox):
    def __init__(self, logger):
        Sandbox.__init__(self, logger)
        self.containerID = None
        self.dockerClient = docker.from_env(version="auto")

    def getID(self):
        return self.containerID.short_id

    def create(self, containerName):
        containerID = None
        mountVols = {
            constants.prevPublishRPMRepo: {'bind': '/publishrpms', 'mode': 'ro'},
            constants.prevPublishXRPMRepo: {'bind': '/publishxrpms', 'mode': 'ro'},
            constants.tmpDirPath: {'bind': '/tmp', 'mode': 'rw'},
            constants.rpmPath: {'bind': constants.topDirPath + "/RPMS", 'mode': 'rw'},
            constants.sourceRpmPath: {'bind': constants.topDirPath + "/SRPMS", 'mode': 'rw'},
#            constants.logPath: {'bind': constants.topDirPath + "/LOGS", 'mode': 'rw'},
        # Prepare an empty chroot environment to let docker use the BUILD folder.
        # This avoids docker using overlayFS which will cause make check failure.

#            chroot.getPath() + constants.topDirPath + "/BUILD": {'bind': constants.topDirPath + "/BUILD",
#                                                         'mode': 'rw'},
            constants.dockerUnixSocket: {'bind': constants.dockerUnixSocket, 'mode': 'rw'}
            }

        containerName = containerName.replace("+", "p")
        try:
            oldContainerID = self.dockerClient.containers.get(containerName)
            if oldContainerID is not None:
                oldContainerID.remove(force=True)
        except docker.errors.NotFound:
            try:
                sys.exc_clear()
            except:
                pass

        #TODO: Is init=True equivalent of --sig-proxy?
        privilegedDocker = False
        cap_list = ['SYS_PTRACE']
#            if packageName in constants.listReqPrivilegedDockerForTest:
#                privilegedDocker = True

        containerID = self.dockerClient.containers.run(constants.buildContainerImage,
                                                       detach=True,
                                                       cap_add=cap_list,
#                                                           privileged=privilegedDocker,
                                                       privileged=False,
                                                       name=containerName,
                                                       network_mode="host",
                                                       volumes=mountVols,
                                                       command="tail -f /dev/null")

        if not containerID:
            raise Exception("Unable to start Photon build container for task " +
                            containerTaskName)
        self.logger.debug("Successfully created container:" + containerID.short_id)
        self.containerID = containerID

    def destroy(self):
        self.containerID.remove(force=True)
        self.containerID = None

    def run(self, cmd, logfile=None, logfn=None):
        result = self.containerID.exec_run(cmd)
        if result.output:
            if logfn:
                logfn(result.output.decode())
            elif logfile:
                with open(logfile, "w") as f:
                    f.write(result.output.decode())
                    f.flush()
        return result.exit_code

    def put(self, src, dest):
        copyCmd = "docker cp " + src + " " + self.containerID.short_id + ":" + dest
        CommandUtils.runCommandInShell(copyCmd)

