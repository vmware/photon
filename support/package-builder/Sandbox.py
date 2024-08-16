#!/usr/bin/env python3

import io
import sys
import shutil
import os.path
import shutil
import docker
import time
import tempfile
import tarfile
import subprocess

from datetime import datetime
from contextlib import suppress
from constants import constants
from CommandUtils import CommandUtils

sandboxDefaultEnv = {
    "HOME": "/root",
    "TERM": "linux",
    "PATH": "/bin:/usr/bin:/sbin:/usr/sbin",
    "SHELL": "/bin/bash",
}


def prepare_chroot_dirs(rootPath):
    top_dirs = [
        "dev",
        "etc",
        "proc",
        "run",
        "sys",
        "tmp",
        "publishrpms",
        "publishxrpms",
        "inputrpms",
    ]
    extra_dirs = ["RPMS", "SRPMS", "SOURCES", "SPECS", "LOGS", "BUILD", "BUILDROOT"]
    for d in top_dirs:
        os.makedirs(os.path.join(rootPath, d), exist_ok=True)
    for d in extra_dirs:
        os.makedirs(os.path.join(rootPath + constants.topDirPath, d), exist_ok=True)


def tar_chroot(rootPath, fmt):
    if fmt != "tar" and fmt != "tgz":
        raise Exception(f"Chroot.archive(): format {fmt} not supported")
    cmd = ["tar", "--one-file-system", "--xattrs", "-S", "-C", rootPath, "-c", "."]
    if fmt == "tgz":
        cmd += ["-z"]
    tarf = tempfile.TemporaryFile(mode="w+b")
    try:
        subprocess.run(cmd, stdout=tarf, check=True)
    except:
        tarf.close()
        raise
    tarf.seek(0, 0)
    return tarf


class Sandbox(object):
    def __init__(self, name, logger, cmdAudit=lambda cmd, env: None):
        self.name = name
        self.logger = logger
        self.cmdAudit = cmdAudit

    def create(self):
        pass

    def destroy(self):
        pass

    def runCmd(self, network_required=False, **kwargs):
        pass

    def archive(self, fmt="tar"):
        pass

    def putFiles(self, src, dest):
        pass

    def hasToolchain(self):
        return False

    def getObservation(self):
        return None

    def getRootPath(self):
        pass

    def _cmd(self, cmd, env={}, cwd=None, **kwargs):
        if cwd is not None:
            raise Exception("Should not specify cwd in Sandbox.runCmd()")
        self.cmdAudit(cmd, env)
        return CommandUtils.runCmd(cmd, env=env, **kwargs)


