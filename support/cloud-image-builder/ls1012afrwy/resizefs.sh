#! /bin/bash

#parted /dev/mmcblk0 resizepart 3 90%
#parted /dev/mmcblk0 mkpart primary linux-swap 90% 100%
#partprobe
#resize2fs /dev/mmcblk0p3
