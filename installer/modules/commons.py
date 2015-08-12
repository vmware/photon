import os
import subprocess
import re

PRE_INSTALL = "pre-install"
POST_INSTALL = "post-install"

def partition_disk(disk):
    partitions_data = {}
    partitions_data['disk'] = disk
    partitions_data['root'] = disk + '2'

    output = open(os.devnull, 'w')

    # Clear the disk
    process = subprocess.Popen(['sgdisk', '-o', '-g', partitions_data['disk']], stdout = output)
    retval = process.wait()
    if retval != 0:
    	return None

    # 1: grub, 2: filesystem
    process = subprocess.Popen(['sgdisk', '-n', '1::+2M', '-n', '2:', '-p', partitions_data['disk']], stdout = output)
    retval = process.wait()
    if retval != 0:
    	return None

    # Add the grub flags
    process = subprocess.Popen(['sgdisk', '-t1:ef02', partitions_data['disk']], stdout = output)
    retval = process.wait()
    if retval != 0:
    	return None

    # format the file system
    process = subprocess.Popen(['mkfs', '-t', 'ext4', partitions_data['root']], stdout = output)
    retval = process.wait()
    if retval != 0:
    	return None
    	
    return partitions_data

def replace_string_in_file(filename,  search_string,  replace_string):
    with open(filename, "r") as source:
        lines=source.readlines()

    with open(filename, "w") as destination:
        for line in lines:
            destination.write(re.sub(search_string,  replace_string,  line))