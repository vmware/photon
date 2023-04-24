---
title:  Network Management
weight: 3
---

## GET Method ##


### Network Details ###

To fetch complete network details, execute a GET request in the following format:

	curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request GET http://localhost/api/v1/network/describe | jq % Total % Received % Xferd Average Speed Time Time Time Current Dload Upload Total Spent Left Speed 100 5238 0 5238 0 0 88919 0 --:--:-- --:--:-- --:--:-- 90310

**Response:**

	{
	   "success":true,
	   "message":{
	      "NetworDescribe":{
	         "AddressState":"routable",
	         "CarrierState":"carrier",
	         "OperationalState":"routable",
	         "OnlineState":"",
	         "IPv4AddressState":"",
	         "IPv6AddressState":"",
	         "DNS":[
	            "10.142.7.1",
	            "10.132.7.1",
	            "10.166.17.90"
	         ],
	         "Domains":null,
	         "RouteDomains":null,
	         "NTP":[
	            "10.128.152.81",
	            "10.166.1.120",
	            "10.188.26.119",
	            "10.84.55.42"
	         ]
	      },
	      "LinksDescribe":{
	         "Interfaces":[
	            {
	               "AddressState":"off",
	               "AlternativeNames":null,
	               "CarrierState":"carrier",
	               "Driver":"",
	               "IPv4AddressState":"",
	               "IPv6AddressState":"",
	               "Index":1,
	               "LinkFile":"",
	               "Model":"",
	               "Name":"lo",
	               "OnlineState":"",
	               "OperationalState":"carrier",
	               "Path":"",
	               "SetupState":"unmanaged",
	               "Type":"loopback",
	               "Vendor":"",
	               "Manufacturer":""
	            },
	            {
	               "AddressState":"routable",
	               "AlternativeNames":null,
	               "CarrierState":"carrier",
	               "Driver":"vmxnet3",
	               "IPv4AddressState":"",
	               "IPv6AddressState":"",
	               "Index":2,
	               "LinkFile":"",
	               "Model":"VMXNET3 Ethernet Controller",
	               "Name":"eth0",
	               "OnlineState":"",
	               "OperationalState":"routable",
	               "Path":"pci-0000:0b:00.0",
	               "SetupState":"configured",
	               "Type":"ether",
	               "Vendor":"VMware",
	               "Manufacturer":"",
	               "NetworkFile":"/etc/systemd/network/99-dhcp-en.network"
	            }
	         ]
	      },
	      "links":[
	         {
	            "Index":1,
	            "MTU":65536,
	            "TxQLen":1000,
	            "Name":"lo",
	            "AlternativeNames":"",
	            "HardwareAddr":"",
	            "Flags":"up|loopback",
	            "RawFlags":65609,
	            "ParentIndex":0,
	            "MasterIndex":0,
	            "Namespace":"",
	            "Alias":"",
	            "Statistics":{
	               "RxPackets":168,
	               "TxPackets":168,
	               "RxBytes":17146,
	               "TxBytes":17146,
	               "RxErrors":0,
	               "TxErrors":0,
	               "RxDropped":0,
	               "TxDropped":0,
	               "Multicast":0,
	               "Collisions":0,
	               "RxLengthErrors":0,
	               "RxOverErrors":0,
	               "RxCrcErrors":0,
	               "RxFrameErrors":0,
	               "RxFifoErrors":0,
	               "RxMissedErrors":0,
	               "TxAbortedErrors":0,
	               "TxCarrierErrors":0,
	               "TxFifoErrors":0,
	               "TxHeartbeatErrors":0,
	               "TxWindowErrors":0,
	               "RxCompressed":0,
	               "TxCompressed":0
	            },
	            "Promisc":0,
	            "Xdp":{
	               "Fd":0,
	               "Attached":false,
	               "Flags":0,
	               "ProgId":0
	            },
	            "EncapType":"loopback",
	            "Protinfo":"",
	            "OperState":"unknown",
	            "NetNsID":0,
	            "NumTxQueues":1,
	            "NumRxQueues":1,
	            "GSOMaxSize":65536,
	            "GSOMaxSegs":65535,
	            "Group":0,
	            "Slave":""
	         },
	         {
	            "Index":2,
	            "MTU":1500,
	            "TxQLen":1000,
	            "Name":"eth0",
	            "AlternativeNames":"",
	            "HardwareAddr":"00:0c:29:68:ed:d8",
	            "Flags":"up|broadcast|multicast",
	            "RawFlags":69699,
	            "ParentIndex":0,
	            "MasterIndex":0,
	            "Namespace":"",
	            "Alias":"",
	            "Statistics":{
	               "RxPackets":179491,
	               "TxPackets":25306,
	               "RxBytes":281174090,
	               "TxBytes":2339627,
	               "RxErrors":0,
	               "TxErrors":0,
	               "RxDropped":120,
	               "TxDropped":0,
	               "Multicast":0,
	               "Collisions":0,
	               "RxLengthErrors":0,
	               "RxOverErrors":0,
	               "RxCrcErrors":0,
	               "RxFrameErrors":0,
	               "RxFifoErrors":0,
	               "RxMissedErrors":0,
	               "TxAbortedErrors":0,
	               "TxCarrierErrors":0,
	               "TxFifoErrors":0,
	               "TxHeartbeatErrors":0,
	               "TxWindowErrors":0,
	               "RxCompressed":0,
	               "TxCompressed":0
	            },
	            "Promisc":0,
	            "Xdp":{
	               "Fd":0,
	               "Attached":false,
	               "Flags":0,
	               "ProgId":0
	            },
	            "EncapType":"ether",
	            "Protinfo":"",
	            "OperState":"up",
	            "NetNsID":0,
	            "NumTxQueues":8,
	            "NumRxQueues":8,
	            "GSOMaxSize":65536,
	            "GSOMaxSegs":65535,
	            "Group":0,
	            "Slave":""
	         }
	      ],
	      "Addresses":[
	         {
	            "Name":"lo",
	            "Ifindex":1,
	            "OperState":"unknown",
	            "Mac":"",
	            "MTU":65536,
	            "Addresses":[
	               {
	                  "IP":"127.0.0.1",
	                  "Mask":8,
	                  "Label":"lo",
	                  "Flags":128,
	                  "Scope":254,
	                  "Peer":"",
	                  "Broadcast":"",
	                  "PreferedLft":4294967295,
	                  "ValidLft":4294967295
	               },
	               {
	                  "IP":"::1",
	                  "Mask":128,
	                  "Label":"",
	                  "Flags":128,
	                  "Scope":254,
	                  "Peer":"",
	                  "Broadcast":"",
	                  "PreferedLft":4294967295,
	                  "ValidLft":4294967295
	               }
	            ]
	         },
	         {
	            "Name":"eth0",
	            "Ifindex":2,
	            "OperState":"up",
	            "Mac":"00:0c:29:68:ed:d8",
	            "MTU":1500,
	            "Addresses":[
	               {
	                  "IP":"10.197.103.42",
	                  "Mask":23,
	                  "Label":"eth0",
	                  "Flags":0,
	                  "Scope":0,
	                  "Peer":"",
	                  "Broadcast":"10.197.103.255",
	                  "PreferedLft":3927,
	                  "ValidLft":3927
	               },
	               {
	                  "IP":"fe80::20c:29ff:fe68:edd8",
	                  "Mask":64,
	                  "Label":"",
	                  "Flags":128,
	                  "Scope":253,
	                  "Peer":"",
	                  "Broadcast":"",
	                  "PreferedLft":4294967295,
	                  "ValidLft":4294967295
	               }
	            ]
	         }
	      ],
	      "Routes":[
	         {
	            "LinkName":"eth0",
	            "LinkIndex":2,
	            "ILinkIndex":0,
	            "Scope":0,
	            "Dst":{
	               "IP":"",
	               "Mask":0
	            },
	            "Src":"10.197.103.42",
	            "Gw":"10.197.103.253",
	            "MultiPath":"",
	            "Protocol":16,
	            "Priority":1024,
	            "Table":254,
	            "Type":1,
	            "Tos":0,
	            "Flags":null,
	            "MPLSDst":"",
	            "NewDst":"",
	            "Encap":"",
	            "MTU":0,
	            "AdvMSS":0,
	            "Hoplimit":0
	         },
	         {
	            "LinkName":"eth0",
	            "LinkIndex":2,
	            "ILinkIndex":0,
	            "Scope":253,
	            "Dst":{
	               "IP":"10.197.102.0",
	               "Mask":23
	            },
	            "Src":"10.197.103.42",
	            "Gw":"",
	            "MultiPath":"",
	            "Protocol":2,
	            "Priority":0,
	            "Table":254,
	            "Type":1,
	            "Tos":0,
	            "Flags":null,
	            "MPLSDst":"",
	            "NewDst":"",
	            "Encap":"",
	            "MTU":0,
	            "AdvMSS":0,
	            "Hoplimit":0
	         },
	         {
	            "LinkName":"eth0",
	            "LinkIndex":2,
	            "ILinkIndex":0,
	            "Scope":253,
	            "Dst":{
	               "IP":"10.197.103.253",
	               "Mask":32
	            },
	            "Src":"10.197.103.42",
	            "Gw":"",
	            "MultiPath":"",
	            "Protocol":16,
	            "Priority":1024,
	            "Table":254,
	            "Type":1,
	            "Tos":0,
	            "Flags":null,
	            "MPLSDst":"",
	            "NewDst":"",
	            "Encap":"",
	            "MTU":0,
	            "AdvMSS":0,
	            "Hoplimit":0
	         },
	         {
	            "LinkName":"lo",
	            "LinkIndex":1,
	            "ILinkIndex":0,
	            "Scope":0,
	            "Dst":{
	               "IP":"::1",
	               "Mask":128
	            },
	            "Src":"",
	            "Gw":"",
	            "MultiPath":"",
	            "Protocol":2,
	            "Priority":256,
	            "Table":254,
	            "Type":1,
	            "Tos":0,
	            "Flags":null,
	            "MPLSDst":"",
	            "NewDst":"",
	            "Encap":"",
	            "MTU":0,
	            "AdvMSS":0,
	            "Hoplimit":0
	         },
	         {
	            "LinkName":"eth0",
	            "LinkIndex":2,
	            "ILinkIndex":0,
	            "Scope":0,
	            "Dst":{
	               "IP":"fe80::",
	               "Mask":64
	            },
	            "Src":"",
	            "Gw":"",
	            "MultiPath":"",
	            "Protocol":2,
	            "Priority":256,
	            "Table":254,
	            "Type":1,
	            "Tos":0,
	            "Flags":null,
	            "MPLSDst":"",
	            "NewDst":"",
	            "Encap":"",
	            "MTU":0,
	            "AdvMSS":0,
	            "Hoplimit":0
	         }
	      ],
	      "Dns":[
	         {
	            "Link":"eth0",
	            "Family":2,
	            "Dns":"10.142.7.1"
	         },
	         {
	            "Link":"eth0",
	            "Family":2,
	            "Dns":"10.132.7.1"
	         },
	         {
	            "Link":"eth0",
	            "Family":2,
	            "Dns":"10.166.17.90"
	         }
	      ],
	      "Domains":null,
	      "NTP":{
	         "ServerName":"",
	         "Family":0,
	         "ServerAddress":"",
	         "SystemNTPServers":null,
	         "LinkNTPServers":[
	            "10.128.152.81",
	            "10.166.1.120",
	            "10.188.26.119",
	            "10.84.55.42"
	         ]
	      }
	   },
	   "errors":""
	}

