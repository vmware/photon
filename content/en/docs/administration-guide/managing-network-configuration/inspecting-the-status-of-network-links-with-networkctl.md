---
title:  Inspecting the Status of Network Links with 'networkctl'
weight: 11
---

You can inspect information about network connections by using the `networkctl` command. This can help you configure networking services and troubleshoot networking problems. 

You can progressively add options and arguments to the `networkctl` command to move from general information about network connections to specific information about a network connection. 

# networkctl Command Without Options

Run the `networkctl` command without options to default to the list command:  

```console
networkctl
IDX LINK             TYPE               OPERATIONAL SETUP
  1 lo               loopback           carrier     unmanaged
  2 eth0             ether              routable    configured
  3 docker0          ether              routable    unmanaged
  11 vethb0aa7a6      ether              degraded    unmanaged
  4 links listed.
```

## 'networkctl status' Command

Run `networkctl` with the status command to display the following information:  

```console
root@photon-rc [ ~ ]# > networkctl status
   State: routable
  Address: 10.197.103.56 on eno1
           172.17.0.1 on docker0
           fe80::20c:29ff:fe44:f92c on eno1
  Gateway: 10.197.103.253 (Cisco Systems, Inc) on eno1
      DNS: 10.142.7.1
           10.132.7.1
           10.166.17.90
      NTP: 10.128.152.81
           10.166.1.120
           10.188.26.119
           10.84.55.42

```

You can see that there are active network links with IP addresses for not only the Ethernet connection but also a Docker container.


### 'networkctl status' Command With Network Link Option


You can add a network link, such as the Ethernet connection, as the argument of the `status` command to show specific information about the link: 

```console
	root@photon-rc [ ~ ]# networkctl status ens33
	* 2: ens33
	         Link File: /usr/lib/systemd/network/99-default.link                                      
                  Network File: /usr/lib/systemd/network/10-eth.network                                       
                          Type: ether                                                                         
                         State: routable (configured)                               
             Alternative Names: enp2s1                                                                        
                          Path: pci-0000:02:01.0                                                              
                        Driver: e1000                                                                         
                        Vendor: Intel Corporation                                                             
                         Model: 82545EM Gigabit Ethernet Controller (Copper) (PRO/1000 MT Single Port Adapter)
                    HW Address: 00:0c:29:5f:d1:39 (VMware, Inc.)                                              
                           MTU: 1500 (min: 46, max: 16110)                                                    
                         QDisc: fq_codel                                                                      
  IPv6 Address Generation Mode: eui64                                                                         
          Queue Length (Tx/Rx): 1/1                                                                           
              Auto negotiation: yes                                                                           
                         Speed: 1Gbps                                                                         
                        Duplex: full                                                                          
                          Port: tp                                                                            
                       Address: 172.16.85.225 (DHCP4 via 172.16.85.254)                                       
                                fe80::20c:29ff:fe5f:d139                                                      
                       Gateway: 172.16.85.2 (VMware, Inc.)                                                    
                           DNS: 172.16.85.2                                                                   
               DHCP4 Client ID: IAID:0x2b9434c1/DUID                                                          
             DHCP6 Client DUID: DUID-EN/Vendor:0000ab11d258482fc7eee6510000                                   
Feb 26 10:19:44 fedora systemd-networkd[650]: ens33: Link UP
Feb 26 10:19:44 fedora systemd-networkd[650]: ens33: Gained carrier
Feb 26 10:19:45 fedora systemd-networkd[650]: ens33: DHCPv4 address 172.16.85.225/24 via 172.16.85.2
Feb 26 10:19:46 fedora systemd-networkd[650]: ens33: Gained IPv6LL
```

### 'networkctl status' Command With Docker Option

You can add a Docker container as the argument of the `status` command to show specific information about the container: 
	
```console
networkctl status docker0
	* 3: docker0
	       Link File: /usr/lib/systemd/network/99-default.link
	    Network File: n/a
	            Type: ether
	           State: routable (unmanaged)
	          Driver: bridge
	      HW Address: 02:42:f0:f7:bd:81
	             MTU: 1500
	         Address: 172.17.0.1
	                  fe80::42:f0ff:fef7:bd81
```

In the example above, the state of the Docker container is unmanaged because Docker handles managing the networking for the containers without using systemd-resolved or systemd-networkd. Docker manages the container connection by using its bridge drive.

For more information about `networkctl` commands and options, see [https://www.freedesktop.org/software/systemd/man/networkctl.html](https://www.freedesktop.org/software/systemd/man/networkctl.html).
