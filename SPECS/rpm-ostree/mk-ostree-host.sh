#!/bin/bash
#################################################
#	Title:	mk-ostree-host			#
#        Date:	2017-09-22	 		#
#     Version:	1.0				#
#      Author:	dheerajs@vmware.com		#
#     Options:					#
#################################################
#	Overview
#		Creating rpm-ostree host raw file
#	End
#
set -o errexit    # exit if any command returns non true return value
set -o nounset    # exit if you try to use uninitialised variable
PRGNAME=${0##*/}  # script name minus the path
LOGFILE=/var/log/"${PRGNAME}-$(date +%Y-%m-%d).log"
source function.inc
NARGS=10
ARGS_PASSED=$#
SDA3=/dev/sda3

while [[ $# > 0 ]]
do
        key="$1"
        shift

        case $key in
                -s|--FILE_SIZE)
                FILE_SIZE="$1"
                shift
        ;;
                -n|--IMG_NAME)
                RAW_IMAGE_NAME="$1".raw
                shift
        ;;
                -i|--IP_ADDR)
                IP_ADDR="$1"
                shift
        ;;
                -r|--REPO_REF)
                REPO_REF="$1"
                shift
        ;;
                -m|--MOUNT_POINT)
                MOUNT_POINT="$1"
                shift
        ;;
                -h|--help)
                echo 'Usage:'
                echo '-s|--FILE_SIZE           :Total Size in GB. Make sure you have this space in your disk'
                echo '-n|--RAW_IMAGE_NAME      :Name of the Raw file'
                echo '-i|--IP_ADDR             :rpm-ostree server IP address'
                echo '-r|--REPO_REF            :rpm-ostree ref ex. photon/2.0/x86_64/base'
                echo '-m|--MOUNT_POINT         :mount point ex. /mnt/photon-root'
                exit 0
        ;;
        *)
                # unknown option
        ;;
        esac
done

if [ $ARGS_PASSED -ne $NARGS ]; then
   echo "Error in the arguments passed. Try ./mk-ostree-host.sh -h for help"
   exit 1
fi

function mount_devices {
    run_command "Mount devices in deployment" "mount -t bind -o bind,defaults /dev  ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/dev" "${LOGFILE}"
    run_command "Mount devices in deployment" "mount -t devpts -o gid=5,mode=620 devpts  ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/dev/pts" "${LOGFILE}"
    run_command "Mount devices in deployment" "mount -t tmpfs -o defaults tmpfs  ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/dev/shm" "${LOGFILE}"
    run_command "Mount devices in deployment" "mount -t proc -o defaults proc  ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/proc" "${LOGFILE}"
    run_command "Mount devices in deployment" "mount -t bind -o bind,defaults /run  ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/run" "${LOGFILE}"
    run_command "Mount devices in deployment" "mount -t sysfs -o defaults sysfs ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/sys" "${LOGFILE}"
}
function unmount_devices {
    run_command "Unmount devices in deployment" "umount ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/sys" "${LOGFILE}"
    run_command "Unmount devices in deployment" "umount ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/run" "${LOGFILE}"
    run_command "Unmount devices in deployment" "umount ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/proc" "${LOGFILE}"
    run_command "Unmount devices in deployment" "umount ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/dev/shm" "${LOGFILE}"
    run_command "Unmount devices in deployment" "umount ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/dev/pts" "${LOGFILE}"
    run_command "Unmount devices in deployment" "umount ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/dev" "${LOGFILE}"
}

function create_systemd_tmpfile {
    run_command "Create systemd-tmpfiles" "systemd-tmpfiles --create --boot --root=${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 --prefix=/var/home" "${LOGFILE}"
    run_command "Create systemd-tmpfiles" "systemd-tmpfiles --create --boot --root=${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 --prefix=/var/roothome" "${LOGFILE}"
    run_command "Create systemd-tmpfiles" "systemd-tmpfiles --create --boot --root=${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 --prefix=/var/lib/rpm" "${LOGFILE}"
    run_command "Create systemd-tmpfiles" "systemd-tmpfiles --create --boot --root=${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 --prefix=/var/opt" "${LOGFILE}"
    run_command "Create systemd-tmpfiles" "systemd-tmpfiles --create --boot --root=${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 --prefix=/var/srv" "${LOGFILE}"
    run_command "Create systemd-tmpfiles" "systemd-tmpfiles --create --boot --root=${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 --prefix=/var/userlocal" "${LOGFILE}"
    run_command "Create systemd-tmpfiles" "systemd-tmpfiles --create --boot --root=${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 --prefix=/var/mnt" "${LOGFILE}"
    run_command "Create systemd-tmpfiles" "systemd-tmpfiles --create --boot --root=${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 --prefix=/var/spool/mail" "${LOGFILE}"
}

function unmount_loop_devices {
    run_command "Unmounting p2" "umount ${ROOT_PARTITION}" "${LOGFILE}"
    run_command "Unmounting p3" "umount ${SYSROOT_BOOT_PARTITION}" "${LOGFILE}"
    run_command "kpartx loop0" "kpartx -d ${DISK_DEVICE}" "${LOGFILE}"
    run_command "delete loop0" "losetup -d ${DISK_DEVICE}" "${LOGFILE}"
}