### Route Details ###

To fetch the route details, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/network/netlink/route

Example:

    root@photon [ ~/4.0/photon ]# curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/network/netlink/route | jq % Total % Received % Xferd Average Speed Time Time Time Current Dload Upload Total Spent Left Speed 100 1407 100 1407 0 0 996k 0 --:--:-- --:--:-- --:--:-- 1374k


**Response:**  
    
	{
	   "success":true,
	   "message":[
	      {
	         "LinkName":"eth0",
	         "LinkIndex":2,
	         "ILinkIndex":0,
	         "Scope":0,
	         "Dst":{
	            "IP":"",
	            "Mask":0
	         },
	         "Src":"10.197.103.42",
	         "Gw":"10.197.103.253",
	         "MultiPath":"",
	         "Protocol":16,
	         "Priority":1024,
	         "Table":254,
	         "Type":1,
	         "Tos":0,
	         "Flags":null,
	         "MPLSDst":"",
	         "NewDst":"",
	         "Encap":"",
	         "MTU":0,
	         "AdvMSS":0,
	         "Hoplimit":0
	      },
	      {
	         "LinkName":"eth0",
	         "LinkIndex":2,
	         "ILinkIndex":0,
	         "Scope":253,
	         "Dst":{
	            "IP":"10.197.102.0",
	            "Mask":23
	         },
	         "Src":"10.197.103.42",
	         "Gw":"",
	         "MultiPath":"",
	         "Protocol":2,
	         "Priority":0,
	         "Table":254,
	         "Type":1,
	         "Tos":0,
	         "Flags":null,
	         "MPLSDst":"",
	         "NewDst":"",
	         "Encap":"",
	         "MTU":0,
	         "AdvMSS":0,
	         "Hoplimit":0
	      },
	      {
	         "LinkName":"eth0",
	         "LinkIndex":2,
	         "ILinkIndex":0,
	         "Scope":253,
	         "Dst":{
	            "IP":"10.197.103.253",
	            "Mask":32
	         },
	         "Src":"10.197.103.42",
	         "Gw":"",
	         "MultiPath":"",
	         "Protocol":16,
	         "Priority":1024,
	         "Table":254,
	         "Type":1,
	         "Tos":0,
	         "Flags":null,
	         "MPLSDst":"",
	         "NewDst":"",
	         "Encap":"",
	         "MTU":0,
	         "AdvMSS":0,
	         "Hoplimit":0
	      },
	      {
	         "LinkName":"lo",
	         "LinkIndex":1,
	         "ILinkIndex":0,
	         "Scope":0,
	         "Dst":{
	            "IP":"::1",
	            "Mask":128
	         },
	         "Src":"",
	         "Gw":"",
	         "MultiPath":"",
	         "Protocol":2,
	         "Priority":256,
	         "Table":254,
	         "Type":1,
	         "Tos":0,
	         "Flags":null,
	         "MPLSDst":"",
	         "NewDst":"",
	         "Encap":"",
	         "MTU":0,
	         "AdvMSS":0,
	         "Hoplimit":0
	      },
	      {
	         "LinkName":"eth0",
	         "LinkIndex":2,
	         "ILinkIndex":0,
	         "Scope":0,
	         "Dst":{
	            "IP":"fe80::",
	            "Mask":64
	         },
	         "Src":"",
	         "Gw":"",
	         "MultiPath":"",
	         "Protocol":2,
	         "Priority":256,
	         "Table":254,
	         "Type":1,
	         "Tos":0,
	         "Flags":null,
	         "MPLSDst":"",
	         "NewDst":"",
	         "Encap":"",
	         "MTU":0,
	         "AdvMSS":0,
	         "Hoplimit":0
	      }
	   ],
	   "errors":""
	}




