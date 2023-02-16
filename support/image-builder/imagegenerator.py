#!/usr/bin/env python3

import os
import re
import shutil
import tarfile
import lzma as xz
import fileinput
import json
import types
import ovagenerator

from utils import Utils
from argparse import ArgumentParser
from CommandUtils import CommandUtils


def create_container_cmd(src_root, photon_docker_image, cmd):
    cmd = (
        f"docker run --ulimit nofile=1024:1024 --rm"
        f" -v {src_root}:/mnt:rw {photon_docker_image}"
        f" /bin/bash -c \"{cmd}\""
    )
    return cmd


def createOutputArtifact(raw_image_path, config, src_root, tools_bin_path):
    cmdUtils = CommandUtils()

    photon_release_ver = os.environ["PHOTON_RELEASE_VER"]
    photon_build_num = os.environ["PHOTON_BUILD_NUM"]

    image_name = config.get("image_name",
                            "photon-" + config["image_type"] + f"-{photon_release_ver}-{photon_build_num}")

    photon_docker_image = config["installer"].get("photon_docker_image", "photon:latest")
    new_name = []
    if type(raw_image_path) is not list:
        raw_image_path = [raw_image_path]
    img_path = os.path.dirname(os.path.realpath(raw_image_path[0]))
    # Rename gce image to disk.raw
    if config["image_type"] == "gce":
        new_name.append(f"{img_path}/disk.raw")
    else:
        for img_num in range(len(raw_image_path)):
            new_name.append(f"{img_path}/{image_name}" + str(img_num) + ".raw")
    for img_num, raw_img in enumerate(raw_image_path):
        shutil.move(raw_img, new_name[img_num])
    raw_image = new_name
    compressed = True

    # Only for artifactype="ova", multidisk support is applicable
    # For other artifacttype, only one disk support (i.e. raw_image[0])
    if config["artifacttype"] == "tgz":
        print("Generating the tar.gz artifact ...")
        outputfile = f"{img_path}/{image_name}.tar.gz"
        compressed = generateCompressedFile(raw_image[0], outputfile, "w:gz")
    elif config["artifacttype"] == "xz":
        print("Generating the xz artifact ...")
        outputfile = f"{img_path}/{image_name}.xz"
        compressed = generateCompressedFile(raw_image[0], outputfile, "w:xz")
    elif "vhd" in config["artifacttype"]:
        relrawpath = os.path.relpath(raw_image[0], src_root)
        vhdname = f"/{image_name}.vhd"
        dockerenv = False
        print("Check if inside docker env")
        out, _, _ = cmdUtils.runBashCmd("grep -c docker /proc/self/cgroup || :", capture=True)
        if out.rstrip() != "0":
            dockerenv = True

        print("Converting raw disk to vhd ...")

        cmd  = (
            f"tdnf install -y qemu-img &> /dev/null;"
            f" qemu-img info -f raw --output json /mnt/{relrawpath}"
        )
        if not dockerenv:
            cmd = create_container_cmd(src_root, photon_docker_image, cmd)
        else:
            cmd = cmd.format(raw_image[0])

        info_out, _, _ = cmdUtils.runBashCmd(cmd, capture=True)
        mbsize = 1024 * 1024
        mbroundedsize = (int(json.loads(info_out)["virtual-size"]) / mbsize + 1) * mbsize

        cmd = (
            f"tdnf install -y qemu-img &> /dev/null;"
            f" qemu-img resize -f raw /mnt/{relrawpath} {mbroundedsize}"
        )
        if not dockerenv:
            cmd = create_container_cmd(src_root, photon_docker_image, cmd)
        else:
            cmd = cmd.format(raw_image[0], mbroundedsize)
        cmdUtils.runBashCmd(cmd)

        cmd = (
            f"tdnf install -y qemu-img &> /dev/null;"
            f" qemu-img convert /mnt/{relrawpath} -O"
            f" vpc -o subformat=fixed,force_size"
            f" /mnt/" + os.path.dirname(relrawpath) + vhdname
        )
        if not dockerenv:
            cmd = create_container_cmd(src_root, photon_docker_image, cmd)
        else:
            cmd = cmd.format(raw_image[0], os.path.dirname(raw_image[0]) + vhdname)
        cmdUtils.runBashCmd(cmd)

        if config["artifacttype"] == "vhd.gz":
            outputfile = f"{img_path}/{image_name}.vhd.tar.gz"
            compressed = generateCompressedFile(img_path + vhdname, outputfile, "w:gz")
            # remove raw image and call the vhd as raw image
            os.remove(raw_image[0])
            raw_image = img_path + vhdname
    elif config["artifacttype"] == "ova":
        ovagenerator.create_ova_image(raw_image, tools_bin_path, config)
    elif config["artifacttype"] == "raw":
        pass
    else:
        raise ValueError("Unknown output format")

    if not compressed:
        print("ERROR: Image compression failed!")
        # Leave the raw disk around if compression failed
        return
    if not config["keeprawdisk"]:
        if type(raw_image) is list:
            for raw_img in raw_image:
                os.remove(raw_img)
        else:
            os.remove(raw_image)


def generateCompressedFile(inputfile, outputfile, formatstring):
    try:
        if formatstring == "w:xz":
            in_file = open(inputfile, "rb")
            in_data = in_file.read()

            out_file = open(f"{inputfile}.xz", "wb")
            out_file.write(xz.compress(in_data))
            in_file.close()
            out_file.close()
        else:
            tarout = tarfile.open(outputfile, formatstring)
            tarout.add(inputfile, arcname=os.path.basename(inputfile))
            tarout.close()
    except Exception as e:
        print(e)
        return False
    return True

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-r", "--raw-image-path", dest="raw_image_path")
    parser.add_argument("-c", "--config-path", dest="config_path")
    parser.add_argument("-t", "--tools-bin-path", dest="tools_bin_path")
    parser.add_argument("-s", "--src-root", dest="src_root")

    options = parser.parse_args()
    if not options.config_path:
        raise Exception("No config file defined")

    config = Utils.jsonread(options.config_path)
    createOutputArtifact(
        options.raw_image_path,
        config,
        options.src_root,
        options.tools_bin_path
    )
