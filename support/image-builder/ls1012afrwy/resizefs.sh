#! /bin/bash

parted /dev/mmcblk0 resizepart 2 90%
parted /dev/mmcblk0 mkpart primary linux-swap 90% 100%
partprobe
resize2fs /dev/mmcblk0p2
mkswap /dev/mmcblk0p3