### All Interfaces Links Details ###

To fetch all the interfaces links details (such as interface, mac address, and transaction), execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/network/netlink/link

Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/network/netlink/link

**Response:**  
    
	{
	   "success":true,
	   "message":[
	      {
	         "Index":1,
	         "MTU":65536,
	         "TxQLen":1000,
	         "Name":"lo",
	         "AlternativeNames":"",
	         "HardwareAddr":"",
	         "Flags":"up|loopback",
	         "RawFlags":65609,
	         "ParentIndex":0,
	         "MasterIndex":0,
	         "Namespace":"",
	         "Alias":"",
	         "Statistics":{
	            "RxPackets":168,
	            "TxPackets":168,
	            "RxBytes":17146,
	            "TxBytes":17146,
	            "RxErrors":0,
	            "TxErrors":0,
	            "RxDropped":0,
	            "TxDropped":0,
	            "Multicast":0,
	            "Collisions":0,
	            "RxLengthErrors":0,
	            "RxOverErrors":0,
	            "RxCrcErrors":0,
	            "RxFrameErrors":0,
	            "RxFifoErrors":0,
	            "RxMissedErrors":0,
	            "TxAbortedErrors":0,
	            "TxCarrierErrors":0,
	            "TxFifoErrors":0,
	            "TxHeartbeatErrors":0,
	            "TxWindowErrors":0,
	            "RxCompressed":0,
	            "TxCompressed":0
	         },
	         "Promisc":0,
	         "Xdp":{
	            "Fd":0,
	            "Attached":false,
	            "Flags":0,
	            "ProgId":0
	         },
	         "EncapType":"loopback",
	         "Protinfo":"",
	         "OperState":"unknown",
	         "NetNsID":0,
	         "NumTxQueues":1,
	         "NumRxQueues":1,
	         "GSOMaxSize":65536,
	         "GSOMaxSegs":65535,
	         "Group":0,
	         "Slave":""
	      },
	      {
	         "Index":2,
	         "MTU":1500,
	         "TxQLen":1000,
	         "Name":"eth0",
	         "AlternativeNames":"",
	         "HardwareAddr":"00:0c:29:68:ed:d8",
	         "Flags":"up|broadcast|multicast",
	         "RawFlags":69699,
	         "ParentIndex":0,
	         "MasterIndex":0,
	         "Namespace":"",
	         "Alias":"",
	         "Statistics":{
	            "RxPackets":226492,
	            "TxPackets":25740,
	            "RxBytes":289546384,
	            "TxBytes":2689948,
	            "RxErrors":0,
	            "TxErrors":0,
	            "RxDropped":120,
	            "TxDropped":0,
	            "Multicast":0,
	            "Collisions":0,
	            "RxLengthErrors":0,
	            "RxOverErrors":0,
	            "RxCrcErrors":0,
	            "RxFrameErrors":0,
	            "RxFifoErrors":0,
	            "RxMissedErrors":0,
	            "TxAbortedErrors":0,
	            "TxCarrierErrors":0,
	            "TxFifoErrors":0,
	            "TxHeartbeatErrors":0,
	            "TxWindowErrors":0,
	            "RxCompressed":0,
	            "TxCompressed":0
	         },
	         "Promisc":0,
	         "Xdp":{
	            "Fd":0,
	            "Attached":false,
	            "Flags":0,
	            "ProgId":0
	         },
	         "EncapType":"ether",
	         "Protinfo":"",
	         "OperState":"up",
	         "NetNsID":0,
	         "NumTxQueues":8,
	         "NumRxQueues":8,
	         "GSOMaxSize":65536,
	         "GSOMaxSegs":65535,
	         "Group":0,
	         "Slave":""
	      }
	   ],
	   "errors":""
	}


