---
title:  Process Details and Configuration Management
weight: 7
---


## Net device property status ##

To get the status of the network device property, use the following command in `pmctl`:

	pmctl status proc net path <PATH> property <PROPERTY>

Example:

	pmctl status proc net path ipv6 property calipso_cache_bucket_size

Response:

	                 Path: ipv6
	             Property: calipso_cache_bucket_size
	                Value: 10


## Net device property configuration ##

To get the network device property configuration details, use the following command in `pmctl`:

	pmctl proc net path <PATH> property <PROPERTY> value <VALUE>

Example:

	>pmctl proc net path ipv6 property calipso_cache_bucket_size value 12


## Net device link property status ##

To get the status of the network device link, use the following command in `pmctl`:

	pmctl status proc net path <PATH> dev <LINK> property <PROPERTY>

Example:

	>pmctl status proc net path ipv6 dev ens37 property mtu

Response:

	                 Path: ipv6
	                 Link: ens37
	             Property: mtu
	                Value: 1300


## Net device link property configuration ##

To get the configuration details of the network device link, use the following command in `pmctl`:


	pmctl proc net path <PATH> dev <LINK> property <PROPERTY> value <VALUE>

Example:

	>pmctl proc net path ipv6 dev ens37 property mtu value 1500



## VM property status ##

To get the property status of the virtual machine, use the following command in `pmctl`:
 
	pmctl status proc vm <PROPERTY>

Example:

	>pmctl status proc vm page-cluster

Response:

	             Property: page-cluster
	                Value: 3


## VM property configuration ##

To get the property configuration details, use the following command in `pmctl`:

	pmctl proc vm <PROPERTY> <VALUE>

Example:

	pmctl proc vm page-cluster 5


## System property status ##

To get system property details, use the following command in `pmctl`:

	pmctl status proc system <PROPERTY>


Example:

	>pmctl status proc system cpuinfo


## ARP status ##

To get the ARP status details, use the following command in `pmctl`:

	pmctl status proc arp


Example:

	>pmctl status proc arp

Response:

             IPAddress: 172.16.61.254
                HWType: 0x1
                 Flags: 0x2
             HWAddress: 00:50:56:f3:5d:48
                  Mask: *
                Device: ens37

             IPAddress: 172.16.61.254
                HWType: 0x1
                 Flags: 0x2
             HWAddress: 00:50:56:f3:5d:48
                  Mask: *
                Device: ens33

             IPAddress: 172.16.61.2
                HWType: 0x1
                 Flags: 0x2
             HWAddress: 00:50:56:f4:e7:22
                  Mask: *
                Device: ens33

             IPAddress: 172.16.61.2
                HWType: 0x1
                 Flags: 0x2
             HWAddress: 00:50:56:f4:e7:22
                  Mask: *
                Device: ens37

## Netstat Details ##

To get the netstat details, use the following command in `pmctl`:

	pmctl status proc netstat <PROTOCOL>

Example:

	>pmctl status proc netstat tcp

## Process status ##

To get the process status details, use the following command in `pmctl`:

	pmctl status proc process <PID> <PROPERTY>

Example:

	>pmctl status proc process 88157 pid-memory-percent

## Protopidstat status ##

To get the protopidstat status details, use the following command in `pmctl`:

	pmctl status proc protopidstat <PID> <PROTOCOL>

Example:

	>pmctl status proc protopidstat 89502 tcp



