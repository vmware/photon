# Commands to Manage Network Service

You manage the network service by using systemd commands, such as `systemd-networkd`, `systemd-resolvd`, and `networkctl`. 

To check the status of the network service, run the following command: 

	systemctl status systemd-networkd

**Output**

	* systemd-networkd.service - Network Service
	   Loaded: loaded (/usr/lib/systemd/system/systemd-networkd.service; enabled; vendor preset: enabled)
	   Active: active (running) since Fri 2016-04-29 15:08:51 UTC; 6 days ago
	     Docs: man:systemd-networkd.service(8)
	 Main PID: 291 (systemd-network)
	   Status: "Processing requests..."
	   CGroup: /system.slice/systemd-networkd.service
	           `-291 /lib/systemd/systemd-networkd

Because Photon OS relies on systemd to manage services, you must use the `systemd` suite of commands and not the deprecated `init.d` commands or other deprecated commands to manage networking. 