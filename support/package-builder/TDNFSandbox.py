#!/usr/bin/env python3

import io
import json
import os
import tempfile
import RepoUtil

from CommandUtils import CommandUtils
from constants import constants
from Sandbox import Container

# This utility helps manage packages in a chroot dir using another sandbox
# Lets say linux-x.y.z is the sandbox into which we want to install BuildRequires packages
# We can use nspawn -D <photon 5 base image extract> --bind <chroot-linux-x.y.z>:/baseroot tdnf install -y <packages> --installroot=/baseroot

cpu_count = os.cpu_count() or 1
ncpus = max(1, cpu_count // 2)

packages_repo_template = """\
[packages-snapshot]
name=packages-snapshot
gpgcheck=0
skip_if_unavailable=1
skip_md_filelists=1
"""

local_repo_template = """\
[local]
name=local
enabled=1
gpgcheck=0
skip_if_unavailable=1
skip_md_filelists=1
priority=10
"""

BOOTSTRAP_REPO = "bootstrap.repo"


class TDNF:
    tdnfCmd = ["tdnf"]

    def __init__(
        self,
        logger,
        installRoot,
        cmdlog=lambda cmd, env: None,
    ):
        self.installRoot = installRoot
        self.installRootSandboxPath = "/installRoot"
        self.logger = logger
        self.cmdUtils = CommandUtils()
        self.cmdlog = cmdlog
        self.repoDir = "/etc/yum.repos.d"
        self.localRepoPath = constants.stagePath

        packageRoot = os.path.basename(installRoot)
        assert constants.sandboxType is not None

        self.sandboxName = f"tdnf-{packageRoot}"
        sandboxRepoSuffix = f"tdnf-repos/local-{packageRoot}"

        self.repoPath = f"{self.localRepoPath}/{sandboxRepoSuffix}"

        binds = [[self.localRepoPath, "/local"]]
        bindsrw = [[self.installRoot, self.installRootSandboxPath]]

        repoPath = self.repoPath
        rpmPath = constants.rpmPath

        if os.path.isdir(repoPath):
            CommandUtils.umountWithRetry(repoPath)
        else:
            os.makedirs(repoPath)

        cmd = ["mount", "--bind", "-o", "ro", rpmPath, repoPath]
        self.cmdUtils.runCmd(cmd, logfn=self.logger.debug)

        if constants.packageRepoPath:
            binds.append([constants.packageRepoPath, "/packages"])

        # Always default to Docker
        self.sandbox = Container(
            name=self.sandboxName,
            baseImagePath=f"photon:{constants.releaseVersionToConsume}",
            optionalMounts={
                "binds": binds,
                "bindsrw": bindsrw,
            },
            logger=self.logger,
            cmdAudit=self.cmdlog,
        )

        self.sandbox.create()
        self._packagesRepoCreated = False

        if constants.bootstrapRepoPath:
            self.sandbox.putFiles(
                [str(os.path.join(os.path.dirname(__file__), BOOTSTRAP_REPO))],
                self.repoDir
            )

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, prefix="local", suffix=".repo"
        ) as temp_file:
            temp_file.write(local_repo_template)
            temp_file.write(f"baseurl=file:///local/{sandboxRepoSuffix}")
            temp_file.flush()
            temp_file_path = temp_file.name
            self.sandbox.putFiles([temp_file_path], self.repoDir)
            os.remove(temp_file_path)

        packagesSnapshotContent = (
            packages_repo_template
            + "enabled=1\n"
            + f"baseurl={RepoUtil.getPackageRepoBaseurl()}\n"
            + "priority=90\n"
        )

        snapShotFn = constants.packageRepoSnapshotURL
        if snapShotFn:
            if os.path.isfile(snapShotFn):
                snapshotCfg = f"snapshot={self.repoDir}/{os.path.basename(snapShotFn)}"
                self.sandbox.putFiles([snapShotFn], self.repoDir)
            else:
                snapshotCfg = f"snapshot={snapShotFn}"

            packagesSnapshotContent += f"\n{snapshotCfg}"

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".repo"
        ) as temp_file:
            temp_file.write(packagesSnapshotContent)
            temp_file.flush()
            temp_file_path = temp_file.name
            self.sandbox.putFiles([temp_file_path], self.repoDir)
            os.remove(temp_file_path)

    def createPackagesRepoFile(self):
        if self._packagesRepoCreated:
            return
        # "packages" is the same repo minus the snapshot pin, disabled by
        # default -- used to resolve ExtraBuildRequiresSansSnapshot packages
        # against the full/live packages repo.
        packagesContent = (
            packages_repo_template.replace("packages-snapshot", "packages")
            + "enabled=0\n"
            + f"baseurl={RepoUtil.getPackageRepoBaseurl()}\n"
            + "priority=100\n"
        )

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".repo"
        ) as temp_file:
            temp_file.write(packagesContent)
            temp_file.flush()
            temp_file_path = temp_file.name
            self.sandbox.putFiles([temp_file_path], self.repoDir)
            os.remove(temp_file_path)
        self._packagesRepoCreated = True

    def run(self, args=[], errMsg="", ignore_rc=False):
        tdnfArgs = args + [f"--installroot={self.installRootSandboxPath}"]
        cmd = self.tdnfCmd + tdnfArgs
        optionalOut = io.StringIO("")

        def logfn(out):
            optionalOut.write(out)
            self.logger.debug(out)

        needRepoLock = any(action in cmd for action in ("install", "update", "upgrade"))

        run_args = {
            "sandbox_user": "root",
            "logfn": logfn,
            "ignore_rc": True,
        }

        if needRepoLock:
            cmd.append("--refresh")
            from RepoUtil import RepoLock
            with RepoLock(constants.stagePath):
                out, err, rc = self.sandbox.runCmd(cmd, **run_args)
        else:
            out, err, rc = self.sandbox.runCmd(cmd, **run_args)

        if rc and not ignore_rc:
            self.logger.error(f"Command Executed: {cmd} rc {rc}")
            self.logger.error(out)
            self.logger.error(err)
            raise Exception(errMsg)

        out = optionalOut.getvalue()
        optionalOut.close()
        return out

    def clean(self):
        self.cmdUtils.umountWithRetry(self.repoPath)
        os.rmdir(self.repoPath)

        if self.sandbox:
            self.sandbox.destroy()

    def processInstalled(self, response):
        # process output of list --installed.
        packages_info = []
        packages = json.loads(response)
        if not isinstance(packages, list):
            return packages_info
        for package in packages:
            name = package["Name"]
            evr = package["Evr"]
            arch = package["Arch"]
            package = f"{name}-{evr}.{arch}"
            packages_info.append(package)
        return packages_info
