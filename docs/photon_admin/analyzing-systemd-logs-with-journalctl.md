# Analyzing systemd Logs with journalctl

The `journalctl` tool queries the contents of the `systemd` journal. 

The following command displays the messages that `systemd` generated the last time the machine started: 

	journalctl -b

The following command reveals the messages for the systemd service unit specified by the `-u` option:

	journalctl -u auditd
	
In the above example, `auditd` is the system service unit.

For more information, see the `journalctl` man page by running the following command on Photon OS: 

```
man journalctl
```
