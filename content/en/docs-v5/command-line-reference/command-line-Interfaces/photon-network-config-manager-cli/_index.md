---
title:  Photon Network Config Manager Command-line Interface (nmctl)
weight: 3
---


You can use `network-config-manager` (`nmctl`) to configure and introspect the state of the network links as seen by `systemd-networkd`. `nmctl` can be used to query and configure devices for Addresses, Routes, Gateways, DNS, NTP, Domain, and hostname. You can also use `nmctl` to create virtual NetDevs (VLAN, VXLAN, Bridge, Bond, and so on). You can configure various configuration of links such as WakeOnLanPassword, Port, BitsPerSecond, Duplex and Advertise, and so on. `nmctl` uses `sd-bus`, `sd-device` APIs to interact with `systemd`, `systemd-networkd`, `systemd-resolved`, `systemd-hostnamed`, and `systemd-timesyncd` via dbus. `nmctl` uses `networkd` verbs to explain output. `nmctl` can generate configurations that persist between reboots.



The following example shows the system status:

```
❯ nmctl
         System Name: zeus
              Kernel: Linux (5.10.152-3.ph4)
     systemd version: v252-1
        Architecture: x86-64
      Virtualization: vmware
    Operating System: VMware Photon OS/Linux
          Machine ID: aa6e4cb92bee4c1aa8b304eafe28166c
        System State: routable
        Online State: partial
           Addresses: fe80::982e:b0ff:fe07:cc12/64   on device cni-podman0
                      fe80::20c:29ff:fe64:cb18/64    on device eth0
                      172.16.130.145/24              on device eth1
                      172.16.130.144/24              on device eth0
                      127.0.0.1/8                    on device lo
                      fe80::20c:29ff:fe5f:d143/64    on device eth1
                      ::1/128                        on device lo
                      fe80::c027:acff:fe19:d741/64   on device vethe8dc6ac9
                      10.88.0.1/16                   on device cni-podman0
             Gateway: 172.16.130.2	                 on device eth1
                      172.16.130.2	                 on device eth0
                 DNS: 172.16.130.2 172.16.130.1 172.16.130.126
                 NTP: 10.128.152.81 10.166.1.120 10.188.26.119 10.84.55.42`

```

The following example shows the network status:

```
❯ nmctl status eth0
           Alternative names: eno1 enp11s0 ens192
                       Flags: UP BROADCAST RUNNING MULTICAST LOWERUP
                        Type: ether
                        Path: pci-0000:0b:00.0
                      Driver: vmxnet3
                      Vendor: VMware
                       Model: VMXNET3 Ethernet Controller
                   Link File: /usr/lib/systemd/network/99-default.link
                Network File: /etc/systemd/network/99-dhcp-en.network
                       State: routable (configured)
               Address State: routable
          IPv4 Address State: routable
          IPv6 Address State: degraded
                Online State: online
         Required for Online: yes
           Activation Policy: up
                  HW Address: 00:0c:29:64:cb:18 (VMware, Inc.)
                         MTU: 1500 (min: 60 max: 9000)
                      Duplex: full
                       Speed: 10000
                       QDISC: mq
              Queues (Tx/Rx): 2/2
             Tx Queue Length: 1000
IPv6 Address Generation Mode: eui64
                GSO Max Size: 65536 GSO Max Segments: 65535
                     Address: 10.197.103.228/23 (DHCPv4 via 10.142.7.86) lease time: 7200 seconds T1: 3600 seconds T2: 6300 seconds
                              fe80::20c:29ff:fe64:cb18/64
                     Gateway: 172.16.130.2
                         DNS: 172.16.130.3 172.16.130.4 172.16.130.5
                         NTP: 172.16.130.6 172.16.130.7 172.16.130.8 172.16.130.9
           DHCP6 Client DUID: DUID-EN/Vendor:0000ab119a69db91b911f3180000

```

To add DNS, use the following command:


```
nmctl add-dns dev eth0 dns 192.168.1.45 192.168.1.46
```

To set mtu, use the following command:

```
nmctl set-mtu dev eth0 mtu 1400
```

To set mac, use the following command:

```
nmctl set-mac dev eth0 mac 00:0c:29:3a:bc:11
```

To set link options, use the following command:

```
nmctl set-link-option dev eth0 arp yes mc yes amc no pcs no
```

To add a static address, use the following command:

```
nmctl add-addr dev eth0 a 192.168.1.45/24
```

To add a default gateway, use the following command:

```
nmctl add-default-gw dev eth0 gw 192.168.1.1 onlink  yes
```


The following example shows how to create VLAN via `nmctl`
The following command creates `.netdev` and `.network` and assigns them to the underlying device. It sets all these file permissions to `systemd-network` automatically.

```
❯ nmctl create-vlan [VLAN name] dev [MASTER DEVICE] id [ID INTEGER] proto [PROTOCOL {802.1q|802.1ad}] Creates vlan netdev and network file

❯ sudo nmctl create-vlan vlan-95 dev eth0 id 19
```


The following example shows how to create VXLAN via `nmctl`:

```
❯ sudo nmctl create-vxlan vxlan-98 vni 32 local 192.168.1.2 remote 192.168.1.3 port 7777 independent yes
```


The following example shows how to create virtual routing and forwarding (VRF):

```
❯ sudo nmctl create-vrf test-vrf table 555                                                                                               
❯ ip -d link show test-vrf
4: test-vrf: <NOARP,MASTER,UP,LOWER_UP> mtu 65575 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 86:ad:9b:50:83:1f brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 1280 maxmtu 65575 
    vrf table 555 addrgenmode none numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535  
```

The following example shows how to remove a virtual netdev:

```
❯ sudo nmctl remove-netdev vlan-95                                                                                         
❯ ip -d link show vlan-95 
Device "vlan-95" does not exist.
```
***Note:*** `nmctl` not only removes the `.netdev` and `.network` files but also removes the virtual netdev.


