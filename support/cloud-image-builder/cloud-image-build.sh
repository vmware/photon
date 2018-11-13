#!/bin/bash

#################################################
#	Title:	cloud-image-build.sh		#
#        Date:	2015-07-22   	 		#
#     Version:	1.0				#
#      Author:	anishs@vmware.com		#
#################################################
#	Overview
#		Create cloud images
#	End
#
set -x
BUILD_SCRIPTS_PATH=$1
IMG_NAME=$2
SRC_ROOT=$3
GENERATED_DATA_PATH=$4
PHOTON_STAGE_PATH=$5
ADDITIONAL_RPMS_PATH=$6
WORKING_DIR=$PHOTON_STAGE_PATH/$IMG_NAME

PHOTON_IMG_OUTPUT_PATH=$PHOTON_STAGE_PATH/$IMG_NAME
VMDK_CONFIG_FILE=${BUILD_SCRIPTS_PATH}/$IMG_NAME/vmdk_$IMG_NAME.json
VMDK_CONFIG_SAFE_FILE=${BUILD_SCRIPTS_PATH}/$IMG_NAME/vmdk_safe_$IMG_NAME.json

cd $BUILD_SCRIPTS_PATH
image_list=`for i in $(ls -d */); do echo ${i%%/}; done`
if ! [[ $image_list =~ (^|[[:space:]])$IMG_NAME($|[[:space:]]) ]] ; then
    echo "Input image name not supported. Aborting."; exit 1;
fi
if [[ $IMG_NAME == ova* ]] ; then
    command -v ovftool >/dev/null 2>&1 || { echo "Ovftool not installed. Aborting." >&2; exit 1; }
fi

rm -rf $WORKING_DIR
mkdir -p $WORKING_DIR/installer
cp -R $SRC_ROOT/installer $WORKING_DIR/

cd $WORKING_DIR/installer
cp $VMDK_CONFIG_FILE $VMDK_CONFIG_SAFE_FILE
cp ${BUILD_SCRIPTS_PATH}/mk-setup-vmdk.sh .
cp ${BUILD_SCRIPTS_PATH}/mk-clean-vmdk.sh .

cp -r ${BUILD_SCRIPTS_PATH}/${IMG_NAME}/* .

PASSWORD=`date | md5sum | cut -f 1 -d ' '`
sed -i "s/PASSWORD/$PASSWORD/" $VMDK_CONFIG_SAFE_FILE

if [ -n "$ADDITIONAL_RPMS_PATH" ]
  then
    mkdir $PHOTON_STAGE_PATH/RPMS/additional
    cp -f $ADDITIONAL_RPMS_PATH/* $PHOTON_STAGE_PATH/RPMS/additional/
fi

./photonInstaller.py -p $GENERATED_DATA_PATH/build_install_options_$IMG_NAME.json -r $PHOTON_STAGE_PATH/RPMS -v $WORKING_DIR/photon-${IMG_NAME} -o $GENERATED_DATA_PATH -d $PHOTON_STAGE_PATH/pkg_info.json -f $VMDK_CONFIG_SAFE_FILE
status=$?
cat $VMDK_CONFIG_SAFE_FILE
rm $VMDK_CONFIG_SAFE_FILE

cd $BUILD_SCRIPTS_PATH
echo $BUILD_SCRIPTS_PATH
rpipath="rpi"
if [[ "$BUILD_SCRIPTS_PATH" =~ "\"rpi\"" ]]; then
    ROOTPART="2"
    echo "rpi"
else
    ROOTPART="3"
    echo "cloud"
fi

[ $status -eq 0 ] && ./customize_cloud_image.py \
 -r ${PHOTON_IMG_OUTPUT_PATH}/photon-${IMG_NAME}.raw \
 -c $VMDK_CONFIG_FILE \
 -w $WORKING_DIR \
 -m $PHOTON_IMG_OUTPUT_PATH/photon-${IMG_NAME} \
 -a $PHOTON_STAGE_PATH/RPMS/additional \
 -i $IMG_NAME \
 -t $SRC_ROOT/tools/bin/ \
 -b $BUILD_SCRIPTS_PATH \
 -s $SRC_ROOT \
 -p $ROOTPART
rm -rf $WORKING_DIR/installer

exit 0
