---
title:  Using the Network Configuration Manager
weight: 2
---

The network-config-manager `nmctl` allows to configure and introspect the state of the network links as seen by s`ystemd-networkd`. `nmctl` can be used to query and configure links for Address, Routes, Gateways and also hostname, DNS, NTP or Domain. `nmctl` uses `sd-bus`, libudev APIs to interact with `systemd`, `systemd-networkd`, `systemd-resolved`, `systemd-hostnamed`, and `systemd-timesyncd` via dbus. `nmctl` uses networkd verbs to explain output. `nmctl` can generate configurations for required network links from YAML description. It also understands kernel command line specified in dracut network configuration format and can generate `systemd-networkd` configuration while the system boots and will persist between reboots.

Note: See `systemd.network` for more information.

`nmctl` is used to configure:

- Static IPv4 and IPv6 Address, Routes, Gateway


- DHCP type (IPv4/IPv6), DHCP4 Client Identifier, UseMTU/UseDNS/UseDomains/UseNTP/UseRoutes.
LLDP, Link Local Addressing, IPv4LLRoute, LLMNR


- DNS, Domains and NTP


- Link MAC, MTU


- Create netdevs, vlan, vxlan, bridge, bond, veth, macvlan/macvtap, ipvlap/ipvtap, veth, tunnels(ipip, sit, gre, sit, vti), wireguard


- Hostname


- Add delete and view nftables table, chains and rules.

You can use `nmctl` to generate network configurations from the following:

- YAML file: `nmctl` can generate configurations for required network links from YAML description. Configuration written to disk under `/etc/systemd/network` will persist between reboots. When `netmgr-yaml-generator.service` is enabled it reads YAML files from `/etc/network-config-manager/yaml` and generates `systemd-networkd` configuration files.

`nmctl` uses similar format as defined by different YAML format.

`nmctl` can generate WPA Supplicant configuration from YAML file. When a YAML file with wifi configuration is found, it generates a configuration file found in `/etc/network-config-manager/wpa_supplicant_photon_os.conf` which is understood by `wpa_supplicant`.

- Dracut kernel command line network configuration: nmctl understands kernel command line specified in dracut's network configuration format and can generate systemd-networkd's configuration while the system boots and will persist between reboots.


Network
       ip={dhcp|on|any|dhcp6|auto6}
           dhcp|on|any: get ip from dhcp server from all links. If root=dhcp, loop
           sequentially through all links (eth0, eth1, ...) and use the first with a valid
           DHCP root-path.

           auto6: IPv6 autoconfiguration

           dhcp6: IPv6 DHCP

       ip=<link>:{dhcp|on|any|dhcp6|auto6}
           dhcp|on|any|dhcp6: get ip from dhcp server on a specific link

           auto6: do IPv6 autoconfiguration

           This parameter can be specified multiple times.

       ip=<client-IP>:[ <server-id>]:<gateway-IP>:<netmask>:<client_hostname>:<link>:{none|off}
           explicit network configuration.

       ifname=<link>:<MAC>
           Assign network device name <link> (ie eth0) to the NIC with MAC <MAC>. Note
           letters in the MAC-address must be lowercase!  Note: If you use this option you must
           specify an ifname= argument for all links used in ip= or fcoe= arguments.  This
           parameter can be specified multiple times.

       nameserver=<IP>[nameserver=<IP> ...]
           specify nameserver(s) to use

      cat /proc/cmdline
       BOOT_IMAGE=/boot/vmlinuz-4.19.52-2.ph3-esx root=PARTUUID=ebf01b6d-7e9c-4345-93f4-122f44eb2726
       init=/lib/systemd/systemd rcupdate.rcu_expedited=1 rw systemd.show_status=0 quiet noreplace-smp
       cpu_init_udelay=0 net.ifnames=0 plymouth.enable=0 systemd.legacy_systemd_cgroup_controller=yes
       ip=dhcp


`network-config-manager-generator.service` is a oneshot type systemd service unit which runs while the system boots. It parses the kernel command line and generates networkd config in `/etc/systemd/network`.

    systemctl enable network-config-manager-generator.service

It creates symlink `/etc/systemd/system/network.target.wants/network-config-manager-generator.service → /usr/lib/systemd/system/network-config-manager-generator.service`.



For more information, see:

- **CLI** - see the ``-net`` commands in the [Photon Management Daemon Command-line Interface (pmd-cli)](../../../command-line-reference/commnad-line-interfaces/photon-management-daemon-cli/)
- **C APIs** - [Network Configuration Manager - C API](../netmgr.c/)
- **Python APIs** - [Network Configuration Manager - Python API](../netmgr.python/)