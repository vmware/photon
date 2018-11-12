# Combining DHCP and Static IP Addresses with IPv4 and IPv6 

This section presents examples that demonstrate how to combine DHCP and static IP addresses with both IPv4 and IPv6. 

Here's how to use DHCP to allocate both IPv4 and IPv6 addresses:

	[Network]
	DHCP=yes

Here's how to use DHCP to allocate only IPv4 addresses:

	[Network]
	DHCP=ipv4

Here's how to use DHCP to allocate only IPv6 addresses:

	[Network]
	DHCP=ipv6

Here's how to use DHCP for IPv4 addresses and static IP addresses for IPv6 addresses: 

	[Network]
	DHCP=ipv4
	Address=fd00::1/48
	Gateway=fd00::252

Here's how to use DHCP for IPv6 addresses and static IP addresses for IPv4: 

	[Network]
	DHCP=ipv6
	Address=10.10.10.1/24
	Gateway=10.10.10.253

Here's how to use static IP addresses for both IPv4 and IPv6: 

	[Network]
	DHCP=ipv6
	Address=10.10.10.1/24
	Gateway=10.10.10.253
	Address=fd00::1/48
	Gateway=fd00::252