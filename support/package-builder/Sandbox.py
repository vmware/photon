#!/usr/bin/env python3

import sys
import os.path
import shutil
import docker

from constants import constants
from CommandUtils import CommandUtils


class Sandbox(object):
    def __init__(self, logger, cmdlog = lambda cmd: None):
        self.logger = logger
        self.cmdlog = cmdlog

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
    def __init__(self, logger, cmdlog = lambda cmd: None):
        Sandbox.__init__(self, logger, cmdlog)
        self.chrootID = None
        self.prepareBuildRootCmd = os.path.join(
            os.path.dirname(__file__), "prepare-build-root.sh"
        )
        self.runInChrootCommand = str(
            os.path.join(os.path.dirname(__file__), "run-in-chroot.sh")
        )
        self.runInChrootCommand += (
            f" {constants.sourcePath} {constants.rpmPath}"
        )
        self.chrootCmdPrefix = None
        self.cmdUtils = CommandUtils()

    def getID(self):
        return self.chrootID

    def create(self, chrootName):
        if self.chrootID:
            raise Exception(
                f"Unable to create: {chrootName}. "
                f"Chroot is already active: {self.chrootID}"
            )

        chrootID = f"{constants.buildRootPath}/{chrootName}"
        self.chrootID = chrootID
        self.chrootCmdPrefix = f"{self.runInChrootCommand} {chrootID} "
        if os.path.isdir(chrootID):
            if constants.resume_build:
                return
            self._destroy(chrootID)

        top_dirs = (
            "dev,etc,proc,run,sys,tmp,publishrpms,publishxrpms,inputrpms"
        )
        extra_dirs = "RPMS,SRPMS,SOURCES,SPECS,LOGS,BUILD,BUILDROOT"
        cmd = f"mkdir -p {chrootID}/{{{top_dirs}}} {chrootID}/{constants.topDirPath}/{{{extra_dirs}}}"  # noqa: E501

        self.cmdlog(cmd)
        # Need to add timeout for this step
        # http://stackoverflow.com/questions/1191374/subprocess-with-timeout
        self.cmdUtils.runBashCmd(cmd)

        self.logger.debug(f"Created new chroot: {chrootID}")

        prepareChrootCmd = f"{self.prepareBuildRootCmd} {chrootID}"
        self.cmdlog(prepareChrootCmd)
        self.cmdUtils.runBashCmd(prepareChrootCmd, logfn=self.logger.debug)

        if os.geteuid() == 0:
            cmd = (
                f"mount --bind {constants.rpmPath} {chrootID}{constants.topDirPath}/RPMS"  # noqa: E501
                f" && mount --bind {constants.sourceRpmPath} {chrootID}{constants.topDirPath}/SRPMS"  # noqa: E501
                f" && mount -o ro --bind {constants.prevPublishRPMRepo} {chrootID}/publishrpms"  # noqa: E501
                f" && mount -o ro --bind {constants.prevPublishXRPMRepo} {chrootID}/publishxrpms"  # noqa: E501
            )
            if constants.inputRPMSPath:
                cmd += f" && mount -o ro --bind {constants.inputRPMSPath} {chrootID}/inputrpms"  # noqa: E501

            self.cmdlog(cmd)
            self.cmdUtils.runBashCmd(cmd)

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

    def run(self, cmd, logfile=None, logfn=None, network_required=False):
        self.logger.debug(f"Chroot.run() cmd: {self.chrootCmdPrefix}{cmd}")
        cmd = cmd.replace('"', '\\"')
        self.cmdlog(f"{self.chrootCmdPrefix}{cmd}")
        (_, _, retval) = self.cmdUtils.runBashCmd(
            f"{self.chrootCmdPrefix}{cmd}", logfile, logfn
        )
        return retval

    def put(self, src, dest):
        shutil.copy2(src, f"{self.chrootID}{dest}")

    def put_list_of_files(self, sources, dest):
        if type(sources) == list:
            sources = " ".join(sources)
        cmd = f"cp -p {sources} {self.chrootID}{dest}"
        self.logger.debug(cmd)
        self.cmdlog(cmd)
        self.cmdUtils.runBashCmd(cmd)

    def _removeChroot(self, chrootPath):
        cmd = f"rm -rf {chrootPath}"
        self.cmdlog(cmd)
        self.cmdUtils.runBashCmd(cmd, logfn=self.logger.debug)

    def unmountAll(self):
        self._unmountAll(self.chrootID)

    def _unmountAll(self, chrootID):
        listmountpoints = self._findmountpoints(chrootID)
        if listmountpoints is None:
            return True
        for mountpoint in listmountpoints:
            cmd = f"umount {mountpoint} && sync"
            self.cmdlog(cmd)
            _, _, rc = self.cmdUtils.runBashCmd(cmd, ignore_rc=True)
            if rc:
                # Try unmount with lazy umount
                cmd = f"umount -l {mountpoint} && sync"
                self.cmdlog(cmd)
                self.cmdUtils.runBashCmd(cmd)

    def _findmountpoints(self, chrootPath):
        if not chrootPath.endswith("/"):
            chrootPath += "/"
        cmd = f"mount | grep {chrootPath} | cut -d' ' -s -f3"
        self.cmdlog(cmd)
        mountpoints, _, _ = self.cmdUtils.runBashCmd(cmd, capture=True)

        mountpoints = mountpoints.replace("\n", " ").strip()
        if mountpoints == "":
            self.logger.debug("No mount points found")
            return None
        listmountpoints = mountpoints.split(" ")
        sorted(listmountpoints)
        listmountpoints.reverse()
        return listmountpoints

