#!/usr/bin/env python3

# This utility helps manage packages in a chroot dir using another sandbox
# Lets say linux-x.y.z is the sandbox into which we want to install BuildRequires packages
# We can use nspawn -D <photon 5 base image extract> --bind <chroot-linux-x.y.z>:/mnt/baseroot tdnf install -y <packages> --installroot=/mnt/baseroot

import os
import shutil
import tempfile

from glob import glob

from CommandUtils import CommandUtils
from constants import BuildMode, BuildStage, constants

cmdUtils = CommandUtils()


@staticmethod
def copyRPMsToRepo(sandboxPath, listRPMFiles=[], listSRPMFiles=[]):
    rpmPath = constants.rpmPath

    rpmTargetPath = constants.sourceRpmPath
    for rpmFile in listSRPMFiles:
        fn = os.path.basename(rpmFile)
        shutil.move(f"{sandboxPath}/{rpmFile}", f"{rpmTargetPath}/{fn}")

    rpmTempPath = tempfile.mkdtemp(prefix=".rpmdir", dir=rpmPath)

    for rpmFile in listRPMFiles:
        shutil.move(f"{sandboxPath}/{rpmFile}", rpmTempPath)

    for d in ["noarch", constants.buildArch]:
        pattern = f"{rpmTempPath}/*.{d}.rpm"
        files = glob(pattern)

        for src in files:
            fn = os.path.basename(src)
            shutil.move(src, f"{rpmPath}/{d}/{fn}")

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
