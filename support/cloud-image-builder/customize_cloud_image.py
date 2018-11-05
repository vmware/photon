#!/usr/bin/python3

import os
import re
import shutil
import tarfile
import fileinput
from argparse import ArgumentParser
import json
from utils import Utils

def create_ova_image(raw_image_name, tools_path, build_scripts_path, config):
    output_path = os.path.dirname(os.path.realpath(raw_image_name))
    utils = Utils()
    # Remove older artifacts
    files = os.listdir(output_path)
    for file in files:
        if file.endswith(".vmdk"):
            os.remove(os.path.join(output_path, file))

    vmx_path = output_path + '/photon-ova.vmx'
    utils.replaceandsaveasnewfile(build_scripts_path + '/vmx-template',
                                  vmx_path, 'VMDK_IMAGE',
                                  output_path + '/photon-ova.vmdk')
    vixdiskutil_path = tools_path + 'vixdiskutil'
    vmdk_path = output_path + '/photon-ova.vmdk'
    ovf_path = output_path + '/photon-ova.ovf'
    mf_path = output_path + '/photon-ova.mf'
    ovfinfo_path = build_scripts_path + '/ovfinfo.txt'
    vmdk_capacity = (int(config['size']['root']) +
                     int(config['size']['swap'])) * 1024
    utils.runshellcommand(
        "{} -convert {} -cap {} {}".format(vixdiskutil_path,
                                           raw_image_name,
                                           vmdk_capacity,
                                           vmdk_path))
    utils.runshellcommand(
        "{} -wmeta toolsVersion 2147483647 {}".format(vixdiskutil_path, vmdk_path))

    utils.runshellcommand("ovftool {} {}".format(vmx_path, ovf_path))
    utils.replaceinfile(ovf_path, 'otherGuest', 'other3xLinux64Guest')

    #Add product info
    if os.path.exists(ovfinfo_path):
        with open(ovfinfo_path) as f:
            lines = f.readlines()
            for line in fileinput.input(ovf_path, inplace=True):
                if line.strip() == '</VirtualHardwareSection>':
                    for ovfinfoline in lines:
                        print(ovfinfoline)
                else:
                    print(line)

    if os.path.exists(mf_path):
        os.remove(mf_path)

    cwd = os.getcwd()
    os.chdir(output_path)
    out = utils.runshellcommand("openssl sha1 photon-ova-disk1.vmdk photon-ova.ovf")
    with open(mf_path, "w") as source:
        source.write(out)
    rawsplit = os.path.splitext(raw_image_name)
    ova_name = rawsplit[0] + '.ova'

    ovatar = tarfile.open(ova_name, "w", format=tarfile.USTAR_FORMAT)
    for name in ["photon-ova.ovf", "photon-ova.mf", "photon-ova-disk1.vmdk"]:
        ovatar.add(name, arcname=os.path.basename(name))
    ovatar.close()
    os.remove(vmx_path)
    os.remove(mf_path)

    if 'additionalhwversion' in config:
        for addlversion in config['additionalhwversion']:
            new_ovf_path = output_path + "/photon-ova-hw{}.ovf".format(addlversion)
            mf_path = output_path + "/photon-ova-hw{}.mf".format(addlversion)
            utils.replaceandsaveasnewfile(
                ovf_path, new_ovf_path, "vmx-.*<", "vmx-{}<".format(addlversion))
            out = utils.runshellcommand("openssl sha1 photon-ova-disk1.vmdk "
                                        "photon-ova-hw{}.ovf".format(addlversion))
            with open(mf_path, "w") as source:
                source.write(out)
            temp_name_list = os.path.basename(ova_name).split('-')
            temp_name_list = temp_name_list[:2] + ["hw{}".format(addlversion)] + temp_name_list[2:]
            new_ova_name = '-'.join(temp_name_list)
            new_ova_path = output_path + '/' + new_ova_name
            ovatar = tarfile.open(new_ova_path, "w", format=tarfile.USTAR_FORMAT)
            for name in [new_ovf_path, mf_path, "photon-ova-disk1.vmdk"]:
                ovatar.add(name, arcname=os.path.basename(name))
            ovatar.close()

            os.remove(new_ovf_path)
            os.remove(mf_path)
    os.chdir(cwd)
    os.remove(ovf_path)
    os.remove(vmdk_path)
    files = os.listdir(output_path)
    for file in files:
        if file.endswith(".vmdk"):
            os.remove(os.path.join(output_path, file))


