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

set +x                 # disable hashall
PRGNAME=${0##*/}	    # script name minus the path
source config.inc		#	configuration parameters
source function.inc		#	commonn functions
LOGFILE=/var/log/"${PRGNAME}-${LOGFILE}"	#	set log file name


# Grab the name of the iso file 
if [ $# -lt 2 ]
then
    echo "Usage : " $0 " <output-iso-with-path>  <rpms-path> <pkg-list-path>"
    exit 1
fi
ISO_OUTPUT_NAME=$1
RPMS_PATH=$2
PACKAGE_LIST_FILE=$3
RPM_LIST=$4
STAGE_PATH=$5
ADDITIONAL_FILES_TO_COPY_FROM_STAGE=$6
LIVE_CD=$7
OUTPUT_DATA_PATH=$8
PHOTON_COMMON_DIR=$(dirname "${PACKAGE_LIST_FILE}")
PACKAGE_LIST_FILE_BASE_NAME=$(basename "${PACKAGE_LIST_FILE}")
#- Step 3 Setting up the boot loader
WORKINGDIR=${BUILDROOT}
BUILDROOT=${BUILDROOT}/photon-chroot

cp -r BUILD_DVD/isolinux ${WORKINGDIR}/

if [ "$LIVE_CD" = true ] ; then
    mv ${WORKINGDIR}/isolinux/live-menu.cfg ${WORKINGDIR}/isolinux/menu.cfg
fi

cp sample_ks.cfg ${WORKINGDIR}/isolinux/

#ID in the initrd.gz now is PHOTON_VMWARE_CD . This is how we recognize that the cd is actually ours. touch this file there.
touch ${WORKINGDIR}/PHOTON_VMWARE_CD

#cp -r ${RPMS_PATH} ${WORKINGDIR}/
(
cd ${RPMS_PATH}
mkdir ${WORKINGDIR}/RPMS
for rpm_name in $RPM_LIST; do
    FILENAME="`find . -name "$rpm_name-[0-9]*" -or -name "$rpm_name-[a-z][0-9]*" -or -name "$rpm_name-debuginfo*" -type f`"
    if [ -n "$FILENAME" ]; then
        cp --parent $FILENAME ${WORKINGDIR}/RPMS/;
    fi
done
)

# Work in sub-shell using ( ... ) to come back to original folder.
(
cd $STAGE_PATH
for file_name in $ADDITIONAL_FILES_TO_COPY_FROM_STAGE; do
    if [ -n "$file_name" ]; then
        cp $file_name ${WORKINGDIR}/;
    fi
done
)

#creating rpm repo in cd..
createrepo --database ${WORKINGDIR}/RPMS

repodatadir=${WORKINGDIR}/RPMS/repodata
if [ -d $repodatadir ]; then
    pushd $repodatadir
    metaDataFile=`find -type f -name "*primary.xml.gz"`
    ln -sfv $metaDataFile primary.xml.gz
    popd
fi

find ${WORKINGDIR}/RPMS -name linux-[0-9]*.rpm | head -1 | xargs rpm2cpio | cpio -iv --to-stdout ./boot/vmlinuz* > ${WORKINGDIR}/isolinux/vmlinuz

mv ${WORKINGDIR}/initrd_ks.img ${WORKINGDIR}/isolinux/initrd.img
#Step 9 Generate the ISO!!!!
pushd $WORKINGDIR
mkisofs -R -l -L -D -b isolinux/isolinux.bin -c isolinux/boot.cat \
		-no-emul-boot -boot-load-size 4 -boot-info-table -V "PHOTON_$(date +%Y%m%d)" \
		$WORKINGDIR >$ISO_OUTPUT_NAME

popd
