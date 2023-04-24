---
title: Configuring a Network Using Network Configuration Manager
weight: 19
---

You can use network-configuration-manager to configure a network in Photon OS. The YAML-based configuration system in network-config-manager makes the network configuration easy and simple.

The following sections in the document demonstrate the configuration of a network in Photon OS using network-config-manager.

You can find the YAML network configuration files at the following location:

	/etc/network-config-manager/yaml/ 

When you install network-configuration-manager, it generates the network-config-manager configuration file for systemd-networkd named `99-dhcp.yml.example`.


Perform the following steps to configure static or dynamic IP addressing in Photon OS:

1. To find the name of the active network interfaces that you want to configure, execute the following command:

```
❯ ip a   
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:0c:29:5f:d1:39 brd ff:ff:ff:ff:ff:ff
    altname enp2s1
    inet 192.168.1.4/24 metric 1024 brd 192.168.1.255 scope global dynamic ens33
       valid_lft 82465sec preferred_lft 82465sec
    inet6 fe80::20c:29ff:fe5f:d139/64 scope link 
       valid_lft forever preferred_lft forever
```   

Note the name of the interface that you want to configure using network-config-manager.


2. To find the network-configuration-manager default configuration file, execute the following command:

	```
	❯ ls /etc/network-config-manager/yaml
	```   

3. To view the content of the network-config-manager network configuration file, execute the following command:

	```
	❯ cat /etc/network-config-manager/yaml/*.yaml
	```   

4. Open the configuration file in an editor.   
	For example, if you use vim editor, execute the following command to open the configuration file in an editor:
	
	```
	❯ sudo vim /etc/network-config-manager/yaml/99-dhcp.yaml
	```   

5. Use the following syntax to update the configuration file as per your networking needs:

	```
	network:
    Version: 2
    Renderer: networkd
    ethernets:
       device:
          dhcp4: yes/no
          nameservers:
             addresses: [NAMESERVER, NAMESERVER, ...]
          addresses: [IPADDRESS/PREFIX]
           routes:
          - to: DESTINATION
            via: GATEWAY
	```     

	Note that for static IP addressing, add the IP address, Gateway, and DNS details. For dynamic IP addressing, you need not add these details as it  is fetched from the DHCP server.

	The following table describes the properties used in the syntax to update the configuration file.

	|Properties		| Description|
	|---------------|------------|
	|device: 		|Name of the interface.
	|dhcp4: 		|yes or no depending upon dynamic or static IP addressing
	|addresses: 	|IP address of the device in prefix notation.
	|routes: to: destination via: |gateway IP address to connect to an outside network
	|nameservers:	| Address of DNS name servers


 
    
**Note**: It is recommended that you use spaces for indentation instead of tabs in the YAML configuration file. If you use a tab instead of spaces for indentation, you might encounter errors.


## Configuring static IP address in Photon OS

To manually configure an IP address, use the previously mentioned file syntax in this topic, and add the IP address, Gateway, and DNS server details.

The following is a sample configuration for the static IP addressing:

```
network:
    ethernets:
        eth0:
            dhcp4: false
            addresses: [192.168.1.202/24]
            nameservers:
              addresses: [8.8.8.8,8.8.4.4,192.168.1.1]
            routes:
            - to: 172.16.0.0/24
              via: 192.168.1.100
```   


## Configure Dynamic IP address in Photon OS

To get the IP address from the DHCP server, use the previously mentioned file syntax in this topic. You need not add the IP address, Gateway, and DNS server details here.

The following is a sample configuration for the dynamic IP addressing:

```
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true
```    

After configuring the IP address, you need to apply the new configuration. Execute the following command as sudo to apply the configuration:

	$ sudo nmctl apply


To verify that the configurations are successfully applied, execute the following command and verify the IP address:

```
❯ nmctl status eth0
                       Flags: UP BROADCAST RUNNING NOARP LOWERUP 
                        Kind: dummy
                        Type: ether
                      Driver: dummy
                   Link File: /usr/lib/systemd/network/99-default.link
                Network File: /etc/systemd/network/10-eth0.network
                       State: routable (configured) 
               Address State: routable
          IPv4 Address State: routable
          IPv6 Address State: degraded
                Online State: online
         Required for Online: yes
           Activation Policy: up
                  HW Address: 56:d3:b9:4f:03:38 ((null))
                         MTU: 1500 (min: 0 max: 0) 
                       QDISC: noqueue 
              Queues (Tx/Rx): 1/1 
             Tx Queue Length: 1000 
IPv6 Address Generation Mode: eui64 
                GSO Max Size: 65536 GSO Max Segments: 65535 
                     Address: fe80::54d3:b9ff:fe4f:338/64
                              192.168.1.202/24
                     Gateway: 192.168.1.100
                         DNS: 8.8.4.4 192.168.1.1 8.8.8.8
           DHCP6 Client DUID: DUID-EN/Vendor:0000ab11d258482fc7eee6510000
```

To see the routes, execute the following command:

```
❯ ip r show dev eth0
172.16.0.0/24 via 192.168.1.100 proto static 
```   
