#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from argparse import ArgumentParser
from installer import Installer
import crypt
import random
import string
import subprocess
import sys
import os
from jsonwrapper import JsonWrapper
from packageselector import PackageSelector
import json

def query_yes_no(question, default="no"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower().strip()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def partition_disk(disk):
    partitions_data = {}
    partitions_data['disk'] = disk
    partitions_data['root'] = disk + '2'
    partitions_data['swap'] = disk + '3'

    # Clear the disk
    process = subprocess.Popen(['sgdisk', '-z', partitions_data['disk']])
    retval = process.wait()

    # 1: grub, 2: swap, 3: filesystem
    process = subprocess.Popen(['sgdisk', '-n', '1::+2M', '-n', '3:-3G:', '-n', '2:', '-p', partitions_data['disk']])
    retval = process.wait()

    # Add the grub flags
    process = subprocess.Popen(['sgdisk', '-t1:ef02', partitions_data['disk']])
    retval = process.wait()

    # format the swap
    process = subprocess.Popen(['mkswap', partitions_data['swap']])
    retval = process.wait()

    # format the file system
    process = subprocess.Popen(['mkfs', '-t', 'ext4', partitions_data['root']])
    retval = process.wait()
    return partitions_data

def create_vmdk_and_partition(config, vmdk_path):
    partitions_data = {}

    process = subprocess.Popen(['./mk-setup-vmdk.sh', '-rp', config['size']['root'], '-sp', config['size']['swap'], '-n', vmdk_path, '-m'], stdout=subprocess.PIPE)
    count = 0
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        if line.startswith("DISK_DEVICE="):
            partitions_data['disk'] = line.replace("DISK_DEVICE=", "").strip()
            count += 1
        elif line.startswith("ROOT_PARTITION="):
            partitions_data['root'] = line.replace("ROOT_PARTITION=", "").strip()
            partitions_data['boot'] = partitions_data['root']
            partitions_data['bootdirectory'] = '/boot/'
            count += 1

    if count == 2:
        partitions_data['partitions'] = [{'path': partitions_data['root'], 'mountpoint': '/', 'filesystem': 'ext4'}]

    return partitions_data, count == 2

def create_rpm_list_to_copy_in_iso(build_install_option, output_data_path):
    json_wrapper_option_list = JsonWrapper(build_install_option)
    option_list_json = json_wrapper_option_list.read()
    options_sorted = option_list_json.items()
    packages = []
    for install_option in options_sorted:
        if install_option[0] != "iso":
            file_path = os.path.join(output_data_path, install_option[1]["file"])
            json_wrapper_package_list = JsonWrapper(file_path)
            package_list_json = json_wrapper_package_list.read()
            packages = packages + package_list_json["packages"]
    return packages

def create_additional_file_list_to_copy_in_iso(base_path, build_install_option):
    json_wrapper_option_list = JsonWrapper(build_install_option)
    option_list_json = json_wrapper_option_list.read()
    options_sorted = option_list_json.items()
    file_list = []
    for install_option in options_sorted:
        if install_option[1].has_key("additional-files"):
            file_list = file_list + map(lambda filename: os.path.join(base_path, filename), install_option[1].get("additional-files")) 
    return file_list

def get_live_cd_status_string(build_install_option):
    json_wrapper_option_list = JsonWrapper(build_install_option)
    option_list_json = json_wrapper_option_list.read()
    options_sorted = option_list_json.items()
    file_list = []
    for install_option in options_sorted:
        if install_option[1].has_key("live-cd"):
            if install_option[1].get("live-cd") == True:
                return "true"
    return "false"

def generate_pkginfo_text_file(list_rpms, pkg_info_json_file_path, pkg_info_text_file_path):
    if not os.path.isfile(pkg_info_json_file_path):
        return
    pkg_info_json_file = open(pkg_info_json_file_path,'r')
    data = json.load(pkg_info_json_file)
    pkg_info_json_file.close()
    list_lines = []
    list_lines.append("#%{name},%{version},%{release},%{arch},%{sourcerpm}\n") 
    for rpm in list_rpms:
       if data.has_key(rpm):
           list_lines.append(data[rpm]["name"]+","+data[rpm]["version"]+","+data[rpm]["release"]+","+data[rpm]["arch"]+","+data[rpm]["sourcerpm"]+"\n") 
    pkg_info_text_file = open(pkg_info_text_file_path,'w')
    pkg_info_text_file.writelines(list_lines)
    pkg_info_text_file.close()

if __name__ == '__main__':

    parser = ArgumentParser(prog='PROG', usage = 'Usage: %prog [options] <config file> <tools path>')

    parser.add_argument("-i", "--iso-path",  dest="iso_path")
    parser.add_argument("-j", "--src-iso-path",  dest="src_iso_path")
    parser.add_argument("-v", "--vmdk-path", dest="vmdk_path")
    parser.add_argument("-w",  "--working-directory",  dest="working_directory", default="/mnt/photon-root")
    parser.add_argument("-l",  "--log-path",  dest="log_path", default="../stage/LOGS")
    parser.add_argument("-r",  "--rpm-path",  dest="rpm_path", default="../stage/RPMS")
    parser.add_argument("-x",  "--srpm-path",  dest="srpm_path", default="../stage/SRPMS")
    parser.add_argument("-o", "--output-data-path", dest="output_data_path", default="../stage/common/data/")
    parser.add_argument("-f", "--force", action="store_true", dest="force", default=False)
    parser.add_argument("-p", "--package-list-file", dest="package_list_file", default="../common/data/build_install_options_all.json")
    parser.add_argument("-m", "--stage-path", dest="stage_path", default="../stage")
    parser.add_argument("-c", "--dracut-configuration", dest="dracut_configuration_file", default="../common/data/dracut_configuration.json")
    parser.add_argument("-s", "--json-data-path", dest="json_data_path", default="../stage/common/data/")
    parser.add_argument("-u", "--pkginfo-json-file", dest="pkginfo_json_file", default="../common/data/pkg_info.json")
    parser.add_argument("-z", "--pkginfo-txt-file", dest="pkginfo_txt_file", default="../stage/pkg_info.txt")
    parser.add_argument('configfile', nargs='?')
    options = parser.parse_args()
    #parser.error("Incorrect arguments")
    if options.iso_path or options.src_iso_path:
        # Check the arguments
        if options.configfile:
            parser.error("Incorrect arguments")
        config = {}
        config['iso_system'] = True
        config['vmdk_install'] = False
    elif options.vmdk_path:
        # Check the arguments
        if not options.configfile:
            parser.error("Incorrect arguments")

        # Read the conf file
        config = (JsonWrapper(options.configfile)).read()
        config['disk'], success = create_vmdk_and_partition(config, options.vmdk_path)
        if not success:
            print "Unexpected failure, please check the logs"
            sys.exit(1)

        config['initrd_dir'] = "/boot"

        config['iso_system'] = False
        config['vmdk_install'] = True

    else:
        # Check the arguments
        if  not options.configfile:
            parser.error("Incorrect arguments")

        # Read the conf file
        config = (JsonWrapper(options.configfile)).read()

        config['iso_system'] = False
        config['vmdk_install'] = False

    if 'password' in config:
        # crypt the password if needed
        if config['password']['crypted']:
            config['password'] = config['password']['text']
        else:
            config['password'] = crypt.crypt(config['password']['text'], "$6$" + "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)]))

    # Check the installation type
    json_wrapper_option_list = JsonWrapper(options.package_list_file)
    option_list_json = json_wrapper_option_list.read()
    options_sorted = option_list_json.items()
    base_path = os.path.dirname(options.package_list_file)

    packages = []
    additional_files_to_copy_from_stage_to_iso = []
    if config['iso_system'] == True:
        for install_option in options_sorted:
            if install_option[0] == "iso":
                json_wrapper_package_list = JsonWrapper(os.path.join(base_path, install_option[1]["file"]))
                package_list_json = json_wrapper_package_list.read()
                packages = package_list_json["packages"]
    else:
        packages = PackageSelector.get_packages_to_install(options_sorted, config['type'], options.output_data_path)

    config['packages'] = packages

    if options.iso_path:
        if os.path.isfile(options.dracut_configuration_file):
            json_wrapper_package_list = JsonWrapper(options.dracut_configuration_file)
            dracut_configuration_list_json = json_wrapper_package_list.read()
            config["dracut_configuration"]=dracut_configuration_list_json["dracut_configuration"]

    # Cleanup the working directory
    if not options.force:
        proceed = query_yes_no("This will remove everything under {0}. Are you sure?".format(options.working_directory))
        if not proceed:
            sys.exit(0)

    if (os.path.isdir(options.working_directory)):
        process = subprocess.Popen(['rm', '-rf', options.working_directory])
        retval = process.wait()
    else:
        process = subprocess.Popen(['mkdir', '-p', options.working_directory])
        retval = process.wait()

    process = subprocess.Popen(['mkdir', '-p', os.path.join(options.working_directory, "photon-chroot")])
    retval = process.wait()

    config['working_directory'] = options.working_directory

    # Run the installer
    package_installer = Installer(config, rpm_path = options.rpm_path, log_path = options.log_path)
    package_installer.install(None)

    # Making the iso if needed
    if options.iso_path:
        rpm_list = " ".join(create_rpm_list_to_copy_in_iso(options.package_list_file, options.output_data_path))
        files_to_copy = " ".join(create_additional_file_list_to_copy_in_iso(os.path.abspath(options.stage_path), options.package_list_file))
        live_cd = get_live_cd_status_string(options.package_list_file)
        process = subprocess.Popen(['./mk-install-iso.sh', '-w', options.working_directory, options.iso_path, options.rpm_path, options.package_list_file, rpm_list, options.stage_path, files_to_copy, live_cd, options.json_data_path])
        retval = process.wait()

    if options.src_iso_path:
        rpm_list = " ".join(create_rpm_list_to_copy_in_iso(options.package_list_file, options.output_data_path))
        process = subprocess.Popen(['./mk-src-iso.sh', '-w', options.working_directory, options.src_iso_path, options.srpm_path, rpm_list])
        retval = process.wait()
        list_rpms = rpm_list.split(" ")
        list_rpms = list(set(list_rpms))
        list_rpms.sort()
        generate_pkginfo_text_file(list_rpms, options.pkginfo_json_file, options.pkginfo_txt_file)

    # Cleaning up for vmdk
    if 'vmdk_install' in config and config['vmdk_install']:
        process = subprocess.Popen(['./mk-clean-vmdk.sh', config['disk']['disk']])
        process.wait()

    #Clean up the working directories
    if (options.iso_path or options.vmdk_path or options.src_iso_path):
        process = subprocess.Popen(['rm', '-rf', options.working_directory])
        retval = process.wait()
