#! /bin/sh


DATE_TAG=`date "+%Y%m%d"`
DST=linux-firmware-$DATE_TAG
mkdir $DST

git clone git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git --depth=1

cp linux-firmware/WHENCE $DST/

mkdir $DST/brcm
cp linux-firmware/brcm/brcmfmac43430-sdio.bin $DST/brcm/
cp linux-firmware/LICENCE.broadcom_bcm43xx $DST/

cp -a linux-firmware/rsi $DST/
cp linux-firmware/rsi_91x.fw $DST/

tar -czvf $DST.tar.gz $DST
