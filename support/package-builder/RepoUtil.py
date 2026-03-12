#!/usr/bin/env python3

# This utility helps manage packages in a chroot dir using another sandbox
# Lets say linux-x.y.z is the sandbox into which we want to install BuildRequires packages
# We can use nspawn -D <photon 5 base image extract> --bind <chroot-linux-x.y.z>:/mnt/baseroot tdnf install -y <packages> --installroot=/mnt/baseroot

import os
import shutil
import tempfile
import fcntl
import sys

from CommandUtils import CommandUtils
from constants import BuildMode, BuildStage, constants
from signing import getSigningCmd, signFile

cmdUtils = CommandUtils()


cpu_count = os.cpu_count() or 1
ncpus = max(1, cpu_count // 2)


class RepoLock:
    def __init__(self, lockFileDir):
        self.lockFileDir = lockFileDir
        self.lock_path = os.path.join(lockFileDir, ".createrepo.lock")
        self.lock_fd = None

    def acquire(self):
        fd = os.open(self.lock_path, os.O_RDWR | os.O_CREAT, 0o644)
        self.lock_fd = None
        try:
            self.lock_fd = os.fdopen(fd, "r+")
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX)
        except Exception:
            if self.lock_fd is not None:
                try:
                    self.lock_fd.close()
                except OSError:
                    pass
                self.lock_fd = None
            else:
                try:
                    os.close(fd)
                except OSError:
                    pass
            raise

    def release(self):
        if self.lock_fd:
            fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
            self.lock_fd.close()
            self.lock_fd = None

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.release()


# This function should be called holding repo lock
def updateRepoData():
    repoPath = constants.rpmPath
    cmd = [
        "createrepo_c",
        "--update",
        f"--workers={ncpus}",
        "--skip-stat",
        "--no-database",
        "--general-compress-type=gz",
        repoPath,
    ]
    if constants.rebuild:
        cmd.remove("--skip-stat")

    out, err, rc = cmdUtils.runCmd(cmd, capture=True, timeout=600, ignore_rc=True)
    if rc:
        print(out, file=sys.stderr)
        print(err, file=sys.stderr)
        raise


def signAndMoveRPMsToRepo(sandboxPath, listRPMFiles, listSRPMFiles):
    rpmPath = constants.rpmPath
    arch = constants.buildArch
    stagePath = constants.stagePath

    signingCmd = getSigningCmd()
    if signingCmd:
        print("Initiate signing RPMs")

    rpmTargetPath = constants.sourceRpmPath
    for rpmFile in listSRPMFiles:
        src = f"{sandboxPath}/{rpmFile}"
        rpmFile = os.path.basename(rpmFile)
        dest = f"{rpmTargetPath}/{rpmFile}"
        shutil.move(src, dest)
        if signingCmd:
            signFile(dest)
            print(f"Signed SRPM: {dest}")

    rpmTempPath = tempfile.mkdtemp(prefix=".rpmdir", dir=stagePath)
    try:
        for rpmFile in listRPMFiles:
            src = f"{sandboxPath}/{rpmFile}"
            rpmFile = os.path.basename(rpmFile)
            dest = f"{rpmTempPath}/{rpmFile}"
            shutil.move(src, dest)
            if signingCmd:
                signFile(dest)
                print(f"Signed RPM: {dest}")

        with RepoLock(constants.stagePath):
            for rpmFile in listRPMFiles:
                fn = os.path.basename(rpmFile)
                src = f"{rpmTempPath}/{fn}"
                if fn.endswith(f".{arch}.rpm"):
                    dest = f"{rpmPath}/{arch}/{fn}"
                else:
                    dest = f"{rpmPath}/noarch/{fn}"

                shutil.move(src, dest)

            updateRepoData()
    finally:
        shutil.rmtree(rpmTempPath, ignore_errors=True)


REPO_LOCAL = "--enablerepo=local"
REPO_PACKAGES = "--enablerepo=packages"
REPO_BOOTSTRAP = "--enablerepo=bootstrap"

# Using packages repo is allowed only during toolchain builds
STAGE_REPOS = {
    BuildStage.PACKAGES: [REPO_LOCAL],
    BuildStage.CORE_TOOLCHAIN: [REPO_PACKAGES, REPO_LOCAL],
    BuildStage.TOOLCHAIN: [REPO_LOCAL, REPO_PACKAGES],
}


def getRepoArgs(buildStage, buildMode):
    repoArgs = ["--disablerepo=*"]

    repos = STAGE_REPOS.get(buildStage)
    if not repos:
        raise Exception(f"ERROR: invalid build stage {buildStage.value}")

    repoArgs += repos

    if buildMode == BuildMode.BOOTSTRAP:
        repoArgs += [REPO_BOOTSTRAP]

    return repoArgs
