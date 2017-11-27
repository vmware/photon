# Photon Management Daemon Command-line Interface (pmd-cli)

Photon OS 2.0 provides the Photon Management Daemon command line interface (pmd-cli).

- [Setup Steps](#setup-steps)
- [Syntax](#syntax)
- [Firewall Management](#firewall-management)
- [Network Management](#network-management)
- [Package Management](#package-management)
- [User Management](#user-management)

# Setup Steps

The pmd-cli utility is included with your Photon OS 2.0 distribution. To make sure that you have the latest version, you can run:
~~~~
tdnf install pmd-cli
~~~~
# Syntax
~~~~
pmd-cli [connection_auth_options] <component> <command> [command_options]
~~~~
Passed-in parameter values can be enclosed in single (&#39;) or double-quotes (&quot;) as long as you use matching characters to denote the beginning and end of the value. Unless a parameter value contains special characters or spaces, you can also omit quotes altogether.

## Connection / Authorization Options

### Local Connections

For local connections, you omit the connection and authorization options:
~~~~
pmd-cli <component> <cmd> <options>
~~~~
Permissions for the currently logged-in user apply when executing commands. This is the same as specifying --servername localhost.

### Remote Connections

For connecting to a remote server (a server other than the local server), you specify two connection / authorization options:

- ``--servername``: name of the server
- ``--user``: username of a user account on the server

**Note:**  For authentication, you can specify the username (–user &lt;username&gt;) on the command line, but never the password. For security reasons, the system must prompt you for the password.

What follows are three options for remote connections.

**System User**
~~~~
pmd-cli --servername <server> --user <username>
~~~~
**Lightwave User**

Before using this method, the pmd server must be joined or should be part of embedded Lightwave.
~~~~
pmd-cli --servername <server> --user <username> --domain <lightwave_domain>
~~~~
**Kerberos spn**

Before using this method, the client must run kinit successfully.
~~~~
pmd-cli --servername <server> --spn <service_principal_name>
~~~~
## Component

``<component>`` is one of the following values:

- ``firewall``
- ``net``
- ``pkg``
- ``usr``

# Firewall Management

The Photon Management Daemon provides CLI commands to help you get information about the firewall.

## Syntax
~~~~
pmd-cli [connection_auth_options] firewall <command> [command_options]
~~~~
## firewall help

Get help for firewall CLI commands.
~~~~
pmd-cli firewall help
~~~~
## firewall rules

Get a list of the current persistent firewall rules.
~~~~
pmd-cli firewall rules [command-options]
~~~~
This command returns information about each firewall rule, such as the chain to which it belongs, the policy to enforce, the table to manipulate, and so on.

Add a new firewall rule.
~~~~
pmd-cli firewall rules --chain <chain_name> --add <rule_specification>
~~~~
Example:
~~~~
pmd-cli firewall rules --chain INPUT --add "-p tcp -m tcp --dport 21 -j ACCEPT"
~~~~
**Note:** To confirm that the firewall rule was added, run iptables -S. Running pmd-cli firewall rules lists only persistent rules.

Delete a new firewall rule.
~~~~
pmd-cli firewall rules --chain <chain_name> --delete <rule_specification>
~~~~
**Note:**  To confirm that the firewall rule was removed, run iptables -S. Running pmd-cli firewall rules lists only persistent rules.

Make firewall rule changes peristent (add --persist flag)
~~~~
pmd-cli firewall rules --chain <chain_name> --add <rule_specification> --persist
~~~~

## firewall version

Get the version number of the fwmgmt component on the server.
~~~~
pmd-cli firewall version
~~~~
# Network Management

The Photon Management Daemon provides CLI commands to help you manage network interfaces.

## Syntax
~~~~
pmd-cli [connection_auth_options] net <command> [command_options]
~~~~
Many of these commands require the interface name (–interface &lt;ifname&gt;). Command options are described below.

## net link_info

Get the mac address, mtu, link state, and link mode for the specified interface.
~~~~
pmd-cli net link_info --get --interface <ifname>
~~~~
Set the MAC address, mode (manual or auto), link state (up or down), link mode (manual or auto), and MTU for the specified interface.
~~~~
pmd-cli net link_info --set --interface <ifname> --macaddr <mac_address> --mode <manual|auto> --state <up|down> --mtu <mtu>
~~~~
## net ip4_address

Get the IPv4 address for the specified interface.
~~~~
pmd-cli net ip4_address --get --interface <ifname>
~~~~
Set the IPv4 address (dot-decimal/prefix notation), mode (dhcp, static, or none), and (optionally) the default gateway for the specified interface.
~~~~
pmd-cli net ip4_address --set --interface <ifname> --mode <dhcp|static|none> --addr <IPv4Address/prefix> --gateway <gateway_address>
~~~~
## net ip6_address

Get IPv6 address(es) for the specified interface.
~~~~
pmd-cli net ip6_address --get --interface <ifname>
~~~~
Add one or more IPv6 addresses (comma-separated list in colon-separated/prefix notation) to the specified interface.
~~~~
pmd-cli net ip6_address --add --interface <ifname> --addrlist <IPv6Addr1/prefix,IPv6Addr2/prefix,...>
~~~~
Delete one or more IPv6 addresses (comma-separated list in colon-separated/prefix notation) from the specified interface.
~~~~
pmd-cli net ip6_address --del --interface <ifname> --addrlist <IPv6Addr1/prefix,IPv6Addr2/prefix,...>
~~~~
Set the DHCP mode (1=enable, 0=disable) and autoconfigure settings (1=enable, 0=disable) for the specified interface.
~~~~
pmd-cli net ip6_address --set --interface <ifname> --dhcp <1|0> --autoconf <1|0>
~~~~
## net ip_route

Get the static IP route for the specified interface.
~~~~
pmd-cli net ip_route --get --interface <ifname>
~~~~
Add the static IP route (gateway IP, destination network, and metric) to the specified interface.
~~~~
pmd-cli net ip_route --add --interface <ifname> --gateway <GatewayIP> --destination <DestinationNetwork/prefix> --metric <N>
~~~~
Delete the specified static IP route from the specified interface.
~~~~
pmd-cli net ip_route --del --interface <ifname> --destination <DestinationNetwork/prefix>
~~~~
## net dns_servers

Get the list of DNS servers.
~~~~
pmd-cli net dns_servers --get
~~~~
Set the DNS mode (dhcp or static) for one or more DNS servers (comma-separated list).
~~~~
pmd-cli net dns_servers --set --mode <dhcp|static> --servers <server1,server2,...>
~~~~
Add a DNS server to the list of DNS servers.
~~~~
pmd-cli net dns_servers --add --servers <server>
~~~~
Remove the specified DNS server from the list of DNS servers.
~~~~
pmd-cli net dns_servers --del --servers <server>
~~~~
## net dns_domains

Get the list of DNS domains.
~~~~
pmd-cli net dns_domains --get
~~~~
Set the list of DNS domains (one or more DNS domains in a comma-separated list).
~~~~
pmd-cli net dns_domains --set --domains <domain1,domain2,...>
~~~~
Add a DNS domain to the list of DNS domains.
~~~~
pmd-cli net dns_domains --add --domains <domain1>
~~~~
Delete a DNS domain from the list of DNS domains.
~~~~
pmd-cli net dns_domains --del --domains <domain1>
~~~~
## net dhcp_duid

Get the DHCP DUID (optionally interface-specific DUID) for the system.
~~~~
pmd-cli net dhcp_duid --get
~~~~
Set the DHCP DUID for the system, optionally per-interface if the interface is specified.
~~~~
pmd-cli net dhcp_duid --set --duid <duid>
~~~~
## net if_iaid

Get the IAID for the specified interface.
~~~~
pmd-cli net if_iaid --get --interface <ifname>
~~~~
Set the IAID for the specified interface.
~~~~
pmd-cli net if_iaid --set --interface <ifname> --iaid <iaid>
~~~~
## net ntp_servers

Get the NTP servers list.
~~~~
pmd-cli net ntp_servers --get
~~~~
Set the NTP servers list.
~~~~
pmd-cli net ntp_servers --set --servers <server1,server2,...>
~~~~
Add the specified server to the NTP servers list.
~~~~
pmd-cli net ntp_servers --add --servers <server>
~~~~
Delete the specified server from the NTP servers list.
~~~~
pmd-cli net ntp_servers --del --servers <server>
~~~~
## net hostname

Get the system hostname.
~~~~
pmd-cli net hostname --get
~~~~
Set the system hostname.
~~~~
pmd-cli net hostname --set --name <hostname>
~~~~
## net wait_for_link

Wait for the specified network interface to be up and usable (it can send and receive packets).
~~~~
pmd-cli net wait_for_link --interface <ifname> --timeout <timeout>
~~~~
The timeout (in seconds) specifies the maximum time to wait. Specify 0 for no timeout (wait indefinitely).

**Note:** You might need to use net wait_for_ip to wait until you can send and receive IP packets.

## net wait_for_ip

Wait for the specified interface to acquire a valid IP address for the specified address type.
~~~~
pmd-cli net wait_for_ip --interface <ifname> --timeout <timeout> --addrtype <ipv4,ipv6,static_ipv4,static_ipv6,dhcp_ipv4,dhcp_ipv6,auto_ipv6,link_local_ipv6>
~~~~
The timeout (in seconds) specifies the maximum time to wait. Specify 0 for no timeout (wait indefinitely).

## net error_info

Get error information about the specified error code.
~~~~
pmd-cli net error_info --errcode <error_code>
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
- 4106 - timout
- 4107 - DCHP timeout

## net net_info

Get the specified network configuration parameter for the specified object.
~~~~
pmd-cli net net_info --get --object <ifname or filename> --paramname <param_name>
~~~~
**Note:** The object can be an interface name (for example, &quot;eth0&quot;) or a file name (for example, /etc/systemd/resolved.conf).

Set the value of the specified network configuration parameter for the specified object (interface or file).
~~~~
pmd-cli net net_info --set --object <ifname or filename> --paramname <param_name> --paramvalue <param_value>
~~~~
**Note** : You can add (+) or remove (-) a parameter by prepending the parameter name with + or -.

# Package Management

The Photon Management Daemon provides CLI commands to help you manage packages and repositories.

## Syntax
~~~~
pmd-cli [connection options] pkg <command> [command options]
~~~~
If a command allows for multiple package names, simply specify on the command line, separated by spaces.
~~~~
pmd-cli pkg info <package_name_1> <package_name_2> <package_name_3> ...
~~~~
## pkg help

Get help text for pkg CLI commands.
~~~~
pmd-cli pkg help
~~~~
## pkg count

Get the total number of packages in all repos (including installed).
~~~~
pmd-cli pkg count
~~~~
## pkg distro-sync

Synchronize installed packages to the latest available versions. If no packages are specified, then all available packages are synchronized.
~~~~
pmd-cli pkg distro-sync
~~~~
## pkg downgrade

Downgrade the specified package(s). If no packages are specified, then all available packages are downgraded.
~~~~
pmd-cli pkg downgrade <package_name>
~~~~
## pkg erase

Remove the specified package(s).
~~~~
pmd-cli pkg erase <package_name>
~~~~
## pkg info

Get general information about the specified package(s),  such as name, version, release, repository, install size, and so on.
~~~~
pmd-cli pkg info <package_name>
~~~~
If no packages are specified, then this command returns information about all packages.
~~~~
## pkg install
~~~~
Install the specified package(s). Update the package if an update is available.
~~~~
pmd-cli pkg install <package_name>
~~~~
## pkg list

Get a list of packages or groups of packages.
~~~~
pmd-cli pkg list
~~~~
You can filter by group: all, available, installed, extras, obsoletes, recent, and upgrades.
~~~~
pmd-cli pkg list upgrades
~~~~
You can also filter by wildcards.
~~~~
pmd-cli pkg list ph\*
~~~~
## pkg reinstall

Reinstall the specified package(s).
~~~~
pmd-cli pkg reinstall <package_name>
~~~~
## pkg repolist

Get a list of the configured software repositories.
~~~~
pmd-cli pkg repolist
~~~~
This command returns a list of the configured software repositories, including the repository ID, repitory name, and status.

## pkg update

Update the specified package(s).
~~~~
pmd-cli pkg update <package_name>
~~~~
If no parameters are specified, then all available packages are updated.

## pkg updateinfo

Get the update information on all enabled repositories (status = enabled). If this command returns nothing, then the update information may not exist on the server.
~~~~
pmd-cli pkg updateinfo
~~~~
# User Management

The Photon Management Daemon provides CLI commands to help you manage users and user groups.

## Syntax
~~~~
pmd-cli [connection options] usr <command> [command options]
~~~~
## usr help

Display help text for user commands.
~~~~
pmd-cli usr users
~~~~
## usr users

Get a list of users. This command returns information about each user, including their user name, user ID, user group (if applicable), home directory, and default shell.
~~~~
pmd-cli usr users
~~~~
## usr useradd

Add a new user. Specify the username.
~~~~
pmd-cli usr useradd <username>
~~~~
The system assigns a user ID, home directory, and default shell to the new user. The user group is unspecified.

## usr userdel

Delete the specified user.
~~~~
pmd-cli usr userdel <username>
~~~~
## usr userid

Get the user ID of the specified user (by name). Used to determine whether the specified user exists.
~~~~
pmd-cli usr userid <username>
~~~~
## usr groups

Get a list of user groups. This command returns the following information about each user group: user group name and user group ID.
~~~~
pmd-cli usr groups
~~~~
## usr groupadd

Add a new user group.
~~~~
pmd-cli usr groupadd <user_group_name>
~~~~
The system assigns a group ID to the new user group.

## usr groupdel

Delete the specified user group.
~~~~
pmd-cli usr groupdel <user_group_name>
~~~~
## usr groupid

Get the group ID for the specified user group (by name). Used to determine whether the specified user group exists.
~~~~
pmd-cli usr groupid <user_group_name>
~~~~
## usr version

Get the version of the usermgmt component at the server.
~~~~
pmd-cli usr version
~~~~
