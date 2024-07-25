# Photon Network Manager Command-line Interface (netmgr)

For locally logged-on users, Photon OS provides a command line interface to manage network configuration of the system.

- [Setup Steps](#setup-steps)
- [Syntax](#syntax)
- [Network Manager CLI](#network-manager-cli)

# Setup Steps

The netmgr tool is included with your Photon OS distribution. To make sure that you have the latest version, you can run:
~~~~
tdnf install netmgmt
~~~~
# Syntax
The CLI is built on set, get, add, delete command model and uses the option-name - option-value model of specifying command parameters.
~~~~
netmgr <network object> <--get | --set | --add | --del> <command options>
~~~~
Passed-in parameter values can be enclosed in single (&#39;) or double-quotes (&quot;) as long as you use matching characters to denote the beginning and end of the value. Unless a parameter value contains special characters or spaces, you can also omit quotes altogether.

## network object

``<network object>`` is one of the following values:

- ``link_info``
- ``ip4_address``
- ``ip6_address``
- ``ip_route``
- ``dns_servers``
- ``dns_domains``
- ``dhcp_duid``
- ``if_iaid``
- ``ntp_servers``
- ``hostname``
- ``wait_for_link``
- ``wait_for_ip``
- ``error_info``
- ``net_info``

# Network Manager CLI

## link_info

Get the mac address, MTU, link state, and link mode for the (optionally) specified interface.
~~~~
netmgr link_info --get --interface <ifname>
~~~~
Set the MAC address, link state (up or down), link mode (manual or auto), or MTU for the specified interface.
~~~~
netmgr link_info --set --interface <ifname> --macaddr <mac_address>
netmgr link_info --set --interface <ifname> --mode <manual|auto>
netmgr link_info --set --interface <ifname> --state <up|down>
netmgr link_info --set --interface <ifname> --mtu <mtu>
~~~~
## ip4_address

Get the IPv4 address for the specified interface.
~~~~
netmgr ip4_address --get --interface <ifname>
~~~~
Set the IPv4 address (dot-decimal/prefix notation), mode (dhcp, static, or none), and (optionally) the default gateway for the specified interface.
~~~~
netmgr ip4_address --set --interface <ifname> --mode <dhcp|static|none> --addr <ipv4_address/prefix> --gateway <gateway_address>
~~~~
## ip6_address

Get IPv6 addresses for the specified interface.
~~~~
netmgr ip6_address --get --interface <ifname>
~~~~
Add one or more IPv6 addresses (comma-separated list in colon-separated/prefix notation) to the specified interface.
~~~~
netmgr ip6_address --add --interface <ifname> --addrlist <ipv6_addr1/prefix,ipv6_addr2/prefix,...>
~~~~
Delete one or more IPv6 addresses (comma-separated list in colon-separated/prefix notation) from the specified interface.
~~~~
netmgr ip6_address --del --interface <ifname> --addrlist <ipv6_addr1/prefix,ipv6_addr2/prefix,...>
~~~~
Set the IPv6 DHCP mode (1=enable, 0=disable) and IPv6 auto-configuration settings (1=enable, 0=disable) for the specified interface.
~~~~
netmgr ip6_address --set --interface <ifname> --dhcp <1|0> --autoconf <1|0>
~~~~
## ip_route

Get the static IP route for the specified interface.
~~~~
netmgr ip_route --get --interface <ifname>
~~~~
Add the static IP route (gateway IP, destination network, and metric) to the specified interface.
~~~~
netmgr ip_route --add --interface <ifname> --gateway <gateway_address> --destination <destination_network/prefix> --metric <N>
~~~~
Delete the specified static IP route from the specified interface.
~~~~
netmgr ip_route --del --interface <ifname> --destination <destination_network/prefix>
~~~~
## dns_servers

Get the list of DNS servers.
~~~~
netmgr dns_servers --get
~~~~
Set the DNS mode (DHCP or static) for one or more DNS servers (comma-separated list).
~~~~
netmgr dns_servers --set --mode <dhcp|static> --servers <server1,server2,...>
~~~~
Add a DNS server to the list of DNS servers.
~~~~
netmgr dns_servers --add --servers <server>
~~~~
Remove the specified DNS server from the list of DNS servers.
~~~~
netmgr dns_servers --del --servers <server>
~~~~
## dns_domains

Get the list of DNS domains.
~~~~
netmgr dns_domains --get
~~~~
Set the list of DNS domains (one or more DNS domains in a comma-separated list).
~~~~
netmgr dns_domains --set --domains <domain1,domain2,...>
~~~~
Add a DNS domain to the list of DNS domains.
~~~~
netmgr dns_domains --add --domains <domain>
~~~~
Delete a DNS domain from the list of DNS domains.
~~~~
netmgr dns_domains --del --domains <domain>
~~~~
## dhcp_duid

Get the DHCP DUID (optionally interface-specific DUID) for the system.
~~~~
netmgr dhcp_duid --get
~~~~
Set the DHCP DUID for the system, optionally per-interface if the interface is specified.
~~~~
netmgr dhcp_duid --set --duid <duid>
~~~~
## if_iaid

Get the IAID for the specified interface.
~~~~
netmgr if_iaid --get --interface <ifname>
~~~~
Set the IAID for the specified interface.
~~~~
netmgr if_iaid --set --interface <ifname> --iaid <iaid>
~~~~
## ntp_servers

Get the NTP servers list.
~~~~
netmgr ntp_servers --get
~~~~
Set the NTP servers list.
~~~~
netmgr ntp_servers --set --servers <server1,server2,...>
~~~~
Add the specified server to the NTP servers list.
~~~~
netmgr ntp_servers --add --servers <server>
~~~~
Delete the specified server from the NTP servers list.
~~~~
netmgr ntp_servers --del --servers <server>
~~~~
## hostname

Get the system hostname.
~~~~
netmgr hostname --get
~~~~
Set the system hostname.
~~~~
netmgr hostname --set --name <hostname>
~~~~
## wait_for_link

Wait for the specified network interface to be up and usable (it can send and receive packets).
~~~~
netmgr wait_for_link --interface <ifname> --timeout <timeout>
~~~~
The timeout (in seconds) specifies the maximum time to wait. Specify 0 for no timeout (wait indefinitely).

**Note:** You might need to use wait_for_ip to wait until you can send and receive IP packets.

## wait_for_ip

Wait for the specified interface to acquire a valid IP address for the specified address type.
~~~~
netmgr wait_for_ip --interface <ifname> --timeout <timeout> --addrtype <ipv4,ipv6,static_ipv4,static_ipv6,dhcp_ipv4,dhcp_ipv6,auto_ipv6,link_local_ipv6>
~~~~
The timeout (in seconds) specifies the maximum time to wait. Specify 0 for no timeout (wait indefinitely).

## error_info

Get error information about the specified error code.
~~~~
netmgr error_info --errcode <error_code>
~~~~
Here is a list of error codes:

- 4097 - invalid parameter
- 4098 - not supported
- 4099 - out of memory
- 4100 - value not found
- 4101 - value exists
- 4102 - invalid interface
- 4103 - invalid mode
- 4104 - bad configuration file
- 4105 - write failed
- 4106 - timeout
- 4107 - DCHP timeout

## net_info

Get the specified network configuration parameter for the specified object.
~~~~
netmgr net_info --get --object <ifname or filename> --paramname <param_name>
~~~~
**Note:** The object can be an interface name (for example, &quot;eth0&quot;) or a file name (for example, /etc/systemd/resolved.conf).

Set the value of the specified network configuration parameter for the specified object (interface or file).
~~~~
netmgr net_info --set --object <ifname or filename> --paramname <param_name> --paramvalue <param_value>
~~~~
**Note** : You can add (+) or remove (-) a parameter by prepending the parameter name with + or -.

For example, in order to add static IPv4 address "10.10.10.1/24" to eth0 interface, the following command adds this **Address** to the **Network** section of the **eth0** network configuration file.
~~~~
netmgr net_info --set --object eth0 --paramname +Network_Address --paramvalue "10.10.10.1/24"
~~~~


