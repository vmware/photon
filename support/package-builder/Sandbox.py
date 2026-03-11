#!/usr/bin/env python3

import os.path
import shutil
import subprocess
import tarfile
import tempfile

from contextlib import ExitStack, suppress

from CommandUtils import CommandUtils
from constants import SandboxType, constants

SB_TYPES = {}


def register(key):
    def decorator(cls):
        SB_TYPES[key] = cls
        return cls

    return decorator


def sandbox_default_env():
    return {
        "HOME": "/root",
        "TERM": "linux",
        "PATH": "/bin:/usr/bin:/sbin:/usr/sbin",
        "SHELL": "/bin/bash",
        "LC_ALL": "en_US.UTF-8",
        **constants.SandboxEnv,
    }


def prepare_chroot_dirs(rootPath):
    if constants.bootstrapRepoPath:
        os.makedirs(f"{rootPath}/mnt/bootstrap", exist_ok=True)
    extra_dirs = ["RPMS", "SRPMS", "SOURCES", "SPECS", "LOGS", "BUILD", "BUILDROOT"]
    for d in extra_dirs:
        os.makedirs(f"{rootPath}{constants.topDirPath}/{d}", exist_ok=True)


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


class Sandbox(object):
    def __init__(
        self,
        name,
        optionalMounts,
        logger,
        cmdAudit=lambda cmd, env: None,
    ):
        self.name = name
        self.cmdAudit = cmdAudit
        self.optionalMounts = optionalMounts
        self.logger = logger

    def create(self):
        pass

    def destroy(self):
        pass

    def runCmd(self, network_required=False, **kwargs):
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

    def mountSandboxBase(self):
        base = f"{constants.buildImagesPath}/sandboxBase"
        rootPath = self.getRootPath()
        cmds = [
            ["mkdir", "-p", f"{rootPath}/upper", f"{rootPath}/work"],
            [
                "mount",
                "-t", "overlay",
                "overlay",
                "-o", f"lowerdir={base},upperdir={rootPath}/upper,workdir={rootPath}/work",
                rootPath,
            ],
        ]

        for cmd in cmds:
            self._cmd(cmd)

    def _adjust_permissions(self, dest):
        # Fix permissions for non-root user
        cmd = [
            "find",
            f"{self.getRootPath()}{dest}",
            "-type",
            "d",
            "-exec",
            "chmod",
            "o+rx",
            "{}",
            ";",
        ]
        self._cmd(cmd, logfn=self.logger.debug)
        cmd = [
            "find",
            f"{self.getRootPath()}{dest}",
            "-type",
            "f",
            "-exec",
            "chmod",
            "o+r",
            "{}",
            ";",
        ]
        self._cmd(cmd, logfn=self.logger.debug)


