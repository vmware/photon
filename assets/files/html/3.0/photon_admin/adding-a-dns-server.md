# Adding a DNS Server 

Photon OS uses `systemd-resolved` to resolve domain names, IP addresses, and network names for local applications. The `systemd-resolved` daemon automatically creates and maintains the `/etc/resolv.conf` file, into which systemd-resolved places the IP address of the DNS server. You must not modify the `/etc/resolv.conf` file.

**Note**: If you want to implement a local resolver like `bind` instead of `systemd-resolved`, stop the `systemd-resolved` service and disable it.

If you open the default `/etc/resolv.conf` file after you deploy Photon OS, it looks like this: 

	root@photon-rc [ ~ ]# cat /etc/resolv.conf
	# This file is managed by systemd-resolved(8). Do not edit.
	#
	# Third party programs must not access this file directly, but
	# only through the symlink at /etc/resolv.conf. To manage
	# resolv.conf(5) in a different way, replace the symlink by a
	# static file or a different symlink.

	nameserver 198.51.100.2

To add a DNS server, insert a DNS key into the Network section of the static network configuration file, for example,  `/etc/systemd/network/10-eth0-static.network` and set it to the IP address of your DNS server: 

	[Match]
	Name=e*

	[Network]
	Address=198.51.0.2/24
	Gateway=198.51.0.1
	DNS=198.51.0.1

If your machine is working with DHCP, you can add a DNS server by modifying the `/etc/systemd/resolved.conf--a` method.

For more information, see https://www.freedesktop.org/software/systemd/man/resolved.conf.html.

You can optionally activate the local DNS stub resolver of systemd-resolved by adding `dns` and `resolve` to the  `/etc/nsswitch.conf` file. To do so, make a backup copy of the `/etc/nsswitch.conf` file and then execute the following command as root:

	sed -i 's/^hosts.*$/hosts: files resolve dns/' /etc/nsswitch.conf

For more information about the `systemd-resolved` service, see https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html.