#! /bin/sh

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <ice_version>" >&2
  echo "Look up the current ice version for the target kernel in" >&2
  echo "common/data/kernel-deps.json (linux_dep_package.kernels-drivers-intel-ice)," >&2
  echo "e.g.: $0 2.3.10" >&2
  exit 1
fi
ice_version=$1

DATE_TAG=`date "+%Y%m%d"`
DST=linux-firmware-$DATE_TAG
mkdir $DST

git clone https://github.com/RPi-Distro/firmware-nonfree.git --branch buster --depth=1
git clone https://git.kernel.org/pub/scm/linux/kernel/git/sforshee/wireless-regdb.git --depth=1
git clone https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git --depth=1
# ICE driver firmware (DDP package)
# As of ice 2.x, this moved from sourceforge.net/projects/e1000 to GitHub.
wget -O ice-$ice_version.tar.gz https://github.com/intel/ethernet-linux-ice/archive/refs/tags/v$ice_version.tar.gz
tar -xpf ice-$ice_version.tar.gz
mv ethernet-linux-ice-$ice_version ice-$ice_version

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
cp linux-firmware/LICENSES/LICENCE.Marvell $DST/

# Compulab Fitlet2 requires:
mkdir $DST/i915
cp linux-firmware/i915/bxt_dmc_ver1_07.bin $DST/i915/
cp linux-firmware/LICENSES/LICENSE.i915 $DST/

mkdir $DST/intel
cp linux-firmware/intel/ibt-11-5.* $DST/intel/
cp linux-firmware/LICENSES/LICENCE.ibt_firmware $DST/
# ICE driver firmware and license
mkdir -p $DST/updates/intel/ice/ddp
cp ice-$ice_version/ddp/ice*.pkg $DST/updates/intel/ice/ddp/
cp ice-$ice_version/ddp/LICENSE $DST/updates/intel/ice/ddp/
chmod 0644 $DST/updates/intel/ice/ddp/ice*.pkg
chmod 0644 $DST/updates/intel/ice/ddp/LICENSE
ice_pkg=$(find ice-$ice_version -name ice*.pkg | cut -d'/' -f3)
ln -s $ice_pkg $DST/updates/intel/ice/ddp/ice.pkg

cp linux-firmware/intel/iwlwifi/iwlwifi-8000C-*.ucode $DST/
cp linux-firmware/LICENSES/LICENCE.iwlwifi_firmware $DST/

mkdir $DST/bnx2x
cp linux-firmware/bnx2x/bnx2x-e2-7.13.1.0.fw $DST/bnx2x/
cp linux-firmware/ql2500_fw.bin $DST/
cp linux-firmware/LICENSES/LICENCE.qla2xxx $DST/

# rpi4 b requires:
cp linux-firmware/brcm/brcmfmac43455-sdio.raspberrypi,4-model-b.txt $DST/brcm/
cp wireless-regdb/regulatory.db $DST/
cp wireless-regdb/regulatory.db.p7s $DST/
cp wireless-regdb/LICENSE $DST/LICENSE.wireless-regdb

# AMD GPU firmware:
mkdir $DST/amdgpu
cp -a linux-firmware/amdgpu/vega10* $DST/amdgpu
# gc_12_0_1/psp_14_0_3/sdma_7_0_1/smu_14_0_3/vcn_5_0_0 required for amdgpu
# to bring up recent AMD GPUs (e.g. Strix-class silicon)
cp -a linux-firmware/amdgpu/gc_12_0_1* $DST/amdgpu
cp -a linux-firmware/amdgpu/psp_14_0_3* $DST/amdgpu
cp -a linux-firmware/amdgpu/sdma_7_0_1* $DST/amdgpu
cp -a linux-firmware/amdgpu/smu_14_0_3* $DST/amdgpu
cp -a linux-firmware/amdgpu/vcn_5_0_0* $DST/amdgpu
cp linux-firmware/LICENSES/LICENSE.amdgpu $DST/

tar -czvf $DST.tar.gz $DST
