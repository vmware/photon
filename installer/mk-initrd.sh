#!/bin/bash
#################################################
#       Title:  mk-initrd                       #
#        Date:  2016-03-14                      #
#     Version:  1.0                             #
#      Author:  xiaolinl@vmware.com             #
#     Options:                                  #
#################################################
#	Overview
#		Generates an initrd
#	End
#

set +x                 # disable hashall
PRGNAME=${0##*/}	   # script name minus the path
source config.inc	   #	configuration parameters
source function.inc	   #	commonn functions
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"	#	set log file name


# Grab the name of the iso file 
if [ $# -lt 2 ]
then
    echo "Usage : " $0 " <output-initrd-name>  <pkg-list-path>"
    exit 1
fi
INITRD_OUTPUT_NAME=$1
PACKAGE_LIST_FILE=$2
LIVE_CD=$3
OUTPUT_DATA_PATH=$4
ROOTDIR=$5
PACKAGE_LIST_FILE_BASE_NAME=$(basename "${PACKAGE_LIST_FILE}")
#- Step 3 Setting up the boot loader
WORKINGDIR=${BUILDROOT}
BUILDROOT=${BUILDROOT}/${ROOTDIR}

rm -f ${BUILDROOT}/installer/*.pyc
rm -rf ${BUILDROOT}/installer/BUILD_DVD
# Copy package list json files, dereference symlinks
cp -rf -L $OUTPUT_DATA_PATH/*.json ${BUILDROOT}/installer/

# Step 4.5 Create necessary devices
mkfifo ${BUILDROOT}/dev/initctl
mknod ${BUILDROOT}/dev/ram0 b 1 0
mknod ${BUILDROOT}/dev/ram1 b 1 1
mknod ${BUILDROOT}/dev/ram2 b 1 2
mknod ${BUILDROOT}/dev/ram3 b 1 3
mknod ${BUILDROOT}/dev/sda b 8 0


#- Step 5 - Creating the boot script
mkdir -p ${BUILDROOT}/etc/systemd/scripts

# Step 6 create fstab
cp BUILD_DVD/fstab ${BUILDROOT}/etc/fstab

mkdir -p ${BUILDROOT}/etc/yum.repos.d
cat >> ${BUILDROOT}/etc/yum.repos.d/photon-iso.repo <<EOF
[photon-iso]
name=VMWare Photon Linux 1.0(x86_64)
baseurl=file:///mnt/cdrom/RPMS
gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
gpgcheck=1
enabled=1
skip_if_unavailable=True​
EOF

#- Step 7 - Create installer script
if [ "$LIVE_CD" = false ] ; then

cat >> ${BUILDROOT}/bin/bootphotoninstaller << EOF
#!/bin/bash
cd /installer
./isoInstaller.py --json-file=$PACKAGE_LIST_FILE_BASE_NAME 2> /var/log/installer && shutdown -r now
/bin/bash
EOF

chmod 755 ${BUILDROOT}/bin/bootphotoninstaller

fi

cat >> ${BUILDROOT}/init << EOF
mount -t proc proc /proc
/lib/systemd/systemd
EOF
chmod 755 ${BUILDROOT}/init

#adding autologin to the root user
# and set TERM=linux for installer
sed -i "s/ExecStart.*/ExecStart=-\/sbin\/agetty --autologin root --noclear %I linux/g" ${BUILDROOT}/lib/systemd/system/getty@.service

#- Step 7 - Create installer script
if [ "$LIVE_CD" = false ] ; then

    sed -i "s/root:.*/root:x:0:0:root:\/root:\/bin\/bootphotoninstaller/g" ${BUILDROOT}/etc/passwd

fi

mkdir -p ${BUILDROOT}/mnt/photon-root/photon-chroot
rm -rf ${BUILDROOT}/RPMS
rm -rf ${BUILDROOT}/LOGS

if [ "$LIVE_CD" = false ] ; then
    # Cleaning up
    #Remove our rpm database as it fills up the ramdisk
    rm -rf ${BUILDROOT}/home/*
    rm -rf ${BUILDROOT}/var/lib/rpm

    # Remove the boot directory
    rm -rf ${BUILDROOT}/boot

    #Remove the include files.
    rm -rf ${BUILDROOT}/usr/include

    # TODO: mbassiouny, Find a clean way to do that
    for i in `ls ${BUILDROOT}/usr/share/`; do
    	if [ $i != 'terminfo' -a $i != 'cracklib' -a $i != 'grub' ]; then
    		rm -rf ${BUILDROOT}/usr/share/$i
    	fi
    done

fi

# Generate the intird
echo "${WORKINGDIR}/isolinux/${INITRD_OUTPUT_NAME}" >> ~/bbb
pushd $BUILDROOT
(find . | cpio -o -H newc --quiet | gzip -9 ) > ${WORKINGDIR}/${INITRD_OUTPUT_NAME}
popd
rm -rf $BUILDROOT