### Network DNS Status ###

To fetch the network DNS status, use the following command in `pmctl`:

	>pmctl status network dns
	Global

	        DNS: 8.8.8.1 8.8.8.2 
	DNS Domains: test3.com test4.com . localdomain . localdomain 
	Link 2 (ens33)
	Current DNS Server:  172.16.61.2
	       DNS Servers:  172.16.61.2

	Link 3 (ens37)
	Current DNS Server:  172.16.61.2
	       DNS Servers:  172.16.61.2


### Network iostat Status ###

To fetch the network iostat status, use the following command in `pmctl`:

	> pmctl status network iostat
	            Name: lo
	Packets received: 7510
	  Bytes received: 7510
	      Bytes sent: 7510
	         Drop in: 7510
	        Drop out: 0
	        Error in: 0
	       Error out: 0
	         Fifo in: 0
	        Fifo out: 0

	            Name: ens33
	Packets received: 46014
	  Bytes received: 19072
	      Bytes sent: 19072
	         Drop in: 19072
	        Drop out: 0
	        Error in: 0
	       Error out: 0
	         Fifo in: 0
	        Fifo out: 0

	            Name: ens37
	Packets received: 9682
	  Bytes received: 10779
	      Bytes sent: 10779
	         Drop in: 10779
	        Drop out: 0
	        Error in: 0
	       Error out: 0
	         Fifo in: 0
	        Fifo out: 0



### Network interfaces status ###

