#! /bin/sh

set -e

DATE_TAG=`date "+%Y%m%d"`
DST=linux-firmware-$DATE_TAG
mkdir $DST

git clone https://github.com/RPi-Distro/firmware-nonfree.git --branch buster --depth=1
git clone git://git.kernel.org/pub/scm/linux/kernel/git/sforshee/wireless-regdb.git --depth=1
git clone git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git --depth=1
# ICE driver firmware
# Version should be same as provided in linux spec
ice_version=$(curl --compressed "https://github.com/vmware/photon/blob/$(git branch | grep '^\*' | cut -d' ' -f2)/SPECS/linux/linux.spec" 2> /dev/null | grep -m 1 'ice_version' | cut -d'<' -f4 | cut -d' ' -f3)
wget https://sourceforge.net/projects/e1000/files/ice%20stable/$ice_version/ice-$ice_version.tar.gz
tar -xpf ice-$ice_version.tar.gz

cp linux-firmware/WHENCE $DST/

mkdir $DST/brcm
# rpi3 b requires:
cp firmware-nonfree/brcm/brcmfmac43430-sdio.bin $DST/brcm/
cp firmware-nonfree/brcm/brcmfmac43430-sdio.txt $DST/brcm/

# rpi3 b+ requires:
cp firmware-nonfree/brcm/brcmfmac43455-sdio.clm_blob $DST/brcm/
cp firmware-nonfree/brcm/brcmfmac43455-sdio.bin $DST/brcm/
cp firmware-nonfree/brcm/brcmfmac43455-sdio.txt $DST/brcm/

# rpi3 licence
cp firmware-nonfree/LICENCE.broadcom_bcm43xx $DST/

# Dell Edge Gateway requires:
mkdir $DST/rtl_nic/
mkdir $DST/mrvl/
cp -a linux-firmware/rsi $DST/
cp linux-firmware/rsi_91x.fw $DST/
cp linux-firmware/rtl_nic/rtl8168f-2.fw $DST/rtl_nic/
wget -P $DST/mrvl/ https://downloads.dell.com/FOLDER04270570M/1/pcie8897_uapsta.bin
cp linux-firmware/LICENCE.Marvell $DST/

# Compulab Fitlet2 requires:
mkdir $DST/i915
cp linux-firmware/i915/bxt_dmc_ver1_07.bin $DST/i915/
cp linux-firmware/LICENSE.i915 $DST/

mkdir $DST/intel
cp linux-firmware/intel/ibt-11-5.* $DST/intel/
cp linux-firmware/LICENCE.ibt_firmware $DST/
# ICE driver firmware and license
mkdir -p $DST/updates/intel/ice/ddp
cp ice-$ice_version/ddp/ice-*.pkg $DST/updates/intel/ice/ddp/
cp ice-$ice_version/ddp/LICENSE $DST/updates/intel/ice/ddp/
chmod 0644 $DST/updates/intel/ice/ddp/ice-*.pkg
chmod 0644 $DST/updates/intel/ice/ddp/LICENSE
ice_pkg=$(find ice-$ice_version -name ice*.pkg | cut -d'/' -f3)
ln -s $ice_pkg $DST/updates/intel/ice/ddp/ice.pkg

cp linux-firmware/iwlwifi-8000C-*.ucode $DST/
cp linux-firmware/LICENCE.iwlwifi_firmware $DST/

mkdir $DST/bnx2x
cp linux-firmware/bnx2x/bnx2x-e2-7.13.1.0.fw $DST/bnx2x/
cp linux-firmware/ql2500_fw.bin $DST/
cp linux-firmware/LICENCE.qla2xxx $DST/

# rpi4 b requires:
cp linux-firmware/brcm/brcmfmac43455-sdio.raspberrypi,4-model-b.txt $DST/brcm/
cp wireless-regdb/regulatory.db $DST/
cp wireless-regdb/regulatory.db.p7s $DST/
cp wireless-regdb/LICENSE $DST/LICENSE.wireless-regdb

# AMD GPU firmware:
mkdir $DST/amdgpu
cp -a linux-firmware/amdgpu/vega10* $DST/amdgpu

tar -czvf $DST.tar.gz $DST
