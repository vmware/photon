#!/bin/bash
# Change the max password days to 99999
cat /etc/shadow | cut -d: -f1 | xargs -I {} chage -I -1 -m 0 -M 99999 -E -1 -W 7 {}
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   99999/' /etc/login.defs
