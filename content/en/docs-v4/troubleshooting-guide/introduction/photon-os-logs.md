---
title:  Photon OS Logs
weight: 5
---

On Photon OS, all the system logs except the installation logs and the cloud-init logs are written into the systemd journal. The `journalctl` command queries the contents of the systemd journal.

The installation log files and the cloud-init log files reside in `/var/log`. If Photon OS is running on a virtual machine in a VMware hypervisor, the log file for the VMware tools, `vmware-vmsvc.log`, also resides in `/var/log`. 

##Journalctl
Journalctl is a utility to query and display logs from journald and systemd’s logging service. Since journald stores log data in a binary format instead of a plain text format, `journalctl` is the standard way of reading log messages processed by journald.

Journald is a service provided by systemd. To see the staus of the daemon, run the following commands:
```
# systemctl status systemd-journald
● systemd-journald.service - Journal Service
Loaded: loaded (/lib/systemd/system/systemd-journald.service; static; vendor preset: enabled)
Active: active (running) since Tue 2020-04-07 14:33:41 CST; 2 days ago
Docs: man:systemd-journald.service(8)
man:journald.conf(5)
Main PID: 943 (systemd-journal)
Status: "Processing requests..."
Tasks: 1 (limit: 4915)
Memory: 18.0M
CGroup: /system.slice/systemd-journald.service
└─943 /lib/systemd/systemd-journald



Apr 07 14:33:41 photon-4a0e7f2307d4 systemd-journald[943]: Journal started
Apr 07 14:33:41 photon-4a0e7f2307d4 systemd-journald[943]: Runtime journal (/run/log/journal/b8cebc61a6cb446a968ee1d4c5bbbbd5) is 8.0M, max 1.5G, 1.5G free.
Apr 07 14:33:41 photon-4a0e7f2307d4 systemd-journald[943]: Time spent on flushing to /var is 88.263ms for 1455 entries.
Apr 07 14:33:41 photon-4a0e7f2307d4 systemd-journald[943]: System journal (/var/log/journal/b8cebc61a6cb446a968ee1d4c5bbbbd5) is 40.0M, max 4.0G, 3.9G free.
root@photon-4a0e7f2307d4 [ ~ ]#
```

The following command are related to `journalctl`:

- `journalctl` : This command displays all the logs after the system has booted up. `journalctl` splits the results into pages, similar to the `less` command in Linux. You can navigate using the arrow keys, the Page Up, Page Down keys or the Space bar. To quit navigation, press the **q** key.
- `journalctl -b` : This command displays the logs for the current boot.

The following commands pull logs based on a time range:

- `journalctl --since "1 hour ago"` : This command displays the journal logs from the past 1 hour.
- `journalctl --since "2 days ago"` : This command displays the logs generated in the past 2 days.
- `journalctl --since "2020-03-25 00:00:00" --until "2020-04-09 00:00:00"` : This command displays the logs generated between the mentioned time frame.

To traverse for logs in the reverse order, run the following command:

- `journalctl -r` : This command displays the logs in reverse order.

**Note**: If you add `-r` at the end of a command, the logs are displayed in the reverse order. For example: `journalctl -u unit.service -r`

To pull logs related to a particular daemon, run the following command:

- `journalctl -u unit.service` : This command displays logs for a specific service. mention the name of the service instead of `unit`. This command helps when a service is not behaving properly or when there are crash/core dumps. 

To see Journal logs by their priority, run the following command:

- `journalctl -p "emerg".."crit` : This command displays logs **emerg** to **critical**. For example: core dumps.

Journalctl can print log messages to the console as they are added, like the Linux `tail` command. Add the `-f` switch to follow a specific service or daemon.
```
journalctl -u unit.service -f
```

To list the boots of the system, run the following command:
```
journalctl --list-boots
```

You can maintain the journalctl logs manually, by running the following `vacuum` commands:

- `journalctl --vacuum-time=2d` : This command retains the logs from the last 2 days.
- `journalctl --vacuum-size=500M` : This command helps retain logs with a maximum size of 500 MB.

You can configure Journald using the conf file located at **/etc/systemd/journald.conf**. Run the following command to configure the file:

```console
# cat /etc/systemd/journald.conf
```
```ini
# This file is part of systemd.
#
# systemd is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# Defaults can be restored by simply deleting this file.
#
# See journald.conf(5) for details.

[Journal]
#Storage=auto
#Compress=yes
#Seal=yes
#SplitMode=uid
#SyncIntervalSec=5m
#RateLimitIntervalSec=30s
#RateLimitBurst=10000
#SystemMaxUse=
#SystemKeepFree=
#SystemMaxFileSize=
#SystemMaxFiles=100
#RuntimeMaxUse=
#RuntimeKeepFree=
#RuntimeMaxFileSize=
#RuntimeMaxFiles=100
#MaxRetentionSec=
#MaxFileSec=1month
#ForwardToSyslog=no
#ForwardToKMsg=no
#ForwardToConsole=no
#ForwardToWall=yes
#TTYPath=/dev/console
#MaxLevelStore=debug
#MaxLevelSyslog=debug
#MaxLevelKMsg=notice
#MaxLevelConsole=info
#MaxLevelWall=emerg
#LineMax=48K
root@photon-4a0e7f2307d4 [ ~ ]#
```

By default `rotate` is disabled in Photon. Once the changes are made to the conf file, for the changes to take effect you must restart the systemd-journald by running the `systemctl restart systemd-journald` command.

## Cloud-init Logs
Cloud-init is the industry standard multi-distribution method for cross-platform cloud instance initialisation. 

If there are with the Cloud-init behaviour, we can debug them by looking at the logs. Run the following command to look at Cloud-init logs:

```console
journalctl -u cloud-init
```

For better understanding/debugging, You can also look at logs from the following locations:

- **/var/log/cloud-init.log** : This log contains information from each stage of Cloud-init.
- **/var/log/cloud-init-output.log** : This log contains errors, warnings, etc..


## Syslog
Syslog is the general standard for logging system and program messages in the Linux environment.

Photon provides the following two packages to support syslog:

- **syslog-ng** : syslog-ng is syslog with some advanced next gen features. It supports TLS encryption, TCP for transport with other existing features. Configurations can be added to the `/etc/syslog-ng/syslog-ng.conf` file.
- **rsyslog** : The official RSYSLOG website defines the utility as "the rocket-fast system for log processing". rsyslog supports some advanced features like relp, imfile, omfile, gnutls protocols. Configurations can be added to the `/etc/rsyslog.conf` file. You can configure the required TLS certificates by editing the conf file.

## Logs for RPMS on Photon
Logs for a particular RPM can be checked in the following ways:

- If the RPM provides a daemon, we can see the status of daemon by running `systemctl` command and check logs using `journactl -u <service name>` command.
- For additional logs, check if a conf file is provided by the RPM by running the `rpm -ql <rpm name> | grep conf` command and find the file path of the log file. You can also check the **/var/log** folder.
