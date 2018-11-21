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

def prepLoopDevice(loop_device_path, mount_path):
    Utils.runshellcommand(
            "mount -t ext4 {} {}".format(loop_device_path, mount_path))
    Utils.runshellcommand("mount -o bind /proc {}".format(mount_path + "/proc"))
    Utils.runshellcommand("mount -o bind /dev {}".format(mount_path + "/dev"))
    Utils.runshellcommand("mount -o bind /dev/pts {}".format(mount_path + "/dev/pts"))
    Utils.runshellcommand("mount -o bind /sys {}".format(mount_path + "/sys"))        

def cleanupMountPoints(mount_path):
    Utils.runshellcommand("umount -l {}".format(mount_path + "/sys"))
    Utils.runshellcommand("umount -l {}".format(mount_path + "/dev/pts"))
    Utils.runshellcommand("umount -l {}".format(mount_path + "/dev"))
    Utils.runshellcommand("umount -l {}".format(mount_path + "/proc"))

    Utils.runshellcommand("sync")
    Utils.runshellcommand("umount -l {}".format(mount_path))

def installAdditionalRpms(mount_path, additional_rpms_path):
    os.mkdir(mount_path + "/additional_rpms")
    Utils.copyallfiles(additional_rpms_path,
                       mount_path + "/additional_rpms")
    Utils.runshellcommand(
        "chroot {} /bin/bash -c 'rpm -i /additional_rpms/*'".format(mount_path))
    shutil.rmtree(mount_path + "/additional_rpms", ignore_errors=True)
    shutil.rmtree(additional_rpms_path, ignore_errors=True)

def writefstabandgrub(mount_path, uuidval, partuuidval):
    os.remove(mount_path + "/etc/fstab")
    f = open(mount_path + "/etc/fstab", "w")
    if uuidval != '':
        f.write("UUID={}    /    ext4    defaults 1 1\n".format(uuidval))
    else:
        f.write("PARTUUID={}    /    ext4    defaults 1 1\n".format(partuuidval))
    f.close()
    Utils.replaceinfile(mount_path + "/boot/grub/grub.cfg",
                        "rootpartition=PARTUUID=.*$",
                        "rootpartition=PARTUUID={}".format(partuuidval))

def generateUuid(loop_device_path):
    partuuidval = (Utils.runshellcommand(
        "blkid -s PARTUUID -o value {}".format(loop_device_path))).rstrip('\n')
    uuidval = (Utils.runshellcommand(
        "blkid -s UUID -o value {}".format(loop_device_path))).rstrip('\n')
    if partuuidval == '':
        sgdiskout = Utils.runshellcommand(
            "sgdisk -i 2 {} ".format(disk_device))
        partuuidval = (re.findall(r'Partition unique GUID.*',
                                  sgdiskout))[0].split(':')[1].strip(' ').lower()

    if partuuidval == '':
        raise RuntimeError("Cannot generate partuuid")

    return (uuidval, partuuidval)

