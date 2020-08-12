#!/usr/bin/python3

import os
import fileinput
import tarfile
from argparse import ArgumentParser
from utils import Utils
import shutil

def create_ova_image(raw_image_name, tools_path, config):
    build_scripts_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config['image_type'])
    image_name = config.get('image_name', 'photon-' + config['image_type'])
    vmx_template_path = config.get('vmx_template', os.path.join(build_scripts_path, 'vmx-template'))
    utils = Utils()
    if type(raw_image_name) is not list:
        raw_image_name = [raw_image_name]
    output_path = os.path.dirname(os.path.realpath(raw_image_name[0]))
    if 'size' in config and 'disks' not in config:
        config['disks'] = {"Boot_Disk": config['size']}
    disks_size = list(config['disks'].values())
    # Remove older artifacts
    files = os.listdir(output_path)
    for file in files:
        if file.endswith(".vmdk"):
            os.remove(os.path.join(output_path, file))

    vmx_path = os.path.join(output_path, image_name + '.vmx')

    # if vmx file is provided then use it as is.
    # otherwise generate the vmx file from vmx-template
    if 'vmx_template' in config:
        if os.path.isfile(vmx_template_path):
            shutil.copy(vmx_template_path, vmx_path)
        else:
            raise Exception("vmx file not found at {}".format(vmx_template_path))
    else:
        utils.generatePhotonVmx(vmx_template_path, vmx_path, 'VMDK_IMAGE', len(raw_image_name))
        for num_img in range(len(raw_image_name)):
            utils.replaceinfile(vmx_path, 'VMDK_IMAGE' + str(num_img),
                                 os.path.join(output_path, image_name + '' + str(num_img) +'.vmdk'))
    vixdiskutil_path = os.path.join(tools_path, 'vixdiskutil')
    ovf_path = os.path.join(output_path, image_name + '.ovf')
    mf_path = os.path.join(output_path, image_name + '.mf')
    ovfinfo_path = os.path.join(build_scripts_path, 'ovfinfo.txt')
    vmdk_path = []
    for num_img,raw_img in enumerate(raw_image_name):
        vmdk_path.append(os.path.join(output_path, image_name + '' + str(num_img) + '.vmdk'))
        utils.runshellcommand(
            "{} -convert {} -cap {} {}".format(vixdiskutil_path,
                                               raw_img,
                                               disks_size[num_img],
                                               vmdk_path[num_img]))
        utils.runshellcommand(
            "{} -wmeta toolsVersion 2147483647 {}".format(vixdiskutil_path, vmdk_path[num_img]))

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
    for num_img in range(len(raw_image_name)):
        out = utils.runshellcommand("openssl sha1 {}-disk{}.vmdk {}.ovf".format(image_name, num_img + 1, image_name))
        with open(mf_path, "w") as source:
            source.write(out)
    rawsplit = os.path.splitext(raw_image_name[0])
    ova_name = rawsplit[0] + '.ova'

    ovatar = tarfile.open(ova_name, "w", format=tarfile.USTAR_FORMAT)
    tar_files = [image_name + ".ovf", image_name + ".mf"]
    for num_img in range(len(raw_image_name)):
        tar_files.append(image_name + "-disk" + str(num_img + 1) + ".vmdk")
    for name in tar_files:
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
            for num_img in range(len(raw_image_name)):
                out = utils.runshellcommand("openssl sha1 {}-disk{}.vmdk ".format(image_name, num_img + 1)
                                            + "{}-hw{}.ovf".format(image_name, addlversion))
                with open(mf_path, "w") as source:
                    source.write(out)
            temp_name_list = os.path.basename(ova_name).split('-')
            temp_name_list = temp_name_list[:2] + ["hw{}".format(addlversion)] + temp_name_list[2:]
            new_ova_name = '-'.join(temp_name_list)
            new_ova_path = output_path + '/' + new_ova_name
            ovatar = tarfile.open(new_ova_path, "w", format=tarfile.USTAR_FORMAT)
            tar_files = [new_ovf_path, mf_path]
            for num_img in range(len(raw_image_name)):
                tar_files.append(image_name + "-disk" + str(num_img + 1) + ".vmdk")
            for name in tar_files:
                ovatar.add(name, arcname=os.path.basename(name))
            ovatar.close()
            os.remove(new_ovf_path)
            os.remove(mf_path)
    os.chdir(cwd)
    os.remove(ovf_path)
    for vmdk_img in vmdk_path:
        os.remove(vmdk_img)
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
    if options.config_path:
        config = Utils.jsonread(options.config_path)
    else:
        raise Exception("No config file defined")

    create_ova_image(options.raw_image_path, options.tools_bin_path, config)
