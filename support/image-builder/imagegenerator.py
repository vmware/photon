#!/usr/bin/python3

import os
import re
import shutil
import tarfile
import lzma as xz
import fileinput
from argparse import ArgumentParser
import json
import types
from utils import Utils
import ovagenerator

def createOutputArtifact(raw_image_path, config, src_root, tools_bin_path):
    photon_release_ver = os.environ['PHOTON_RELEASE_VER']
    photon_build_num = os.environ['PHOTON_BUILD_NUM']
    image_name = config.get('image_name', 'photon-' + config['image_type']
                       + '-' + photon_release_ver + '-' + photon_build_num)
    new_name = []
    if type(raw_image_path) is not list:
        raw_image_path = [raw_image_path]
    img_path = os.path.dirname(os.path.realpath(raw_image_path[0]))
    # Rename gce image to disk.raw
    if config['image_type'] == "gce":
        new_name.append(img_path + '/disk.raw')
    else:
        for img_num in range(len(raw_image_path)):
            new_name.append(img_path + '/' + image_name + '' + str(img_num) + '.raw')
    for img_num, raw_img in enumerate(raw_image_path):
        shutil.move(raw_img, new_name[img_num])
    raw_image = new_name
    compressed = True

    # Only for artifactype='ova', multidisk support is applicable
    # For other artifacttype, only one disk support (i.e. raw_image[0])
    if config['artifacttype'] == 'tgz':
        print("Generating the tar.gz artifact ...")
        outputfile = (img_path + '/' + image_name + '.tar.gz')
        compressed = generateCompressedFile(raw_image[0], outputfile, "w:gz")
    elif config['artifacttype'] == 'xz':
        print("Generating the xz artifact ...")
        outputfile = (img_path + '/' + image_name + '.xz')
        compressed = generateCompressedFile(raw_image[0], outputfile, "w:xz")
    elif 'vhd' in config['artifacttype']:
        relrawpath = os.path.relpath(raw_image[0], src_root)
        vhdname = ('/' + image_name + '.vhd')
        print("Converting raw disk to vhd ...")
        info_output = Utils.runshellcommand(
            "docker run -v {}:/mnt:rw photon:{} /bin/bash -c "
            "'tdnf install -y qemu-img > /dev/null 2>&1; qemu-img info -f raw --output json {}'"
            .format(src_root, photon_release_ver, '/mnt/' + relrawpath))
        mbsize = 1024 * 1024
        mbroundedsize = ((int(json.loads(info_output)["virtual-size"])/mbsize + 1) * mbsize)
        Utils.runshellcommand(
            "docker run -v {}:/mnt:rw photon:{} /bin/bash -c "
            "'tdnf install -y qemu-img > /dev/null 2>&1; qemu-img resize -f raw {} {}'"
            .format(src_root, photon_release_ver, '/mnt/' + relrawpath, mbroundedsize))
        Utils.runshellcommand(
            "docker run -v {}:/mnt:rw photon:{} /bin/bash -c "
            "'tdnf install -y qemu-img > /dev/null 2>&1; qemu-img convert {} -O "
            "vpc -o subformat=fixed,force_size {}'"
            .format(src_root, photon_release_ver, '/mnt/' + relrawpath, '/mnt/'
                + os.path.dirname(relrawpath) + vhdname))
        if config['artifacttype'] == 'vhd.gz':
            outputfile = (img_path + '/' + image_name + '.vhd.tar.gz')
            compressed = generateCompressedFile(img_path + vhdname, outputfile, "w:gz")
            # remove raw image and call the vhd as raw image
            os.remove(raw_image[0])
            raw_image = img_path + vhdname
    elif config['artifacttype'] == 'ova':
        ovagenerator.create_ova_image(raw_image, tools_bin_path, config)
    elif config['artifacttype'] == 'raw':
        pass
    else:
        raise ValueError("Unknown output format")

    if not compressed:
        print("ERROR: Image compression failed!")
        # Leave the raw disk around if compression failed
        return
    if not config['keeprawdisk']:
        if type(raw_image) is list:
            for raw_img in raw_image:
                os.remove(raw_img)
        else:
            os.remove(raw_image)

def generateCompressedFile(inputfile, outputfile, formatstring):
    try:
        if formatstring == "w:xz":
            in_file = open(inputfile, 'rb')
            in_data = in_file.read()

            out_file = open(inputfile+".xz", 'wb')
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

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("-r", "--raw-image-path", dest="raw_image_path")
    parser.add_argument("-c", "--config-path", dest="config_path")
    parser.add_argument("-t", "--tools-bin-path", dest="tools_bin_path")
    parser.add_argument("-s", "--src-root", dest="src_root")

    options = parser.parse_args()
    if options.config_path:
        config = Utils.jsonread(options.config_path)
    else:
        raise Exception("No config file defined")

    createOutputArtifact(
                options.raw_image_path,
                config,
                options.src_root,
                options.tools_bin_path
                )