To fetch the network status of the network interfaces, use the following command in `pmctl`:

	> pmctl status network interfaces
	            Name: lo
	           Index: 1
	             MTU: 65536
	           Flags: up loopback
	Hardware Address: 
	       Addresses: 127.0.0.1/8 ::1/128
	
	            Name: ens33
	           Index: 2
	             MTU: 1500
	           Flags: up broadcast multicast
	Hardware Address: 00:0c:29:7c:6f:84
	       Addresses: 172.16.61.128/24 fe80::c099:2598:cc4c:14d1/64
	
	            Name: ens37
	           Index: 3
	             MTU: 1500
	           Flags: up broadcast multicast
	Hardware Address: 00:0c:29:7c:6f:8e
	       Addresses: 172.16.61.134/24 fe80::be9:7746:7729:3e2/64



### Configure Network Link Section Using pmctl ###

You can configure the network links using `pmctl` command. The following section lists the commands you can use to configure network links.


#### Configure Network dhcp

	pmctl network set-dhcp <deviceName> <DHCPMode>

Example: 
	
	>pmctl network set-dhcp ens37 ipv4


#### Configure network linkLocalAddressing

	pmctl network set-link-local-addr <deviceName> <linkLocalAddressingMode>

Example: 

	>pmctl network set-link-local-addr ens37 ipv4


#### Configure network multicastDNS

	pmctl network set-multicast-dns <deviceName> <MulticastDNSMode>

Example: 	

	>pmctl network set-multicast-dns ens37 resolve


#### Configure network address

	pmctl network add-link-address <deviceName> address <Address> peer <Address> label <labelValue> scope <scopeValue>

Example: 

	>pmctl network add-link-address ens37 address 192.168.0.15/24 peer 192.168.10.10/24 label ipv4 scope link


#### Configure network route

	pmctl network add-route dev <deviceName> gw <Gateway> gwonlink <GatewayOnlink> src <Source> dest <Destination> prefsrc <preferredSource> table <Table> scope <Scope>

Example: 

	>pmctl network add-route dev ens33 gw 192.168.1.0 gwonlink no src 192.168.1.15/24 dest 192.168.10.10/24 prefsrc 192.168.8.9 table 1234 scope link


#### Configure network dns

	pmctl network add-dns dev <deviceName> dns <dnslist>

Example: 

	>pmctl network add-dns dev ens37 dns 8.8.8.8,8.8.4.4,8.8.8.1,8.8.8.2


#### Configure network domains

	pmctl network add-domain dev <deviceName> domains <domainlist>

Example: 

	>pmctl network add-domain dev ens37 domains test1.com,test2.com,test3.com,test4.com


#### Configure network ntp

	pmctl network add-ntp dev <deviceName> ntp <ntplist>

Example:

	>pmctl network add-ntp dev ens37 ntp 198.162.1.15,test3.com


#### Configure network ipv6AcceptRA

	pmctl network set-ipv6-accept-ra <deviceName> <IPv6AcceptRA>

Example: 

	>pmctl network set-ipv6-accept-ra ens37 false


#### Configure link mode

	pmctl network set-link-mode dev <device> mode <unmanagedValue> arp <arpValue> mc <multicastValue> amc <allmulticastValue> pcs <PromiscuousValue> rfo <RequiredForOnline>

Example:

	>pmctl network set-link-mode dev ens37 arp 1 mc no amc true pcs yes rfo on


#### Configure link mtubytes

	pmctl network set-mtu <deviceName> <mtubytesValue>

Example:

	>pmctl network set-mtu ens37 2048



#### Configure link mac

	pmctl network set-mac <deviceName> <MACAddress>

Example:

	>pmctl network set-gmac ens37 00:a0:de:63:7a:e6


#### Configure link group

	pmctl network set-group <deviceName> <groupValue>

Example:

	>pmctl network set-group ens37 2147483647


#### Configure link requiredFamilyForOnline

	pmctl network set-rf-online <deviceName> <familyValue>

Example:

	>pmctl network set-rf-online ens37 ipv4



#### Configure link activationPolicy

	pmctl network set-active-policy <deviceName> <policyValue>

Example: 

	>pmctl network set-active-policy ens37 always-up


#### Configure network routingPolicyRule

	pmctl network add-rule dev <deviceName> tos <TypeOfService> from <Address> to <Address> fwmark <FirewallMark> table <Table> prio <Priority> iif <IncomingInterface> oif <OutgoingInterface> srcport <SourcePort> destport <DestinationPort> ipproto <IPProtocol> invertrule <InvertRule> family <Family> usr <User> suppressprefixlen <SuppressPrefixLength> suppressifgrp <SuppressInterfaceGroup> type <Type>

Example: 

	>pmctl network add-rule dev ens37 tos 12 from 192.168.1.10/24 to 192.168.2.20/24 fwmark 7/255 table 8 prio 3 iif ens37 oif ens37 srcport 8000-8080 destport 9876 ipproto 17 invertrule yes family ipv4 usr 1001 suppressprefixlen 128 suppressifgrp 2098 type prohibit


#### Remove network routingPolicyRule

	pmctl network delete-rule dev <deviceName> tos <TypeOfService> from <Address> to <Address> fwmark <FirewallMark> table <Table> prio <Priority> iif <IncomingInterface> oif <OutgoingInterface> srcport <SourcePort> destport <DestinationPort> ipproto <IPProtocol> invertrule <InvertRule> family <Family> usr <User> suppressprefixlen <SuppressPrefixLength> suppressifgrp <SuppressInterfaceGroup> type <Type>

