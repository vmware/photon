#!/bin/bash

#################################################
#	Title:	image-builder.sh		            #
#   Date:	2015-07-22        	 		        #
#   Version:	1.1				                #
#   Author:	anishs@vmware.com    		        #
#################################################
#	Overview
#		Create images like ami, azure, gce, ova, rpi3
#	End
#

for i in "$@"
do
    case $i in
        -b=*|--build-scripts-path=*)
        BUILD_SCRIPTS_PATH="${i#*=}"
        shift
        ;;
        -i=*|--img-name=*)
        IMG_NAME="${i#*=}"
        shift
        ;;
        -s=*|--src-root=*)
        SRC_ROOT="${i#*=}"
        shift
        ;;
        -g=*|--generated-data-path=*)
        GENERATED_DATA_PATH="${i#*=}"
        shift
        ;;
        -s=*|--stage-path=*)
        PHOTON_STAGE_PATH="${i#*=}"
        shift
        ;;
        -r=*|--additional-rpms-path=*)
        ADDITIONAL_RPMS_PATH="${i#*=}"
        shift
        ;;
        *)
        ;;
    esac
done

WORKING_DIR=$PHOTON_STAGE_PATH/$IMG_NAME

PHOTON_IMG_OUTPUT_PATH=$PHOTON_STAGE_PATH/$IMG_NAME
IMAGE_CONFIG_FILE=${BUILD_SCRIPTS_PATH}/$IMG_NAME/config_$IMG_NAME.json
IMAGE_CONFIG_SAFE_FILE=${BUILD_SCRIPTS_PATH}/$IMG_NAME/config_safe_$IMG_NAME.json

cd $BUILD_SCRIPTS_PATH
image_list=`for i in $(ls -d */); do echo ${i%%/}; done`
if ! [[ $image_list =~ (^|[[:space:]])$IMG_NAME($|[[:space:]]) ]] ; then
    echo "Input image name not supported. Aborting."; exit 1;
fi
if [[ $IMG_NAME == ova* ]] ; then
    command -v ovftool >/dev/null 2>&1 || { echo "Ovftool not installed. Aborting." >&2; exit 1; }
fi

rm -rf $WORKING_DIR
mkdir -p $WORKING_DIR
INSTALLER_PATH=$SRC_ROOT/installer

cd $WORKING_DIR
cp $IMAGE_CONFIG_FILE $IMAGE_CONFIG_SAFE_FILE

DISK_SETUP="--disk-setup-script ${BUILD_SCRIPTS_PATH}/mk-setup-vmdk.sh"
if [ -f ${BUILD_SCRIPTS_PATH}/$IMG_NAME/mk-setup-vmdk.sh ]; then
    DISK_SETUP="--disk-setup-script ${BUILD_SCRIPTS_PATH}/$IMG_NAME/mk-setup-vmdk.sh"
fi

DISK_CLEANUP="--disk-cleanup-script ${BUILD_SCRIPTS_PATH}/mk-clean-vmdk.sh"
if [ -f ${BUILD_SCRIPTS_PATH}/$IMG_NAME/mk-clean-vmdk.sh ]; then
    DISK_CLEANUP="--disk-cleanup-script ${BUILD_SCRIPTS_PATH}/$IMG_NAME/mk-clean-vmdk.sh"
fi

PREPARE_SYSTEM="--prepare-script ${INSTALLER_PATH}/mk-prepare-system.sh"
if [ -f ${BUILD_SCRIPTS_PATH}/$IMG_NAME/mk-prepare-system.sh ]; then
    PREPARE_SYSTEM="--prepare-script ${BUILD_SCRIPTS_PATH}/$IMG_NAME/mk-prepare-system.sh"
fi

GRUB_SCRIPT="--setup-grub-script ${INSTALLER_PATH}/mk-setup-grub.sh"
if [ -f ${BUILD_SCRIPTS_PATH}/$IMG_NAME/mk-setup-grub.sh ]; then
    GRUB_SCRIPT="--setup-grub-script ${BUILD_SCRIPTS_PATH}/$IMG_NAME/mk-setup-grub.sh"
fi

PASSWORD=`date | md5sum | cut -f 1 -d ' '`
sed -i "s/PASSWORD/$PASSWORD/" $IMAGE_CONFIG_SAFE_FILE

if [ -n "$ADDITIONAL_RPMS_PATH" ]
  then
    mkdir -p $PHOTON_STAGE_PATH/RPMS/additional
    cp -f $ADDITIONAL_RPMS_PATH/* $PHOTON_STAGE_PATH/RPMS/additional/
fi

${INSTALLER_PATH}/photonInstaller.py -r $PHOTON_STAGE_PATH/RPMS -v $WORKING_DIR/photon-${IMG_NAME} $GRUB_SCRIPT $PREPARE_SYSTEM $DISK_CLEANUP $DISK_SETUP -o $GENERATED_DATA_PATH -d $PHOTON_STAGE_PATH/pkg_info.json -f $IMAGE_CONFIG_SAFE_FILE
status=$?
rm $IMAGE_CONFIG_SAFE_FILE

cd $BUILD_SCRIPTS_PATH

[ $status -eq 0 ] && ./customize_image.py \
 -r ${PHOTON_IMG_OUTPUT_PATH}/photon-${IMG_NAME}.raw \
 -c $IMAGE_CONFIG_FILE \
 -w $WORKING_DIR \
 -m $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME} \
 -a $PHOTON_STAGE_PATH/RPMS/additional \
 -i $IMG_NAME \
 -t $SRC_ROOT/tools/bin/ \
 -b $BUILD_SCRIPTS_PATH \
 -s $SRC_ROOT

exit 0
