---
title:  Turning Off DHCP
weight: 6
---

By default, when Photon OS first starts, it creates a DHCP network configuration file or rule, which appears in `/etc/systemd/network`, the highest priority directory for network configuration files with the lowest priority filename:

```console
cat /etc/systemd/network/99-dhcp-en.network
[Match]
Name=e*

[Network]
DHCP=yes
```

To turn off DHCP for all Ethernet interfaces, change the value of `DHCP` from `yes` to `no`, save the changes, and then restart the `systemd-networkd` service: 

```console
	systemctl restart systemd-networkd
```

Or you can reload and reconfigure the settings:

```console
networkctl reload
networkctl reconfigure <interface_name>/<index_number>`
```

{{% alert title="Note:" %}} 
>The advantage of using reload and reconfigure is that the settings of other interfaces are not disturbed and only the settings of the specific interface are reloaded and reconfigured.{{% /alert %}}

If you create a configuration file with a higher priority filename (e.g. `10-static-en.network`), it is not necessary but still recommended to turn off DHCP.

You can also check the status of a specific interface:

```console
networkctl status <interface_name>/<index_number>
```

(`ens33 `is an example)

```console
    2: ens33
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