Example:

	>pmctl network delete-rule dev ens37 tos 12 from 192.168.1.10/24 to 192.168.2.20/24 fwmark 7/255 table 8 prio 3 iif ens37 oif ens37 srcport 8000-8080 destport 9876 ipproto 17 invertrule yes family ipv4 usr 1001 suppressprefixlen 128 suppressifgrp 2098 type prohibit


#### Configure network DHCPv4 id's

	pmctl network set-dhcpv4-id dev <deviceName> clientid <ClientIdentifier> vendorclassid <VendorClassIdentifier> iaid <IAID>

Example: 

	>pmctl network set-dhcpv4-id dev ens37 clientid duid vendorclassid 101 iaid 201



#### Configure network DHCPv4 duid

	pmctl network set-dhcpv4-duid dev <deviceName> duidtype <DUIDType> duidrawdata <DUIDRawData>

Example: 

	>pmctl network set-dhcpv4-duid dev ens37 duidtype vendor duidrawdata af:03:ff:87


#### Configure network DHCPv4 use options

	pmctl network set-dhcpv4-use dev <deviceName> usedns <UseDNS> usentp <UseNTP> usesip <UseSIP> usemtu <UseMTU> usehostname <UseHostname> usedomains <UseDomains> useroutes <UseRoutes> usegateway <UseGateway> usetimezone <UseTimezone>

Example: 

	>pmctl network set-dhcpv4-use dev ens37 usedns false usentp false usesip false usemtu yes usehostname true usedomains yes useroutes no usegateway yes usetimezone no


#### Configure network DHCPv6

	pmctl network set-dhcpv6 dev <deviceName> mudurl <MUDURL> userclass <UserClass> vendorclass <VendorClass> prefixhint <IPV6ADDRESS> withoutra <WithoutRA>

Example:

	>pmctl network set-dhcpv6 dev ens37 mudurl https://example.com/devB userclass usrcls1,usrcls2 vendorclass vdrcls1 prefixhint 2001:db1:fff::/64 withoutra solicit


#### Configure network DHCPv6 id's

	pmctl network set-dhcpv6-id dev <deviceName> iaid <IAID> duidtype <DUIDType> duidrawdata <DUIDRawData>

Example: 

	>pmctl network set-dhcpv6-id dev ens37 iaid 201 duidtype vendor duidrawdata af:03:ff:87


#### Configure network DHCPv6 Use

	pmctl network set-dhcpv6-use dev <deviceName> useaddr <UseAddress> useprefix <UsePrefix> usedns <UseDNS> usentp <UseNTP> usehostname <UseHostname> usedomains <UseDomains>

Example: 

	>pmctl network set-dhcpv6-use dev ens37 useaddr yes useprefix no usedns false usentp false usehostname true usedomains yes


#### Configure network DHCPv6 Options 

	pmctl network set-dhcpv6-option dev <deviceName> reqopt <RequestOptions> sendopt <SendOption> sendvendoropt <SendVendorOption>

Example: 

	>pmctl network set-dhcpv6-option dev ens37 reqopt 10,198,34 sendopt 34563 sendvendoropt 1987653,65,ipv6address,af:03:ff:87


#### Configure network DHCPServer

	pmctl network add-dhcpv4-server dev <Devicename> pool-offset <poolOffset> pool-size <PoolSize> default-lease-time-sec <DefaultLeaseTimeSec> max-lease-time-sec <MaxLeaseTimeSec> dns <DNS> emit-dns <EmitDNS> emit-ntp <EmitNTP> emit-router <EmitRouter>

Example: 

	>pmctl network add-dhcpv4-server dev ens37 pool-offset 100 pool-size 200 default-lease-time-sec 10 max-lease-time-sec 30 dns 192.168.1.2,192.168.10.10,192.168.20.30 emit-dns yes emit-ntp no emit-router yes


#### Remove network DHCPServer

	pmctl network remove-dhcpv4-server <Devicename>

Example: 

	>pmctl network remove-dhcpv4-server ens37


#### Configure network IPv6SendRA

	pmctl network add-ipv6ra dev <deviceName> rt-pref <RouterPreference> emit-dns <EmitDNS> dns <DNS> emit-domains <EmitDomains> domains <Domains> dns-lifetime-sec <DNSLifetimeSec> prefix <Prefix> pref-lifetime-sec <PreferredLifetimeSec> valid-lifetime-sec <ValidLifetimeSec> assign <Assign> route <Route> lifetime-sec <LifetimeSec>

Example:

	>pmctl network add-ipv6ra dev ens37 rt-pref medium emit-dns yes dns 2002:da8:1::1,2002:da8:2::1 emit-domains yes domains test1.com,test2.com dns-lifetime-sec 100 prefix 2002:da8:1::/64 pref-lifetime-sec 100 valid-lifetime-sec 200 assign yes route 2001:db1:fff::/64 lifetime-sec 1000


#### Remove network IPv6SendRA

	pmctl network remove-ipv6ra <Devicename>

Example: 

	>pmctl network remove-ipv6ra ens37




### Configure Network Device using `pmctl`

You can configure the network devices using `pmctl` command. Use the following commands to configure network devices.


#### Configure VLan

	pmctl network create-vlan <vlanName> dev <device> id <vlanId>