function rpm_ostree_init_deploy {
    run_command "Init the Ostree Repo" "ostree --repo=${MOUNT_POINT}/repo init --mode=archive-z2" "${LOGFILE}"
    run_command "Ostree Init FS" "ostree admin --sysroot=${MOUNT_POINT} init-fs ${MOUNT_POINT}" "${LOGFILE}"
    run_command "Add Remote" "ostree remote add --repo=${MOUNT_POINT}/ostree/repo --set=gpg-verify=false photon http://${IP_ADDR}" "${LOGFILE}"
    run_command "Pull Repo" "ostree pull --repo=${MOUNT_POINT}/ostree/repo photon ${REPO_REF}" "${LOGFILE}"
    run_command "Init-OS" "ostree admin --sysroot=${MOUNT_POINT} os-init photon" "${LOGFILE}"
    run_command "Deploy Ostree" "ostree admin --sysroot=${MOUNT_POINT} deploy --os=photon photon:${REPO_REF}" "${LOGFILE}"
}

function install_generate_grub {
    run_command "Install grub" "chroot ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 bash -c \"grub2-install /dev/loop0\"" "${LOGFILE}"
    run_command "Generate grub.cfg file" "chroot ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 bash -c \"grub2-mkconfig -o /boot/grub2/grub.cfg\"" "${LOGFILE}"
    run_command "Set boot volume in grub config file" "chroot ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 bash -c \"ostree admin instutil set-kargs root=${ROOT_PARTITION}\"" "${LOGFILE}"
    run_command "Replace ${ROOT_PARTITION} with ${SDA3} in cfg file" "sed -i 's:${ROOT_PARTITION}:${SDA3}:' ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/boot/loader/grub.cfg" "${LOGFILE}"
    run_command "Replace ${ROOT_PARTITION} with ${SDA3} in loader conf file" "sed -i 's:${ROOT_PARTITION}:${SDA3}:' ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/boot/loader/entries/ostree-photon-0.conf" "${LOGFILE}"
    run_command "Remove grub config from /boot/grub2" "chroot ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 bash -c \"rm /boot/grub2/grub.cfg\"" "${LOGFILE}"
    run_command "Create a link file to /boot/loader/grub.cfg from /boot/grub2" "chroot ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 bash -c \"cd /boot/grub2/ && ln -sf ../loader/grub.cfg ./grub.cfg\"" "${LOGFILE}"
}

function update_fstab {
    run_command "Update /etc/fstab in chroot for /dev/sda3" "echo \"/dev/sda3    /        ext4   defaults   1 1  \" >> ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/etc/fstab" "${LOGFILE}"
    run_command "Update /etc/fstab in chroot for /dev/sda2" "echo \"/dev/sda2    /boot    ext4   defaults   1 2  \" >> ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/etc/fstab" "${LOGFILE}"
}

function create_password {
    run_command "Echo password to a file. Change this password" "echo \"root:changeme\" >> ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/root/mypwdfile" "${LOGFILE}"
    run_command "Change Password of root to changeme" "chroot ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0 bash -c \"cat root/mypwdfile | chpasswd\"" "${LOGFILE}"
    run_command "Delete the temporary mypwdfile" "rm ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/root/mypwdfile" "${LOGFILE}"
}

run_command "Install gptfdisk kpartx and device-mapper-devel" "tdnf -y install gptfdisk kpartx device-mapper-devel device-mapper-libs" "${LOGFILE}"

echo "Creating raw disk file " $RAW_IMAGE_NAME " of size " $FILE_SIZE
dd if=/dev/zero of=$RAW_IMAGE_NAME bs=1 seek=$(($FILE_SIZE * 1024 * 1024 * 1024)) count=0
chmod 755 $RAW_IMAGE_NAME

echo "Associating loopdevice to raw disk"
DISK_DEVICE=`losetup --show -f $RAW_IMAGE_NAME`

echo "Creating partition on raw disk"
sgdisk -n 1::+2M -n 2::+300M -n 3: -p $DISK_DEVICE 
sgdisk -t1:ef02 $DISK_DEVICE

echo "Mapping device partition to loop device"
kpartx -avs $DISK_DEVICE

DEVICE_NAME=`echo $DISK_DEVICE|cut -c6- `

echo "Adding file system to device partition"
mkfs -t ext4 /dev/mapper/${DEVICE_NAME}p2
mkfs -t ext4 /dev/mapper/${DEVICE_NAME}p3

ROOT_PARTITION=/dev/mapper/${DEVICE_NAME}p3
SYSROOT_BOOT_PARTITION=/dev/mapper/${DEVICE_NAME}p2

SYSROOT_BOOT=${MOUNT_POINT}/boot
SYSROOT_OSTREE=${MOUNT_POINT}/ostree

run_command "Making Mount Point Directory" "mkdir -p ${MOUNT_POINT}" "${LOGFILE}"
run_command "Mount Root" "mount ${ROOT_PARTITION} ${MOUNT_POINT}" "$LOGFILE"
run_command "Making Sysroot Boot Directory" "mkdir -p ${SYSROOT_BOOT}" "${LOGFILE}"
run_command "Mount Sysroot Boot" "mount ${SYSROOT_BOOT_PARTITION} ${SYSROOT_BOOT}" "${LOGFILE}"
run_command "Make repo directory for ostree" "mkdir -p ${MOUNT_POINT}/repo" "${LOGFILE}"

rpm_ostree_init_deploy

id=$(cat ${MOUNT_POINT}/ostree/repo/refs/remotes/photon/${REPO_REF})

create_systemd_tmpfile

mount_devices

run_command "Mount Boot" "mount --bind ${MOUNT_POINT}/boot ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/boot" "${LOGFILE}"
run_command "Mount Sysroot" "mount --bind ${MOUNT_POINT} ${MOUNT_POINT}/ostree/deploy/photon/deploy/${id}.0/sysroot" "${LOGFILE}"

install_generate_grub

update_fstab

create_password

unmount_devices

unmount_loop_devices
