#!/usr/bin/env python3

import os.path
import shutil
import tempfile
import tarfile
import subprocess

from contextlib import suppress, ExitStack
from constants import constants
from CommandUtils import CommandUtils


def sandbox_default_env():
    return {
        "HOME": "/root",
        "TERM": "linux",
        "PATH": "/bin:/usr/bin:/sbin:/usr/sbin",
        "SHELL": "/bin/bash",
        **constants.SandboxEnv,
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


def copy_file_from_container(container, path):
    f = tempfile.NamedTemporaryFile()
    try:
        with tempfile.TemporaryFile(mode="w+b") as tarf:
            archive, stat = container.get_archive(path)
            for buf in archive:
                tarf.write(buf)

            tarf.seek(0, 0)
            tar = tarfile.open(fileobj=tarf, mode="r:")
            shutil.copyfileobj(
                tar.extractfile(os.path.basename(path)),
                f,
            )
            # Go back to the beginning of the file
            f.seek(0, 0)
    except Exception as e:
        f.close()
        raise Exception(f"ERROR: {e}")
    return f


def tar_chroot(rootPath, fmt):
    if fmt != "tar" and fmt != "tgz":
        raise Exception(f"Chroot.archive(): format {fmt} not supported")
    cmd = ["tar", "--one-file-system", "--xattrs", "-S", "-C", rootPath, "-c", "."]
    if fmt == "tgz":
        cmd += ["-z"]
    tarf = tempfile.TemporaryFile(mode="w+b")
    try:
        subprocess.run(cmd, stdout=tarf, check=True)
    except Exception as e:
        tarf.close()
        raise Exception(f"ERROR: {e}")
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
        env = {**sandbox_default_env(), **env}
        self.logger.debug(f"Chroot.runCmd({cmd}, env={env})")
        return self._cmd(
            ["chroot", self.chrootPath] + cmd, clean_env=True, env=env, **kwargs
        )

    def archive(self, fmt="tar"):
        return tar_chroot(self.chrootPath, fmt)

    def putFiles(self, files, dest):
        if not os.path.isabs(dest):
            raise Exception(f"{dest} is not an absolute path")
        destDir = dest
        if isinstance(files, str):
            files = [files]
            destDir = os.path.dirname(dest)
        # Do NOT use os.pain.join(), as dest is an absolute path
        # os.path.join() will discard chrootPath, and return dest instead
        os.makedirs(self.chrootPath + destDir, exist_ok=True)
        for f in files:
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
        Sandbox.__init__(self, name, logger, cmdAudit)
        self.nspawnRootPath = os.path.join(constants.buildRootPath, self.name)
        self.observationFile = None

    def create(self):
        if os.path.isdir(self.nspawnRootPath):
            if constants.resume_build:
                return
            self.destroy()

        prepare_chroot_dirs(self.nspawnRootPath)

        self.logger.debug(f"Successfully created nspawn root: {self.nspawnRootPath}")

    def destroy(self):
        self.logger.debug(f"Deleting nspawn chroot: {self.nspawnRootPath}")

        container_name = os.path.basename(self.nspawnRootPath)
        if container_name in subprocess.run(["machinectl", "list"], capture_output=True, text=True).stdout:
            self.logger.debug(f"Removing nspawn container: {container_name} ...")
            self._cmd(f"machinectl terminate {container_name}".split(), ignore_rc=True)

        self._cmd(["rm", "--one-file-system", "-rf", self.nspawnRootPath])

    def runCmd(
        self, cmd, network_required=False, env={}, clean_env=True, shell=False, **kwargs
    ):
        if shell:
            raise Exception("SystemdNspawn.runCmd() does not support shell=True")
        nspawnEnv = {"SYSTEMD_NSPAWN_TMPFS_TMP": "0"}
        env = {**sandbox_default_env(), **env}
        self.logger.debug(f"SystemdNspawn.runCmd({cmd}, env={env})")

        nspawnCmd = [
            "systemd-nspawn",
            "--property=DeviceAllow=char-*",  # Allows mknod char devices
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

        with ExitStack() as stack:
            # Processes in a sandbox may access external resources only through proxy.
            # We use SRP observer as a proxy, which also records all proxy activities to provenance observation file.
            # Observer daemon will be run in a docker container, and systemd-nspawn instance will be attached to the
            # same network namespace. It will allow rpmbuild children access observer via local 127.0.0.1:8989 port
            if network_required:
                observer = stack.enter_context(Observer(self))
                if observer is None:
                    self.logger.warning(
                        "Observer is not available. Sandbox will not have a networking"
                    )
                    network_required = False
                else:
                    observer.injectCaCert()
                    env = {**env, **observer.getProxyEnv()}

            if network_required:
                nspawnCmd += ["--network-namespace-path", observer.getNetworkNS()]
            else:
                nspawnCmd += ["--private-network"]

            for k, v in env.items():
                nspawnCmd += ["--setenv", f"{k}={v}"]
            return self._cmd(nspawnCmd + cmd, clean_env=True, env=nspawnEnv, **kwargs)

    def archive(self, fmt="tar"):
        return tar_chroot(self.nspawnRootPath, fmt)

    def putFiles(self, files, dest):
        if not os.path.isabs(dest):
            raise Exception(f"{dest} is not an absolute path")
        destDir = dest
        if isinstance(files, str):
            files = [files]
            destDir = os.path.dirname(dest)
        # Do NOT use os.pain.join(), as dest is an absolute path
        # os.path.join() will discard chrootPath, and return dest instead
        os.makedirs(self.nspawnRootPath + destDir, exist_ok=True)
        for f in files:
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

        # TODO: Is init=True equivalent of --sig-proxy?
        # privilegedDocker = False
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

        env = {**sandbox_default_env(), **env}
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
        if isinstance(files, str):
            arcnames = os.path.basename(dest)
            dest = os.path.dirname(dest)
        else:
            arcnames = [os.path.basename(f) for f in files]
        with tempfile.TemporaryFile(mode="w+b") as tarf:
            tar = tarfile.open(fileobj=tarf, mode="w:")
            for i, f in enumerate(files):
                tar.add(f, arcnames[i])
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


class Observer(object):
    def __init__(self, sandbox):
        import docker

        # Observer has reference to sandbox, not the other way around
        self.sandbox = sandbox
        self.dockerClient = docker.from_env(version="auto")
        self.container = None

    def getNetworkNS(self):
        # Return network namespace path systemd-nspawn attach to
        return self.container.attrs["NetworkSettings"]["SandboxKey"]

    def getProxyEnv(self):
        observerURL = "http://127.0.0.1:8989"
        return {
            "HTTP_PROXY": observerURL,
            "http_proxy": observerURL,
            "HTTPS_PROXY": observerURL,
            "https_proxy": observerURL,
        }

    def getCaCertFile(self):
        return copy_file_from_container(
            self.container,
            "/observer/bin/runtime/observer/.mitmproxy/mitmproxy-ca-cert.pem",
        )

    def injectCaCert(self):
        caFile = self.getCaCertFile()
        tempCaPath = f"/root/mitm-ca-cert-{self.container.short_id}.crt"
        self.sandbox.putFiles(caFile.name, tempCaPath)
        caFile.close()
        # Append the MITM ca-cert to ca-bundle
        self.sandbox.runCmd(
            [
                "dd",
                f"if={tempCaPath}",
                "of=/etc/pki/tls/certs/ca-bundle.crt",
                "oflag=append",
                "conv=notrunc",
                "status=none",
            ]
        )
        # Optionally use keytool to import ca-cert into java keystore
        javaHome, _, retval = self.sandbox.runCmd(
            ["java", "/root/print-java-home.java"], ignore_rc=True, capture=True
        )
        if retval == 0:
            self.sandbox.logger.debug(
                f"observer: java.home at {javaHome}, import mitm ca-cert to java keystore"
            )
            self.sandbox.runCmd(
                [
                    "keytool",
                    "-import",
                    "-noprompt",
                    "-storepass",
                    "changeit",
                    "-trustcacerts",
                    "-keystore",
                    f"{javaHome}/lib/security/cacerts",
                    "-file",
                    tempCaPath,
                    "-alias",
                    f"mitm-proxy-{self.container.short_id}",
                ]
            )

    def __enter__(self):
        if not constants.observerDockerImage:
            self.sandbox.logger.warning(
                "Unable to start an observer container. Docker image is not provided."
            )
            return None
        runArgs = {
            "image": constants.observerDockerImage,
            "command": ["tail", "-f", "/dev/null"],
            "detach": True,
            "privileged": False,
            "name": f"ph-build-observer-{self.sandbox.name}",
        }
        if constants.isolatedDockerNetwork:
            runArgs["network"] = constants.isolatedDockerNetwork
        else:
            runArgs["network_mode"] = "bridge"

        self.container = self.dockerClient.containers.run(**runArgs)
        if not self.container:
            raise Exception("Unable to start an observer. Docker run failed.")
        result = self.container.exec_run(
            ["/observer/bin/observer_agent", "-m", "start_observer"]
        )
        if result.exit_code:
            self.container.remove(force=True)
            self.container = None
            raise Exception("Unable to start an observer daemon")

        # Update attributes
        self.container.reload()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.container is None:
            return
        if exc_type is None:
            # Only reap observations when there's no exception
            result = self.container.exec_run(
                ["/observer/bin/observer_agent", "-m", "stop_observer"]
            )
            if result.exit_code:
                raise Exception("Unable to stop the observer daemon.")

            self.sandbox.observationFile = copy_file_from_container(
                self.container, "/provenance.json"
            )
        self.container.remove(force=True)
        self.container = None
