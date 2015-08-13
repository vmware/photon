import os
import subprocess
import re

PRE_INSTALL = "pre-install"
POST_INSTALL = "post-install"

def partition_disk(disk, docker_partition_size = None, swap_partition_size = None):
    partitions_data = {}
    partitions_data['disk'] = disk

    root_partition_number = 2
    curr_partition_number = root_partition_number
    partitions_data['root'] = disk + `root_partition_number`

    if docker_partition_size != None:
        docker_partition_number = curr_partition_number + 1
        curr_partition_number = curr_partition_number + 1
        partitions_data['docker'] = disk + `docker_partition_number`

    if swap_partition_size != None:
        swap_partition_number = curr_partition_number + 1
        curr_partition_number = curr_partition_number + 1
        partitions_data['swap'] = disk + `swap_partition_number`

    output = open(os.devnull, 'w')

    # Clear the disk
    process = subprocess.Popen(['sgdisk', '-o', '-g', partitions_data['disk']], stdout = output)
    retval = process.wait()
    if retval != 0:
    	return None


    partition_cmd = ['sgdisk', '-n', '1::+2M']
    if swap_partition_size != None:
        partition_cmd.extend(['-n', '{}:-{}M'.format(swap_partition_number, swap_partition_size)])
    if docker_partition_size != None:
        partition_cmd.extend(['-n', '{}:-{}M'.format(docker_partition_number, docker_partition_size)])       
    partition_cmd.extend(['-n', `root_partition_number`, '-p', partitions_data['disk']])

    process = subprocess.Popen(partition_cmd, stdout = output)
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

    # format the docker partition
    if docker_partition_size != None:
        process = subprocess.Popen(['mkfs', '-t', 'ext4', partitions_data['docker']], stdout = output)
        retval = process.wait()
        if retval != 0:
            return None 

    # format the swap partition
    if swap_partition_size != None:
        process = subprocess.Popen(['mkswap', partitions_data['swap']], stdout = output)
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