class Chroot(Sandbox):
    def __init__(self, name, logger, cmdAudit=lambda cmd, env: None):
        Sandbox.__init__(self, name, logger, cmdAudit)
        self.chrootPath = os.path.join(constants.buildRootPath, self.name)
        self.prepareBuildRootCmd = os.path.join(
            os.path.dirname(__file__), "prepare-build-root.sh"
        )

    def create(self):
        if os.geteuid() != 0:
            raise Exception(f"Unable to create {self.name} as non-root user")

        if os.path.isdir(self.chrootPath):
            if constants.resume_build:
                return
            self.destroy()

        prepare_chroot_dirs(self.chrootPath)

        prepareCmds = [
            [self.prepareBuildRootCmd, self.chrootPath],
            [
                "mount",
                "--bind",
                constants.rpmPath,
                os.path.join(self.chrootPath + constants.topDirPath, "RPMS"),
            ],
            [
                "mount",
                "--bind",
                constants.sourceRpmPath,
                os.path.join(self.chrootPath + constants.topDirPath, "SRPMS"),
            ],
            [
                "mount",
                "-o",
                "ro",
                "--bind",
                constants.prevPublishRPMRepo,
                os.path.join(self.chrootPath, "publishrpms"),
            ],
            [
                "mount",
                "-o",
                "ro",
                "--bind",
                constants.prevPublishXRPMRepo,
                os.path.join(self.chrootPath, "publishxrpms"),
            ],
        ]
        if constants.inputRPMSPath:
            prepareCmds.append(
                [
                    "mount",
                    "-o",
                    "ro",
                    "--bind",
                    constants.inputRPMSPath,
                    os.path.join(self.chrootPath, "inputrpms"),
                ]
            )

        for cmd in prepareCmds:
            self._cmd(cmd)

        self.logger.debug(f"Successfully created chroot: {self.chrootPath}")

    def destroy(self):
        self.logger.debug(f"Deleting chroot: {self.chrootPath}")
        self._unmountAll()
        self._cmd(["rm", "--one-file-system", "-rf", self.chrootPath])

    def runCmd(
        self, cmd, network_required=False, env={}, clean_env=True, shell=False, **kwargs
    ):
        if shell:
            raise Exception("Chroot.runCmd() does not support shell=True")
        env = {**sandboxDefaultEnv, **env}
        self.logger.debug(f"Chroot.runCmd({cmd}, env={env})")
        return self._cmd(
            ["chroot", self.chrootPath] + cmd, clean_env=True, env=env, **kwargs
        )

    def archive(self, fmt="tar"):
        return tar_chroot(self.chrootPath, fmt)

    def putFiles(self, files, dest):
        if not os.path.isabs(dest):
            raise Exception(f"{dest} is not an absolute path")
        for f in files:
            # Do NOT use os.pain.join(), as dest is an absolute path
            # os.path.join() will discard chrootPath, and return dest instead
            shutil.copy2(f, self.chrootPath + dest)

    def getRootPath(self):
        return self.chrootPath

    def _unmountAll(self):
        dirsToTry = [
            os.path.join(self.chrootPath, d)
            for d in [
                "dev/pts",
                "dev",
                "proc",
                "run",
                "sys",
                "tmp",
                "publishrpms",
                "publishxrpms",
                "inputrpms",
            ]
        ]
        dirsToTry += [
            os.path.join(self.chrootPath + constants.topDirPath, d)
            for d in ["RPMS", "SRPMS"]
        ]
        for d in dirsToTry:
            # Python os.path.ismount can't reliably detect bind mounts
            # Thus, use mountpoint command instead (which consults /proc/self/mountinfo)
            _, _, rc = CommandUtils.runCmd(
                ["mountpoint", d], ignore_rc=True, capture=True
            )
            if rc:
                # Not a mountpoint
                continue
            _, _, rc = self._cmd(["umount", "-R", d], ignore_rc=True)
            if rc:
                # Try unmount with lazy umount
                self._cmd(["umount", "-R", "-l", d], ignore_rc=True)


