---
title: Configure SR-IOV using Network Configuration Manager
weight: 2
---

SR-IOV technology enables multiple virtual machines to share a single PCIe device. SR-IOV allows a single PCIe device to appear as multiple and separate PCIe interfaces. This enables direct connection of multiple virtual machines to the PCIe devices. PCI-SIG (Peripheral Component Interconnect Special Interest Group) defines the standard interface and requirements in the SR-IOV specification to promote interoperability of the SR-IOV enabled devices.


SR-IOV introduces the concept of Physical Functions (PFs) and Virtual Functions (VFs). PFs refer to full-featured PCIe functions. VFs refer to the lightweight functions that lack certain configuration resources.


 You can configure SR-IOV on Photon OS using the Network Configuration Manager (`nmctl`). Note that the `systemd-networkd`  also supports SR-IOV.

You can use kernel module `netdevsim` to configure and test it as shown in the following example:

```
➜  ~  modprobe netdevsim                                                                                                                    
➜  ~  lsmod | grep netdevsim 
netdevsim             102400  0
psample                20480  1 netdevsim

➜  ~  echo "10 1" > /sys/bus/netdevsim/new_device 

➜  ~ sudo echo "99 1" > /sys/bus/netdevsim/new_device

➜  ~ ip -d link show eni99np1
287: eni99np1: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/ether ca:28:ff:4e:73:2a brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 68 maxmtu 65535 addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 65536 tso_max_segs 65535 gro_max_size 65536 portname p1 switchid 82ae398327c5db81a27dc2756c43f00315f442de1779fcfbfc582bbb3e62cb parentbus netdevsim parentdev netdevsim99 

➜  ~ echo "3" > /sys/bus/netdevsim/devices/netdevsim99/sriov_numvfs

➜  ~ ip -d link show eni99np1                                      
287: eni99np1: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/ether ca:28:ff:4e:73:2a brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 68 maxmtu 65535 addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 65536 tso_max_segs 65535 gro_max_size 65536 portname p1 switchid 82ae398327c5db81a27dc2756c43f00315f442de1779fcfbfc582bbb3e62cb parentbus netdevsim parentdev netdevsim99 
    vf 0     link/ether 00:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff, spoof checking off, link-state auto, trust off, query_rss off
    vf 1     link/ether 00:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff, spoof checking off, link-state auto, trust off, query_rss off
    vf 2     link/ether 00:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff, spoof checking off, link-state auto, trust off, query_rss off
```


To configure SR-IOV using `nmctl`, use the command as shown in the following example:

```
➜  ~ nmctl add-sr-iov dev eni99np1 vf 0 vlanid 5 qos 1 macspoofck yes qrss True trust yes linkstate yes macaddr 00:11:22:33:44:55

➜  ~ ip -d link show eni99np1                                                                                                
287: eni99np1: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/ether ca:28:ff:4e:73:2a brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 68 maxmtu 65535 addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 65536 tso_max_segs 65535 gro_max_size 65536 portname p1 switchid 82ae398327c5db81a27dc2756c43f00315f442de1779fcfbfc582bbb3e62cb parentbus netdevsim parentdev netdevsim99 
    vf 0     link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff, vlan 5, qos 1, spoof checking on, link-state enable, trust on, query_rss on


➜  ~ sudo cat /etc/systemd/network/10-eni99np1.network
[Match]
Name=eni99np1


[SR-IOV]
VirtualFunction=0
VLANId=5
QualityOfService=1
MACSpoofCheck=yes
QueryReceiveSideScaling=yes
Trust=yes
LinkState=yes
MACAddress=00:11:22:33:44:55
```


The `nmctl` generates the SR-IOV configuration in the `systemd-networkd` format. Since `nmctl` reloads the configuration, `systemd-networkd` also configures the VF.

To configure the other VFs, use the command as shown in the following example:

```
➜  ~ nmctl add-sr-iov dev eni99np1 vf 1 vlanid 6 qos 2 macspoofck yes qrss True trust yes linkstate yes macaddr 00:11:22:33:44:56
➜  ~ nmctl add-sr-iov dev eni99np1 vf 1 vlanid 6 qos 2 macspoofck yes qrss True trust yes linkstate yes macaddr 00:11:22:33:44:5

➜  ~ ip -d link show eni99np1                                                                                                
287: eni99np1: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/ether ca:28:ff:4e:73:2a brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 68 maxmtu 65535 addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 65536 tso_max_segs 65535 gro_max_size 65536 portname p1 switchid 82ae398327c5db81a27dc2756c43f00315f442de1779fcfbfc582bbb3e62cb parentbus netdevsim parentdev netdevsim99 
    vf 0     link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff, vlan 5, qos 1, spoof checking on, link-state enable, trust on, query_rss on
    vf 1     link/ether 00:11:22:33:44:56 brd ff:ff:ff:ff:ff:ff, vlan 6, qos 2, spoof checking on, link-state enable, trust on, query_rss on
    vf 2     link/ether 00:11:22:33:44:57 brd ff:ff:ff:ff:ff:ff, vlan 7, qos 3, spoof checking on, link-state enable, trust on, query_rss on
```

`nmctl` generates the `.network`:

```
➜  ~ cat /etc/systemd/network/10-eni99np1.network
[Match]
Name=eni99np1


[SR-IOV]
VirtualFunction=0
VLANId=5
QualityOfService=1
MACSpoofCheck=yes
QueryReceiveSideScaling=yes
Trust=yes
LinkState=yes
MACAddress=00:11:22:33:44:55


[SR-IOV]
VirtualFunction=1
VLANId=6
QualityOfService=2
MACSpoofCheck=yes
QueryReceiveSideScaling=yes
Trust=yes
LinkState=yes
MACAddress=00:11:22:33:44:56


[SR-IOV]
VirtualFunction=2
VLANId=7
QualityOfService=3
MACSpoofCheck=yes
QueryReceiveSideScaling=yes
Trust=yes
LinkState=yes
MACAddress=00:11:22:33:44:57
```