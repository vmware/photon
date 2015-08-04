#!/bin/sh
# Script to upload files to bintray. All files in source-path are uploaded to location 
# configured in following parameters.

ACCOUNT=vmware
REPO=photon
PACKAGE=rpm-ostree
VERSION=dev

if [ $# -lt 3 ]
then
    echo "Usage : " $0 " <Source Path>  <Username> <APIKEY>"
    exit 1
fi

SRC_DIR=$1
USER=$2
APIKEY=$3

(cd $SRC_DIR

for FILE in `find . -type f`; do

  echo "Uploading " $FILE
  curl -vvf -T $FILE -u$USER:$APIKEY -H "X-Bintray-Package:$PACKAGE" -H "X-Bintray-Version:$VERSION" https://api.bintray.com/content/$ACCOUNT/$REPO/$PACKAGE/$VERSION/$FILE

done)
