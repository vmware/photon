#!/bin/bash

echo -e "changeme\nchangeme" | passwd root

# create empty cracklib dictionary and remove cracklib-dicts rpm
echo a | cracklib-packer /root/pw_dict
rpm -e cracklib-dicts --nodeps
mv /root/pw_dict* /usr/share/cracklib/

# removing this file is safe
rm /boot/system.map*

# TODO: remove it from grub rpm - not used
rm -rf /boot/grub/fonts
# TODO: clean up spec file
rm -rf /usr/include
