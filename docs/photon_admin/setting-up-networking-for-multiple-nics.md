# Setting Up Networking for Multiple NICs

If your machine contains multiple NICs, it is recommend that you create a `.network` configuration file for each network interface. The following scenario demonstrates how to set one wired network interface to use a static IP address and another wired network interface to use a dynamic IP address obtained through DHCP. 

**Note**: The following configurations are examples and you must change the IP addresses and other information to match your network and requirements.  

First, create the `.network` file for the static Ethernet connection in `/etc/systemd/network`. A best practice is to match the exact name of the network interface, which is `eth0` in this example. This example file also includes a DNS server for the static IP address. As a result, the configuration sets the UseDNS key to false in the DHCP column so that Photon OS ignores the DHCP server for DNS for this interface.  

	cat > /etc/systemd/network/10-eth0-static-en.network << "EOF"
	[Match]
	Name=eth0

	[Network]
	Address=10.137.20.11/19
	Gateway=10.137.23.253
	DNS=10.132.71.1

	[DHCP]
	UseDNS=false
	EOF

Second, create the `.network` file for the second network interface, which is `eth1` in this example. This configuration file sets the eth1 interface to an IP address from DHCP and sets DHCP as the source for DNS lookups. Setting the DHCP key to `yes` acquires an IP address for IPv4 and IPv6. To acquire an IP address for IPv4 only, set the DHCP key to `ipv4`.

	cat > /etc/systemd/network/50-eth1-dhcp-en.network << "EOF"

	[Match]
	Name=eth1

	[Network]
	DHCP=yes  

	[DHCP]
	UseDNS=true
	EOF