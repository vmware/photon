#!/bin/sh

cp runrpmbuild.sh stage/photonroot/$1
cd stage/photonroot
chroot $1 ./runrpmbuild.sh $2
