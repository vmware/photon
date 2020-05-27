#!/usr/bin/python3

import os
import fileinput
import tarfile
from argparse import ArgumentParser
from utils import Utils

def create_ova_image(raw_image_name, tools_path, config):
    build_scripts_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config['image_type'])
    output_path = os.path.dirname(os.path.realpath(raw_image_name))
    image_name = config.get('image_name', 'photon-' + config['image_type'])
    utils = Utils()
    # Remove older artifacts
    files = os.listdir(output_path)
    for file in files:
        if file.endswith(".vmdk"):
            os.remove(os.path.join(output_path, file))

    vmx_path = os.path.join(output_path, image_name + '.vmx')
    utils.replaceandsaveasnewfile(os.path.join(build_scripts_path, 'vmx-template'),
                                  vmx_path, 'VMDK_IMAGE',
                                  os.path.join(output_path, image_name + '.vmdk'))
    vixdiskutil_path = os.path.join(tools_path, 'vixdiskutil')
    vmdk_path = os.path.join(output_path, image_name + '.vmdk')
    ovf_path = os.path.join(output_path, image_name + '.ovf')
    mf_path = os.path.join(output_path, image_name + '.mf')
    ovfinfo_path = os.path.join(build_scripts_path, 'ovfinfo.txt')
    utils.runshellcommand(
        "{} -convert {} -cap {} {}".format(vixdiskutil_path,
                                           raw_image_name,
                                           config['size'],
                                           vmdk_path))
    utils.runshellcommand(
        "{} -wmeta toolsVersion 2147483647 {}".format(vixdiskutil_path, vmdk_path))

    utils.runshellcommand("ovftool {} {}".format(vmx_path, ovf_path))

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
    out = utils.runshellcommand("openssl sha1 {}-disk1.vmdk {}.ovf".format(image_name, image_name))
    with open(mf_path, "w") as source:
        source.write(out)
    rawsplit = os.path.splitext(raw_image_name)
    ova_name = rawsplit[0] + '.ova'

    ovatar = tarfile.open(ova_name, "w", format=tarfile.USTAR_FORMAT)
    for name in [image_name + ".ovf", image_name + ".mf", image_name + "-disk1.vmdk"]:
        ovatar.add(name, arcname=os.path.basename(name))
    ovatar.close()
    os.remove(vmx_path)
    os.remove(mf_path)

    if 'additionalhwversion' in config:
        for addlversion in config['additionalhwversion']:
            new_ovf_path = output_path + "/{}-hw{}.ovf".format(image_name, addlversion)
            mf_path = output_path + "/{}-hw{}.mf".format(image_name, addlversion)
            utils.replaceandsaveasnewfile(
                ovf_path, new_ovf_path, "vmx-.*<", "vmx-{}<".format(addlversion))
            out = utils.runshellcommand("openssl sha1 {}-disk1.vmdk ".format(image_name)
                                        + "{}-hw{}.ovf".format(image_name, addlversion))
            with open(mf_path, "w") as source:
                source.write(out)
            temp_name_list = os.path.basename(ova_name).split('-')
            temp_name_list = temp_name_list[:2] + ["hw{}".format(addlversion)] + temp_name_list[2:]
            new_ova_name = '-'.join(temp_name_list)
            new_ova_path = output_path + '/' + new_ova_name
            ovatar = tarfile.open(new_ova_path, "w", format=tarfile.USTAR_FORMAT)
            for name in [new_ovf_path, mf_path, image_name + "-disk1.vmdk"]:
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
    parser = ArgumentParser()

    parser.add_argument("-r", "--raw-image-path", dest="raw_image_path")
    parser.add_argument("-c", "--config-path", dest="config_path")
    parser.add_argument("-t", "--tools-bin-path", dest="tools_bin_path")

    options = parser.parse_args()

    create_ova_image(options.raw_image_path, options.tools_bin_path, config)