if __name__ == '__main__':
    usage = "Usage: %prog [options]"
    parser = ArgumentParser(usage)

    parser.add_argument("-r", "--raw-image-path", dest="raw_image_path")
    parser.add_argument("-c", "--vmdk-config-path", dest="vmdk_config_path")
    parser.add_argument("-w", "--working-directory", dest="working_directory")
    parser.add_argument("-m", "--mount-path", dest="mount_path")
    parser.add_argument("-a", "--additional-rpms-path", dest="additional_rpms_path")
    parser.add_argument("-i", "--image-name", dest="image_name")
    parser.add_argument("-t", "--tools-bin-path", dest="tools_bin_path")
    parser.add_argument("-b", "--build-scripts-path", dest="build_scripts_path")
    parser.add_argument("-s", "--src-root", dest="src_root")

    options = parser.parse_args()
    utils = Utils()
    config = utils.jsonread(options.vmdk_config_path)
    print(options)

    disk_device = (utils.runshellcommand(
        "losetup --show -f {}".format(options.raw_image_path))).rstrip('\n')
    disk_partitions = utils.runshellcommand("kpartx -as {}".format(disk_device))
    device_name = disk_device.split('/')[2]

    if not os.path.exists(options.mount_path):
        os.mkdir(options.mount_path)

    if options.image_name == 'ls1012afrwy':
        loop_device_path = "/dev/mapper/{}p3".format(device_name)
    else:
        loop_device_path = "/dev/mapper/{}p2".format(device_name)

    try:
        print("Generating PARTUUID for the loop device ...")
        partuuidval = (utils.runshellcommand(
            "blkid -s PARTUUID -o value {}".format(loop_device_path))).rstrip('\n')
        uuidval = (utils.runshellcommand(
            "blkid -s UUID -o value {}".format(loop_device_path))).rstrip('\n')
        if partuuidval == '':
            sgdiskout = utils.runshellcommand(
                "sgdisk -i 2 {} ".format(disk_device))
            partuuidval = (re.findall(r'Partition unique GUID.*',
                                      sgdiskout))[0].split(':')[1].strip(' ').lower()

        if partuuidval == '':
            raise RuntimeError("Cannot generate partuuid")

        # Mount the loop device
        print("Mounting the loop device for customization ...")
        print(loop_device_path)
        utils.runshellcommand(
            "mount -t ext4 {} {}".format(loop_device_path, options.mount_path))
        shutil.rmtree(options.mount_path + "/installer", ignore_errors=True)
        shutil.rmtree(options.mount_path + "/LOGS", ignore_errors=True)
        # Clear the root password if not set explicitly from the config file
        if config['password']['text'] != 'PASSWORD':
            utils.replaceinfile(options.mount_path + "/etc/shadow",
                                'root:.*?:', 'root:*:')
        # Clear machine-id so it gets regenerated on boot
        open(options.mount_path + "/etc/machine-id", "w").close()
        os.remove(options.mount_path + "/etc/fstab")

        f = open(options.mount_path + "/etc/fstab", "w")
        if uuidval != '':
            f.write("UUID={}    /    ext4    defaults 1 1\n".format(uuidval))
        else:
            f.write("PARTUUID={}    /    ext4    defaults 1 1\n".format(partuuidval))
        f.close()
        utils.replaceinfile(options.mount_path + "/boot/grub/grub.cfg",
                            "rootpartition=PARTUUID=.*$",
                            "rootpartition=PARTUUID={}".format(partuuidval))

        if os.path.exists(options.additional_rpms_path):
            print("Installing additional rpms")
            os.mkdir(options.mount_path + "/additional_rpms")
            os.mkdir(options.mount_path + "/var/run")
            utils.copyallfiles(options.additional_rpms_path,
                               options.mount_path + "/additional_rpms")
            utils.runshellcommand(
                "chroot {} /bin/bash -c 'rpm -i /additional_rpms/*'".format(options.mount_path))
            shutil.rmtree(options.mount_path + "/additional_rpms", ignore_errors=True)
            shutil.rmtree(options.additional_rpms_path, ignore_errors=True)

        utils.runshellcommand("mount -o bind /proc {}".format(options.mount_path + "/proc"))
        utils.runshellcommand("mount -o bind /dev {}".format(options.mount_path + "/dev"))
        utils.runshellcommand("mount -o bind /dev/pts {}".format(options.mount_path + "/dev/pts"))
        utils.runshellcommand("mount -o bind /sys {}".format(options.mount_path + "/sys"))

        if 'additionalfiles' in config:
            print("  Copying additional files into the raw image ...")
            for filetuples in config['additionalfiles']:
                for src, dest in filetuples.items():
                    if (os.path.isdir(options.build_scripts_path + '/' +
                                      options.image_name + '/' + src)):
                        shutil.copytree(options.build_scripts_path + '/' +
                                        options.image_name + '/' + src,
                                        options.mount_path + dest, True)
                    else:
                        shutil.copyfile(options.build_scripts_path + '/' +
                                        options.image_name + '/' + src,
                                        options.mount_path + dest)


        if 'postinstallscripts' in config:
            print("  Running post install scripts ...")
            if not os.path.exists(options.mount_path + "/tempscripts"):
                os.mkdir(options.mount_path + "/tempscripts")
            for script in config['postinstallscripts']:
                shutil.copy(options.build_scripts_path + '/' +
                            options.image_name + '/' + script,
                            options.mount_path + "/tempscripts")
            for script in os.listdir(options.mount_path + "/tempscripts"):
                print("     ...running script {}".format(script))
                utils.runshellcommand(
                    "chroot {} /bin/bash -c '/tempscripts/{}'".format(options.mount_path, script))
            shutil.rmtree(options.mount_path + "/tempscripts", ignore_errors=True)

    except Exception as e:
        print(e)

    finally:
        utils.runshellcommand("umount -l {}".format(options.mount_path + "/sys"))
        utils.runshellcommand("umount -l {}".format(options.mount_path + "/dev/pts"))
        utils.runshellcommand("umount -l {}".format(options.mount_path + "/dev"))
        utils.runshellcommand("umount -l {}".format(options.mount_path + "/proc"))

        utils.runshellcommand("sync")
        utils.runshellcommand("umount -l {}".format(options.mount_path))

        mount_out = utils.runshellcommand("mount")
        print("List of mounted devices:")
        print(mount_out)

        utils.runshellcommand("kpartx -d {}".format(disk_device))
        utils.runshellcommand("losetup -d {}".format(disk_device))

        shutil.rmtree(options.mount_path)

        photon_release_ver = os.environ['PHOTON_RELEASE_VER']
        photon_build_num = os.environ['PHOTON_BUILD_NUM']
        raw_image = options.raw_image_path
        new_name = ""
        img_path = os.path.dirname(os.path.realpath(raw_image))
        # Rename gce image to disk.raw
        if options.image_name == "gce":
            print("Renaming the raw file to disk.raw ...")
            new_name = img_path + '/disk.raw'

        else:
            new_name = (img_path + '/photon-' + options.image_name +
                        '-' + photon_release_ver + '-' +
                        photon_build_num + '.raw')

        shutil.move(raw_image, new_name)
        raw_image = new_name

        if config['artifacttype'] == 'tgz':
            print("Generating the tar.gz artifact ...")
            tarname = (img_path + '/photon-' + options.image_name +
                       '-' + photon_release_ver + '-' +
                       photon_build_num + '.tar.gz')

            tgzout = tarfile.open(tarname, "w:gz")
            tgzout.add(raw_image, arcname=os.path.basename(raw_image))
            tgzout.close()
        elif config['artifacttype'] == 'xz':
            print("Generating the xz artifact ...")
            utils.runshellcommand("xz -z -k {}".format(raw_image))
