#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from optparse import OptionParser
from installer import Installer
import crypt
import random
import string
import subprocess
import sys
import os
from jsonwrapper import JsonWrapper

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
            count += 1
    
    return partitions_data, count == 2

if __name__ == '__main__':
    usage = "Usage: %prog [options] <config file> <tools path>"
    parser = OptionParser(usage)

    parser.add_option("-i", "--iso-path",  dest="iso_path")
    parser.add_option("-v", "--vmdk-path", dest="vmdk_path")
    parser.add_option("-w",  "--working-directory",  dest="working_directory", default="/mnt/photon-root")
    parser.add_option("-t",  "--tools-path",  dest="tools_path", default="../stage")
    parser.add_option("-r",  "--rpm-path",  dest="rpm_path", default="../stage/RPMS")
    parser.add_option("-f", "--force", action="store_true", dest="force", default=False)
    parser.add_option("-p", "--package-list-file", dest="package_list_file", default="package_list.json")
    
    (options,  args) = parser.parse_args()
    
    if options.iso_path:
        # Check the arguments
        if (len(args)) != 0:
            parser.error("Incorrect arguments")
        config = {}
        config['iso_system'] = True

    elif options.vmdk_path:
        # Check the arguments
        if (len(args)) != 1:
            parser.error("Incorrect arguments")

        # Read the conf file
        config = (JsonWrapper(args[0])).read()
        config['disk'], success = create_vmdk_and_partition(config, options.vmdk_path)
        if not success:
            print "Unexpected failure, please check the logs"
            sys.exit(1)

        config['iso_system'] = False
        config['vmdk_install'] = True

    else:
        # Check the arguments
        if (len(args)) != 1:
            parser.error("Incorrect arguments")

        # Read the conf file
        config = (JsonWrapper(args[0])).read()

        config['iso_system'] = False

    if 'password' in config:
        # crypt the password if needed
        if config['password']['crypted']:
            config['password'] = config['password']['text']
        else:
            config['password'] = crypt.crypt(config['password']['text'], "$6$" + "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)]))


    # Check the installation type
    package_list = JsonWrapper(options.package_list_file).read()
    if config['iso_system']:
        packages = package_list["iso_packages"]
    elif config['type'] == 'micro':
        packages = package_list["micro_packages"]
    elif config['type'] == 'minimal':
        packages = package_list["minimal_packages"]
    elif config['type'] == 'full':
        packages = package_list["minimal_packages"] + package_list["optional_packages"]
    else:
        #TODO: error
        packages = []
    config['packages'] = packages

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

    config['working_directory'] = options.working_directory

    # Run the installer
    package_installer = Installer(config, tools_path = options.tools_path, rpm_path = options.rpm_path, log_path = options.tools_path + "/LOGS")
    package_installer.install(None)

    # Making the iso if needed
    if config['iso_system']:
        process = subprocess.Popen(['./mk-install-iso.sh', '-w', options.working_directory, options.iso_path, options.tools_path, options.rpm_path, options.package_list_file])
        retval = process.wait()

    # Cleaning up for vmdk
    if 'vmdk_install' in config and config['vmdk_install']:
        process = subprocess.Popen(['./mk-clean-vmdk.sh', config['disk']['disk']])
        process.wait()

    #Clean up the working directories
    if (options.iso_path or options.vmdk_path):
        process = subprocess.Popen(['rm', '-rf', options.working_directory])
        retval = process.wait()
