import os
import subprocess
import re

PRE_INSTALL = "pre-install"
POST_INSTALL = "post-install"

LOG_LEVEL_DESC = ["emerg", "alert", "crit", "err", "warning", "notice", "info", "debug"]
LOG_FILE_NAME  = "/var/log/installer.log"
SIGNATURE   = "Photon echo"
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

def partition_compare(p1, p2):
    if 'mountpoint' in p1 and 'mountpoint' in p2:
        if len(p1['mountpoint']) == len(p2['mountpoint']):
            return cmp(p1['mountpoint'], p2['mountpoint'])
        return len(p1['mountpoint']) - len(p2['mountpoint'])
    return 0

def partition_disk(disk, partitions):
    partitions_data = {}
    partitions_data['disk'] = disk
    partitions_data['partitions'] = partitions
    output = open(os.devnull, 'w')

    # Clear the disk
    process = subprocess.Popen(['sgdisk', '-o', '-g', disk], stdout = output)
    retval = process.wait()
    if retval != 0:
        log(LOG_ERROR, "Failed clearing disk {0}".format(disk))
        return None

    # Partitioning the disk
    extensible_partition = None
    partitions_count = len(partitions)
    partition_number = 1
    # Adding the bios partition
    partition_cmd = ['sgdisk', '-n', `partitions_count + 1` + ':-2M:']
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
        if 'nvme' in disk:
            prefix = 'p'
        partition['path'] = disk + prefix + `partition_number`

    # Adding the last extendible partition
    if extensible_partition:
        partition_cmd.extend(['-n', `extensible_partition['partition_number']`])

    partition_cmd.extend(['-p', disk])

    # Run the partitioning command
    process = subprocess.Popen(partition_cmd, stdout = output)
    retval = process.wait()
    if retval != 0:
        log(LOG_ERROR, "Faild partition disk, command: {0}". format(partition_cmd))
        return None

    # Add the grub flags
    grub_flag = ':ef02'
    if os.path.isdir("/sys/firmware/efi"):
        grub_flag = ':ef00'

    process = subprocess.Popen(['sgdisk', '-t' + `partitions_count + 1` + grub_flag, disk], stdout = output)
    retval = process.wait()
    if retval != 0:
        log(LOG_ERROR, "Failed to setup grub partition")
        return None

    # Format the filesystem
    for partition in partitions:
        if "mountpoint" in partition:
            if partition['mountpoint'] == '/':
                partitions_data['root'] = partition['path']
            elif partition['mountpoint'] == '/boot':
                partitions_data['boot'] = partition['path']
                partitions_data['bootdirectory'] = '/'
        if partition['filesystem'] == "swap":
            process = subprocess.Popen(['mkswap', partition['path']], stdout = output)
            retval = process.wait()
            if retval != 0:
                log(LOG_ERROR, "Failed to create swap partition @ {}".format(partition['path']))
                return None
        else:
            process = subprocess.Popen(['mkfs', '-t', partition['filesystem'], partition['path']], stdout = output)
            retval = process.wait()
            if retval != 0:
                log(LOG_ERROR, "Failed to format {} partition @ {}".format(partition['filesystem'], partition['path']))
                return None

    # Check if there is no root partition
    if not 'root' in partitions_data:
        log(LOG_ERROR, "There is no partition assigned to root '/'")
        return None

    if not 'boot' in partitions_data:
        partitions_data['boot'] = partitions_data['root']
        partitions_data['bootdirectory'] = '/boot/'

    partitions.sort(lambda p1,p2: partition_compare(p1, p2))
	
    return partitions_data

def replace_string_in_file(filename,  search_string,  replace_string):
    with open(filename, "r") as source:
        lines=source.readlines()

    with open(filename, "w") as destination:
        for line in lines:
            destination.write(re.sub(search_string,  replace_string,  line))

def log(type, message):
    command = 'systemd-cat echo \"<{}> {} : {}\"'.format(type, LOG_LEVEL_DESC[type], message)
    process = subprocess.Popen([command], shell=True)
    retval = process.wait()
    return retval

def dump(type, filename):
    command = "journalctl -p {0} | grep --line-buffered \"{1}\" > {2}".format(LOG_LEVEL_DESC[type], SIGNATURE, filename)
    process = subprocess.Popen([command], shell=True)
    retval = process.wait()
    return retval

def dump(filename):
    command = "journalctl | grep --line-buffered \"{0}\" > {1}".format(SIGNATURE, filename)
    process = subprocess.Popen([command], shell=True)
    retval = process.wait()    
    return retval
