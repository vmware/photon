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

(`eth0 `is an example)

```console
❯ networkctl status eth0
● 2: eth0
                     Link File: /usr/lib/systemd/network/99-default.link
                  Network File: /etc/systemd/network/50-dhcp-en.network
                         State: routable (configured)
                  Online state: online
                          Type: ether
                          Path: pci-0000:0b:00.0
                        Driver: vmxnet3
                        Vendor: VMware
                         Model: VMXNET3 Ethernet Controller
             Alternative Names: eno1
                                enp11s0
                                ens192
              Hardware Address: 00:50:56:ba:43:98 (VMware, Inc.)
                           MTU: 1500 (min: 60, max: 9000)
                         QDisc: fq_codel
  IPv6 Address Generation Mode: eui64
      Number of Queues (Tx/Rx): 1/1
              Auto negotiation: no
                         Speed: 10Gbps
                        Duplex: full
                          Port: tp
                       Address: 192.168.1.8/24 (DHCPv4 via 192.168.1.1)
                                fe80::250:56ff:feba:4398
                       Gateway: 192.168.1.1
                           DNS: 192.168.1.1
                                192.168.1.2
                                192.168.1.3
                           NTP: 192.168.1.1
                                192.168.1.2
                                192.168.1.3
                                192.168.1.4
             Activation Policy: up
           Required For Online: yes
               DHCP4 Client ID: IAID:0xb6220feb/DUID

May 04 10:37:14 photon systemd-networkd[625]: eth0: found matching network '/etc/systemd/network/50-dhcp-en.network', based on potentially unpredictable interface name.
May 04 10:37:14 photon systemd-networkd[625]: eth0: Configuring with /etc/systemd/network/50-dhcp-en.network.
May 04 10:37:14 photon systemd-networkd[625]: eth0: Link UP
May 04 10:37:14 photon systemd-networkd[625]: eth0: Gained carrier
May 04 10:37:14 photon systemd-networkd[625]: eth0: found matching network '/etc/systemd/network/50-dhcp-en.network', based on potentially unpredictable interface name.
```    
