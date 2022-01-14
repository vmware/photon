---
title:  Writing a Plugin
weight: 4
---


`photon-mgmtd` is designed with a robust plugin-based architecture in mind. You can easily add and remove modules to `photon-mgmtd`. The plugins are separate modules with well-defined interfaces that make implementing application features easier. You can create custom versions of an application with minimal source code modifications.

You can perform the following steps to write a plugin:

1.  Choose a namespace under plugins directory (systemd, system, proc) where you want to put your module.
2.  Write the sub router. For example, `plugins/systemd/`
3.  Write your module: `module.go` and `module_router.go`
4.  Write `RegisterRouterModule` 
5.  Register `RegisterRouterModule` with the parent router. 
For example, for login registered with `RegisterRouterSystem` under `system` namespace, write `login.RegisterRouterLogin`.


You can use the `pmctl` tool to view and configure system, network, and service status. The following example illustrates how to view the status:

Service status:


	❯ pmctl service status nginx.service
	                  Name: nginx.service 
	           Description: The nginx HTTP and reverse proxy server 
	               MainPid: 45732 
	             LoadState: loaded 
	           ActiveState: active 
	              SubState: running 
	         UnitFileState: disabled 
	  StateChangeTimeStamp: Sun Oct 31 12:02:02 IST 2021 
	  ActiveEnterTimestamp: Sun Oct 31 12:02:02 IST 2021 
	 InactiveExitTimestamp: Sun Oct 31 12:02:02 IST 2021 
	   ActiveExitTimestamp: 0 
	 InactiveExitTimestamp: Sun Oct 31 12:02:02 IST 2021 
	                Active: active (running) since Sun Oct 31 12:02:02 IST 2021



System status:
  
	❯ pmctl status  system
	              System Name: Zeus
	                   Kernel: Linux (5.14.0-0.rc7.54.fc36.x86_64) #1 SMP Mon Aug 23 13:55:32 UTC 2021
	                  Chassis: vm
	           Hardware Model: VMware Virtual Platform
	          Hardware Vendor: VMware, Inc.
	             Product UUID: 979e4d56b63718b18534e112e64cb18
	         Operating System: VMware Photon OS/Linux
	Operating System Home URL: https://vmware.github.io/photon/
	          Systemd Version: v247.10-3.ph4
	             Architecture: x86-64
	           Virtualization: vmware
	            Network State: routable (carrier)
	     Network Online State: online
	                      DNS: 172.16.130.2
	                  Address: 172.16.130.132/24 on link ens33
	                           172.16.130.131/24 on link ens33
	                           fe80::3279:c56d:55f9:aed7/64 on link ens33
	                           172.16.130.138/24 on link ens37
	                  Gateway: 172.16.130.2 on link ens37
	                           172.16.130.2 on link ens33
	                   Uptime: Running Since (2 days, 3 hours, 8 minutes) Booted (Wed Dec 22 15:57:24 IST 2021) Users (9) Proc (284)
	                   Memory: Total (13564788736) Used (13564788736) Free (589791232) Available (9723891712)


Network status:

	❯ pmctl status network -i ens33
	             Name: ens33
	Alternative Names: enp2s1
	            Index: 2
	        Link File: /usr/lib/systemd/network/99-default.link
	     Network File: /etc/systemd/network/10-ens33.network
	             Type: ether
	            State: routable (configured)
	           Driver: e1000
	           Vendor: Intel Corporation
	            Model: 82545EM Gigabit Ethernet Controller (Copper) (PRO/1000 MT Single Port Adapter)
	             Path: pci-0000:02:01.0
	    Carrier State: carrier
	     Online State: online
	IPv4Address State: routable
	IPv6Address State: degraded
	       HW Address: 00:0c:29:5f:d1:39
	              MTU: 1500
	        OperState: up
	            Flags: up|broadcast|multicast
	        Addresses: 172.16.130.132/24 172.16.130.131/24 fe80::3279:c56d:55f9:aed7/64
	          Gateway: 172.16.130.2
	              DNS: 172.16.130.2

