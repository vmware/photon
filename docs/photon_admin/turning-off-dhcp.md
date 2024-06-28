# Turning Off DHCP

By default, when Photon OS first starts, it creates a DHCP network configuration file or rule, which appears in `/etc/systemd/network`, the highest priority directory for network configuration files with the lowest priority filename:

	cat /etc/systemd/network/99-dhcp-en.network
	[Match]
	Name=e*

	[Network]
	DHCP=yes

To turn off DHCP for all Ethernet interfaces, change the value of `DHCP` from `yes` to `no`, save the changes, and then restart the `systemd-networkd` service: 

	systemctl restart systemd-networkd

If you create a configuration file with a higher priority filename (e.g. `10-static-en.network`), it is not necessary but still recommended to turn off DHCP.
