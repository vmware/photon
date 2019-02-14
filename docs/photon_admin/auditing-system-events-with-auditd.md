# Auditing System Events with auditd

To manage security on Photon OS, the Linux auditing service `auditd` is enabled and active by default on the full version of Photon OS.

The folloiwng command shows the security status:
	
```
systemctl status auditd
	* auditd.service - Security Auditing Service
	   Loaded: loaded (/usr/lib/systemd/system/auditd.service; enabled; vendor preset: enabled)
	   Active: active (running) since Fri 2016-04-29 15:08:50 UTC; 1 months 9 days ago
	 Main PID: 250 (auditd)
	   CGroup: /system.slice/auditd.service
	           `-250 /sbin/auditd -n
```

To help improve security, the `auditd` service can monitor file changes, system calls, executed commands, authentication events, and network access. After you implement an audit rule to monitor an event, the `aureport` tool generates reports to display information about the events. 

You can use the auditctl utility to set a rule that monitors the `sudoers` file for changes:

	auditctl -w /etc/sudoers -p wa -k sudoers_changes

This rule specifies that the auditd service must watch (`-w`) the `/etc/sudoers` file to log permissions changes (`-p`) to the write access (`w`) or attributes (`a`) of the file and to identify them in logs as `sudoers_changes`. The auditing logs appear in `/var/log/audit/audit.log`. You can list the auditing rules as follows: 

	auditctl -l
	-w /etc/sudoers -p wa -k sudoers_changes

For more information on the Linux Audit Daemon, see the `auditd` man page: 

	man auditd

For more information on setting auditing rules and options, see the `auditctl` man page:

	man auditctl

For more information on viewing reports on audited events, see the `aureport` man page:

	man aureport