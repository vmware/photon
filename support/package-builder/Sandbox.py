#!/usr/bin/env python3

import sys
import os.path
import shutil
import time
import tempfile

from constants import constants
from Logger import Logger
from CommandUtils import CommandUtils


class Sandbox(object):
    def __init__(self, logger, cmdlog = lambda cmd: None):
        self.logger = logger
        self.cmdlog = cmdlog

    def create(self, name):
        pass

    def destroy(self):
        pass

    def run(self, logfile, logfn, network_required):
        pass

    def put(self, src, dest):
        pass

    def getID(self):
        pass

    def hasToolchain(self):
        return False

    def getObservationFile(self):
        return None

    def removeObservationFile(self):
        pass

class Chroot(Sandbox):
    def __init__(self, logger, cmdlog = lambda cmd: None):
        Sandbox.__init__(self, logger, cmdlog)
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
                f"mount --bind {constants.rpmPath} {chrootID}{constants.topDirPath}/RPMS"
                f" && mount --bind {constants.sourceRpmPath} {chrootID}{constants.topDirPath}/SRPMS"
                f" && mount -o ro --bind {constants.prevPublishRPMRepo} {chrootID}/publishrpms"
                f" && mount -o ro --bind {constants.prevPublishXRPMRepo} {chrootID}/publishxrpms"
            )
            if constants.inputRPMSPath:
                cmd += f" && mount -o ro --bind {constants.inputRPMSPath} {chrootID}/inputrpms"

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
        (_, _, retval) = self.cmdUtils.runBashCmd(f"{self.chrootCmdPrefix}{cmd}", logfile, logfn)
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
        import docker

        Sandbox.__init__(self, logger, cmdlog)
        self.chrootID = None
        self.chrootName = None
        self.nspawnCmdPrefix = None
        self.observationFile = None
        self.cmdUtils = CommandUtils()
        self.dockerClient = docker.from_env(version="auto")
        self.observerContainer = None
        self.observerURL = "http://127.0.0.1:8989"

    def getID(self):
        return self.chrootID

    def create(self, chrootName):
        if self.chrootID:
            raise Exception(f"Unable to create: {chrootName}. Chroot is already active: {self.chrootID}")

        self.chrootName = chrootName
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

    def _startObserver(self):
        if not constants.observerDockerImage:
            self.logger.warning("Unable to start an observer container. Docker image is not provided.")
            return None
        runArgs = {
            "image": constants.observerDockerImage,
            "command": "tail -f /dev/null",
            "detach": True,
            "privileged": False,
            "name": self.chrootName,
            # Map tls/certs folder of the sandbox in observer container. So, observer can modify certificates and hijack a traffic.
            "volumes": {f"{self.chrootID}/etc/pki/tls/certs": {'bind': "/etc/pki/tls/certs", 'mode': 'rw'}}
        }
        if constants.isolatedDockerNetwork:
            runArgs["network"] = constants.isolatedDockerNetwork
        else:
            runArgs["network_mode"] = "bridge"

        observerContainer = self.dockerClient.containers.run(**runArgs)
        if not observerContainer:
            self.logger.warning("Unable to start an observer. Docker run failed.")
            return None
        self.observerContainer = observerContainer
        result = self.observerContainer.exec_run("/observer/bin/observer_agent -m start_observer")
        if result.exit_code:
            self.logger.warning("Unable to start an observer daemon")
            self.observerContainer.remove(force=True)
            self.observerContainer = None
            return None

        # Update attributes
        self.observerContainer.reload()
        # Return network namespace path systemd-nspawn attach to
        return self.observerContainer.attrs['NetworkSettings']['SandboxKey']

    def _stopObserver(self):
        result = self.observerContainer.exec_run("/observer/bin/observer_agent -m stop_observer")
        if result.exit_code:
            self.logger.warning("Unable to stop an observer daemon. No observation file provided")
            self.observerContainer.remove(force=True)
            self.observerContainer = None
            return

        result = self.observerContainer.exec_run("cat /provenance.json")
        if result.exit_code:
            self.logger.warning("No observation file provided")
            self.observerContainer.remove(force=True)
            self.observerContainer = None
            return

        with tempfile.NamedTemporaryFile(prefix=f"{self.chrootName}_", suffix="_observations.json", delete=False) as f:
            filename = f.name
            f.write(result.output)
            f.flush()

        self.observationFile = filename
        self.observerContainer.remove(force=True)
        self.observerContainer = None

    def run(self, cmd, logfile=None, logfn=None, network_required=False):
        netnsPath = None
        if network_required:
            # Processes in a sandbox may access external resources only through proxy.
            # We use SRP observer as a proxy, which also records all proxy activities to provenance observation file.
            # Observer daemon will be run in a docker container, and systemd-nspawn instance will be attached to the
            # same network namespace. It will allow rpmbuild children access observer via local 127.0.0.1:8989 port
            netnsPath = self._startObserver()
            if not netnsPath:
                self.logger.warning("Observer is not available. Sandbox will not have a networking")


        if netnsPath:
            cmdPrefix = f"{self.nspawnCmdPrefix} --network-namespace-path={netnsPath} --setenv=HTTP_PROXY={self.observerURL} --setenv=HTTPS_PROXY={self.observerURL} --setenv=http_proxy={self.observerURL} --setenv=https_proxy={self.observerURL} "
        else:
            cmdPrefix = f"{self.nspawnCmdPrefix} --private-network "

        self.logger.debug(f"systemd-nspawn.run() cmd: {cmdPrefix}{cmd}")
        self.cmdlog(f"{cmdPrefix}{cmd}")
        try:
            (_, _, retval) = self.cmdUtils.runBashCmd(f"{cmdPrefix}{cmd}", logfile, logfn)
        finally:
            if netnsPath:
                self._stopObserver()
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

    def getObservationFile(self):
        return self.observationFile

    def removeObservationFile(self):
        if self.observationFile and os.path.isfile(self.observationFile):
            os.remove(self.observationFile)
        self.observationFile = None


class Container(Sandbox):
    def __init__(self, logger, cmdlog = lambda cmd: None):
        import docker
        Sandbox.__init__(self, logger, cmdlog)
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
        except docker.errors.NotFound:
            try:
                sys.exc_clear()
            except:
                pass

        # TODO: Is init=True equivalent of --sig-proxy?
        privilegedDocker = False
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
            raise Exception(f"Unable to start Photon build container for task {containerTaskName}")
        self.logger.debug(f"Successfully created container: {containerID.short_id}")
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
