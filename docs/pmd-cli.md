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
tndf install pmd-cli
~~~~
# Syntax
~~~~
pmd-cli [connection_auth_options] &lt;component&gt; &lt;command&gt; [command_options]
~~~~
Passed-in parameter values can be enclosed in single (&#39;) or double-quotes (&quot;) as long as you use matching characters to denote the beginning and end of the value. Unless a parameter value contains special characters or spaces, you can also omit quotes altogether.

## Connection / Authorization Options

### Local Connections

For local connections, you omit the connection and authorization options:
~~~~
pmd-cli &lt;component&gt; &lt;cmd&gt; &lt;options&gt;
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
pmd-cli --servername &lt;server&gt; --user &lt;username&gt;
~~~~
**Lightwave User**

Before using this method, the pmd server must be joined or should be part of embedded Lightwave.
~~~~
pmd-cli --servername &lt;server&gt; --user &lt;username&gt; --domain &lt;lightwave_domain&gt;
~~~~
**Kerberos spn**

Before using this method, the client must run kinit successfully.
~~~~
pmd-cli --servername &lt;server&gt; --spn &lt;service_principal_name&gt;
~~~~
## Component

``&lt;component&gt;`` is one of the following values:

- ``firewall``
- ``net``
- ``pkg``
- ``usr``

# Firewall Management

The Photon Management Daemon provides CLI commands to help you get information about the firewall.

## Syntax
~~~~
pmd-cli [connection_auth_options] firewall &lt;command&gt; [command_options]
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
pmd-cli firewall rules --chain &lt;chain_name&gt; --add &lt;rule_specification&gt;
~~~~
Example:
~~~~
pmd-cli firewall rules --chain INPUT --add &quot;-p tcp -m tcp --dport 21 -j ACCEPT&quot;
~~~~
**Note:** To confirm that the firewall rule was added, run iptables -S. Running pmd-cli firewall rules lists only persistent rules.

Delete a new firewall rule.
~~~~
pmd-cli firewall rules --chain &lt;chain_name&gt; --delete &lt;rule_specification&gt;
~~~~
**Note:**  To confirm that the firewall rule was removed, run iptables -S. Running pmd-cli firewall rules lists only persistent rules.

## firewall version

Get the version number of the fwmgmt component on the server.
~~~~
pmd-cli firewall version
~~~~
# Network Management

The Photon Management Daemon provides CLI commands to help you manage network interfaces.

## Syntax
~~~~
pmd-cli [connection_auth_options] net &lt;command&gt; [command_options]
~~~~
Many of these commands require the interface name (–interface &lt;ifname&gt;). IP addresses can be specified in dot-decimal notation or as prefixes. Other command options are described below.

## net link_info

Get the mac address, mtu, link state, and link mode for the specified interface.
~~~~
pmd-cli net link_info --get --interface &lt;ifame&gt;
~~~~
Set the MAC address, mode (manual or auto), link state (up or down), link mode (manual or auto), and MTU for the specified interface.
~~~~
pmd-cli net link_info --set --interface &lt;ifname&gt; --macaddr &lt;mac_address&gt; --mode &lt;manual|auto&gt; --state &lt;up|down&gt; --mtu &lt;mtu&gt;
~~~~
## net ip4_address

Get the IPv4 address for the specified interface.
~~~~
pmd-cli net ip4_address --get --interface &lt;ifame&gt;
~~~~
Set the IPv4 address (dot-decimal or prefix notation), mode (dhcp, static, or none), and (optionally) the default gateway for the specified interface.
~~~~
pmd-cli net ip4_address --set --interface &lt;ifname&gt; --mode &lt;dhcp|static|none&gt; --addr &lt;IPv4Address/prefix&gt; --gateway &lt;gateway_address&gt;
~~~~
## net ip6_address

Get IPv6 address(es) for the specified interface.
~~~~
pmd-cli net ip6_address --get --interface &lt;ifame&gt;
~~~~
Add one or more IPv6 addresses (comma-separated list in dot-decimal or prefix notation) to the specified interface.
~~~~
pmd-cli net ip6_address --add --interface &lt;ifame&gt; --addrlist &lt;IPv6Addr1/prefix,IPv6Addr2/prefix,...&gt;
~~~~
Delete one or more IPv6 addresses (comma-separated list in dot-decimal or prefix notation) from the specified interface.
~~~~
pmd-cli net ip6_address --del --interface &lt;ifame&gt; --addrlist &lt;IPv6Addr1/prefix,IPv6Addr2/prefix,...&gt;
~~~~
Set the DHCP mode (1=enable, 0=disable) and autoconfigure settings (1=enable, 0=disable) for the specified interface.
~~~~
pmd-cli net ip6_address --set --interface &lt;ifname&gt; --dhcp &lt;1|0&gt; --autoconf &lt;1|0&gt;
~~~~
## net ip_route

Get the static IP route for the specified interface.
~~~~
pmd-cli net ip_route --get --interface &lt;ifame&gt;
~~~~
Add the static IP route (gateway IP, destination network, and metric) to the specified interface.
~~~~
pmd-cli net ip_route --add --interface &lt;ifname&gt; --gateway &lt;GatewayIP&gt; --destination &lt;DestinationNetwork/prefix&gt; --metric &lt;N&gt;
~~~~
Delete the specified static IP route from the specified interface.
~~~~
pmd-cli net ip_route --del --interface &lt;ifname&gt; --destination &lt;DestIP/N&gt;
~~~~
## net dns_servers

Get the list of DNS servers.
~~~~
pmd-cli net dns_servers --get
~~~~
Set the DNS mode (dhcp or static) for one or more DNS servers (comma-separated list).
~~~~
pmd-cli net dns_servers --set --mode &lt;dhcp|static&gt; --servers &lt;server1,server2,...&gt;
~~~~
Add a DNS server to the list of DNS servers.
~~~~
pmd-cli net dns_servers --add --servers &lt;server&gt;
~~~~
Remove the specified DNS server from the list of DNS servers.
~~~~
pmd-cli net dns_servers --del --servers &lt;server&gt;
~~~~
## net dns_domains

Get the list of DNS domains.
~~~~
pmd-cli net dns_domains --get
~~~~
Set the list of DNS domains (one or more DNS domains in a comma-separated list).
~~~~
pmd-cli net dns_domains --set --domains &lt;domain1,domain2,...&gt;
~~~~
Add a DNS domain to the list of DNS domains.
~~~~
pmd-cli net dns_domains --add --domains &lt;domain1&gt;
~~~~
Delete a DNS domain from the list of DNS domains.
~~~~
pmd-cli net dns_domains --del --domains &lt;domain1&gt;
~~~~
## net dhcp_duid

Get the DHCP DUID per interface for all interfaces in the system.
~~~~
pmd-cli net dhcp_duid --get
~~~~
Set the DHCP DUID for all interfaces in the system.
~~~~
pmd-cli net dhcp_duid --set --duid &lt;duid&gt;
~~~~
## net if_iaid

Get the IAID for the specified interface.
~~~~
pmd-cli net if_iaid --get --interface &lt;ifname&gt;
~~~~
Set the IAID for the specified interface.
~~~~
pmd-cli net if_iaid --set --interface &lt;ifname&gt; --iaid &lt;iaid&gt;
~~~~
## net ntp_servers

Get the NTP servers list.
~~~~
pmd-cli net ntp_servers --get
~~~~
Set the NTP servers list.
~~~~
pmd-cli net ntp_servers --set --servers &lt;server1,server2,...&gt;
~~~~
Add the specified server to the NTP servers list.
~~~~
pmd-cli net ntp_servers --add --servers &lt;server&gt;
~~~~
Delete the specified server from the NTP servers list.
~~~~
pmd-cli net ntp_servers --del --servers &lt;server&gt;
~~~~
## net hostname

Get the system hostname.
~~~~
pmd-cli net hostname --get
~~~~
Set the system hostname.
~~~~
pmd-cli net hostname --set --name &lt;hostname&gt;
~~~~
## net wait_for_link

Wait for the specified network interface to be up and usable (it can send and receive packets).
~~~~
pmd-cli net wait_for_link --interface &lt;ifname&gt; --timeout &lt;timeout&gt;
~~~~
The timeout (in seconds) specifies the maximum time to wait. Specify 0 for no timeout (wait indefinitely).

**Note:** You might need to use net wait_for_ip to wait until you can send and receive IP packets.

## net wait_for_ip

Wait for the specified interface to acquire a valid IP address for the specified address type.
~~~~
pmd-cli net wait_for_ip --interface &lt;ifname&gt; --timeout &lt;timeout&gt; --addrtype &lt;ipv4,ipv6,static_ipv4,static_ipv6,dhcp_ipv4,dhcp_ipv6,auto_ipv6,link_local_ipv6&gt;
~~~~
The timeout (in seconds) specifies the maximum time to wait. Specify 0 for no timeout (wait indefinitely).

## net error_info

Get error information about the specified error code.
~~~~
pmd-cli net error_info --errcode &lt;error_code&gt;
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
pmd-cli net net_info --get --object &lt;ifname or filename&gt; --paramname &lt;param_name&gt;
~~~~
**Note:** The object can be an interface name (for example, &quot;eth0&quot;) or a file name (for example, /etc/systemd/resolved.conf).

Set the value of the specified network configuration parameter for the specified object (interface or file).
~~~~
pmd-cli net net_info --set --object &lt;ifname or filename&gt; --paramname &lt;param_name&gt; --paramvalue &lt;param_value&gt;
~~~~
**Note** : You can add (+) or remove (-) a parameter by prepending the parameter name with + or -.

# Package Management

The Photon Management Daemon provides CLI commands to help you manage packages and repositories.

## Syntax
~~~~
pmd-cli [connection options] pkg &lt;command&gt; [command options]
~~~~
If a command allows for multiple package names, simply specify on the command line, separated by spaces.
~~~~
pmd-cli pkg info &lt;package_name_1&gt; &lt;package_name_2&gt; &lt;package_name_3&gt; ...
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
pmd-cli pkg downgrade &lt;package_name&gt;
~~~~
## pkg erase

Remove the specified package(s).
~~~~
pmd-cli pkg erase &lt;package_name&gt;
~~~~
## pkg info

Get general information about the specified package(s),  such as name, version, release, repository, install size, and so on.
~~~~
pmd-cli pkg info &lt;package_name&gt;
~~~~
If no packages are specified, then this command returns information about all packages.
~~~~
## pkg install
~~~~
Install the specified package(s). Update the package if an update is available.
~~~~
pmd-cli pkg install &lt;package_name&gt;
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
pmd-cli pkg reinstall &lt;package_name&gt;
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
pmd-cli pkg update &lt;package_name&gt;
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
pmd-cli [connection options] usr &lt;command&gt; [command options]
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
pmd-cli usr useradd &lt;username&gt;
~~~~
The system assigns a user ID, home directory, and default shell to the new user. The user group is unspecified.

## usr userdel

Delete the specified user.
~~~~
pmd-cli usr userdel &lt;username&gt;
~~~~
## usr userid

Get the user ID of the specified user (by name). Used to determine whether the specified user exists.
~~~~
pmd-cli usr userid &lt;username&gt;
~~~~
## usr groups

Get a list of user groups. This command returns the following information about each user group: user group name and user group ID.
~~~~
pmd-cli usr groups
~~~~
## usr groupadd

Add a new user group.
~~~~
pmd-cli usr groupadd &lt;user_group_name&gt;
~~~~
The system assigns a group ID to the new user group.

## usr groupdel

Delete the specified user group.
~~~~
pmd-cli usr groupdel &lt;user_group_name&gt;
~~~~
## usr groupid

Get the group ID for the specified user group (by name). Used to determine whether the specified user group exists.
~~~~
pmd-cli usr groupid &lt;user_group_name&gt;
~~~~
## usr version

Get the version of the usermgmt component at the server.
~~~~
pmd-cli usr version
~~~~