Example:

	>pmctl network create-vlan vlan1 dev ens37 id 101


#### Configure Bond

	pmctl network create-bond <bondName> dev <device> mode <modeType> thp <TransmitHashPolicyType> ltr <LACPTransmitRateType> mms <MIIMonitorSecTime>

Example: 

	>pmctl network create-bond bond1 dev ens37,ens38 mode 802.3ad thp layer2+3 ltr slow mms 1s


#### Configure Bond with default

Example:  
	
	>pmctl network create-bond bond1 dev ens37,ens38


#### Configure Bridge with default

	pmctl network create-bridge <bridgeName> dev <device list>

Example:

	>pmctl network create-bridge br0 dev ens37,ens38


#### Configure MacVLan

	pmctl network create-macvlan <macvlanName> dev <device> mode <modeName>

Example:

	>pmctl network create-macvlan macvlan1 dev ens37 mode private 


#### Configure IpVLan

	pmctl network create-ipvlan <ipvlanName> dev <device> mode <modeName> flags <flagsName>

Example:

	>pmctl network create-ipvlan ipvlan1 dev ens37 mode l2 flags vepa


#### Configure IpVLan with default

Example:

	>pmctl network create-ipvlan ipvlan1 dev ens38


#### Configure VxLan

	pmctl network create-vxlan <vxlanName> dev <device> remote <RemoteAddress> local <LocalAddress> group <GroupAddress> destport <DestinationPort> independent <IndependentFlag>


Example:

	>pmctl network create-vxlan vxlan1 dev ens37 vni 16777215 remote 192.168.1.3 local 192.168.1.2 group 192.168.0.0 destport 4789 independent no 


#### Configure WireGuard

	pmctl network create-wg <wireguardName> dev <device> skey <privateKey> pkey<publicKey> endpoint <address:Port> port <listenport> ips <allowedIPs>

Example:

	>pmctl network create-wg wg1 dev ens37 skey wCmc/74PQpRoxTgqGircVFtdArZFUFIiOoyQY8kVgmI= pkey dSanSzExlryduCwNnAFt+rzpI5fKeHuJx1xx2zxEG2Q= endpoint 10.217.69.88:51820 port 51822 ips fd31:bf08:57cb::/48,192.168.26.0/24


#### Configure WireGuard with default

Example: 

	>pmctl network create-wg wg1 dev ens37 skey wCmc/74PQpRoxTgqGircVFtdArZFUFIiOoyQY8kVgmI= pkey dSanSzExlryduCwNnAFt+rzpI5fKeHuJx1xx2zxEG2Q= endpoint 10.217.69.88:51820



### Remove Network Device Using `pmctl`

To remove a network device, use the following command in `pmctl`:

	pmctl network remove-netdev <kindDeviceName> kind <kindType>


Example:

	>pmctl network remove-netdev ipvlan1 dev ens37 kind ipvlan



### Configure link using pmctl


Use the following commands to configure links using the `pmctl` command.



#### Configure Link MACAddress

	pmctl link set-mac dev <deviceName> macpolicy <MACAddressPolicy> macaddr <MACAddress>

Example:

	>pmctl link set-mac dev eth0 macpolicy none macaddr 00:a0:de:63:7a:e6

#### Configure Link Name

	pmctl link set-name dev <deviceName> namepolicy <NamePolicy> name <Name>

Example:

	>pmctl link set-name dev ens37 namepolicy mac,kernel,database,onboard,keep,slot,path

#### Configure Link AlternativeNames

	pmctl link set-name dev <deviceName> altnamespolicy <AlternativeNamesPolicy> altname <AlternativeName>

Example:

	>pmctl link set-alt-name dev ens37 altnamespolicy mac,database,onboard,slot,path

#### Configure Link ChecksumOffload

	pmctl link set-csum-offload dev <deviceName> rco <ReceiveCheksumOffload> tco <TransmitChecksumOffload>

Example:

	>pmctl link set-csum-offload dev ens37 rxco true txco true

#### Configure Link TCPSegmentationOffload

	pmctl link set-tcp-offload dev <deviceName> tcpso <TCPSegmentationOffload> tcp6so <TCP6SegmentationOffload>

Example:

	>pmctl link set-tcp-offload dev ens37 tcpso true tcp6so true

#### Configure Link GenericOffload

	pmctl link set-generic-offload dev <deviceName> gso <GenericSegmentationOffload> gro <GenericReceiveOffload> grohw <GenericReceiveOffloadHardware> gsomaxbytes <GenericSegmentOffloadMaxBytes> gsomaxseg <GenericSegementOffloadMaxSegments>

Example: 

	>pmctl link set-generic-offload dev ens37 gso true gro true grohw false gsomaxbytes 65536 gsomaxseg 65535

#### Configure Link VLANTAG

	pmctl link set-vlan-tags dev <deviceName> rxvlanctaghwacl <ReceiveVLANCTAGHardwareAcceleration> txvlanctaghwacl <TransmitVLANCTAGHardwareAcceleration> rxvlanctagfilter <ReceiveVLANCTAGFilter> txvlanstaghwacl <TransmitVLANSTAGHardwareAcceleration>