#            tarname = img_path + '/photon-' + options.image_name +
#            '-' + photon_release_ver + '-' + photon_build_num +
#            '.xz'
#            tgzout = tarfile.open(tarname, "w:xz")
#            tgzout.add(raw_image, arcname=os.path.basename(raw_image))
#            tgzout.close()
        elif config['artifacttype'] == 'vhd':
            relrawpath = os.path.relpath(raw_image, options.src_root)
            vhdname = (os.path.dirname(relrawpath) + '/photon-' +
                       options.image_name + '-' + photon_release_ver + '-' +
                       photon_build_num + '.vhd')
            print("Converting raw disk to vhd ...")
            info_output = utils.runshellcommand(
                "docker run -v {}:/mnt:rw anishs/qemu-img info -f raw --output json {}"
                .format(options.src_root, '/mnt/' + relrawpath))
            mbsize = 1024 * 1024
            mbroundedsize = ((int(json.loads(info_output)["virtual-size"])/mbsize + 1) * mbsize)
            utils.runshellcommand(
                "docker run -v {}:/mnt:rw anishs/qemu-img resize -f raw {} {}"
                .format(options.src_root, '/mnt/' + relrawpath, mbroundedsize))
            utils.runshellcommand(
                "docker run -v {}:/mnt:rw anishs/qemu-img convert {} -O "
                "vpc -o subformat=fixed,force_size {}"
                .format(options.src_root, '/mnt/' + relrawpath, '/mnt/' + vhdname))
        elif config['artifacttype'] == 'ova':
            create_ova_image(raw_image, options.tools_bin_path,
                             options.build_scripts_path + '/' + options.image_name, config)
            if 'customartifacts' in config:
                if 'postinstallscripts' in config['customartifacts']:
                    custom_path = img_path + '/photon-custom'
                    if not os.path.exists(custom_path):
                        os.mkdir(custom_path)
                    index = 1
                    for script in config['customartifacts']['postinstallscripts']:
                        print("Creating custom ova {}...".format(index))
                        if index > 1:
                            raw_image_custom = (img_path + "/photon-custom-{}".format(index) +
                                                photon_release_ver + '-' +
                                                photon_build_num + '.raw')
                        else:
                            raw_image_custom = (img_path + "/photon-custom-" +
                                                photon_release_ver + '-' +
                                                photon_build_num + '.raw')
                        shutil.move(raw_image, raw_image_custom)
                        disk_device = (
                            utils.runshellcommand(
                                "losetup --show -f {}".format(raw_image_custom))).rstrip('\n')
                        disk_partitions = utils.runshellcommand(
                            "kpartx -as {}".format(disk_device))
                        device_name = disk_device.split('/')[2]
                        loop_device_path = "/dev/mapper/{}p2".format(device_name)

                        print("Mounting the loop device for ova customization ...")
                        utils.runshellcommand(
                            "mount -t ext4 {} {}".format(loop_device_path, custom_path))
                        if not os.path.exists(custom_path + "/tempscripts"):
                            os.mkdir(custom_path + "/tempscripts")
                        shutil.copy(options.build_scripts_path + '/' + options.image_name +
                                    '/' + script, custom_path + "/tempscripts")
                        print("Running custom ova script {}".format(script))
                        utils.runshellcommand("chroot {} /bin/bash -c '/tempscripts/{}'"
                                              .format(custom_path, script))
                        shutil.rmtree(custom_path + "/tempscripts", ignore_errors=True)
                        utils.runshellcommand("umount -l {}".format(custom_path))

                        mount_out = utils.runshellcommand("mount")
                        print("List of mounted devices:")
                        print(mount_out)

                        utils.runshellcommand("kpartx -d {}".format(disk_device))
                        utils.runshellcommand("losetup -d {}".format(disk_device))
                        create_ova_image(raw_image_custom, options.tools_bin_path,
                                         options.build_scripts_path + '/' + options.image_name,
                                         config)
                        raw_image = raw_image_custom
                        index = index + 1

                    shutil.rmtree(custom_path)

        else:
            raise ValueError("Unknown output format")

        if config['keeprawdisk'] == 'false':
            os.remove(raw_image)