class SystemdNspawn(Sandbox):
    def __init__(self, logger, cmdlog = lambda cmd: None):
        Sandbox.__init__(self, logger, cmdlog)
        self.chrootID = None
        self.nspawnCmdPrefix = None
        self.cmdUtils = CommandUtils()

    def getID(self):
        return self.chrootID

    def create(self, chrootName):
        if self.chrootID:
            raise Exception(f"Unable to create: {chrootName}. Chroot is already active: {self.chrootID}")

        chrootID = f"{constants.buildRootPath}/{chrootName}"
        self.chrootID = chrootID
        self.nspawnCmdPrefix = f"SYSTEMD_NSPAWN_TMPFS_TMP=0 systemd-nspawn --quiet --directory {chrootID} " \
            f"--bind {constants.rpmPath}:{constants.topDirPath}/RPMS " \
            f"--bind {constants.sourceRpmPath}:{constants.topDirPath}/SRPMS " \
            f"--bind-ro {constants.prevPublishRPMRepo}:/publishrpms " \
            f"--bind-ro {constants.prevPublishXRPMRepo}:/publishxrpms "

        if constants.inputRPMSPath:
            self.nspawnCmdPrefix += f"--bind-ro {constants.inputRPMSPath}:/inputrpms "

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
        self.cmdlog(cmd)
        self.cmdUtils.runBashCmd(cmd)

        self.logger.debug(f"Created new chroot: {chrootID}")

        self.logger.debug(f"Successfully created chroot: {chrootID}")

    def destroy(self):
        self._destroy(self.chrootID)
        self.chrootID = None

    def _destroy(self, chrootID):
        if not chrootID:
            return
        self.logger.debug(f"Deleting chroot: {chrootID}")
        cmd = f"rm -rf {chrootID}"
        self.cmdlog(cmd)
        self.cmdUtils.runBashCmd(cmd, logfn=self.logger.debug)

    def run(self, cmd, logfile=None, logfn=None, network_required=False):
        self.logger.debug(f"systemd-nspawn.run() cmd: {self.nspawnCmdPrefix}{cmd}")
        self.cmdlog(f"{self.nspawnCmdPrefix}{cmd}")
        (_, _, retval) = self.cmdUtils.runBashCmd(f"{self.nspawnCmdPrefix}{cmd}", logfile, logfn)
        return retval

    def put(self, src, dest):
        shutil.copy2(src, f"{self.chrootID}{dest}")

    def put_list_of_files(self, sources, dest):
        if type(sources) == list:
            sources = " ".join(sources)
        cmd = f"cp -p {sources} {self.chrootID}{dest}"
        self.logger.debug(cmd)
        self.cmdlog(cmd)
        self.cmdUtils.runBashCmd(cmd)

class Container(Sandbox):
    def __init__(self, logger, cmdlog = lambda cmd: None):
        Sandbox.__init__(self, logger, cmdlog)
        self.containerID = None
        self.dockerClient = docker.from_env(version="auto")

    def getID(self):
        return self.containerID.short_id

    def create(self, containerName):
        containerID = None
        mountVols = {
            constants.prevPublishRPMRepo: {
                "bind": "/publishrpms",
                "mode": "ro",
            },
            constants.prevPublishXRPMRepo: {
                "bind": "/publishxrpms",
                "mode": "ro",
            },
            constants.tmpDirPath: {"bind": "/tmp", "mode": "rw"},
            constants.rpmPath: {
                "bind": f"{constants.topDirPath}/RPMS",
                "mode": "rw",
            },
            constants.sourceRpmPath: {
                "bind": f"{constants.topDirPath}/SRPMS",
                "mode": "rw",
            },
            constants.dockerUnixSocket: {
                "bind": constants.dockerUnixSocket,
                "mode": "rw",
            },
        }

        if constants.inputRPMSPath:
            mountVols[constants.inputRPMSPath] = {
                "bind": "/inputrpms",
                "mode": "ro",
            }

        containerName = containerName.replace("+", "p")
        try:
            oldContainerID = self.dockerClient.containers.get(containerName)
            if oldContainerID:
                oldContainerID.remove(force=True)
        except docker.errors.NotFound:
            try:
                sys.exc_clear()
            except Exception:
                pass

        #  TODO: Is init=True equivalent of --sig-proxy?
        #  privilegedDocker = False
        cap_list = ["SYS_PTRACE"]
        #  if packageName in constants.listReqPrivilegedDockerForTest:
        #  privilegedDocker = True

        containerID = self.dockerClient.containers.run(
            constants.buildContainerImage,
            detach=True,
            cap_add=cap_list,
            # privileged=privilegedDocker,
            privileged=False,
            name=containerName,
            network_mode="host",
            volumes=mountVols,
            command="tail -f /dev/null",
        )
        if not containerID:
            raise Exception(
                "Unable to start Photon build container for task "
                "tail -f /dev/null"
            )
        self.logger.debug(
            f"Successfully created container: {containerID.short_id}"
        )
        self.containerID = containerID

    def run(self, cmd, logfile=None, logfn=None, network_required=False):
        self.cmdlog(cmd)
        result = self.containerID.exec_run(cmd)
        if result.output:
            if logfn:
                logfn(result.output.decode())
            elif logfile:
                with open(logfile, "w") as f:
                    f.write(result.output.decode())
                    f.flush()
        return result.exit_code

    def destroy(self):
        self.containerID.remove(force=True)
        self.containerID = None

    def put(self, src, dest):
        copyCmd = f"docker cp {src} {self.containerID.short_id}:{dest}"
        self.cmdlog(copyCmd)
        self.cmdUtils.runBashCmd(copyCmd)

    def hasToolchain(self):
        return True
