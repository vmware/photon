---
title:  Photon Management Daemon Command-line Interface (pmd-cli)
weight: 2
---

Photon OS provides the Photon Management Daemon command line interface (pmd-cli).

- [Setup Steps](#setup-steps)
- [Syntax](#syntax)
- [Firewall Management](#firewall-management)
- [Network Management](#network-management)
- [Package Management](#package-management)
- [User Management](#user-management)

# Setup Steps

The pmd-cli utility is included with your Photon OS distribution. To make sure that you have the latest version, you can run:

```console
tdnf install pmd-cli
```

# Syntax

```console
pmd-cli [connection_auth_options] <component> <command> [command_options]
```

Passed-in parameter values can be enclosed in single (&#39;) or double-quotes (&quot;) as long as you use matching characters to denote the beginning and end of the value. Unless a parameter value contains special characters or spaces, you can also omit quotes altogether.

## Connection / Authorization Options

### Local Connections

For local connections, you omit the connection and authorization options:

```console
pmd-cli <component> <cmd> <options>
```

Permissions for the currently logged-in user apply when executing commands. This is the same as specifying --servername localhost.

### Remote Connections

For connecting to a remote server (a server other than the local server), you specify two connection / authorization options:

- `--servername`: name of the server
- `--user`: username of a user account on the server

**Note:**  For authentication, you can specify the username (–user &lt;username&gt;) on the command line, but never the password. For security reasons, the system must prompt you for the password.

The option for remote connection is as follows:

**System User**
```console
pmd-cli --servername <server> --user <username>
```

## Component

`<component>` is one of the following values:

- `firewall`
- `net`
- `pkg`
- `usr`

# Firewall Management

The Photon Management Daemon provides CLI commands to help you get information about the firewall.

## Syntax

```console
pmd-cli [connection_auth_options] firewall <command> [command_options]
```

## firewall help

Get help for firewall CLI commands.

```console
pmd-cli firewall help
```

## firewall rules

Get a list of the current persistent firewall rules.

```console
pmd-cli firewall rules [command-options]
```

This command returns information about each firewall rule, such as the chain to which it belongs, the policy to enforce, the table to manipulate, and so on.

Add a new firewall rule.

```console
pmd-cli firewall rules --chain <chain_name> --add <rule_specification>
```

Example:

```console
pmd-cli firewall rules --chain INPUT --add "-p tcp -m tcp --dport 21 -j ACCEPT"
```

**Note:** To confirm that the firewall rule was added, run iptables -S. Running pmd-cli firewall rules lists only persistent rules.

Delete a new firewall rule.

```console
pmd-cli firewall rules --chain <chain_name> --delete <rule_specification>
```

**Note:**  To confirm that the firewall rule was removed, run iptables -S. Running pmd-cli firewall rules lists only persistent rules.

Make firewall rule changes peristent (add --persist flag)

```console
pmd-cli firewall rules --chain <chain_name> --add <rule_specification> --persist
```

## firewall version

Get the version number of the fwmgmt component on the server.

```console
pmd-cli firewall version
```

# Network Management

The Photon Management Daemon provides CLI commands to help you manage network interfaces.

## Syntax

```console
pmd-cli [connection_auth_options] net <command> [command_options]

Query and control the netmanager subsystem.
  -h --help                    Show this help message and exit
  -v --version                 Show package version
```

Many of these commands require the interface name (–interface &lt;ifname&gt;). Command options are described below.

```console
    Command                      Command Option                                     Description

----------------------------------------------------------------------------------------------------

 
    set-mtu                      [LINK] [MTU]                                          Set Link MTU

    set-mac                      [LINK] [MAC]                                          Set Link MAC

    set-link-mode                [LINK] [MODE { yes | no | on | off | 1 | 0} ]         Set Link managed by networkd

    set-dhcp-mode                [LINK] [DHCP-MODE { yes | no | ipv4 | ipv6 } ]        Set Link DHCP setting

    set-dhcp4-client-identifier  [LINK] [IDENTIFIER { mac | duid | duid-only}

    set-dhcp-iaid                [LINK] [IAID]                                         Sets the DHCP Identity Association
                                                                                       Identifier (IAID) for the
                                                                                       interface, a 32-bit unsigned
                                                                                       integer.

    set-dhcp-duid                [LINK | system] [DUID { link-layer-time |             Sets the DHCP Client DUID type which
                                 vendor | link-layer | uuid } ] [RAWDATA]              specifies how the DUID should be 
                                                                                       generated and [RAWDATA] to overides the
                                                                                       global DUIDRawData.

    set-link-state               [LINK] [STATE { up | down } ]                         Set Link State

    add-link-address             [LINK] [ADDRESS] [PEER] ]                             Add Link Address

    delete-link-address          [LINK]                                                Removes Address from Link

    add-default-gateway          [LINK] [GW address] onlink [ONLINK                    Add Link Default Gateway
                                 { yes | no | on | off | 1 | 0}] 

    delete-gateway               [LINK]                                                Removes Gateway from Link

    add-route                    [LINK] [GW address] metric [METRIC { number }]        Set Link route

    delete-route                 [LINK]                                                Removes route from Link

    add-additional-gw            [LINK] [ADDRESS] [ROUTE address] [GW address]         Configures additional gateway for   
                                 [ROUTING POLICY TABLE number]                         another NIC with routing policy rules

    set-hostname                 [HOSTNAME]                                            Sets hostname

    add-dns                      [LINK | system] [ADDRESS]                             Set Link DNS servers

    add-domain                   [LINK | system] [DOMAIN]                              Set Link DOMAIN 

    revert-resolve-link          [LINK]                                                Flushes all DNS server and Domain 
                                                                                       settings of the link

    set-link-local-address       [LINK] [LinkLocalAddressing                           Set Link link-local
                                 { yes | no | on | off | 1 | 0}]                        address autoconfiguration


    set-ipv4ll-route             [LINK] [IPv4LLRoute                                   Set the route needed                              
                                 { yes | no | on | off | 1 | 0}]                       for non-IPv4LL hosts to communicate
                                                                                       with IPv4LL-only hosts

    set-llmnr                    [LINK] [LLMNR { yes | no | on | off | 1 | 0}]         Set Link Link-Local Multicast Name
                                                                                       Resolution

    set-multicast-dns            [LINK] [MulticastDNS { yes | no | on | off | 1 | 0}]  Set Link Multicast DNS

    set-lldp                     [LINK] [LLDP { yes | no | on | off | 1 | 0}]          Set Link Ethernet LLDP packet reception

    set-emit-lldp                [LINK] [EmitLLDP { yes | no | on | off | 1 | 0}]      Set Link Ethernet LLDP packet emission

    set-ipforward                [LINK] [IPForward { yes | no | on | off | 1 | 0}]     Set Link IP packet forwarding for the system

    set-ipv6acceptra             [LINK] [IPv6AcceptRA { yes | no | on | off | 1 | 0}]  Set Link IPv6 Router Advertisement (RA) reception
                                                                                       support for the interface

    set-ipmasquerade             [LINK] [IPMasquerade { yes | no | on | off | 1 | 0}]  Set IP masquerading for the network interface

    set-dhcp4-use-dns            [LINK] [UseDNS { yes | no | on | off | 1 | 0}]        Set Link DHCP4 Use DNS

    set-dhcp4-use-domains        [LINK] [UseDomains { yes | no | on | off | 1 | 0}]    Set Link DHCP4 Use DOMAINS

    set-dhcp4-use-mtu            [LINK] [UseMTU { yes | no | on | off | 1 | 0}]        Set Link DHCP4 Use MTU

    set-dhcp4-use-ntp            [LINK] [UseNTP { yes | no | on | off | 1 | 0}]        Set Link DHCP4 Use NTP

    set-dhcp4-use-dns            [LINK] [UseDNS { yes | no | on | off | 1 | 0}]        Set Link DHCP4 Use DNS

    set-dhcp6-use-dns            [LINK] [UseDNS { yes | no | on | off | 1 | 0}]        Set Link DHCP6 Use DNS

    set-dhcp6-use-ntp            [LINK] [UseNTP { yes | no | on | off | 1 | 0}]        Set Link DHCP6 Use NTP

    add-ntp                      [LINK] [NTP]                                          Add Link NTP server address. This option may be
                                                                                       specified more than once.
                                                                                       This setting is read by systemd-timesyncd.service(8)

    set-ntp                      [LINK] [NTP]                                          Set Link NTP server address. This option may be 
                                                                                       specified more than once.
                                                                                       This setting is read by systemd-timesyncd.service(8)

    delete-ntp                   [LINK] [NTP]                                          Delete Link NTP server address. This option may be
                                                                                       specified more than once.
                                                                                       This setting is read by systemd-timesyncd.service(8)

    disable-ipv6                 [LINK]                                                Disables IPv6 on the interface.

    enable-ipv6                  [LINK]                                                Enables IPv6 on the interface.

    create-vlan                  [VLAN name] dev [LINK master] id [ID INTEGER]         Creates vlan netdev and sets master to device

    create-bridge                [BRIDGE name] [LINK] [LINK] ...                       Creates bridge netdev and sets master to device

    create-bond                  [BOND name] mode [MODE {balance-rr                    Creates bond netdev and sets master to device
                                 | active-backup | balance-xor | broadcast
                                 | 802.3ad | balance-tlb | balance-alb}]
                                 [LINK] [LINK] ...

    create-vxlan                 [VXLAN name] [dev LINK] vni [INTEGER]                 Creates vxlan VXLAN
                                 [local ADDRESS] [remote ADDRESS]                      (Virtual eXtensible Local Area Network) tunneling.                
                                 [port PORT] 
                                 [independent { yes | no | on | off | 1 | 0}].

    create-macvlan               [MACVLAN name] dev [LINK] mode                        Creates macvlan virtualized bridged networking.
                                 [MODE {private | vepa | bridge | passthru | source}]
                                  

    create-macvtap               [MACVTAP name] dev [LINK] mode [MODE                  Creates macvtap virtualized bridged networking.
                                 {private | vepa | bridge | passthru | source}] 

    create-ipvlan                [IPVLAN name] dev [LINK] mode                         Creates ipvlan, virtual LAN, separates    
                                 [MODE {l2 | l3 | l3s}]                                broadcast domains by adding tags to network packet.

    create-ipvtap                [IPVTAP name] dev [LINK]                              Create ipvtap.
                                 mode [MODE {l2 | l3 | l3s}]

    create-vrf                   [VRF name] table [INTEGER}]                           Creates Virtual routing and forwarding (VRF).

    create-veth                  [VETH name] peer [PEER name}]                         Creates virtual Ethernet devices.

    create-ipip                  [IPIP name] [dev LINK] local [ADDRESS]                Creates ipip tunnel.
                                 remote [ADDRESS] [independent
                                 { yes | no | on | off | 1 | 0}]

    create-sit                   [SIT name] [dev LINK] local [ADDRESS]                 Creates sit tunnel.
                                 remote [ADDRESS] [independent 
                                 { yes | no | on | off | 1 | 0}]

    create-vti                    [VTI name] [dev LINK] local [ADDRESS]                Creates vti tunnel.
                                  remote [ADDRESS] [independent
                                  { yes | no | on | off | 1 | 0}]

    create-gre                   [GRE name] [dev LINK] local [ADDRESS]                 Creates gre tunnel.
                                 remote [ADDRESS] [independent 
                                 { yes | no | on | off | 1 | 0}]

    create-wg                    [WIREGUARD name] private-key [PRIVATEKEY]             Creates a wireguard tunnel.
                                 listen-port [PORT INTEGER] public-key
                                 [PUBLICKEY] preshared-key [PRESHAREDKEY]
                                 allowed-ips [IP,IP ...] endpoint [IP:PORT]

    reload                                                                             Reload .network and .netdev files.

    reconfigure                  [LINK]                                                Reconfigure Link.

    add-nft-table                [FAMILY {ipv4 | ipv6 | ip}] [TABLE]                   Adds a new table.

    get-nft-tables               [FAMILY {ipv4 | ipv6 | ip}] [TABLE]                   shows nftable's tables.

    delete-nft-table             [FAMILY {ipv4 | ipv6 | ip}] [TABLE]                   deletes a existing nftable's table.

    add-nft-chain                [FAMILY {ipv4 | ip}] [TABLE] [CHAIN]                  adds a new nftable's chain.

    get-nft-chains               [FAMILY {ipv4 | ipv6 | ip}] [TABLE] [CHAIN]           shows nftable's chains.

    delete-nft-chain             [FAMILY {ipv4 | ipv6 | ip}] [TABLE] [CHAIN]           deletes a nftable's chain from table

    add-nft-rule                 [FAMILY {ipv4 | ipv6 | ip}] [TABLE] [CHAIN]           configures a nft rule for a port.     
                                 [PROTOCOL { tcp | udp}] 
                                 [SOURCE PORT / DESTINATION PORT {sport|dport}]
                                 [PORT] [ACTION {accept | drop}]

    get-nft-rules                [TABLE]                                               shows nftable's rules.

    delete-nft-rule              [FAMILY {ipv4 | ipv6 | ip}] [TABLE]                   deletes a nftable's rule from table
                                 [CHAIN] [HANDLE] 

    nft-run                                                                            runs a nft command.  See man NFT(8)

    is-networkd-running                                                                Check if systemd-networkd is running or not. 

    get-hostname                                                                       Gets hostname

    get-dns-servers                                                                    Gets DNS Servers

    get-dns-domains                                                                    Gets DNS Server DOMAINS

    get-ntp                      [LINK]                                                Get Link NTP server address

    get-link-address             [LINK]                                                Get Link Address

    get-link-route               [LINK]                                                Get Link route

    get-dhcp-mode                [LINK]                                                Get Link DHCP setting. 
                                 [DHCP-MODE { yes | no | ipv4 | ipv6 }]

    get-mac                      [LINK]                                                Get Link MAC


    get-mtu                      [LINK]                                                Get Link MTU

    get-dhcp-iaid                [LINK]                                                Get the DHCP Identity Association Identifier (IAID)
                                                                                       for the interface, a 32-bit unsigned integer.

 
    get-dhcp4-client-identifier  [LINK]                                                Get Link DHCP4 Client Identifier.



    net                          -v                                                    Get the network-config-manager supported version
```

{{% alert title="Note"%}} 
> You can add (+) or remove (-) a parameter by prepending the parameter name with `+` or `-`.
{{%/alert%}}

# Package Management

The Photon Management Daemon provides CLI commands to help you manage packages and repositories.

## Syntax

```console
pmd-cli [connection options] pkg <command> [command options]
```

If a command allows for multiple package names, simply specify on the command line, separated by spaces.

```console
pmd-cli pkg info <package_name_1> <package_name_2> <package_name_3> ...
```

## pkg check-local 

Checks local rpm folder for problems.

```console
pmd-cli pkg check-local 
```

## pkg check-update

Check for available package upgrades. 

```console
pmd-cli pkg check-update
```

## pkg clean all

Remove cached data from tdnf.

```console
pmd-cli pkg clean all
```

## pkg help

Get help text for pkg CLI commands.

```console
pmd-cli pkg help
```

## pkg count

Get the total number of packages in all repos (including installed).

```console
pmd-cli pkg count
```

## pkg distro-sync

Synchronize installed packages to the latest available versions. If no packages are specified, then all available packages are synchronized.

```console
pmd-cli pkg distro-sync
```

## pkg downgrade

Downgrade the specified package(s). If no packages are specified, then all available packages are downgraded.

```console
pmd-cli pkg downgrade <package_name>
```

## pkg erase

Remove the specified package(s).

```console
pmd-cli pkg erase <package_name>
```

## pkg info

Get general information about the specified package(s),  such as name, version, release, repository, install size, and so on.

```console
pmd-cli pkg info <package_name>
```

If no packages are specified, then this command returns information about all packages.

```console
pmd-cli pkg install
```

Install the specified package(s). Update the package if an update is available.

```console
pmd-cli pkg install <package_name>
```

## pkg list

Get a list of packages or groups of packages.

```console
pmd-cli pkg list
```

You can filter by group: all, available, installed, extras, obsoletes, recent, and upgrades.

```console
pmd-cli pkg list upgrades
```

You can also filter by wildcards.

```console
pmd-cli pkg list ph\*
```

## pkg provides openssh

Find what package provides the given binary.

```console
pmd-cli pkg provides openssh
```

## pkg reinstall

Reinstall the specified package(s).

```console
pmd-cli pkg reinstall <package_name>
```

## pkg repolist

Get a list of the configured software repositories.

```console
pmd-cli pkg repolist
```

This command returns a list of the configured software repositories, including the repository ID, repitory name, and status.

## pkg search ssh

Search package details for the given string. 

```console
pmd-cli pkg search ssh
```

If no parameters are specified, then all available packages are updated.

## pkg update

Update the specified package(s).

```console
pmd-cli pkg update *package_name*
```

If no parameters are specified, then all available packages are updated.

## pkg updateinfo

Get the update information on all enabled repositories (status = enabled). If this command returns nothing, then the update information may not exist on the server.

```console
pmd-cli pkg updateinfo
```

# User Management

The Photon Management Daemon provides CLI commands to help you manage users and user groups.

## Syntax

```console
pmd-cli [connection options] usr <command> [command options]
```

## usr help

Display help text for user commands.

```console
pmd-cli usr users
```

## usr users

Get a list of users. This command returns information about each user, including their user name, user ID, user group (if applicable), home directory, and default shell.

```console
pmd-cli usr users
```

## usr useradd

Add a new user. Specify the username.

```console
pmd-cli usr useradd <username>
```

The system assigns a user ID, home directory, and default shell to the new user. The user group is unspecified.

## usr userdel

Delete the specified user.

```console
pmd-cli usr userdel <username>
```

## usr userid

Get the user ID of the specified user (by name). Used to determine whether the specified user exists.

```console
pmd-cli usr userid <username>
```

## usr groups

Get a list of user groups. This command returns the following information about each user group: user group name and user group ID.

```console
pmd-cli usr groups
```

## usr groupadd

Add a new user group.

```console
pmd-cli usr groupadd <user_group_name>
```

The system assigns a group ID to the new user group.

## usr groupdel

Delete the specified user group.

```console
pmd-cli usr groupdel <user_group_name>
```

## usr groupid

Get the group ID for the specified user group (by name). Used to determine whether the specified user group exists.

```console
pmd-cli usr groupid <user_group_name>
```

## usr version

Get the version of the usermgmt component at the server.

```console
pmd-cli usr version
```
