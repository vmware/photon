# This utility helps manage packages in a chroot dir using another sandbox
# Lets say linux-x.y.z is the sandbox into which we want to install BuildRequires packages
# We can use nspawn -D <photon 5 base image extract> --bind <chroot-linux-x.y.z>:/mnt/baseroot tdnf install -y <packages> --installroot=/mnt/baseroot

import os
import shutil
import tempfile

from CommandUtils import CommandUtils
from constants import BuildMode, BuildStage, constants

cmdUtils = CommandUtils()


@staticmethod
def snapshotLocalRepo(repoPath, logfn):
    cmds = [
        ["rm", "-rf", repoPath],
        ["mkdir", "-p", repoPath],
        ["cp", "-al", f"{constants.rpmPath}/noarch", f"{repoPath}/noarch"],
        [
            "cp",
            "-al",
            f"{constants.rpmPath}/{constants.buildArch}",
            f"{repoPath}/{constants.buildArch}",
        ],
        ["createrepo", "--general-compress-type=gz", repoPath],
    ]

    for cmd in cmds:
        cmdUtils.runCmd(cmd, logfn=logfn)


@staticmethod
def copyRPMsToRepo(sandboxPath, listRPMFiles=[], listSRPMFiles=[]):
    rpmPath = constants.rpmPath
    rpmTargetPath = f"{constants.stagePath}/SRPMS/"
    for rpmFile in listSRPMFiles:
        shutil.copy(f"{sandboxPath}/{rpmFile}", rpmTargetPath)
    rpmTempPath = tempfile.mkdtemp(prefix=".rpmdir", dir=rpmPath)
    # Two step copy to repo to avoid creating incomplete/partial repo
    rpmTempFiles = []
    for rpmFile in listRPMFiles:
        rpmTargetPath = None
        if rpmFile.endswith("noarch.rpm"):
            rpmTargetPath = f"{rpmTempPath}/noarch/"
        else:
            rpmTargetPath = f"{rpmTempPath}/{constants.buildArch}/"
        os.makedirs(rpmTargetPath, exist_ok=True)
        rpmTempFiles.append(shutil.copy(f"{sandboxPath}/{rpmFile}", rpmTargetPath))

    for rpmFile in rpmTempFiles:
        rpmTargetPath = None
        if rpmFile.endswith("noarch.rpm"):
            rpmTargetPath = f"{rpmPath}/noarch/"
        else:
            rpmTargetPath = f"{rpmPath}/{constants.buildArch}/"
        os.makedirs(rpmTargetPath, exist_ok=True)
        shutil.move(rpmFile, rpmTargetPath)

    shutil.rmtree(rpmTempPath, ignore_errors=True)


@staticmethod
def getRepoArgs(buildStage, buildMode):
    repoArgs = []

    if buildStage is BuildStage.CORE_TOOLCHAIN:
        repoArgs += ["--disablerepo=*", "--enablerepo=packages"]
    elif buildStage is BuildStage.TOOLCHAIN:
        repoArgs += [
            "--disablerepo=*",
            "--enablerepo=local",
            "--enablerepo=packages",
        ]
    else:
        repoArgs += ["--disablerepo=*", "--enablerepo=local"]

    if buildMode is not BuildMode.BOOTSTRAP:
        repoArgs += ["--enablerepo=bootstrap"]

    return repoArgs
