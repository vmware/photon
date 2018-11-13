import os
import subprocess
import re

PRE_INSTALL = "pre-install"
POST_INSTALL = "post-install"

LOG_LEVEL_DESC = ["emerg", "alert", "crit", "err", "warning", "notice", "info", "debug"]
LOG_FILE_NAME = "/var/log/installer.log"
TDNF_LOG_FILE_NAME = "/var/log/tdnf.log"
TDNF_CMDLINE_FILE_NAME = "/var/log/tdnf.cmdline"
KS_POST_INSTALL_LOG_FILE_NAME = "/var/log/installer-kickstart.log"
SIGNATURE   = "localhost echo"
LOG_EMERG   = 0
LOG_ALERT   = 1
LOG_CRIT    = 2
LOG_ERROR   = 3
LOG_WARNING = 4
LOG_NOTICE  = 5
LOG_INFO    = 6
LOG_DEBUG   = 7

default_partitions = [
    {"mountpoint": "/", "size": 0, "filesystem": "ext4"},
    ]

def partition_compare(p):
    if 'mountpoint' in p:
        return (1, len(p['mountpoint']), p['mountpoint'])
    return (0, 0, "A")

def partition_disk(disk, partitions):
    partitions_data = {}
    partitions_data['disk'] = disk
    partitions_data['partitions'] = partitions
    output = open(os.devnull, 'w')

    # Clear the disk
    process = subprocess.Popen(['sgdisk', '-o', '-g', disk], stderr=output, stdout=output)
    retval = process.wait()
    if retval != 0:
        log(LOG_ERROR, "Failed clearing disk {0}".format(disk))
        return None

    # Partitioning the disk
    extensible_partition = None
    partitions_count = len(partitions)
    partition_number = 3
    # Add part size and grub flags

    bios_flag = ':ef02'
    part_size = '+2M'
    # Adding the bios partition
    partition_cmd = ['sgdisk', '-n 1::' + part_size]

    efi_flag = ':ef00'
    part_size = '+3M'
    # Adding the efi partition
    partition_cmd.extend(['-n 2::' + part_size])
    # Adding the known size partitions
    for partition in partitions:
        if partition['size'] == 0:
            # Can not have more than 1 extensible partition
            if extensible_partition != None:
                log(LOG_ERROR, "Can not have more than 1 extensible partition")
                return None
            extensible_partition = partition
        else:
            partition_cmd.extend(['-n', '{}::+{}M'.format(partition_number, partition['size'])])

        partition['partition_number'] = partition_number
        prefix = ''
        if 'nvme' in disk or 'mmcblk' in disk:
            prefix = 'p'
        partition['path'] = disk + prefix + repr(partition_number)
        partition_number = partition_number + 1

    # Adding the last extendible partition
    if extensible_partition:
        partition_cmd.extend(['-n', repr(extensible_partition['partition_number'])])

    partition_cmd.extend(['-p', disk])

    # Run the partitioning command
    process = subprocess.Popen(partition_cmd, stderr=output, stdout=output)
    retval = process.wait()
    if retval != 0:
        log(LOG_ERROR, "Faild partition disk, command: {0}". format(partition_cmd))
        return None

    process = subprocess.Popen(['sgdisk', '-t1' + bios_flag, disk], stderr=output, stdout=output)
    retval = process.wait()
    if retval != 0:
        log(LOG_ERROR, "Failed to setup bios partition")
        return None

    process = subprocess.Popen(['sgdisk', '-t2' + efi_flag, disk], stderr=output, stdout=output)
    retval = process.wait()
    if retval != 0:
        log(LOG_ERROR, "Failed to setup efi partition")
        return None
    partitions_data['dualboot'] = 'true'
    # Format the filesystem
    for partition in partitions:
        if "mountpoint" in partition:
            if partition['mountpoint'] == '/':
                partitions_data['root'] = partition['path']
                partitions_data['root_partition_number'] = partition['partition_number']
            elif partition['mountpoint'] == '/boot':
                partitions_data['boot'] = partition['path']
                partitions_data['boot_partition_number'] = partition['partition_number']
                partitions_data['bootdirectory'] = '/'
        if partition['filesystem'] == "swap":
            process = subprocess.Popen(['mkswap', partition['path']], stderr=output, stdout=output)
            retval = process.wait()
            if retval != 0:
                log(LOG_ERROR, "Failed to create swap partition @ {}".format(partition['path']))
                return None
        else:
            mkfs_cmd = ['mkfs', '-t', partition['filesystem'], partition['path']]
            process = subprocess.Popen(mkfs_cmd, stderr=output, stdout=output)
            retval = process.wait()
            if retval != 0:
                log(LOG_ERROR,
                    "Failed to format {} partition @ {}".format(partition['filesystem'],
                                                                partition['path']))
                return None

    # Check if there is no root partition
    if 'root' not in partitions_data:
        log(LOG_ERROR, "There is no partition assigned to root '/'")
        return None

    if 'boot' not in partitions_data:
        partitions_data['boot'] = partitions_data['root']
        partitions_data['boot_partition_number'] = partitions_data['root_partition_number']
        partitions_data['bootdirectory'] = '/boot/'

    partitions.sort(key=lambda p: partition_compare(p))

    return partitions_data

def replace_string_in_file(filename, search_string, replace_string):
    with open(filename, "r") as source:
        lines = source.readlines()

    with open(filename, "w") as destination:
        for line in lines:
            destination.write(re.sub(search_string, replace_string, line))

def log(type, message):
    command = 'systemd-cat echo \"<{}> {} : {}\"'.format(type, LOG_LEVEL_DESC[type], message)
    process = subprocess.Popen([command], shell=True)
    retval = process.wait()
    return retval

def dump(type, filename):
    command = ("journalctl -p {0} | grep --line-buffered \"{1}\" > {2}"
               .format(LOG_LEVEL_DESC[type], SIGNATURE, filename))
    process = subprocess.Popen([command], shell=True)
    retval = process.wait()
    return retval

def dump(filename):
    command = "journalctl | grep --line-buffered \"{0}\" > {1}".format(SIGNATURE, filename)
    process = subprocess.Popen([command], shell=True)
    retval = process.wait()
    return retval
