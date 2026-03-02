#!/usr/bin/env python3

import io
import json
import os
import shutil
import tempfile

from CommandUtils import CommandUtils
from constants import constants
from Sandbox import Container

# This utility helps manage packages in a chroot dir using another sandbox
# Lets say linux-x.y.z is the sandbox into which we want to install BuildRequires packages
# We can use nspawn -D <photon 5 base image extract> --bind <chroot-linux-x.y.z>:/baseroot tdnf install -y <packages> --installroot=/baseroot

cpu_count = os.cpu_count() or 1
ncpus = max(1, cpu_count // 2)

packages_repo_template = """\
[packages]
name=packages
enabled=1
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
"""

BOOTSTRAP_REPO = "bootstrap.repo"


class TDNF:
    tdnfCmd = ["tdnf"]

    def __init__(
        self,
        logger,
        installRoot,
        repoArgs=[],
        defaultArgs=["-y"],
        cmdlog=lambda cmd, env: None,
    ):
        self.installRoot = installRoot
        self.installRootSandboxPath = "/installRoot"
        self.logger = logger
        self.cmdUtils = CommandUtils()
        self.cmdlog = cmdlog
        self.repoArgs = repoArgs
        self.defaultArgs = defaultArgs
        self.repoDir = "/etc/yum.repos.d"
        self.localRepoPath = constants.stagePath

        packageRoot = os.path.basename(installRoot)
        assert constants.sandboxType is not None

        self.sandboxName = f"tdnf-{packageRoot}"
        sandboxRepoSuffix = f"tdnf-repos/local-{packageRoot}"

        self.repoPath = f"{self.localRepoPath}/{sandboxRepoSuffix}"

        binds = [[self.localRepoPath, "/local"]]
        bindsrw = [[self.installRoot, self.installRootSandboxPath]]

        arch = constants.buildArch
        repoPath = self.repoPath
        rpmPath = constants.rpmPath

        for d in ["noarch", arch]:
            if not os.path.isdir(repoPath):
                os.makedirs(f"{repoPath}/noarch")
                os.makedirs(f"{repoPath}/{arch}")
                break
            _, _, rc = self.cmdUtils.runCmd(["mountpoint", f"{repoPath}/{d}"],
                                            ignore_rc=True, capture=True)
            if rc == 0:
                self.cmdUtils.runCmd(["umount", "-lR", f"{repoPath}/{d}"])

        for d in ["noarch", arch]:
            cmd = ["mount", "--bind", "-o", "ro", f"{rpmPath}/{d}", f"{repoPath}/{d}"]
            self.cmdUtils.runCmd(cmd, logfn=self.logger.debug)

        cmd = ["createrepo", f"--workers={ncpus}", "--general-compress-type=gz", f"{repoPath}"]
        self.cmdUtils.runCmd(cmd, capture=True)

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

        if constants.bootstrapRepoPath:
            self.sandbox.putFiles(
                [str(os.path.join(os.path.dirname(__file__), BOOTSTRAP_REPO))],
                self.repoDir,
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

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".repo"
        ) as temp_file:
            temp_file.write(packages_repo_template)
            if constants.packageRepoPath:
                temp_file.write("baseurl=file:///packages")
            else:
                temp_file.write(f"baseurl={constants.packageRepoURL}")

            snapShotFn = constants.packageRepoSnapshotURL
            if snapShotFn:
                if os.path.isfile(snapShotFn):
                    snapshotCfg = f"snapshot={self.repoDir}/{os.path.basename(snapShotFn)}"
                    self.sandbox.putFiles([snapShotFn], self.repoDir)
                else:
                    snapshotCfg = f"snapshot={snapShotFn}"

                temp_file.write(f"\n{snapshotCfg}")

            temp_file.flush()
            temp_file_path = temp_file.name
            self.sandbox.putFiles([temp_file_path], self.repoDir)
            os.remove(temp_file_path)

    def run(self, subCmd=[], repoArgs=[], args=[], errMsg=""):
        if not repoArgs:
            repoArgs = self.repoArgs

        tdnfArgs = repoArgs + [f"--installroot={self.installRootSandboxPath}"] + args + self.defaultArgs
        cmd = self.tdnfCmd + tdnfArgs + subCmd
        optionalOut = io.StringIO("")

        def logfn(out):
            optionalOut.write(out)
            self.logger.debug(out)

        out, err, rc = self.sandbox.runCmd(cmd, sandbox_user="root", logfn=logfn, ignore_rc=True)
        if rc:
            self.logger.error(f"Command Executed: {cmd} rc {rc}")
            self.logger.error(out)
            self.logger.error(err)
            raise Exception(errMsg)

        out = optionalOut.getvalue()
        optionalOut.close()
        return out

    def clean(self):
        for d in ["noarch", constants.buildArch]:
            d = f"{self.repoPath}/{d}"
            self.cmdUtils.umountWithRetry(d)
            os.rmdir(d)

        shutil.rmtree(f"{self.repoPath}/repodata")
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
            name = package.get("Name", None)
            evr = package.get("Evr", None)
            arch = package.get("Arch", None)
            if name and evr and arch:
                package = f"{name}-{evr}.{arch}"
                packages_info.append(package)
        return packages_info