Example:

	>pmctl link set-vlan-tags dev ens37 rxvlanctaghwacl true txvlanctaghwacl false rxvlanctagfilter true txvlanstaghwacl true

# Configure Link Channels

	pmctl link set-channel dev <deviceName> rxch <RxChannels> txch <TxChannels> oth <OtherChannels> coch <CombinedChannels>

Example:

	>pmctl link set-channel dev ens37 rxch 1024 txch 2045 och 45678 coch 32456

#### Configure Link Buffers

	pmctl link set-buffer dev <deviceName> rxbufsz <RxBufferSize> rxmbufsz <RxMiniBufferSize> rxjbufsz <RxJumboBufferSize> txbufsz <TxBufferSize>

Example:

	>pmctl link set-buffer dev ens37 rxbufsz 100009 rxmbufsz 1998 rxjbufsz 10999888 txbufsz 83724

#### Configure Link Queues

	pmctl link set-queue dev <deviceName> rxq <ReceiveQueues> txq <TransmitQueues> txqlen <TransmitQueueLength>

Example:

	>pmctl link set-queue dev ens37 rxq 4096 txq 4096 txqlen 4294967294

#### Configure Link FlowControls

	pmctl link set-flow-ctrl dev <deviceName> rxfctrl <RxFlowControl> txfctrl <TxFlowControl> anfctrl <AutoNegotiationFlowControl>

Example:

	>pmctl link set-flow-ctrl dev ens37 rxfctrl true txfctrl true anfctrl true

#### Configure Link UseAdaptiveCoalesce

	pmctl link set-adpt-coalesce dev <deviceName> uarxc <UseAdaptiveRxCoalesce> uatxc <UseAdaptiveTxCoalesce>

Example:

	>pmctl link set-adpt-coalesce dev ens37 uarxc true uatxc true

#### Configure Link ReceiveCoalesce

	pmctl link set-rx-coalesce dev <deviceName> rxcs <RxCoalesceSec> rxcsirq <RxCoalesceIrqSec> rxcslow <RxCoalesceLowSec> rxcshigh <RxCoalesceHighSec>

Example: 

	>pmctl link set-rx-coalesce dev ens37 rxcs 23 rxcsirq 56 rxcslow 5 rxcshigh 76788

#### Configure Link TransmitCoalesce

	pmctl link set-tx-coalesce dev <deviceName> txcs <TxCoalesceSec> txcsirq <TxCoalesceIrqSec> txcslow <TxCoalesceLowSec> txcshigh <TxCoalesceHighSec>

Example:

	>pmctl link set-tx-coalesce dev ens37 txcs 23 txcsirq 56 txcslow 5 txcshigh 76788

#### Configure Link ReceiveMaxCoalescedFrames

	pmctl link set-rx-coald-frames dev <deviceName> rxcmf <RxMaxCoalescedFrames> rxcmfirq <RxMaxCoalescedIrqFrames> rxcmflow <RxMaxCoalescedLowFrames> rxcmfhigh <RxMaxCoalescedHighFrames>

Example:

	>pmctl link set-rx-coald-frames dev ens37 rxmcf 23 rxmcfirq 56 rxmcflow 5 rxmcfhigh 76788

#### Configure Link TransmitMaxCoalescedFrames

	pmctl link set-tx-coald-frames dev <deviceName> txcmf <TxMaxCoalescedFrames> txcmfirq <TxMaxCoalescedIrqFrames> txcmflow <TxMaxCoalescedLowFrames> txcmfhigh <TxMaxCoalescedHighFrames>

Example:

	>pmctl link set-tx-coald-frames dev ens37 txmcf 23 txmcfirq 56 txmcflow 5 txmcfhigh 76788

#### Configure Link CoalescePacketRate

	pmctl link set-coalesce-pkt dev <deviceName> cprlow <CoalescePacketRateLow> cprhigh <CoalescePacketRateHigh> cprsis <CoalescePacketRateSampleIntervalSec>

Example:

	>pmctl link set-coalesce-pkt dev ens37 cprlow 1000 cprhigh 32456 cprsis 102

#### Configure Other Links 

You can configure links for Alias, Description, port, duplex, and so on. 


	pmctl link set-link dev ens37 alias <Alias> desc <Description> mtub <MTUBytes> bits <BitsPerSecond> duplex <Duplex> auton <AutoNegotiation> wol <WakeOnLan> wolpassd <WakeOnLanPassword> port <Port> advertise <Advertise> lrxo <LargeReceiveOffload> ntf <NTupleFilter> ssbcs <StatisticsBlockCoalesceSec>

Example:

	>pmctl link set-link dev ens37 alias ifalias desc configdevice mtub 10M bits 5G duplex full auton no wol phy,unicast,broadcast,multicast,arp,magic,secureon wolpassd cb:a9:87:65:43:21  port mii advertise 10baset-half,10baset-full,20000basemld2-full lrxo true ntf true ssbcs 1024


### Ethtool status ###

To fetch the Ethtool Status, use the following command:

```bash

\#Get Ethtool all status 

	pmctl status ethtool <LINK>

Example: 

	>pmctl status ethtool ens37

\#Get Ethtool status based on action

	pmctl status ethtool <LINK> <ACTION>

Example:

	>pmctl status ethtool ens37 bus







