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

packages_repo_template = """
[packages]
name = packages
enabled=1
gpgcheck=0
skip_if_unavailable=True
"""

LOCAL_REPO = "local.repo"
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
        self.logger = logger
        self.cmdUtils = CommandUtils()
        self.cmdlog = cmdlog
        self.repoArgs = repoArgs
        self.defaultArgs = defaultArgs
        packageRoot = os.path.basename(installRoot)
        assert constants.sandboxType is not None
        self.sandboxName = f"tdnf-{packageRoot}"
        self.repoPath = f"{constants.tdnfBasePath}/local-{packageRoot}"
        binds = [[self.repoPath, "/local"]]
        bindsrw = [[self.installRoot, "/installRoot"]]
        RepoUtil.snapshotLocalRepo(self.repoPath, self.logger.debug)
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
        self.sandbox.putFiles(
            [str(os.path.join(os.path.dirname(__file__), LOCAL_REPO))],
            "/etc/yum.repos.d",
        )
        if constants.bootstrapRepoPath:
            self.sandbox.putFiles(
                [str(os.path.join(os.path.dirname(__file__), BOOTSTRAP_REPO))],
                "/etc/yum.repos.d",
            )

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".repo"
        ) as temp_file:
            # Write the string constant to the temporary file
            temp_file.write(packages_repo_template)
            if constants.packageRepoPath:
                temp_file.write("\n")
                temp_file.write("baseurl = file:///packages")
            else:
                temp_file.write("\n")
                temp_file.write(f"baseurl = {constants.packageRepoURL}")

            if constants.packageRepoSnapshotFilePath:
                temp_file.write("\n")
                temp_file.write(
                    f"snapshot = /etc/yum.repos.d/{os.path.basename(constants.packageRepoSnapshotFilePath)}"
                )

            temp_file.flush()
            temp_file_path = temp_file.name
            self.sandbox.putFiles(
                [temp_file_path],
                "/etc/yum.repos.d",
            )
            if constants.packageRepoSnapshotFilePath:
                self.sandbox.putFiles(
                    [constants.packageRepoSnapshotFilePath],
                    "/etc/yum.repos.d",
                )

    def run(self, subCmd=[], repoArgs=[], args=[], errMsg=""):
        if not repoArgs:
            repoArgs = self.repoArgs
        args = self.defaultArgs + args
        tdnfArgs = repoArgs + ["--installroot=/installRoot"] + args
        cmd = self.tdnfCmd + tdnfArgs + subCmd
        optionalOut = io.StringIO("")

        def logfn(out):
            optionalOut.write(out)
            self.logger.debug(out)

        _, _, rc = self.sandbox.runCmd(cmd, sandbox_user="root", logfn=logfn)
        if rc:
            self.logger.debug(f"Command Executed: {cmd} rc {rc}")
            raise Exception(errMsg)
        out = optionalOut.getvalue()
        optionalOut.close()
        return out

    def clean(self):
        self.cmdUtils.runCmd(f"rm -rf {self.repoPath}".split())
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
