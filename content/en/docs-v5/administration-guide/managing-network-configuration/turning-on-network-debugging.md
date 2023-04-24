---
title:  Turning On Network Debugging
weight: 12
---

You can set `systemd-networkd` to work in debug mode so that you can analyze log files with debugging information to help troubleshoot networking problems. 

You can turn on network debugging by adding a drop-in file in `/etc/systemd` to customize the default systemd configuration in `/usr/lib/systemd`. 

**Procedure**

1. Run the following command as root to create a directory with the name `systemd-networkd.service.d`, including the `.d` extension:
	
	```console
	mkdir -p /etc/systemd/system/systemd-networkd.service.d/
	```

1. Run the following command as root to establish a `systemd` drop-in unit with a debugging configuration for the network service:

	```console
	cat > /etc/systemd/system/systemd-networkd.service.d/override.conf
		[Service]
		Environment=SYSTEMD_LOG_LEVEL=debug
		EOF
	```

1. Reload the `systemctl` daemon and restart the `systemd-networkd` service for the changes to take effect: 
	
	```console
	systemctl daemon-reload
	systemctl restart systemd-networkd
	```

1. Verify your changes:

	```console
	systemd-delta --type=extended
	```

1. View the log files by running this command: 
	
	```console
	journalctl -u systemd-networkd
	```

1. After debugging the network connections, turn debugging off by deleting the drop-in file: 
	
	```console
	rm /etc/systemd/system/systemd-networkd.service.d/10-loglevel-debug.conf
	```
