# Analyzing System Logs with `journalctl`

The journalctl tool queries the contents of the systemd journal. On Photon OS, all the system logs except the installation log and the cloud-init log are written into the systemd journal. 

When you run the `journalctl` command without any parameters, it displays all the contents of the journal, beginning with the oldest entry. 

To display the output in reverse order with new entries first, include the `-r` option in the command:

	journalctl -r

The `journalctl` command includes many options to filter its output. For help troubleshooting systemd, two journalctl queries are particularly useful: 

- Showing the log entries for the last boot. 
    
    The following command displays the messages that systemd generated during the last time the machine started: 

	journalctl -b

- Showing the log entries for a systemd service unit.Item
    
    The following command reveals the messages for only the systemd service unit specified by the `-u` option, which in the following example is the auditing service: 

	journalctl -u auditd

You can look at the messages for systemd itself or for the network service:

	journalctl -u systemd
	journalctl -u systemd-networkd

Example:  

	root@photon-1a0375a0392e [ ~ ]# journalctl -u systemd-networkd
	-- Logs begin at Tue 2016-08-23 14:35:50 UTC, end at Tue 2016-08-23 23:45:44 UTC. --
	Aug 23 14:35:52 photon-1a0375a0392e systemd[1]: Starting Network Service...
	Aug 23 14:35:52 photon-1a0375a0392e systemd-networkd[458]: Enumeration completed
	Aug 23 14:35:52 photon-1a0375a0392e systemd[1]: Started Network Service.
	Aug 23 14:35:52 photon-1a0375a0392e systemd-networkd[458]: eth0: Gained carrier
	Aug 23 14:35:53 photon-1a0375a0392e systemd-networkd[458]: eth0: DHCPv4 address 198.51.100.1
	Aug 23 14:35:54 photon-1a0375a0392e systemd-networkd[458]: eth0: Gained IPv6LL
	Aug 23 14:35:54 photon-1a0375a0392e systemd-networkd[458]: eth0: Configured


For more information, see [journalctl](https://www.freedesktop.org/software/systemd/man/journalctl.html) or the journalctl man page by running this command: `man journalctl`