class SystemdNspawn(Sandbox):
    def __init__(self, name, logger, cmdAudit=lambda cmd, env: None):
        import docker

        Sandbox.__init__(self, name, logger, cmdAudit)
        self.nspawnRootPath = os.path.join(constants.buildRootPath, self.name)
        self.dockerClient = docker.from_env(version="auto")
        self.observationFile = None
        self.observerContainer = None
        self.observerURL = "http://127.0.0.1:8989"

    def create(self):
        if os.path.isdir(self.nspawnRootPath):
            if constants.resume_build:
                return
            self.destroy()

        prepare_chroot_dirs(self.nspawnRootPath)

        self.logger.debug(f"Successfully created nspawn root: {self.nspawnRootPath}")

    def destroy(self):
        self.logger.debug(f"Deleting nspawn chroot: {self.nspawnRootPath}")
        self._cmd(["rm", "--one-file-system", "-rf", self.nspawnRootPath])

    def _startObserver(self):
        if not constants.observerDockerImage:
            self.logger.warning(
                "Unable to start an observer container. Docker image is not provided."
            )
            return None

        runArgs = {
            "image": constants.observerDockerImage,
            "command": ["tail", "-f", "/dev/null"],
            "detach": True,
            "privileged": False,
            "name": f"ph-build-observer-{self.name}",
            # Map tls/certs folder of the sandbox in observer container. So, observer can modify certificates and hijack a traffic.
            "volumes": {
                os.path.join(self.nspawnRootPath, "/etc/pki/tls/certs"): {
                    "bind": "/etc/pki/tls/certs",
                    "mode": "rw",
                }
            },
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
        result = self.observerContainer.exec_run(
            ["/observer/bin/observer_agent", "-m", "start_observer"]
        )
        if result.exit_code:
            self.logger.warning("Unable to start an observer daemon")
            self.observerContainer.remove(force=True)
            self.observerContainer = None
            return None

        # Update attributes
        self.observerContainer.reload()
        # Return network namespace path systemd-nspawn attach to
        return self.observerContainer.attrs["NetworkSettings"]["SandboxKey"]

    def _stopObserver(self):
        result = self.observerContainer.exec_run(
            ["/observer/bin/observer_agent", "-m", "stop_observer"]
        )
        if result.exit_code:
            self.logger.warning(
                "Unable to stop an observer daemon. No observation file provided"
            )
            self.observerContainer.remove(force=True)
            self.observerContainer = None
            return

        self.observationFile = tempfile.TemporaryFile()
        try:
            with tempfile.TemporaryFile(mode="w+b") as tarf:
                archive, stat = self.observerContainer.get_archive("/provenance.json")
                for buf in archive:
                    tarf.write(buf)

                tarf.seek(0, 0)
                tar = tarfile.open(fileobj=tarf, mode="r:")
                shutil.copyfileobj(
                    io.TextIOWrapper(
                        tar.extractfile("provenance.json"), encoding="utf-8"
                    ),
                    self.observationFile,
                )

                # Go back to the beginning of the file
                self.observationFile.seek(0, 0)
        except Exception as e:
            self.logger.exception(e)
            self.logger.error("Failed to extract observation file")
            self.observationFile.close()
            raise
        finally:
            self.observerContainer.remove(force=True)
            self.observerContainer = None

    def runCmd(
        self, cmd, network_required=False, env={}, clean_env=True, shell=False, **kwargs
    ):
        if shell:
            raise Exception("SystemdNspawn.runCmd() does not support shell=True")
        nspawnEnv = {"SYSTEMD_NSPAWN_TMPFS_TMP": "0"}
        env = {**sandboxDefaultEnv, **env}
        self.logger.debug(f"SystemdNspawn.runCmd({cmd}, env={env})")

        nspawnCmd = [
            "systemd-nspawn",
            "--quiet",
            "--console=pipe",
            "--directory",
            self.nspawnRootPath,
            "--bind",
            f"{constants.rpmPath}:{constants.topDirPath}/RPMS",
            "--bind",
            f"{constants.sourceRpmPath}:{constants.topDirPath}/SRPMS",
            "--bind-ro",
            f"{constants.prevPublishRPMRepo}:/publishrpms",
            "--bind-ro",
            f"{constants.prevPublishXRPMRepo}:/publishxrpms",
        ]

        if constants.inputRPMSPath:
            nspawnCmd += ["--bind-ro", f"{constants.inputRPMSPath}:/inputrpms"]

        netnsPath = None
        if network_required:
            # Processes in a sandbox may access external resources only through proxy.
            # We use SRP observer as a proxy, which also records all proxy activities to provenance observation file.
            # Observer daemon will be run in a docker container, and systemd-nspawn instance will be attached to the
            # same network namespace. It will allow rpmbuild children access observer via local 127.0.0.1:8989 port
            netnsPath = self._startObserver()
            if not netnsPath:
                self.logger.warning(
                    "Observer is not available. Sandbox will not have a networking"
                )

        if netnsPath:
            nspawnCmd += ["--network-namespace-path", netnsPath]
            env["HTTP_PROXY"] = self.observerURL
            env["http_proxy"] = self.observerURL
            env["HTTPS_PROXY"] = self.observerURL
            env["https_proxy"] = self.observerURL
        else:
            nspawnCmd += ["--private-network"]

        for k, v in env.items():
            nspawnCmd += ["--setenv", f"{k}={v}"]
        try:
            return self._cmd(nspawnCmd + cmd, clean_env=True, env=nspawnEnv, **kwargs)
        finally:
            if netnsPath:
                self._stopObserver()

    def archive(self, fmt="tar"):
        return tar_chroot(self.nspawnRootPath, fmt)

    def putFiles(self, files, dest):
        if not os.path.isabs(dest):
            raise Exception(f"{dest} is not an absolute path")
        for f in files:
            # Do NOT use os.pain.join(), as dest is an absolute path
            # os.path.join() will discard chrootPath, and return dest instead
            shutil.copy2(f, self.nspawnRootPath + dest)

    def getRootPath(self):
        return self.nspawnRootPath

    def getObservation(self):
        fp = self.observationFile
        self.observationFile = None
        return fp


class Container(Sandbox):
    def __init__(self, name, logger, cmdAudit=lambda cmd, env: None):
        import docker

        Sandbox.__init__(self, name, logger, cmdAudit)
        self.dockerClient = docker.from_env(version="auto")
        self.containerName = "photon-sandbox-" + self.name.replace("+", "p")
        self.container = None

    def create(self):
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

        # Remove existing container
        with suppress(Exception):
            existing = self.dockerClient.containers.get(self.containerName)
            if existing is not None:
                existing.remove(force=True)

        #  TODO: Is init=True equivalent of --sig-proxy?
        #  privilegedDocker = False
        cap_list = ["SYS_PTRACE"]
        #  if packageName in constants.listReqPrivilegedDockerForTest:
        #  privilegedDocker = True

        self.container = self.dockerClient.containers.run(
            constants.buildContainerImage,
            entrypoint="/usr/bin/tail",
            detach=True,
            cap_add=cap_list,
            # privileged=privilegedDocker,
            privileged=False,
            name=self.containerName,
            network_mode="host",
            volumes=mountVols,
            command=["-f", "/dev/null"],
        )

        self.logger.debug(
            f"Successfully created docker container: {self.container.short_id}"
        )

    def runCmd(
        self,
        cmd,
        logfile=None,
        logfn=None,
        capture=False,
        network_required=False,
        env={},
        clean_env=True,
        shell=False,
        ignore_rc=False,
        **kwargs,
    ):
        if shell:
            raise Exception("Container.runCmd() does not support shell=True")
        if logfn:
            capture = True
        if logfile and capture:
            raise Exception(
                "Container.runCmd() does not support specifying both logfile and logfn/capture"
            )

        env = {**sandboxDefaultEnv, **env}
        self.logger.debug(f"Container.runCmd({cmd}, env={env})")
        containerCmd = ["/usr/bin/env", "-i"]
        for k, v in env.items():
            containerCmd.append(f"{k}={v}")
        # synthesize docker exec command
        self.cmdAudit(["docker", "exec", self.containerName] + containerCmd, env)

        execInst = self.dockerClient.api.exec_create(self.container.id, containerCmd)
        # Only demux stdout/stderr when logfile is not specified.
        output = self.dockerClient.api.exec_start(
            execInst["Id"], stream=logfile is not None, demux=logfile is None
        )
        if logfile:
            for chunk in output:
                logfile.write(chunk)
        elif logfn:
            logfn(output.stdout.decode())

        retval = self.dockerClient.api.exec_inspec(execInst["Id"])["ExitCode"]
        if retval != 0 and not ignore_rc:
            raise Exception(f"Container.runCmd(): {cmd} failed")
        if logfile:
            return "", "", retval
        return output.stdout.decode(), output.stderr.decode(), retval

    def archive(self, fmt="tar"):
        if fmt != "tar":
            raise Exception("only tar format is supported in Container.archive()")
        tarStream = self.container.export()
        tarf = tempfile.TemporaryFile(mode="w+b")
        for buf in tarStream:
            tarf.write(buf)
        tarf.seek(0, 0)
        return tarf

    def destroy(self):
        self.container.remove(force=True)
        self.container = None

    def putFiles(self, files, dest):
        if not os.path.isabs(dest):
            raise Exception(f"{dest} is not an absolute path")
        with tempfile.TemporaryFile(mode="w+b") as tarf:
            tar = tarfile.open(fileobj=tarf, mode="w:")
            for f in files:
                tar.add(f)
            tar.close()
            tarf.seek(0, 0)
            if not self.container.put_archive(dest, tarf):
                raise Exception(
                    f"failed to copy {files} into {self.containerName}:{dest}"
                )

    def getRootPath(self):
        raise Exception("Cannot get rootpath from Container sandbox")

    def hasToolchain(self):
        return True
