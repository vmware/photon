#!/bin/bash

echo -e "changeme\nchangeme" | passwd root
chage -d 0 -M 999 root

#mouting should start here to modify /etc/fstab

