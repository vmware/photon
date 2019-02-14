#! /bin/sh


DATE_TAG=`date "+%Y%m%d"`
DST=linux-firmware-$DATE_TAG
mkdir $DST

git clone https://github.com/RPi-Distro/firmware-nonfree.git --depth=1
git clone https://github.com/NXP/qoriq-engine-pfe-bin.git --depth=1
git clone git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git --depth=1

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
cp -a linux-firmware/rsi $DST/
cp linux-firmware/rsi_91x.fw $DST/

# NXP ls1012a FRWY requires:
mkdir $DST/ls1012a_ppe/
cp qoriq-engine-pfe-bin/ls1012a/slow_path/ppfe_class_ls1012a.elf $DST/ls1012a_ppe/
cp qoriq-engine-pfe-bin/ls1012a/slow_path/ppfe_tmu_ls1012a.elf $DST/ls1012a_ppe/
cp qoriq-engine-pfe-bin/NXP-Binary-EULA.txt $DST/ls1012a_ppe/

# Compulab Fitlet2 requires:
mkdir $DST/i915
cp linux-firmware/i915/bxt_dmc_ver1_07.bin $DST/i915/
cp linux-firmware/LICENSE.i915 $DST/

mkdir $DST/intel
cp linux-firmware/intel/ibt-11-5.* $DST/intel/
cp linux-firmware/LICENCE.ibt_firmware $DST/

cp linux-firmware/iwlwifi-8000C-*.ucode $DST/
cp linux-firmware/LICENCE.iwlwifi_firmware $DST/

tar -czvf $DST.tar.gz $DST