@register(SandboxType.CHROOT)
class Chroot(Sandbox):
    def __init__(
        self,
        name,
        optionalMounts,
        logger,
        cmdAudit=lambda cmd, env: None,
    ):
        Sandbox.__init__(self, name, optionalMounts, logger, cmdAudit)
        self.chrootPath = f"{constants.buildRootPath}/{self.name}"
        self.prepareBuildRootCmd = os.path.join(
            os.path.dirname(__file__), "prepare-build-root.sh"
        )

    def create(self):
        if os.geteuid():
            raise Exception(f"Unable to create {self.name} as non-root user")

        if os.path.isdir(self.chrootPath):
            if constants.resume_build:
                return
            self.destroy()
        self.mountSandboxBase()
        prepare_chroot_dirs(rootPath=self.chrootPath)
        self._cmd([self.prepareBuildRootCmd, self.chrootPath])
        self._prepare_mounts()
        self.logger.debug(f"Successfully created chroot: {self.chrootPath}")

    def destroy(self):
        self.logger.debug(f"Deleting chroot: {self.chrootPath}")
        self._unmountAll()
        self._cmd(["rm", "--one-file-system", "-rf", self.chrootPath])

    def runCmd(
        self,
        cmd,
        sandbox_user=None,
        network_required=False,
        env={},
        clean_env=True,
        shell=False,
        **kwargs,
    ):
        if shell:
            raise Exception("Chroot.runCmd() does not support shell=True")
        env = {**sandbox_default_env(), **env}
        chroot_prefix = ["chroot"]
        if sandbox_user:
            chroot_prefix += ["--userspec", sandbox_user]
        self.logger.debug(f"Chroot.runCmd({cmd}, env={env})")
        chroot_prefix += [self.chrootPath]
        return self._cmd(chroot_prefix + cmd, clean_env=True, env=env, **kwargs)

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

    def _prepare_mounts(self):
        for bind in self.optionalMounts.get("binds", []):
            self._mountOne(bind[0], f"{self.chrootPath}{bind[1]}", True)
        for bind in self.optionalMounts.get("bindsrw", []):
            self._mountOne(bind[0], f"{self.chrootPath}{bind[1]}", False)

    def _mountOne(self, src, dest, readOnly=True):
        os.makedirs(dest, exist_ok=True)
        cmd = ["mount", "--bind"]
        if readOnly:
            cmd.append("--read-only")
        cmd += [src, dest]
        self._cmd(cmd)

    def _unmountAll(self):
        dirsToTry = []
        # unmount any left over custom bind paths
        for bind in self.optionalMounts.get("binds", []):
            dirsToTry.append(self.chrootPath + bind[1])
        for bind in self.optionalMounts.get("bindsrw", []):
            dirsToTry.append(self.chrootPath + bind[1])
        dirsToTry += [
            f"{self.chrootPath}/{d}"
            for d in [
                "dev/pts",
                "dev",
                "proc",
                "sys",
                "tmp",
            ]
        ]
        dirsToTry += [
            f"{self.chrootPath}{constants.topDirPath}/{d}"
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

        CommandUtils.umountWithRetry(self.chrootPath)


@register(SandboxType.SYSTEMD_NSPAWN)
class SystemdNspawn(Sandbox):
    def __init__(
        self,
        name,
        optionalMounts,
        logger,
        cmdAudit=lambda cmd, env: None,
    ):
        Sandbox.__init__(self, name, optionalMounts, logger, cmdAudit)
        self.nspawnRootPath = f"{constants.buildRootPath}/{self.name}"
        self.observationFile = None

    def create(self):
        if os.path.isdir(self.nspawnRootPath):
            if constants.resume_build:
                return
            self.destroy()
        self.mountSandboxBase()
        prepare_chroot_dirs(self.nspawnRootPath)

        self.logger.debug(f"Successfully created nspawn root: {self.nspawnRootPath}")

    def destroy(self):
        self.logger.debug(f"Deleting nspawn chroot: {self.nspawnRootPath}")

        container_name = os.path.basename(self.nspawnRootPath)
        if (
            container_name
            in subprocess.run(
                ["machinectl", "list"], capture_output=True, text=True
            ).stdout
        ):
            self.logger.debug(f"Removing nspawn container: {container_name} ...")
            self._cmd(["machinectl", "terminate", container_name], ignore_rc=True)

        CommandUtils.umountWithRetry(self.nspawnRootPath)
        self._cmd(["rm", "--one-file-system", "-rf", self.nspawnRootPath])

    def _prepare_mount_arguments(self) -> list[str]:
        args = []
        for bind in self.optionalMounts.get("binds", []):
            args += ["--bind-ro", f"{bind[0]}:{bind[1]}"]
        for bind in self.optionalMounts.get("binds", []):
            args += ["--bind", f"{bind[0]}:{bind[1]}"]
        return args

    def runCmd(
        self,
        cmd,
        sandbox_user=None,
        network_required=False,
        env={},
        clean_env=True,
        shell=False,
        **kwargs,
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
        ]

        nspawnCmd += self._prepare_mount_arguments()

        if constants.bootstrapRepoPath:
            nspawnCmd += ["--bind-ro", f"{constants.bootstrapRepoPath}:/bootstrap"]

        with ExitStack() as stack:
            # Processes in a sandbox may access external resources only through proxy.
            # We use SRP observer as a proxy, which also records all proxy activities to provenance observation file.
            # Observer daemon will be run in a docker container, and systemd-nspawn instance will be attached to the
            # same network namespace. It will allow rpmbuild children access observer via local 127.0.0.1:8989 port
            if network_required:
                observer = stack.enter_context(Observer(self))
                if observer is None:
                    self.logger.warning(
                        "Observer is not available. Sandbox will not have networking"
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


@register(SandboxType.CONTAINER)
class Container(Sandbox):
    def __init__(
        self,
        name,
        baseImagePath,
        optionalMounts,
        logger,
        cmdAudit=lambda cmd, env: None,
    ):
        import docker

        Sandbox.__init__(self, name, optionalMounts, logger, cmdAudit)
        self.dockerClient = docker.from_env(version="auto")
        self.containerName = "photon-sandbox-" + self.name.replace("+", "p")
        self.container = None
        self.baseImagePath = baseImagePath

    def create(self):
        mountVols = {
            constants.tmpDirPath: {"bind": "/tmp", "mode": "rw"},
            constants.dockerUnixSocket: {
                "bind": constants.dockerUnixSocket,
                "mode": "rw",
            },
        }

        for bind in self.optionalMounts.get("binds", []):
            mountVols[bind[0]] = {
                "bind": bind[1],
                "mode": "ro",
            }
        for bind in self.optionalMounts.get("bindsrw", []):
            mountVols[bind[0]] = {
                "bind": bind[1],
                "mode": "rw",
            }

        if constants.bootstrapRepoPath:
            mountVols[constants.bootstrapRepoPath] = {
                "bind": "/bootstrap",
                "mode": "ro",
            }

        # Remove existing container
        with suppress(Exception):
            existing = self.dockerClient.containers.get(self.containerName)
            if existing is not None:
                existing.remove(force=True)

        cap_list = ["SYS_PTRACE"]

        self.container = self.dockerClient.containers.run(
            self.baseImagePath,
            entrypoint="/usr/bin/tail",
            detach=True,
            cap_add=cap_list,
            privileged=False,
            name=self.containerName,
            network_mode="host",
            volumes=mountVols,
            command=["-f", "/dev/null"],
        )

        self.logger.debug(
            f"Successfully created docker container: {self.container.short_id} {mountVols}"
        )

    def runCmd(
        self,
        cmd,
        sandbox_user=None,
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
        # synthesize docker exec command
        self.cmdAudit(["docker", "exec", self.containerName] + cmd, env)

        execInst = self.dockerClient.api.exec_create(
            self.container.id, cmd=cmd, environment=env
        )
        # Only demux stdout/stderr when logfile is not specified.
        output = self.dockerClient.api.exec_start(
            execInst["Id"], stream=logfile is not None, demux=logfile is None
        )
        if logfile:
            for chunk in output:
                logfile.write(chunk)
            output = (None, None)
        elif logfn and output[0]:
            logfn(output[0].decode("utf-8"))

        retval = self.dockerClient.api.exec_inspect(execInst["Id"])["ExitCode"]
        if retval and not ignore_rc:
            stdout = output[0].decode() if output[0] else ""
            stderr = output[1].decode() if output[1] else ""
            raise Exception(
                f"Container.runCmd(): {cmd} failed {retval} {stdout} {stderr}"
            )

        stdout = output[0].decode() if output[0] else ""
        stderr = output[1].decode() if output[1] else ""
        return stdout, stderr, retval

    def destroy(self):
        if self.container:
            self.container.remove(force=True)
            self.container = None
        if self.dockerClient:
            self.dockerClient.close()
            self.dockerClient = None

    def putFiles(self, files, dest):
        self.logger.debug(f"{files} to {dest}")
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


def init_sandbox(sandboxType, name, optionalMounts, logger, cmdAudit):
    return SB_TYPES[sandboxType](
        name=name,
        logger=logger,
        cmdAudit=cmdAudit,
        optionalMounts=optionalMounts,
    )
