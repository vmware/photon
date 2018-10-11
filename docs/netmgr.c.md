# Network Configuration Manager - C API

Photon OS 2.0 provides a C API for the Network Configuration Manager.

- [About the Network Configuration Manager C API](#about-the-network-configuration-manager-c-api)
- [Interface Configuration APIs](#interface-configuration-apis)
- [IP Address Configuration APIs](#ip-address-configuration-apis)
- [Route Configuration APIs](#route-configuration-apis)
- [DNS Configuration APIs](#dns-configuration-apis)
- [DHCP Options DUID and IAID Configuration APIs](#dhcp-options-duid-and-iaid-configuration-apis)
- [NTP Configuration APIs](#ntp-configuration-apis)
- [Service Management APIs](#service-management-apis)

# About the Network Configuration Manager C API

Use the Network Configuration Manager C API to simplify common network configuration tasks for:

- interfaces
- IP addresses (IPv4 and IPv6 addresses)
- routes
- DNS server and domain settings
- DHCP DUID and IAID settings
- NTP server settings
- service management
- object parameters (interfaces and files)

## Header File

Header files for all the C APIs are defined in the following location:

[https://github.com/](https://github.com/vmware/pmd/tree/master/include) [vmware](https://github.com/vmware/pmd/tree/master/include) [/pmd/tree/master/include](https://github.com/vmware/pmd/tree/master/include)

To install the Network Configuration Manager header file, run the following command:

``tdnf install netmgmt-devel``
n
Once installed, you can reference the header file in the following location:

``/usr/include/netmgmt/netmgr.h``

## Freeing Memory

For all get APIs that take a pointer-to-pointer parameter, the caller has the responsibility to free the memory upon successful response from API by calling free().

## Error Codes

All C API calls return 0 for success, or one of the following error codes for failure.

- 4097 - NM_ERR_INVALID_PARAMETER
- 4098 - NM_ERR_NOT_SUPPORTED
- 4099 - NM_ERR_OUT_OF_MEMORY
- 4100 - NM_ERR_VALUE_NOT_FOUND
- 4101 - NM_ERR_VALUE_EXISTS
- 4102 - NM_ERR_INVALID_INTERFACE
- 4103 - NM_ERR_INVALID_ADDRESS
- 4104 - NM_ERR_INVALID_MODE
- 4105 - NM_ERR_BAD_CONFIG_FILE
- 4106 - NM_ERR_WRITE_FAILED
- 4107 - NM_ERR_TIME_OUT
- 4108 - NM_ERR_DHCP_TIME_OUT

Use nm_get_error_info to retrieve information about an error code.
~~~~
 const char \*
 nm_get_error_info(
     uint32_t nmErrCode
 );``
~~~~
# Interface Configuration APIs

The Photon OS 2.0 network manager C API enables you to manage network interfaces.

## Structure Declarations

### Link Mode

**Description**

Link mode. Available settings:

- ``LINK_AUTO`` - the specified interface is managed and configured by systemd network manager
- ``LINK_MANUAL`` - systemd will not bring up or configure the specified interface
- ``LINK_MODE_UNKNOWN`` - the link mode is unknown

**Declaration**
~~~~
 typedef enum _NET_LINK_MODE
 {
     LINK_AUTO = 0,
     LINK_MANUAL,
     LINK_MODE_UNKNOWN
 } NET_LINK_MODE;``
~~~~
### Link State

**Description**

Link state. Available settings:

- ``LINK_DOWN`` - the link is being administratively down or has no carrier signal
- ``LINK_UP`` - the link is configured up and has carrier signal
- ``LINK_STATE_UNKNOWN`` - link state is unknown

**Declaration**
~~~~
 typedef enum _NET_LINK_STATE
 {
     LINK_DOWN = 0,
     LINK_UP,
     LINK_STATE_UNKNOWN,
 } NET_LINK_STATE;
~~~~
### Link Information

**Description**

Link information. Includes the following information:

- ``pszInterfaceName`` - interface name
- ``pszMacAddress`` - interface hardware address specified in a colon-separated format (for example: "00:0c:29:99:a5:7b")
- ``mtu`` - maximum transmission unit (MTU)
- ``mode`` - link mode (see above)
- ``state`` - link state (see above)

**Declaration**
~~~~
 typedef struct _NET_LINK_INFO
 {
     struct _NET_LINK_INFO \*pNext;
     char \*pszInterfaceName;
     char \*pszMacAddress;
     uint32_t mtu;
     NET_LINK_MODE mode;
     NET_LINK_STATE state;
 } NET_LINK_INFO, \*PNET_LINK_INFO;
~~~~
## nm_set_link_mac_addr

**Description**

Set the MAC address of the interface.

**Declaration**
~~~~
uint32_t

nm_set_link_mac_addr(

     const char \*pszInterfaceName,
     const char \*pszMacAddress
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pszMacAddress`` - interface hardware address specified in a colon-separated format (for example: "00:0c:29:99:a5:7b")

**Returns**

- success: 0
- failure: error code

## nm_get_link_mac_addr

**Description**

Get the MAC address of the interface.

**Declaration**
~~~~
uint32_t
 nm_get_link_mac_addr(
     const char \*pszInterfaceName,
     char \*\*ppszMacAddress
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``ppszMacAddress`` - interface hardware address specified in a colon-separated format (for example: "00:0c:29:99:a5:7b")

**Returns**

- success: 0
- failure: error code

## nm_set_link_mode

**Description**

Set the mode of the interface (auto or manual).

**Declaration**
~~~~
uint32_t
 nm_set_link_mode(
     const char \*pszInterfaceName,
     NET_LINK_MODE mode
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``mode`` - link mode. One of the following values:
  - ``LINK_AUTO`` - the specified interface is managed and configured by systemd network manager
  - ``LINK_MANUAL`` - systemd will not bring up or configure the specified interface
  - ``LINK_MODE_UNKNOWN`` - the link mode is unknown

**Returns**

- success: 0
- failure: error code

## nm_get_link_mode

**Description**

Get the mode of the interface (auto or manual).

**Declaration**
~~~~
uint32_t
 nm_get_link_mode(
     const char \*pszInterfaceName,
     NET_LINK_MODE \*pLinkMode
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pLinkMode`` - link mode. One of the following values:
  - ``LINK_AUTO`` - the specified interface is managed and configured by systemd network manager
  - ``LINK_MANUAL`` - systemd will not bring up or configure the specified interface
  - ``LINK_MODE_UNKNOWN`` - the link mode is unknown

**Returns**

- success: 0
- failure: error code

## nm_set_link_mtu

**Description**

Set the maximum transmission unit (MTU) of the interface.

**Declaration**
~~~~
uint32_t
 nm_set_link_mtu(
     const char \*pszInterfaceName,
     uint32_t mtu
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``mtu`` - maximum transmission unit (MTU)

**Returns**

- success: 0
- failure: error code

## nm_get_link_mtu

**Description**

Get the maximum transmission unit (MTU) of the interface.

**Declaration**
~~~~
nm_get_link_mtu
 uint32_t
 nm_get_link_mtu(
     const char \*pszInterfaceName,
     uint32_t \*pMtu
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pMtu`` - maximum transmission unit (MTU)

**Returns**

- success: 0
- failure: error code

## nm_set_link_state

**Description**

Set the link state of the interface (up or down).

**Declaration**
~~~~
 uint32_t
 nm_set_link_state(
     const char \*pszInterfaceName,
     NET_LINK_STATE state
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``state`` - link state. One of the following values:
  - ``LINK_DOWN`` - the link is being administratively down or has no carrier signal.
  - ``LINK_UP`` - the link is configured up and has carrier signal.
  - ``LINK_STATE_UNKNOWN`` - the link state is unknown

**Returns**

- success: 0
- failure: error code

## nm_get_link_state

**Description**

Get the link state of the interface (up or down).

**Declaration**
~~~~
uint32_t
 nm_get_link_state(
     const char \*pszInterfaceName,
     NET_LINK_STATE \*pLinkState
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pLinkState`` - link state. One of the following values:
  - ``LINK_DOWN`` - the link is being administratively down or has no carrier signal
  - ``LINK_UP`` - the link is configured up and has carrier signal
  - ``LINK_STATE_UNKNOWN`` - the link state is unknown

**Returns**

- success: 0
- failure: error code

## nm_ifup

**Description**

Set the specified interface state to UP. Additionally, if the interface is configured to have an IP address, it waits for the interface to acquire the IP address, and then updates neighbors of its IP address via the address resolution protocol (ARP) messages.

**Declaration**
~~~~
 uint32_t
 nm_ifup(
     const char \*pszInterfaceName
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name

**Returns**

- success: 0
- failure: error code

## nm_ifdown

**Description**

Set the specified interface state to DOWN.

**Declaration**
~~~~
uint32_t
 nm_ifdown(
     const char \*pszInterfaceName
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name

**Returns**

- success: 0
- failure: error code

## nm_get_link_info

**Description**

Get link information for the interface. The caller is responsible for freeing ppLinkInfo by calling nm_free_link_info.

**Declaration**
~~~~
uint32_t
 nm_get_link_info(
     const char \*pszInterfaceName,
     NET_LINK_INFO \*\*ppLinkInfo
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``ppLinkInfo``, which includes the following information:
  - \*``pszInterfaceName`` - interface name
  - \*``pszMacAddress`` - interface hardware address specified in a colon-separated format (for example: "00:0c:29:99:a5:7b")
  - ``mtu`` - maximum transmission unit (MTU)
  - ``mode`` - One of the following values:
    - ``LINK_AUTO`` - the specified interface is managed and configured by systemd network manager
    - ``LINK_MANUAL`` - systemd will not bring up or configure the specified interface
    - ``LINK_MODE_UNKNOWN`` - the link mode is unknown
  - ``state`` - One of the following values:
    - ``LINK_DOWN`` - the link is being administratively down or has no carrier signal
    - ``LINK_UP`` - the link is configured up and has carrier signal
    - ``LINK_STATE_UNKNOWN`` - the link state is unknown

**Returns**

- success: 0
- failure: error code

## nm_free_link_info

**Description**

Frees the NET_LINK_INFO structure returned by a successful nm_get_link_info call.

**Declaration**
~~~~
void
 nm_free_link_info(
     NET_LINK_INFO \*pNetLinkInfo
 );
~~~~
**Arguments**

- ``pNetLinkInfo``, which includes the following information:
  - \*``pszInterfaceName`` - interface name
  - \*``pszMacAddress`` - interface hardware address specified in a colon-separated format (for example: "00:0c:29:99:a5:7b")
  - ``mtu`` - maximum transmission unit (MTU)
  - ``mode`` - One of the following values:
    - ``LINK_AUTO`` - the specified interface is managed and configured by systemd network manager
    - ``LINK_MANUAL`` - systemd will not bring up or configure the specified interface
    - ``LINK_MODE_UNKNOWN`` - the link mode is unknown
  - ``state`` - One of the following values:
    - ``LINK_DOWN`` - the link is being administratively down or has no carrier signal
    - ``LINK_UP`` - the link is configured up and has carrier signal
    - ``LINK_STATE_UNKNOWN`` - the link state is unknown

**Returns**

- success: 0
- failure: error code

# IP Address Configuration APIs

The Photon OS 2.0 network manager C API enables you to manage IP addresses for interfaces that are managed by systemd network manager.

## Structure Declarations

### IP Address Mode

**Description**

Defines the IP address mode. One of the following values:

- ``IPV4_ADDR_MODE_NONE`` - no IPv4 address configured on the interface
- ``IPV4_ADDR_MODE_STATIC`` - the interface is configured with a static IPv4 address
- ``IPV4_ADDR_MODE_DHCP`` -  the interface is configured with a DHCP IPv4 address

**Declaration**
~~~~
 typedef enum _NET_IPV4_ADDR_MODE
 {
     IPV4_ADDR_MODE_NONE = 0,
     IPV4_ADDR_MODE_STATIC,
     IPV4_ADDR_MODE_DHCP,
     IPV4_ADDR_MODE_MAX
 } NET_IPV4_ADDR_MODE;
~~~~
### Address Type

**Description**

Defines the type of IP address. One of the following options:

- ``STATIC_IPV4`` - static IPv4 address
- ``STATIC_IPV6`` - static IPv6 address
- ``DHCP_IPV4`` - DHCP IPv4 address
- ``DHCP_IPV6`` - DHCP IPv6 address
- ``AUTO_IPV6`` - stateless dynamic IPv6 address
- ``LINK_LOCAL_IPV6`` - link local IPv6 address

**Declaration**
~~~~
 typedef enum _NET_ADDR_TYPE
 {
     STATIC_IPV4        =  0x00000001,
     STATIC_IPV6        =  0x00000002,
     DHCP_IPV4          =  0x00000010,
     DHCP_IPV6          =  0x00000020,
     AUTO_IPV6          =  0x00000040,
     LINK_LOCAL_IPV6    =  0x00000080,
 } NET_ADDR_TYPE;
~~~~
### IP Addresses

**Description**

Defines IP addresses.

- ``pszInterfaceName`` - interface name
- ``type`` - address type
- ``pszIPAddrPrefix`` - IP address

**Declarations**
~~~~
 typedef struct _NET_IP_ADDR
 {
     char \*pszInterfaceName;
     NET_ADDR_TYPE type;
     char \*pszIPAddrPrefix;
 } NET_IP_ADDR, \*PNET_IP_ADDR;
~~~~
## nm_set_ipv4_addr_gateway

**Description**

Set the IPv4 address and (optionally) the default gateway address for the interface.

**Declaration**
~~~~
 uint32_t

 nm_set_ipv4_addr_gateway(

     const char \*pszInterfaceName,
     NET_IPV4_ADDR_MODE mode,
     const char \*pszIPv4AddrPrefix,
     const char \*pszIPv4Gateway
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``mode`` - IP address mode; one of the following values:
  - ``IPV4_ADDR_MODE_NONE``
  - ``IPV4_ADDR_MODE_STATIC``
  - ``IPV4_ADDR_MODE_DHCP``
- ``pszIPv4AddrPrefix`` - IPv4 address specified in dot-decimal / prefix notation (for example, 10.10.10.101/23). If the prefix is not specified, then a /32 prefix is assumed.
- ``pszIPv4Gateway`` - IPv4 gateway (optional) specified in the dot-decimal format (for example,10.10.20.30).

**Returns**

- success: 0
- failure: error code

## nm_get_ipv4_addr_gateway

**Description**

Get the IPv4 address and the default gateway address for the interface.

**Declaration**
~~~~
uint32_t
 nm_get_ipv4_addr_gateway(
     const char \*pszInterfaceName,
     NET_IPV4_ADDR_MODE \*pMode,
     char \*\*ppszIPv4AddrPrefix,
     char \*\*ppszIPv4Gateway
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pmode`` - IP mode; one of the following values:
  - ``IPV4_ADDR_MODE_NONE``
  - ``IPV4_ADDR_MODE_STATIC``
  - ``IPV4_ADDR_MODE_DHCP``
- ``ppszIPv4AddrPrefix`` - IPv4 address returned in dot-decimal / prefix notation (for example, 10.10.10.101/23). If the prefix is not specified, then a /32 prefix is assumed.
- ``ppszIPv4Gateway`` - IPv4 gateway (optional) returned in the dot-decimal format (for example,10.10.10.250).

**Returns**

- success: 0
- failure: error code

## nm_add_static_ipv6_addr

**Description**

Add an IPv6 address to the specified interface.

**Declaration**
~~~~
uint32_t
 nm_add_static_ipv6_addr(
     const char \*pszInterfaceName,
     const char \*pszIPv6AddrPrefix
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pszIPv6AddrPrefix`` - IPv6 address specified in the standard colon-separated IPv6 address format followed by the prefix (for example, 2010:a1:b2::25/64). If the not prefix is specified, then a /128 prefix is assumed.

**Returns**

- success: 0
- failure: error code

## nm_delete_static_ipv6_addr

**Description**

Delete a static IPv6 address from the interface.

**Declaration**
~~~~
uint32_t
 nm_delete_static_ipv6_addr(
     const char \*pszInterfaceName,
     const char \*pszIPv6AddrPrefix
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pszIPv6AddrPrefix`` - IPv6 address specified in the standard colon-separated IPv6 address format followed by the prefix (for example, 2010:a1:b2::25/64). If the not prefix is specified, then a /128 prefix is assumed.

**Returns**

- success: 0
- failure: error code

## nm_set_ipv6_addr_mode

**Description**

Set the mode for the interface.

**Declaration**
~~~~
uint32_t
 nm_set_ipv6_addr_mode(
     const char \*pszInterfaceName,
     uint32_t enableDhcp,
     uint32_t enableAutoconf
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``enableDhcp`` - enable (1) or disable (0) DHCP; enabling configures the interface to acquire a DHCP IPv6 address.
- ``enableAutoconf`` - enable (1) or disable (0) autoconf; enabling configures the interface to acquire a stateless autoconfiguration IPv6 address.

**Returns**

- success: 0
- failure: error code

## nm_get_ipv6_addr_mode

**Description**

Get the mode for the interface.

**Declaration**
~~~~
 uint32_t
 nm_get_ipv6_addr_mode(
     const char \*pszInterfaceName,
     uint32_t \*pDhcpEnabled,
     uint32_t \*pAutoconfEnabled
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pDhcpEnabled`` - returns whether IPv6 DHCP is enabled (1) or disabled (0).
- ``pAutoconfEnabled`` - returns whether IPv6 stateless autoconfiguration is enabled (1) or disabled (0).

**Returns**

- success: 0
- failure: error code

## nm_get_ip_addr

**Description**

Get the IP address for the interface.

**Declaration**
~~~~
uint32_t
 nm_get_ip_addr(
     const char \*pszInterfaceName,
     uint32_t addrTypes,
     size_t \*pCount,
     NET_IP_ADDR \*\*\*pppIpAddrList
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``addrTypes`` - type of IP address; one of the following values:
  - ``STATIC_IPV4``
  - ``STATIC_IPV6``
  - ``DHCP_IPV4``
  - ``DHCP_IPV6``
  - ``AUTO_IPV6``
  - ``LINK_LOCAL_IPV6``
- ``pCount`` - number of IP address structures in the pppIpAddrList array returned by the API call.
- ``pppIpAddrList`` - array of NET_IP_ADDR elements that includes the following:
  - ``pszInterfaceName``
  - ``type``
  - ``pszIPAddrPrefix``

**Returns**

- success: 0
- failure: error code

## nm_set_ipv6_gateway

**Description**

Set the default IPv6 gateway for the interface.

**Declaration**
~~~~
 uint32_t
 nm_set_ipv6_gateway(
     const char \*pszInterfaceName,
     const char \*pszIPv6Gateway
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pszIPv6Gateway`` - IPv6 gateway specified in the standard colon-separated IPv6 address format (for example, 2010:125::100)

**Returns**

- success: 0
- failure: error code

## nm_get_ipv6_gateway

**Description**

Get the default IPv6 gateway for the interface.

**Declaration**
~~~~
 uint32_t
 nm_get_ipv6_gateway(
     const char \*pszInterfaceName,
     char \*\*ppszIPv6Gateway
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``ppszIPv6Gateway`` - IPv6 gateway specified in the standard colon-separated IPv6 address format (for example, 2010:125::100)

**Returns**

- success: 0
- failure: error code

# Route Configuration APIs

The Photon OS 2.0 network manager C API enables you to manage static IP routes configuration.

## Structure Declarations

### Route Scope

**Description**

Defines the scope of a route. One of the following options.

- ``GLOBAL_ROUTE`` - route to a destination one or more hops away
- ``LINK_ROUTE`` - route to a destination on the local network
- ``HOST_ROUTE`` - route to a destination address on the local host

**Declaration**
~~~~
 typedef enum _NET_ROUTE_SCOPE
 {
     GLOBAL_ROUTE = 0,
     LINK_ROUTE,
     HOST_ROUTE,
     NET_ROUTE_SCOPE_MAX
 } NET_ROUTE_SCOPE;
~~~~
### IP Route

**Description**

Defines an IP route. Includes the following information:

- ``pszInterfaceName`` - interface through which the specified destination network can be reached
- ``pszDestNetwork`` - destination IP network reached by the specified route
- ``pszSourceNetwork`` - source network for the specified route
- ``pszGateway`` - IP gateway through which the specified destination network can be reached
- ``scope`` - scope of this route entry; one of the following values: GLOBAL_ROUTE, LINK_ROUTE, or HOST_ROUTE as defined above
- ``metric`` - metric of this route, an unsigned integer
- ``table`` - identifier for the route table to which this route belongs.

**Declaration**
~~~~
 typedef struct _NET_IP_ROUTE
 {
     char \*pszInterfaceName;
     char \*pszDestNetwork;
     char \*pszSourceNetwork;
     char \*pszGateway;
     NET_ROUTE_SCOPE scope;
     uint32_t metric;
     uint32_t table;
 } NET_IP_ROUTE, \*PNET_IP_ROUTE;
~~~~
## nm_add_static_ip_route

**Description**

Add a static IP route.

**Declaration**
~~~~
uint32_t
 nm_add_static_ip_route(
     NET_IP_ROUTE \*pRoute
 );
~~~~
**Arguments**

- ``pRoute`` - static IP route

**Returns**

- success: 0
- failure: error code

## nm_delete_static_ip_route

**Description**

Delete a static IP route.

**Declaration**
~~~~
 uint32_t
 nm_delete_static_ip_route(
     NET_IP_ROUTE \*pRoute
 );
~~~~
**Arguments**

- ``pRoute`` - static IP route

**Returns**

- success: 0
- failure: error code

## nm_get_static_ip_routes

**Description**

Get the static IP routes for an interface.

**Declaration**
~~~~
 uint32_t
 nm_get_static_ip_routes(
     const char \*pszInterfaceName,
     size_t \*pCount,
     NET_IP_ROUTE \*\*\*pppRouteList
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pCount`` - number of NET_IP_ROUTE elements returned in the pppRouteList array by the API call upon success
- ``pppRouteList`` - array of static IP routes

**Returns**

- success: 0
- failure: error code

# DNS Configuration APIs

The Photon OS 2.0 network manager C API enables you to manage the DNS and Domains configuration.

## Structure Declarations

### DNS Mode

**Description**

DNS mode. Any of the following values:

- ``DNS_MODE_INVALID`` - DNS mode is unknown
- ``STATIC_DNS`` - DNS servers are statically configured
- ``DHCP_DNS`` - DNS servers configuration is acquired from DHCP protocol.

**Declaration**
~~~~
 typedef enum _NET_DNS_MODE
 {
     DNS_MODE_INVALID = 0,
     STATIC_DNS,
     DHCP_DNS,
     DNS_MODE_MAX,
 } NET_DNS_MODE;
~~~~
## nm_set_dns_servers

**Description**

Set the DNS servers list for the interface.

**Declaration**
~~~~
uint32_t
 nm_set_dns_servers(
     const char \*pszInterfaceName,
     NET_DNS_MODE mode,
     size_t count,
     const char \*\*ppszDnsServers
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name (optional, can be NULL)
- ``mode`` - DNS mode. One of the following values:
  - ``DNS_MODE_INVALID`` = 0
  - ``DNS_MODE_MA``
  - ``DHCP_DNS``
  - ``STATIC_DNS``
- ``count`` - number of NUL terminated DNS server entries passed in the ppszDnsServers array to the API call (for example, 10.10.10.200 or 2020::40)
- ``ppszDnsServers`` - array of DNS servers

**Returns**

- success: 0
- failure: error code

## nm_add_dns_server

**Description**

Add a server to the DNS servers list associated with an interface.

**Declaration**
~~~~
uint32_t
 nm_add_dns_server(
     const char \*pszInterfaceName,
     const char \*pszDnsServer
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name (optional, can be NULL)
- ``ppszDnsServer`` - server to add to the DNS server list

**Returns**

- success: 0
- failure: error code

## nm_delete_dns_server

**Description**

Delete a server from the DNS servers list associated with an interface.

**Declaration**
~~~~
 uint32_t
 nm_delete_dns_server(
     const char \*pszInterfaceName,
     const char \*pszDnsServer
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name (optional, can be NULL)
- ``ppszDnsServer`` - server to remove from the DNS server list

**Returns**

- success: 0
- failure: error code

## nm_get_dns_servers

**Description**

Get the the DNS servers list for the interface.

**Declaration**
~~~~
uint32_t
 nm_get_dns_servers(
     const char \*pszInterfaceName,
     NET_DNS_MODE \*pMode,
     size_t \*pCount,
     char \*\*\*pppszDnsServers
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name (optional, can be NULL)
- ``pMode`` - DNS mode. One of the following values:
  - ``DNS_MODE_INVALID``
  - ``DHCP_DNS``
  - ``STATIC_DNS``
- ``pCount`` - number of NUL terminated DNS server entries in the pppszDnsServers array returned by the API call (for example, 10.10.10.200 or 2020::40)
- ``pppszDnsServers`` - array of DNS servers

**Returns**

- success: 0
- failure: error code

## nm_set_dns_domains

**Description**

Set the DNS domain list.

**Declaration**
~~~~
uint32_t
 nm_set_dns_domains(
     const char \*pszInterfaceName,
     size_t count,
     const char \*\*ppszDnsDomains
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name (optional, can be NULL)
- ``count`` - number of DNS domains specified in the ppszDnsDomains array to the API call (for example, if count = 2, then there are two elements: ppszDnsDomains[0] and ppszDnsDomains[1])
- ``ppszDnsDomains`` - array of DNS domains

**Returns**

- success: 0
- failure: error code

## nm_add_dns_domain

**Description**

Add a DNS domain to the DNS domain list.

**Declaration**
~~~~
uint32_t
 nm_add_dns_domain(
     const char \*pszInterfaceName,
     const char \*pszDnsDomain
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name (optional, can be NULL)
- ``pszDnsDomain`` - DNS domain to add to the list

**Returns**

- success: 0
- failure: error code

## nm_delete_dns_domain

**Description**

Delete a DNS domain from the DNS domain list.

**Declaration**
~~~~
uint32_t
 nm_delete_dns_domain(
     const char \*pszInterfaceName,
     const char \*pszDnsDomain
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name (optional, can be NULL)
- ``pszDnsDomain`` - DNS domain to remove from the list

**Returns**

- success: 0
- failure: error code

## nm_get_dns_domains

**Description**

Get the list of DNS domains.

**Declaration**
~~~~
uint32_t
 nm_get_dns_domains(
     const char \*pszInterfaceName,
     size_t \*pCount,
     char \*\*\*pppszDnsDomains
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name (optional, can be NULL)
- ``pCount`` - number of DNS domains returned in the pppszDnsDomains from the API call (for example, if count = 2, then there are two elements: ppszDnsDomains[0] and ppszDnsDomains[1])
- ``pppszDnsDomains`` - array of DNS domains

**Returns**

- success: 0
- failure: error code

# DHCP Options DUID and IAID Configuration APIs

The Photon OS 2.0 network manager C API enables you to manage DHCP DUID and Interface IAID.

## nm_set_iaid

**Description**

Set the IAID for the interface.

**Declaration**
~~~~
uint32_t
 nm_set_iaid(
     const char \*pszInterfaceName,
     uint32_t iaid
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``iaid`` - interface association identifier (IAID)

**Returns**

- success: 0
- failure: error code

## nm_get_iaid

**Description**

Get the IAID for the interface.

**Declaration**
~~~~
uint32_t
 nm_get_iaid(
     const char \*pszInterfaceName,
     uint32_t \*pIaid
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``pIaid`` - interface association identifier (IAID)

**Returns**

- success: 0
- failure: error code

## nm_set_duid

**Description**

Set the DUID for the interface.

**Declaration**
~~~~
uint32_t
 nm_set_duid(
     const char \*pszInterfaceName,
     const char \*pszDuid
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name (optional, specify NULL to set system global DUID configuration)
- ``pszDuid`` - DHCP unique identifier (DUID)

**Returns**

- success: 0
- failure: error code

## nm_get_duid

**Description**

Get the DUID for the interface.

**Declaration**
~~~~
uint32_t
 nm_get_duid(
     const char \*pszInterfaceName,
     char \*\*ppszDuid
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name (optional, specify NULL to query system global DUID configuration)
- ``ppszDuid`` - DHCP unique identifier (DUID)

**Returns**

- success: 0
- failure: error code

# NTP Configuration APIs

The Photon OS 2.0 network manager C API enables you to manage NTP servers configured for the system.

## nm_set_ntp_servers

**Description**

Set the list of NTP servers.

**Declaration**
~~~~
 uint32_t
 nm_set_ntp_servers(
     size_t count,
     const char \*\*ppszNtpServers
 );
~~~~
**Arguments**

- ``count`` - number of NTP servers in the ppszNtpServers array passed to the API call.
- ``ppszNtpServers`` - array of NTP servers

**Returns**

- success: 0
- failure: error code

## nm_add_ntp_servers

**Description**

Add a server to the NTP servers list.

**Declaration**
~~~~
 uint32_t
 nm_add_ntp_servers(
     size_t count,
     const char \*\*ppszNtpServers
 );
~~~~
**Arguments**

- ``count`` - number of NTP servers to add (specified in the ppszNtpServers array) passed to the API call.
- ``ppszNtpServers`` - array of NTP servers to add

**Returns**

- success: 0
- failure: error code

## nm_delete_ntp_servers

**Description**

Delete a server from the NTP servers list.

**Declaration**
~~~~
 uint32_t
 nm_delete_ntp_servers(
     size_t count,
     const char \*\*ppszNtpServers
 );
~~~~
**Arguments**

- ``count`` - number of NTP servers to delete (specified in the ppszNtpServers array) passed to the API call
- ``ppszNtpServers`` - array of NTP servers to delete

**Returns**

- success: 0
- failure: error code

## nm_get_ntp_servers

**Description**

Get the NTP servers list.

**Declaration**
~~~~
 uint32_t
 nm_get_ntp_servers(
     size_t \*pCount,
     char \*\*\*pppszNtpServers
 );
~~~~
**Arguments**

- ``pCount`` - number of NTP servers in the pppszNtpServers array returned from the API call
- ``pppszNtpServers`` - array of NTP servers

**Returns**

- success: 0
- failure: error code

Other APIs

## nm_set_hostname

**Description**

Set the host name for the system.

**Declaration**
~~~~
 uint32_t
 nm_set_hostname(
     const char \*pszHostname
 );
~~~~
**Arguments**

- ``pszHostname`` - host name

**Returns**

- success: 0
- failure: error code

## nm_get_hostname

**Description**

Get the host name for the system.

**Declaration**
~~~~
 uint32_t
 nm_get_hostname(
     char \*\*ppszHostname
 );
~~~~
**Arguments**

- ``ppszHostname`` - host name

**Returns**

- success: 0
- failure: error code

## nm_wait_for_link_up

**Description**

Wait for the specified interface to come up.

**Declaration**
~~~~
 uint32_t
 nm_wait_for_link_up(
     const char \*pszInterfaceName,
     uint32_t timeout
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``timeout`` - maximum time (in seconds) to wait (until the link is up) before timing out of the request; specify 0 for no timeout (wait indefinitely)

**Returns**

- success: 0
- failure: error code

## nm_wait_for_ip

**Description**

Wait for the interface to acquire an IP address of the specified IP address type.

**Declaration**
~~~~
 uint32_t
 nm_wait_for_ip(
     const char \*pszInterfaceName,
     uint32_t timeout,
     NET_ADDR_TYPE addrTypes
 );
~~~~
**Arguments**

- ``pszInterfaceName`` - interface name
- ``timeout`` - maximum time (in seconds) to wait (until the link has an IP address of the specified address type) before timing out of the request; specify 0 for no timeout (wait indefinitely)
- ``addrTypes`` - type of IP address; one of the following values:
  - ``STATIC_IPV4``
  - ``STATIC_IPV6``
  - ``DHCP_IPV4``
  - ``DHCP_IPV6``
  - ``AUTO_IPV6``
  - ``LINK_LOCAL_IPV6``

**Returns**

- success: 0
- failure: error code

## nm_set_network_param

**Description**

Set the value of a network parameter for an object.

**Declaration**
~~~~
uint32_t
 nm_set_network_param(
     const char \*pszObjectName,
     const char \*pszParamName,
     const char \*pszParamValue
 );
~~~~
**Arguments**

- ``pszObjectName`` - an interface name (for example, "eth0") or a file name (for example, /etc/systemd/resolved.conf)
- ``pszParamName`` - name of a parameter associated with the object; specified in the format SectionName_KeyName (for example, Link_MTUBytes represents the MtuBytes key in [Link] section in [https://www.freedesktop.org/software/systemd/man/systemd.network.html](https://www.freedesktop.org/software/systemd/man/systemd.network.html))
- ``pszParamValue`` - points to the parameter value to set; you can add (+) or remove (-) a parameter by prepending the parameter name with + or -. For example:

netmgr net_info --set --object eth1 --paramname +Network_Address --paramvalue "10.10.10.1/24"

**Returns**

- success: 0
- failure: error code

## nm_get_network_param

**Description**

Get the value of a network parameter associated with an object.

**Declaration**
~~~~
 uint32_t
 nm_get_network_param(
     const char \*pszObjectName,
     const char \*pszParamName,
     char \*\*ppszParamValue
 );
~~~~
**Arguments**

- ``pszObjectName`` - an interface name (for example, "eth0") or a file name (for example, /etc/systemd/resolved.conf)
- ``pszParamName`` - name of a parameter associated with the object; returned in the format SectionName_KeyName (for example, Link_MTUBytes represents the MtuBytes key in [Link] section in  [https://www.freedesktop.org/software/systemd/man/systemd.network.html](https://www.freedesktop.org/software/systemd/man/systemd.network.html))
- ``ppszParamValue`` - parameter value

**Returns**

- success: 0
- failure: error code

# Service Management APIs

## nm_stop_network_service

**Description**

Stop the network service.

**Declaration**
~~~~
 uint32_t
 nm_stop_network_service();
~~~~
**Returns**

- success: 0
- failure: error code

## nm_restart_network_service

**Description**

Restart the network service.

**Declaration**
~~~~
 uint32_t
 nm_restart_network_service();
~~~~
**Returns**

- success: 0
- failure: error code

nm_stop_dns_service

**Description**

Stop the DNS service.

**Declaration**
~~~~
uint32_t
 nm_stop_dns_service();
~~~~
**Returns**

- success: 0
- failure: error code

## nm_restart_dns_service

**Description**

Restart the DNS service.

**Declaration**
~~~~
 uint32_t
 nm_restart_dns_service();
~~~~
**Returns**

- success: 0
- failure: error code

## nm_stop_ntp_service

**Description**

Stop the NTP service.

**Declaration**
~~~~
 uint32_t
 nm_stop_ntp_service();
~~~~
**Returns**

- success: 0
- failure: error code

## nm_restart_ntp_service

**Description**

Restart the NTP service.

**Declaration**
~~~~
 uint32_t
 nm_restart_ntp_service();
~~~~
**Returns**

- success: 0
- failure: error code