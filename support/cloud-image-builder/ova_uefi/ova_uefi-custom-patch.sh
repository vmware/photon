#!/bin/bash
echo -e "changeme\nchangeme" | passwd root
chage -d 0 root
