# Configuring Network Interfaces

Network configuration files for systemd-networkd reside in /etc/systemd/network and /usr/lib/systemd/network. Example:

	root@photon-rc [ ~ ]# ls /etc/systemd/network/
	99-dhcp-en.network

By default, when Photon OS starts, it creates a DHCP network configuration file, or rule, which appears in /etc/systemd/network, the highest priority directory for network configuration files with the lowest priority filename:

	cat /etc/systemd/network/99-dhcp-en.network
	[Match]
	Name=e*

	[Network]
	DHCP=yes

Network configuration files can also appear in the system network directory, /usr/lib/systemd/network, as the results of the following search illustrate:

	root@photon-rc [ ~ ]# updatedb
	root@photon-rc [ ~ ]# locate systemd/network
	/etc/systemd/network
	/etc/systemd/network/99-dhcp-en.network
	/usr/lib/systemd/network
	/usr/lib/systemd/network/80-container-host0.network
	/usr/lib/systemd/network/80-container-ve.network
	/usr/lib/systemd/network/99-default.link
	root@photon-rc [ ~ ]#

As you can see, the /usr/lib/systemd/network directory contains several network configuration files. Photon OS applies the configuration files in the [lexicographical order](https://en.wikipedia.org/wiki/Lexicographical_order) specified by the file names without regard for the network configuration directory in which the file resides unless the file name is the same. Photon OS processes files with identical names by giving precedence to files in the /etc directory over the other directory. Thus, the settings in /etc/systemd/network override those in /usr/lib/systemd/network. Once Photon OS matches an interface in a file, Photon OS ignores the interface if it appears in files processed later in the lexicographical order. 

Each .network file contains a matching rule and a configuration that Photon OS applies when a device matches the rule. You set the matching rule and the configuration as sections containing vertical sets of key-value pairs according to the information at https://www.freedesktop.org/software/systemd/man/systemd.network.html. 

To configure Photon OS to handle a networking use case, such as setting a static IP address or adding a name server, you create a configuration file with a `.network` extension and place it in the /etc/systemd/network directory.

After you create a network configuration file with a `.network` extension, you must run the `chmod` command to set the new file's mode bits to `644`. Example: 

    chmod 644 10-static-en.network

For Photon OS to apply the new configuration, you must restart the `systemd-networkd` service by running the following command: 

	systemctl restart systemd-networkd

For information about network configuration files, their processing order, and their matching rules, sections, and keys, see https://www.freedesktop.org/software/systemd/man/systemd.network.html.

For information about creating virtual network device files (`.netdev`), see https://www.freedesktop.org/software/systemd/man/systemd.netdev.html.