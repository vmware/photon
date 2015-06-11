#!/bin/bash
#################################################
#       Title:  mk-install-iso                  #
#        Date:  2014-11-26                      #
#     Version:  1.0                             #
#      Author:  dthaluru@vmware.com             #
#     Options:                                  #
#################################################
#	Overview
#		Generates a photon iso
#	End
#

set -o errexit		# exit if error...insurance ;)
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
PRGNAME=${0##*/}	# script name minus the path
source config.inc		#	configuration parameters
source function.inc		#	commonn functions
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"	#	set log file name


# Grab the name of the iso file 
if [ $# -lt 2 ]
	then
		echo "Usage : " $0 " <output-iso-with-path>  <tools path>"
		exit 1
fi
ISO_OUTPUT_NAME=$1
TOOLS_PATH=$2
PACKAGE_LIST_FILE=$3


#- Step 3 Setting up the boot loader

mkdir ${BUILDROOT}/isolinux
cp BUILD_DVD/isolinux/* ${BUILDROOT}/isolinux/

mv ${BUILDROOT}/boot/* ${BUILDROOT}/isolinux/
rmdir ${BUILDROOT}/boot
ln -s isolinux ${BUILDROOT}/boot

find ${BUILDROOT} -name linux-[0-9]*.rpm | head -1 | xargs rpm2cpio | cpio -iv --to-stdout ./boot/vmlinuz* > ${BUILDROOT}/boot/vmlinuz

cp -r ../installer ${BUILDROOT}/${PARENT}
# replace default package_list with specific one
cp $PACKAGE_LIST_FILE ${BUILDROOT}/${PARENT}/installer/package_list.json
rm -f ${BUILDROOT}/${PARENT}/installer/*.pyc

#ID in the initrd.gz now is PHOTON_VMWARE_CD . This is how we recognize that the cd is actually ours. touch this file there.
touch ${BUILDROOT}/PHOTON_VMWARE_CD

#- Step 4 - Move /etc /var /root /home to /fake/needwrite

mkdir -p ${BUILDROOT}/fake/{needwrite,ramdisk}
mv ${BUILDROOT}/var/ ${BUILDROOT}/tmp ${BUILDROOT}/fake/needwrite/
ln -s fake/needwrite/var ${BUILDROOT}/var
ln -s fake/needwrite/tmp ${BUILDROOT}/tmp

# Step 4.5 Create necessary devices
mkfifo ${BUILDROOT}/dev/initctl
mknod ${BUILDROOT}/dev/ram0 b 1 0
mknod ${BUILDROOT}/dev/ram1 b 1 1
mknod ${BUILDROOT}/dev/ram2 b 1 2
mknod ${BUILDROOT}/dev/ram3 b 1 3
mknod ${BUILDROOT}/dev/sda b 8 0


#- Step 5 - Creating the boot script
mkdir -p ${BUILDROOT}/etc/systemd/scripts
cp BUILD_DVD/create_ramdisk ${BUILDROOT}/bin/create_ramdisk

# Step 6 create fstab

cp BUILD_DVD/fstab ${BUILDROOT}/etc/fstab

#- Step 7 - Create installer script

cat >> ${BUILDROOT}/bin/bootphotoninstaller << EOF
#!/bin/bash
create_ramdisk
cd ${PARENT}/installer
./isoInstaller.py 2> /var/log/installer && shutdown -r now
/bin/bash
EOF

chmod 755 ${BUILDROOT}/bin/bootphotoninstaller

#adding autologin to the root user
sed -i "s/ExecStart.*/ExecStart=-\/sbin\/agetty --autologin root --noclear %I $TERM/g" ${BUILDROOT}/lib/systemd/system/getty@.service

sed -i "s/root:.*/root:x:0:0:root:\/root:\/bin\/bootphotoninstaller/g" ${BUILDROOT}/etc/passwd

mkdir -p ${BUILDROOT}/mnt/photon-root
cp $TOOLS_PATH/tools.tar.gz ${BUILDROOT}/${PARENT}/

#creating rpm repo in cd..
createrepo --database ${BUILDROOT}/${PARENT}/RPMS

rm -rf ${BUILDROOT}/${PARENT}/LOGS

#Remove our rpm database as it fills up the ramdisk
rm -rf ${BUILDROOT}/var/lib/rpm
find "$BUILDROOT"/{,usr/}lib -type f -exec strip --strip-debug '{}' ';' > /dev/null 2>&1
find "$BUILDROOT"/{,usr/}{bin,sbin} -type f -exec strip --strip-unneeded '{}' ';' > /dev/null 2>&1
rm -rf $BUILDROOT/tools
#Step 9 Generate the ISO!!!!
pushd $BUILDROOT
mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat \
		-no-emul-boot -boot-load-size 4 -boot-info-table -V "PHOTON_$(date +%Y%m%d)" \
		$BUILDROOT >$ISO_OUTPUT_NAME

popd




