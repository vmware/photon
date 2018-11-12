# Network Configuration Manager - Python API

Photon OS 2.0 provides a Python API for the Network Configuration Manager.

- [Setup Instructions](#setup-instructions)
- [Initialization Steps](#initialization-steps)
- [Get Online Help](#get-online-help)
- [Basic Information](#basic-information)
- [Interface Configuration](#interface-configuration)
- [IP Address Configuration](#ip-address-configuration)
- [DNS Configuration](#dns-configuration)
- [DHCP Options, DUID, and IAID Configuration](#dhcp-options-duid-and-iaid-configuration)
- [NTP Servers](#ntp-servers)

## Setup Instructions

To set up and run the latest version of the Network Manager API for Python:

````
# tdnf install pmd pmd-python3
# systemctl start pmd
````

## Initialization Steps

````
# python3
>>> import pmd
>>> net = pmd.server().net
````
## Get Online Help

Get help for all commands.
````
>>> help(net)
````
Get help for a specific command.
````
>>> help(net.add_ntp_servers)
-in function add_ntp_servers:
add_ntp_servers(...) method of  [server.net](http://server.net/) instance
    net.add_ntp_servers(ntpservers = ["20.20.20.20", "25.30.40.70"])
    adds ntp servers. returns success: 0, failure: exception.
(END)
````

## Basic Information

### get_system_network_info

Get network information details that are common to the entire system.

**Syntax**

````
net.get_system_network_info()
````
**Returns**

- details about the system network (DUID, DNS mode, DNS server list, DNS domain list, NTP server list)

**Example**
````
>>> system_network_info = netmgmt.get_system_network_info()

>>> print ( system_network_info)

[{DUID: 00:02:11:22:33:44:55:66:77:20, DNS Mode: (null), DNS ServerList: ['10.10.100.100', '20.20.200.10'], DNS domain list: [' [abcd.com](http://abcd.com)'], NTP ServerList: (null)}]
````

### get_err_info

Get information about the specified error number.

**Syntax**
````
net.get_err_info(error = <error_number>)
````
**Parameters**

- error - error number

Here is the list of error numbers:

- 4097 - invalid parameter
- 4098 - not supported
- 4099 - out of memory
- 4100 - value not found
- 4101 - value exists
- 4102 - invalid interface
- 4103 - invalid mode
- 4104 - bad configuration file
- 4105 - write failed
- 4106 - timout
- 4107 - DCHP timeout

**Returns**

- success: 0
- failure: exception

Example
````
>> net.get_err_info(error = 4097)

'invalid parameter'
````
## Interface Configuration

Use these commands to manage the configuration for a network interface.

### get_link_info

Get the link info for the specified interface or for all interfaces (if no interface is specified).

**Syntax**
````
net.get_link_info(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name (optional)

**Returns**

- success: link info
- failure: exception

### get_link_macaddr

Get the MAC address for the specified interface or for all interfaces (if no interface is specified).

**Syntax**
````
net.get_link_macaddr(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name (optional)

**Returns**

- success: MAC address
- failure: exception

### get_link_mode

Get the link mode for the specified interface (auto or manual), or for all interfaces (if no interface is specified).

**Syntax**
````
net.get_link_mode(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name (optional)

**Returns**

- success: link mode (auto, manual, or unknown)
- failure: exception

### get_link_mtu

Get the MTU of the specified interface or for all interfaces (if no interface is specified).

**Syntax**
````
net.get_link_mtu(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name (optional)

**Returns**

- success: link MTU
- failure: exception

### get_link_state

Get the link state of the specified interface or for all interfaces (if no interface is specified).

**Syntax**
````
net.get_link_state(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name (optional)

**Returns**

- success: link state (up, down, unknown)
- failure: exception

### set_link_down

Bring down the specified interface.

**Syntax**

````
net.set_link_down(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name

**Returns**

- success: 0
- failure: exception

### set_link_macaddr

Set the MAC address of the specified interface.

**Syntax**
````
net.set_link_macaddr(ifname = interface_name, macaddr = mac_address)
````
**Parameters**

- ``ifname`` - interface name
- ``macaddr`` = MAC address

**Returns**

- success: 0
- failure: exception

### set_link_mode

Set the mode (auto or manual) of the specifed interface.

**Syntax**
````
net.set_link_mode(ifname = interface_name, link_mode = [auto, manual])
````
**Parameters**

- ``ifname`` - interface name
- ``link_mode`` - auto or manual

**Returns**

- success: 0
- failure: exception

### set_link_mtu

Set the MTU for the specified interface.

**Syntax**
````
net.set_link_mtu(ifname = interface_name, mtu = mtu)
````
**Parameters**

- ``ifname`` - interface name
- ``mtu`` - ``mtu``

**Returns**

- success: 0
- failure: exception

### set_link_state

Set the state (up or down) of the specified interface.

**Syntax**
````
net.set_link_state(ifname = interface_name, link_state = [down, up])
````
**Parameters**

- ``ifname`` - interface name
- ``link_state`` - down or up

**Returns**

- success: 0
- failure: exception

### set_link_up

Brings up the specified interface.

**Syntax**
````
net.set_link_up(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name
- ``link_state`` - down or up

**Returns**

- success: 0
- failure: exception

## IP Address Configuration

Use these commands to manage IP address configuration for a network interface.

### add_static_ipv6_addr

Add a static IPv6 address to the specified interface.

**Syntax**
````
net.add_static_ipv6_addr(ifname = interface_name, addr_prefix = ipv6address_prefix)
````
**Parameters**

- ``ifname`` - interface name
- ``addr_prefix`` - IPv6 address prefix

**Returns**

- success: 0
- failure: exception

### del_static_ipv6_addr

Delete a static IPv6 address from the specified interface.

**Syntax**
````
net.del_static_ipv6_addr(ifname = interface_name, addr_prefix = ipv6address_prefix)
````
**Parameters**

- ``ifname`` - interface name
- ``addr_prefix`` - IPv6 address prefix

**Returns**

- success: 0
- failure: exception

### get_ipv4_addr_gateway

Get the IPv4 address with the prefix and gateway for the specified interface.

**Syntax**
````
net.get_ipv4_addr_gateway(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name

**Returns**

- success: IPv4 address with the prefix and gateway
- failure: exception

### get_ipv6_addr

Get the list of IPv6 addresses for the specified interface.

**Syntax**
````
net.get_ipv6_addr(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name

**Returns**

- success: IPv6 address list
- failure: exception

### get_ipv6_addr_mode

Get the address mode for the specified interface to determine whether DHCPv6, autoconf are enabled or disabled.

**Syntax**
````
net.get_ipv6_addr_mode(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name

**Returns**

- Status for DHCPv6, autoconf (True=enabled, False=disabled)
- failure: exception

### get_ipv6_gateway

Get the IPv6 gateway for the specified interface.

**Syntax**
````
net.get_ipv6_gateway(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name

**Returns**

- success: IPv6 gateway
- failure: exception

### set_ipv4_addr_gateway

Set the IPv4 address with the prefix and gateway for the specified interface.

**Syntax**
````
net.get_ipv4_addr_gateway(ifname = interface_name, addr_mode = [dhcp, static, none], addr_prefix = ipv4addressprefix, gateway = ipv4gateway)
````
**Parameters**

- ``ifname`` - interface name
- ``addr_mode`` - address mode - dhcp, static, or none
- ``addr_prefix`` -  IPv4 address or prefix
- ``gateway`` - IPv4 gateway

**Returns**

- success: 0
- failure: exception

### set_ipv6_addr_mode

Set the address mode for the specified interface.

**Syntax**
````
net.set_ipv6_addr_mode(ifname = interface_name, enable_dhcp = [True, False], enable_autoconf = [True, False])
````
**Parameters**

- ``ifname`` - interface name
- ``enable_dhcp`` - True to enable, False to disable
- ``enable_autoconf`` - True to enable, False to disable

**Returns**

- success: 0
- failure: exception

### set_ipv6_gateway

Set the IPv6 gateway for the specified interface.

**Syntax**
````
net.set_ipv6_gateway(ifname = interface_name, gateway = ipv6gateway)
````
**Parameters**

- ``ifname`` - interface name
- ``gateway`` - IPv6 gateway

**Returns**

- success: 0
- failure: exception

## DNS Configuration

Use these commands to manage DNS domains and servers for a network interface.

### get_dns_domains

Get the list of DNS domains for the specified interface.

**Syntax**
````
net.get_dns_domains(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name

**Returns**

- success: list of DNS domains
- failure: exception

### get_dns_servers

Get the list of DNS servers and the mode for the specified interface.

**Syntax**
````
net.get_dns_servers(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name

**Returns**

- success: list of DNS servers and mode
- failure: exception

### set_dns_domains

Set the list of DNS domains for the specified interface.

**Syntax**
````
net.set_dns_domains(domains = ["domain1","domain2",...], ifname = interface_name)
````
**Parameters**

- ``domains`` - comma-separated list of one or more domains
- ``ifname`` - interface name

**Returns**

- success: 0
- failure: exception

### set_dns_servers

Set the list of DNS servers for the specified interface.

**Syntax**
````
net.set_dns_servers(dns_mode = [dhcp, static], servers = ["server1","server2", ...], ifname = interface_name)
````
**Parameters**

- ``dns_mode`` - dhcp or static
- ``servers`` - comma-separate list of one or more servers
- ``ifname`` - interface name

**Returns**

- success: 0
- failure: exception

## DHCP Options DUID and IAID Configuration

### get_link_iaid

Get the IAID for the specified interface.

**Syntax**
````
net.get_link_iaid(ifname = interface)
````
**Parameters**

- ``ifname`` - interface name

**Returns**

- success: IAID
- failure: exception

### set_link_iaid

Set the IAID for the specified interface.

**Syntax**
````
net.set_link_iaid(ifname = interface_name, iaid = <iaid>)
````
**Parameters**

- ``ifname`` - interface name
- iaid - IAID

**Returns**

- success: 0
- failure: exception

### get_dhcp_duid

Get the DCHP DUID.

**Syntax**
````
net.get_dhcp_duid(ifname = interface_name)
````
**Parameters**

- ``ifname`` - interface name (optional)

**Returns**

- success: DUID
- failure: exception

### set_dhcp_duid

Set the DCHP DUID.

**Syntax**
````
net.set_dhcp_duid(ifname = interface_name duid = duid)
````
**Parameters**

- ``ifname`` - interface name (optional)
- ``duid`` - DUID to set

**Returns**

- success: 0
- failure: exception

## NTP Servers

Use these commands to manage the NTP servers list.

### add_ntp_servers

Add one or more NTP servers to the NTP servers list.

**Syntax**
````
net.add_ntp_servers(ntpservers = ["server1", "server2", ...])
````
**Parameters**

- ``ntpservers`` - Comma-separated list of NTP servers to add to the list.

**Returns**

- success: 0
- failure: exception

### del_ntp_servers

Remove one or more NTP servers from the NTP servers list.

**Syntax**
````
net.del_ntp_servers(ntpservers = ["server1", "server2", ...])
````
**Parameters**

- ``ntpservers`` - Comma-separated list of NTP servers to remove from the list.

**Returns**

- success: 0
- failure: exception

### get_ntp_servers

Get the NTP servers list.

**Syntax**
````
net.get_ntp_servers()
````
**Returns**

- success: NTP servers list
- failure: exception

### set_ntp_servers

Set the NTP servers list.

**Syntax**
````
net.set_ntp_servers(ntpservers = ["server1", "server2", ...])
````
**Parameters**

- ``ntpservers`` - Comma-separated list of NTP servers to set in the list.

**Returns**

- success: 0
- failure: exception

### get_hostname

Get the host name.

**Syntax**

net.get_hostname()

**Returns**

- success: host name
- failure: exception

### set_hostname

Set the host name.

**Syntax**
````
net.set_hostname(hostname)
````
**Parameters**

- ``hostname`` - name to assign to the host

**Returns**

- success: 0
- failure: exception

### wait_for_ip

Wait for the specified interface to acquire a valid IP address of the specified IP address type.

**Syntax**
````
net.wait_for_ip(ifname = interface_name, timeout = timeout, addrtypes = [ipv4, ipv6, static_ipv4, static_ipv6, dhcp_ipv4, dhcp_ipv6, auto_ipv6, link_local_ipv6])
````
**Parameters**

- ``ifname`` - interface name
- ``timeout`` - maximum time (in seconds) to wait (until the link is up) before timing out of the request; specify 0 for no timeout (wait indefinitely)
- ``addrtypes`` - one of the following address types: ipv4, ipv6, static_ipv4, static_ipv6, dhcp_ipv4, dhcp_ipv6, auto_ipv6, or link_local_ipv6

**Returns**

- success: 0 (when the link has an IP of the specified type)
- failure: exception (for example, timeout expired)

### wait_for_link_up

Wait for the specified interface to come up.

**Syntax**
````
net.wait_for_link_up(ifname = interface_name, timeout = timeout)
````
**Parameters**

- ``ifname`` - interface name
- ``timeout`` - maximum time (in seconds) to wait (until the link is up) before timing out of the request; specify 0 for no timeout (wait indefinitely)

**Returns**

- success: 0 (when link is up)
- failure: exception (for example, timeout expired)

### get_network_param

Get the specified network configuration parameter for the specified interface or filename.

**Syntax**
````
net.get_network_param(object = IfName or Filename, paramname = SectionName_KeyName)
````
**Parameters**

- ``object`` - an interface name (for example, &quot;eth0&quot;) or a file name (for example, /etc/systemd/resolved.conf)
- ``paramname`` - name of a parameter associated with the object; specified in the format SectionName_KeyName (for example, Link_MTUBytes represents the MtuBytes key in [Link] section in  [https://www.freedesktop.org/software/systemd/man/systemd.network.html](https://www.freedesktop.org/software/systemd/man/systemd.network.html))

**Returns**

- success: 0
- failure: exception

### set_network_param

Set the value of a network configuration parameter for the specified interface or filename.

**Syntax**
````
net.set_network_param(object = interface_name or filename, paramname = SectionName_KeyName, paramvalue = key_value)
````
**Parameters**

- ``object`` - an interface name (for example, &quot;eth0&quot;) or a file name (for example, /etc/systemd/resolved.conf)
- ``paramname`` - name of a parameter associated with the object; specified in the format SectionName_KeyName (for example, Link_MTUBytes represents the MtuBytes key in [Link] section in  [https://www.freedesktop.org/software/systemd/man/systemd.network.html](https://www.freedesktop.org/software/systemd/man/systemd.network.html))

**Returns**

- success: 0
- failure: exception
