import os
import subprocess
import commons

install_phase = commons.PRE_INSTALL
enabled = True

def partition_disk(disk):
    partitions_data = {}
    partitions_data['disk'] = disk
    partitions_data['root'] = disk + '2'

    output = open(os.devnull, 'w')

    # Clear the disk
    process = subprocess.Popen(['sgdisk', '-o', '-g', partitions_data['disk']], stdout = output)
    retval = process.wait()

    # 1: grub, 2: filesystem
    process = subprocess.Popen(['sgdisk', '-n', '1::+2M', '-n', '2:', '-p', partitions_data['disk']], stdout = output)
    retval = process.wait()

    # Add the grub flags
    process = subprocess.Popen(['sgdisk', '-t1:ef02', partitions_data['disk']], stdout = output)
    retval = process.wait()

    # format the file system
    process = subprocess.Popen(['mkfs', '-t', 'ext4', partitions_data['root']], stdout = output)
    retval = process.wait()
    return partitions_data

def execute(name, ks_config, config, root):

	if ks_config:
		config['disk'] = partition_disk(ks_config['disk'])
