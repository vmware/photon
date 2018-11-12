# Use `ip` and `ss` Commands

Although the `ifconfig` command and the `netstat` command work on Photon OS, VMware recommends that you use the `ip` or `ss` commands. The `ipconfig` and `netstat` commands are deprecated. 

For example, instead of running `netstat` to display a list of network interfaces, run the `ss` command. Similarly, to display information for IP addresses, instead of running `ifconfig -a`, run the `ip addr` command. Examples:

	USE THIS IPROUTE COMMAND 	INSTEAD OF THIS NET-TOOL COMMAND
	ip addr 					ifconfig -a
	ss 							netstat
	ip route 					route
	ip maddr 					netstat -g
	ip link set eth0 up 		ifconfig eth0 up
	ip -s neigh					arp -v
	ip link set eth0 mtu 9000	ifconfig eth0 mtu 9000

Using the `ip route` version of a command instead of the net-tools version often provides more complete, accurate information on Photon OS, as the following example demonstrates: 

	ip neigh
	198.51.100.2 dev eth0 lladdr 00:50:56:e2:02:0f STALE
	198.51.100.254 dev eth0 lladdr 00:50:56:e7:13:d9 STALE
	198.51.100.1 dev eth0 lladdr 00:50:56:c0:00:08 DELAY

	arp -a
	? (198.51.100.2) at 00:50:56:e2:02:0f [ether] on eth0
	? (198.51.100.254) at 00:50:56:e7:13:d9 [ether] on eth0
	? (198.51.100.1) at 00:50:56:c0:00:08 [ether] on eth0