def customizeImage(config, mount_path):
    build_scripts_path = os.path.dirname(os.path.abspath(__file__))
    image_name = config['image_type']
    if 'additionalfiles' in config:
        for filetuples in config['additionalfiles']:
            for src, dest in filetuples.items():
                if (os.path.isdir(build_scripts_path + '/' +
                                  image_name + '/' + src)):
                    shutil.copytree(build_scripts_path + '/' +
                                    image_name + '/' + src,
                                    mount_path + dest, True)
                else:
                    shutil.copyfile(build_scripts_path + '/' +
                                    image_name + '/' + src,
                                    mount_path + dest)
    if 'postinstallscripts' in config:
        if not os.path.exists(mount_path + "/tempscripts"):
            os.mkdir(mount_path + "/tempscripts")
        for script in config['postinstallscripts']:
            shutil.copy(build_scripts_path + '/' +
                        image_name + '/' + script,
                        mount_path + "/tempscripts")
        for script in os.listdir(mount_path + "/tempscripts"):
            print("     ...running script {}".format(script))
            Utils.runshellcommand(
                "chroot {} /bin/bash -c '/tempscripts/{}'".format(mount_path, script))
        shutil.rmtree(mount_path + "/tempscripts", ignore_errors=True)
    if 'expirepassword' in config and config['expirepassword']:
        # Do not run 'chroot -R' from outside. It will not find nscd socket.
        Utils.runshellcommand("chroot {} /bin/bash -c 'chage -d 0 root'".format(mount_path))

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

    if config['artifacttype'] == 'tgz':
        print("Generating the tar.gz artifact ...")
        outputfile = (img_path + '/photon-' + config['image_type'] +
                      '-' + photon_release_ver + '-' +
                      photon_build_num + '.tar.gz')
        generateCompressedFile(raw_image, outputfile, "w:gz")
    elif config['artifacttype'] == 'xz':
        print("Generating the xz artifact ...")
        outputfile = (img_path + '/photon-' + config['image_type'] +
                      '-' + photon_release_ver + '-' +
                      photon_build_num + '.xz')
        generateCompressedFile(raw_image, outputfile, "w:xz")
    elif 'vhd' in config['artifacttype']:
        relrawpath = os.path.relpath(raw_image, src_root)
        vhdname = (os.path.dirname(relrawpath) + '/photon-' +
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
            .format(src_root, '/mnt/' + relrawpath, '/mnt/' + vhdname))
        if config['artifacttype'] == 'vhd.gz':
            outputfile = (img_path + '/photon-' + config['image_type'] +
                          '-' + photon_release_ver + '-' +
                          photon_build_num + '.vhd.tar.gz')
            generateCompressedFile(vhdname, outputfile, "w:gz")
    elif config['artifacttype'] == 'ova':
        ovagenerator.create_ova_image(raw_image, tools_bin_path, config)
    elif config['artifacttype'] == 'raw':
        pass
    else:
        raise ValueError("Unknown output format")

    if not config['keeprawdisk']:
        os.remove(raw_image)

def generateCompressedFile(inputfile, outputfile, formatstring):
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

def generateImage(raw_image_path, additional_rpms_path, tools_bin_path, src_root, config):
    working_directory = os.path.dirname(raw_image_path)
    mount_path = os.path.splitext(raw_image_path)[0]
    build_scripts_path = os.path.dirname(os.path.abspath(__file__))

    if os.path.exists(mount_path) and os.path.isdir(mount_path):
        shutil.rmtree(mount_path)
    os.mkdir(mount_path)
    disk_device = (Utils.runshellcommand(
        "losetup --show -f {}".format(raw_image_path))).rstrip('\n')
    disk_partitions = Utils.runshellcommand("kpartx -as {}".format(disk_device))
    device_name = disk_device.split('/')[2]
    if not device_name:
        raise Exception("Could not create loop device and partition")

    root_part = config['rootfs_part']
    if root_part:
        loop_device_path = "/dev/mapper/{}{}".format(device_name, root_part)
    else:
        loop_device_path = "/dev/mapper/{}p2".format(device_name)

    print(loop_device_path)

    try:
        (uuidval, partuuidval) = generateUuid(loop_device_path)
        # Prep the loop device
        prepLoopDevice(loop_device_path, mount_path)
        # Clear the root password if not set explicitly from the config file
        if config['passwordtext'] == 'PASSWORD':
            Utils.replaceinfile(mount_path + "/etc/shadow",
                                'root:.*?:', 'root:*:')
        # Clear machine-id so it gets regenerated on boot
        open(mount_path + "/etc/machine-id", "w").close()
        # Write fstab
        writefstabandgrub(mount_path, uuidval, partuuidval)
        if additional_rpms_path and os.path.exists(additional_rpms_path):
            installAdditionalRpms(mount_path, additional_rpms_path)
        # Perform additional steps defined in installer config
        customizeImage(config, mount_path)
    except Exception as e:
        print(e)
    finally:
        cleanupMountPoints(mount_path)
        Utils.runshellcommand("kpartx -d {}".format(disk_device))
        Utils.runshellcommand("losetup -d {}".format(disk_device))

        shutil.rmtree(mount_path)
        createOutputArtifact(raw_image_path, config, src_root, tools_bin_path)
    
if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("-r", "--raw-image-path", dest="raw_image_path")
    parser.add_argument("-c", "--config-path", dest="config_path")
    parser.add_argument("-a", "--additional-rpms-path", dest="additional_rpms_path")
    parser.add_argument("-t", "--tools-bin-path", dest="tools_bin_path")
    parser.add_argument("-s", "--src-root", dest="src_root")

    options = parser.parse_args()
    if config_path:
        config = Utils.jsonread(options.config_path)
    else:
        raise Exception("No config file defined")

    generateImage(
                options.raw_image_path,
                options.working_directory,
                options.additional_rpms_path,
                options.tools_bin_path,
                options.src_root,
                config
                )

