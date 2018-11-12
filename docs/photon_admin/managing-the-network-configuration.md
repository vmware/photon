# Managing the Network Configuration

The network service, which is enabled by default, starts when the system boots. You manage the network service by using systemd commands, such as systemd-networkd, systemd-resolvd, and networkctl. You can check its status of the network service by running the following command: 

	systemctl status systemd-networkd

Here is a healthy result of the command: 

	* systemd-networkd.service - Network Service
	   Loaded: loaded (/usr/lib/systemd/system/systemd-networkd.service; enabled; vendor preset: enabled)
	   Active: active (running) since Fri 2016-04-29 15:08:51 UTC; 6 days ago
	     Docs: man:systemd-networkd.service(8)
	 Main PID: 291 (systemd-network)
	   Status: "Processing requests..."
	   CGroup: /system.slice/systemd-networkd.service
	           `-291 /lib/systemd/systemd-networkd

Because Photon OS relies on systemd to manage services, you should employ the systemd suite of commands, not deprecated init.d commands or other deprecated commands, to manage networking. 