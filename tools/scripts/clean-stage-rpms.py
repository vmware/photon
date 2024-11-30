#!/usr/bin/python3

import os
import sys

from argparse import ArgumentParser


def listRPMfilenames():
    output = []
    arch = constants.buildArch
    for base_pkg in SPECS.getData().getListPackages():
        for version in SPECS.getData().getVersions(base_pkg):
            listRPMPackages = SPECS.getData().getRPMPackages(base_pkg, version)
            for pkg in listRPMPackages:
                release = SPECS.getData().getRelease(pkg, version)
                buildarch = SPECS.getData().getBuildArch(pkg, version)
                filename = os.path.join(
                    f"{buildarch}/{pkg}-{version}-{release}.{buildarch}.rpm"
                )
                output.append(filename)

            if SPECS.getData().getBuildArch(base_pkg, version) == arch:
                filename = os.path.join(
                    f"{buildarch}/{base_pkg}-debuginfo-{version}-{release}.{buildarch}.rpm"
                )
                output.append(filename)

    return output


def clean_stage_rpms():
    allFiles = []
    arch = constants.buildArch
    rpmPath = constants.rpmPath

    for i in ["noarch", arch]:
        d_path = f"{rpmPath}/{i}"
        if not os.path.exists(d_path):
            continue
        for f in os.listdir(d_path):
            if os.path.isfile(f"{d_path}/{f}"):
                allFiles.append(f"{i}/{f}")

    if not allFiles:
        print("Nothing to clean ...")
        return

    keepFiles = listRPMfilenames()
    removeFiles = list(set(allFiles) - set(keepFiles))
    for f in removeFiles:
        filePath = f"{rpmPath}/{f}"
        print(f"Removing {f}")
        try:
            os.remove(filePath)
        except Exception as e:
            print(f"ERROR: while removing file {filePath}: {e}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-t", "--top-dir", dest="topDir", default=".")
    opts = parser.parse_args()

    topDir = opts.topDir
    sys.path.insert(0, os.path.join(topDir, "support/package-builder"))

    from SpecData import SPECS
    from constants import constants

    constants.specPath = f"{topDir}/SPECS"
    constants.rpmPath = f"{topDir}/stage/RPMS"
    constants.logPath = f"{topDir}/stage/LOGS"
    constants.addMacro("with_check", "0")
    constants.addMacro("dist", ".ph3")

    clean_stage_rpms()
