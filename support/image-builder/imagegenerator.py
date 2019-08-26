#!/usr/bin/python3

import os
import re
import shutil
import tarfile
import lzma as xz
import fileinput
from argparse import ArgumentParser
import json
from utils import Utils
import ovagenerator

def createOutputArtifact(raw_image_path, config, src_root, tools_bin_path):
    photon_release_ver = os.environ['PHOTON_RELEASE_VER']
    photon_build_num = os.environ['PHOTON_BUILD_NUM']
    new_name = ""
    img_path = os.path.dirname(os.path.realpath(raw_image_path))
    # Rename gce image to disk.raw
    if config['image_type'] == "gce":
        new_name = img_path + '/disk.raw'

    else:
        new_name = (img_path + '/photon-' + config['image_type'] +
                    '-' + photon_release_ver + '-' +
                    photon_build_num + '.raw')

    shutil.move(raw_image_path, new_name)
    raw_image = new_name
    compressed = True

    if config['artifacttype'] == 'tgz':
        print("Generating the tar.gz artifact ...")
        outputfile = (img_path + '/photon-' + config['image_type'] +
                      '-' + photon_release_ver + '-' +
                      photon_build_num + '.tar.gz')
        compressed = generateCompressedFile(raw_image, outputfile, "w:gz")
    elif config['artifacttype'] == 'xz':
        print("Generating the xz artifact ...")
        outputfile = (img_path + '/photon-' + config['image_type'] +
                      '-' + photon_release_ver + '-' +
                      photon_build_num + '.xz')
        compressed = generateCompressedFile(raw_image, outputfile, "w:xz")
    elif 'vhd' in config['artifacttype']:
        relrawpath = os.path.relpath(raw_image, src_root)
        vhdname = ('/photon-' +
                   config['image_type'] + '-' + photon_release_ver + '-' +
                   photon_build_num + '.vhd')
        print("Converting raw disk to vhd ...")
        info_output = Utils.runshellcommand(
            "docker run -v {}:/mnt:rw anishs/qemu-img info -f raw --output json {}"
            .format(src_root, '/mnt/' + relrawpath))
        mbsize = 1024 * 1024
        mbroundedsize = ((int(json.loads(info_output)["virtual-size"])/mbsize + 1) * mbsize)
        Utils.runshellcommand(
            "docker run -v {}:/mnt:rw anishs/qemu-img resize -f raw {} {}"
            .format(src_root, '/mnt/' + relrawpath, mbroundedsize))
        Utils.runshellcommand(
            "docker run -v {}:/mnt:rw anishs/qemu-img convert {} -O "
            "vpc -o subformat=fixed,force_size {}"
            .format(src_root, '/mnt/' + relrawpath, '/mnt/' + os.path.dirname(relrawpath) + vhdname))
        if config['artifacttype'] == 'vhd.gz':
            outputfile = (img_path + '/photon-' + config['image_type'] +
                          '-' + photon_release_ver + '-' +
                          photon_build_num + '.vhd.tar.gz')
            compressed = generateCompressedFile(img_path + vhdname, outputfile, "w:gz")
            # remove raw image and call the vhd as raw image
            os.remove(raw_image)
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
