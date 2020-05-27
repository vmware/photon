# Inspecting IP Addresses

VMware recommends that you use the `ip` or `ss` commands as the `ifconfig` and `netstat` commands are deprecated. 

To display a list of network interfaces, run the `ss` command. Similarly, to display information for IP addresses, run the `ip addr` command. 

Examples:

	USE THIS IPROUTE COMMAND 	INSTEAD OF THIS NET-TOOL COMMAND
	ip addr 					ifconfig -a
	ss 							netstat
	ip route 					route
	ip maddr 					netstat -g
	ip link set eth0 up 		ifconfig eth0 up
	ip -s neigh					arp -v
	ip link set eth0 mtu 9000	ifconfig eth0 mtu 9000

Use the `ip route` version of a command instead of the net-tools to get accurate information: 

	ip neigh
	198.51.100.2 dev eth0 lladdr 00:50:56:e2:02:0f STALE
	198.51.100.254 dev eth0 lladdr 00:50:56:e7:13:d9 STALE
	198.51.100.1 dev eth0 lladdr 00:50:56:c0:00:08 DELAY

	arp -a
	? (198.51.100.2) at 00:50:56:e2:02:0f [ether] on eth0
	? (198.51.100.254) at 00:50:56:e7:13:d9 [ether] on eth0
	? (198.51.100.1) at 00:50:56:c0:00:08 [ether] on eth0

**Important:** If you modify an IPv6 configuration or add an IPv6 interface, you must restart `systemd-networkd`. Traditional methods of using `ifconfig` commands will be inadequate to register the changes. Run the following command instead: 

	systemctl restart systemd-networkd
