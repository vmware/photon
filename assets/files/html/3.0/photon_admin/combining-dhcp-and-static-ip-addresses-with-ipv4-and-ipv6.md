# Combining DHCP and Static IP Addresses with IPv4 and IPv6 

You can combine DHCP and static IP addresses with both IPv4 and IPv6. 

## Examples 

The following example shows how to use DHCP to allocate both IPv4 and IPv6 addresses:

	[Network]
	DHCP=yes

The following example shows how to use DHCP to allocate only IPv4 addresses:

	[Network]
	DHCP=ipv4

The following example shows how to use DHCP to allocate only IPv6 addresses:

	[Network]
	DHCP=ipv6

The following example shows how to use DHCP for IPv4 addresses and static IP addresses for IPv6 addresses: 

	[Network]
	DHCP=ipv4
	Address=fd00::1/48
	Gateway=fd00::252

The following example shows how to use DHCP for IPv6 addresses and static IP addresses for IPv4: 

	[Network]
	DHCP=ipv6
	Address=10.10.10.1/24
	Gateway=10.10.10.253

The following example shows how to use static IP addresses for both IPv4 and IPv6: 

	[Network]
	DHCP=ipv6
	Address=10.10.10.1/24
	Gateway=10.10.10.253
	Address=fd00::1/48
	Gateway=fd00::252