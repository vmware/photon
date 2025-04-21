#!/usr/bin/env python3

import os.path
import subprocess
import shutil
import time
import docker

from constants import constants
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

    def getID(self):
        pass

    def hasToolchain(self):
        return False


class Chroot(Sandbox):
    def __init__(self, logger):
        Sandbox.__init__(self, logger)
        self.chrootID = None
        self.prepareBuildRootCmd = os.path.join(os.path.dirname(__file__), "prepare-build-root.sh")
        self.runInChrootCommand = str(os.path.join(os.path.dirname(__file__), "run-in-chroot.sh"))
        self.runInChrootCommand += f" {constants.sourcePath} {constants.rpmPath}"
        self.chrootCmdPrefix = None
        self.cmdUtils = CommandUtils()

    def getID(self):
        return self.chrootID

    def create(self, chrootName):
        if self.chrootID:
            raise Exception(f"Unable to create: {chrootName}. Chroot is already active: {self.chrootID}")

        chrootID = f"{constants.buildRootPath}/{chrootName}"
        self.chrootID = chrootID
        self.chrootCmdPrefix = f"{self.runInChrootCommand} {chrootID} "
        if os.path.isdir(chrootID):
            if constants.resume_build:
                return
            self._destroy(chrootID)

        top_dirs = "dev,etc,proc,run,sys,tmp,publishrpms,publishxrpms,inputrpms"
        extra_dirs = "RPMS,SRPMS,SOURCES,SPECS,LOGS,BUILD,BUILDROOT"
        cmd = (
            f"mkdir -p {chrootID}/{{{top_dirs}}} {chrootID}/{constants.topDirPath}/{{{extra_dirs}}}"
        )

        # Need to add timeout for this step
        # http://stackoverflow.com/questions/1191374/subprocess-with-timeout
        if self.cmdUtils.runCommandInShell(cmd):
            self.logger.error("Prepare build root script failed.Unable to prepare chroot.")
            raise Exception(f"Unable to create chroot: {chrootID}. Unknown error.")

        self.logger.debug(f"Created new chroot: {chrootID}")

        prepareChrootCmd = f"{self.prepareBuildRootCmd} {chrootID}"
        if self.cmdUtils.runCommandInShell(prepareChrootCmd, logfn=self.logger.debug):
            self.logger.error("Prepare build root script failed. Unable to prepare chroot.")
            raise Exception("Prepare build root script failed")

        if os.geteuid() == 0:
            cmd = (
                f"mount --bind {constants.rpmPath} {chrootID}{constants.topDirPath}/RPMS"
                f" && mount --bind {constants.sourceRpmPath} {chrootID}{constants.topDirPath}/SRPMS"
                f" && mount -o ro --bind {constants.prevPublishRPMRepo} {chrootID}/publishrpms"
                f" && mount -o ro --bind {constants.prevPublishXRPMRepo} {chrootID}/publishxrpms"
            )
            if constants.inputRPMSPath:
                cmd += f" && mount -o ro --bind {constants.inputRPMSPath} {chrootID}/inputrpms"

            if self.cmdUtils.runCommandInShell(cmd):
                msg = f"failed to mount directories in {chrootID}"
                self.logger.error(msg)
                raise Exception(msg)

        self.logger.debug(f"Successfully created chroot: {chrootID}")

    def destroy(self):
        self._destroy(self.chrootID)
        self.chrootID = None

    def _destroy(self, chrootID):
        if not chrootID:
            return
        self.logger.debug(f"Deleting chroot: {chrootID}")
        self._unmountAll(chrootID)
        self._removeChroot(chrootID)

    def run(self, cmd, logfile=None, logfn=None):
        self.logger.debug(f"Chroot.run() cmd: {self.chrootCmdPrefix}{cmd}")
        cmd = cmd.replace('"', '\\"')
        return self.cmdUtils.runCommandInShell(f"{self.chrootCmdPrefix}{cmd}", logfile, logfn)

    def put(self, src, dest):
        shutil.copy2(src, f"{self.chrootID}{dest}")

    def put_list_of_files(self, sources, dest):
        if isinstance(sources, list):
            sources = " ".join(sources)
        cmd = f"cp -p {sources} {self.chrootID}{dest}"
        self.logger.debug(cmd)
        self.cmdUtils.runBashCmd(cmd)

    def _removeChroot(self, chrootPath):
        cmd = f"rm -rf {chrootPath}"
        if self.cmdUtils.runCommandInShell(cmd, logfn=self.logger.debug):
            self.logger.debug(f"Unable to remove files from chroot {chrootPath}")
            # Some files are hold by some processes?
            # Print lsof output, wait 10 seconds and repeat
            self.cmdUtils.runCommandInShell(f"lsof +D {chrootPath}", logfn=self.logger.debug)
            time.sleep(10)
            if self.cmdUtils.runCommandInShell(cmd, logfn=self.logger.debug):
                raise Exception(f"Unable to remove files from chroot {chrootPath}")

    def unmountAll(self):
        self._unmountAll(self.chrootID)

    def _unmountAll(self, chrootID):
        listmountpoints = self._findmountpoints(chrootID)
        if listmountpoints is None:
            return True
        for mountpoint in listmountpoints:
            cmd = f"umount {mountpoint}"
            process = subprocess.Popen(f"{cmd} && sync && sync && sync",
                                       shell=True, executable="/bin/bash",
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            if process.wait():
                # Try unmount with lazy umount
                cmd = f"umount -l {mountpoint}"
                process = subprocess.Popen(f"{cmd} && sync && sync && sync",
                                           shell=True, executable="/bin/bash",
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                if process.wait():
                    raise Exception(f"Unable to unmount {mountpoint}")

    def _findmountpoints(self, chrootPath):
        if not chrootPath.endswith("/"):
            chrootPath += "/"
        cmd = f"mount | grep {chrootPath} | cut -d' ' -s -f3"
        process = subprocess.Popen(f"{cmd}", shell=True, executable="/bin/bash",
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        if process.wait():
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
            #constants.logPath: {'bind': constants.topDirPath + "/LOGS", 'mode': 'rw'},
            # Prepare an empty chroot environment to let docker use the BUILD folder.
            # This avoids docker using overlayFS which will cause make check failure.
            #chroot.getID() + constants.topDirPath + "/BUILD": {'bind': constants.topDirPath + "/BUILD", 'mode': 'rw'},
            constants.dockerUnixSocket: {'bind': constants.dockerUnixSocket, 'mode': 'rw'}
        }

        if constants.inputRPMSPath:
            mountVols[constants.inputRPMSPath] = {'bind': '/inputrpms', 'mode': 'ro'}

        containerName = containerName.replace("+", "p")
        try:
            oldContainerID = self.dockerClient.containers.get(containerName)
            if oldContainerID is not None:
                oldContainerID.remove(force=True)
        except Exception:
            pass

        # TODO: Is init=True equivalent of --sig-proxy?
        #privilegedDocker = False
        cap_list = ['SYS_PTRACE']
        #if packageName in constants.listReqPrivilegedDockerForTest:
            #privilegedDocker = True

        containerID = self.dockerClient.containers.run(constants.buildContainerImage,
                                                       detach=True,
                                                       cap_add=cap_list,
                                                       #privileged=privilegedDocker,
                                                       privileged=False,
                                                       name=containerName,
                                                       network_mode="host",
                                                       volumes=mountVols,
                                                       command="tail -f /dev/null")
        if not containerID:
            raise Exception(f"Unable to start Photon build container for task {containerName}")
        self.logger.debug(f"Successfully created container: {containerID.short_id}")
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
        copyCmd = f"docker cp {src} {self.containerID.short_id}:{dest}"
        self.cmdUtils.runCommandInShell(copyCmd)

    def hasToolchain(self):
        return True
