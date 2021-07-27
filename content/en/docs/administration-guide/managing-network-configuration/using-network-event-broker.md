---
title: Using Network Event Broker
weight: 18
---

`network-event-broker` is a daemon that configures network and executes scripts on network events such as `systemd-networkd`'s DBus events, `dhclient` lease gains, and so on. 

`network-event-broker` also detects the following events:

- An IP address is added/removed/modified
- A link is added or removed


In the `/etc/network-event-broker` directory, `network-event-broker` creates the link state directories such as `carrier.d`, `configured.d`, `degraded.d`, `no-carrier.d`, `routable.d` and manager state directory such as `manager.d` . You can also keep the executable scripts in these directories.

## Use Case: Running command when a new address is acquired via DHCP. ##


1. `systemd-networkd`: `systemd-networkd`'s scripts are executed when the daemon receives the relevant event from `systemd-networkd`. 


		May 14 17:08:13 Zeus cat[273185]: OperationalState="routable"  
		May 14 17:08:13 Zeus cat[273185]: LINK=ens33


2. `dhclient`: For `dhclient`, scripts are executed in the `routable.d` directory when `dhclient` modifies the `/var/lib/dhclient/dhclient.leases` file and lease information is passed to the scripts as environmental arguments.

Environment variables such as `LINK`, `LINKINDEX=` and DHCP lease information `DHCP_LEASE=` are passed to the scripts. 


## Configuration ##

To manage the `network-event-broker` configuration, use the configuration file named `network-broker.toml` located in the following directory: `/etc/network-broker/` 


### [System] section ###
You can set values for the following keys in the `[System]` section:



`LogLevel=`  
Specifies the log level. The key takes one of the following values: `info`, `warn`, `error`, `debug` and `fatal`. Default is `info`.


`Generator=`  
Specifies the network event generator source. The key takes one of the following values: `systemd-networkd` or `dhclient`. Default is `systemd-networkd`.


### [Network] section
You can set values for the following keys in the `[Network]` section:

`Links=`  
A whitespace-separated list of links whose events should be monitored. No default value is set for this key.

`RoutingPolicyRules=`  
A whitespace-separated list of links for which you want to configure the routing policy rules per address. When you set this configuration, `network-event-broker` automatically adds the `to` and  `from` routing policy rules in another routing table `(ROUTE_TABLE_BASE = 9999 + ifindex)`. When these addresses are removed, the routing policy rules are dropped. No default value is set for this key.

`UseDNS=`  
Specifies whether you want to send the DNS server details to `systemd-resolved`. The key takes one of the following values: `true`, `false`. When set to `true`, the DNS server details are sent to `systemd-resolved` via DBus. This is applicable only to the DHClient. Default is false.


`UseDomain=`  
Specifies whether you want to send the DNS domain details to `systemd-resolved`. The key takes one of the following values: `true`, `false`. When set to `true`, the DNS domain details are sent to `systemd-resolved` via DBus. This is applicable only to the DHClient. Default is false.


`UseHostname=`  
Specifies whether you want to send the host name to `systemd-hostnamed`. The key takes one of the following values: `true`, `false`. When set to `true`, the host name is sent to `systemd-hostnamed` via DBus. This is applicable only to the DHClient. Default is false.


	❯ sudo cat /etc/network-broker/network-broker.toml 
	[System]
	LogLevel="debug"
	Generator="dhclient"
	
	[Network]
	Links="ens33 ens37"
	RoutingPolicyRules="ens33 ens37"
	UseDNS="true"
	UseDomain="true"
