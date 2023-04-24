---
title:  Configuring WireGuard using Network Configuration Manager
weight: 1
---

WireGuard is a lightweight, simple, fast, and secure VPN that is built into Linux kernel 5.6 and above. This topic provides sample WireGuard configurations for `systemd-networkd` using `network-config-manager` on Photon OS, a Linux-based operating system.

To generate the required configuration, you need to install WireGuard tools. You can download the WireGuard tools or install the WireGuard tools using `tdnf`.

To install the WireGuard tools using `tdnf`, run the following command:

```
❯ sudo tdnf install wireguard-tools -y
```

To configure WireGuard VPN, you need to create a pair of keys on both the sites between which you want to establish the VPN connection. Each site needs the public key of the other site.	To create the pair of keys, use the following command:

```
❯ wg genkey | tee wg-private.key | wg pubkey > wg-public.key
```

You also need to change the permission of the files to make them readable for `systemd-network` users as shown in the following example:

```
❯ chown root:systemd-network wg-privatge.key wg-public.key
```

The following examples show the configurations of the two sites:

#### Site 1

```
❯ nmctl
         System Name: photon
              Kernel: Linux (5.10.152-6.ph4)
     systemd version: v247.11-4.ph4
        Architecture: x86-64
      Virtualization: vmware
    Operating System: VMware Photon OS/Linux
          Machine ID: 5103175aac7f4967acbdf97946c27ca3
        System State: routable
           Addresses: fe80::20c:29ff:fe3c:d58f/64    on device eth0
                      fe80::20c:29ff:fe3c:d599/64    on device eth1
                      127.0.0.1/8                    on device lo
                      192.168.1.10/24                on device eth0
                      192.168.1.9/24                 on device eth1
                      ::1/128                        on device lo
             Gateway: 192.168.1.1                    on device eth0
                      192.168.1.1                    on device eth1
                 DNS: 125.99.61.254 116.72.253.254



❯ cat wg-public.key 
d0AR4V68TJPA65ddKADmyTBbEgPTo75Xq/EVE1nsVFA=y
```
 
#### Site 2

```
❯ nmctl        
         System Name: Zeus
              Kernel: Linux (6.1.0-0.rc7.20221130git01f856ae6d0c.53.fc38.x86_64)
     systemd version: 252.2-591.fc38
        Architecture: x86-64
      Virtualization: vmware
    Operating System: Fedora Linux 38 (Workstation Edition Prerelease)
          Machine ID: d4f740d7e70d423cb46c8b1def547701
        System State: routable
        Online State: partial
           Addresses: fe80::20c:29ff:fe5f:d139/64    on device ens33
                      fe80::20c:29ff:fe5f:d143/64    on device ens37
                      127.0.0.1/8                    on device lo
                      ::1/128                        on device lo
                      192.168.1.8/24                 on device ens33
                      192.168.1.7/24                 on device ens37
             Gateway: 192.168.1.1                    on device ens33
                      192.168.1.1                    on device ens37
                 DNS: 125.99.61.254 116.72.253.254


➜ cat wg-public.key lhR9C3iZGKC+CIibXsOxDql8m7YulZA5I2tqgU2PnhM=y
```

To generate the WireGuard configuration using `nmctl` for Site 1, use the following command:

```
➜ nmctl create-wg wg99 private-key-file /etc/systemd/network/wg-private.key listen-port 34966 public-key lhR9C3iZGKC+CIibXsOxDql8m7YulZA5I2tqgU2PnhM= endpoint 192.168.1.11:34966 allowed-ips 10.0.0.2/32

➜ nmctl add-addr dev wg99 a 10.0.0.1/24
```

The following configuration is generated for `systemd-networkd`:

```
❯ cat 10-wg99.netdev

[NetDev]
Name=wg99
Kind=wireguard


[WireGuard]
PrivateKeyFile=/etc/systemd/network/wg-private.key
ListenPort=34966


[WireGuardPeer]
# Public key of Site #2
PublicKey=lhR9C3iZGKC+CIibXsOxDql8m7YulZA5I2tqgU2PnhM=
Endpoint=192.168.1.11:34966
AllowedIPs=10.0.0.2/32

❯ cat 10-wg99.network
[Match]
Name=wg99


[Address]
Address=10.0.0.1/24

➜  ~ nmctl status wg99
    Flags: UP RUNNING NOARP LOWERUP 
                        Kind: wireguard
                        Type: wireguard
                      Driver: wireguard
                   Link File: /usr/lib/systemd/network/99-default.link
                Network File: /etc/systemd/network/10-wg99.network
                       State: routable (configured) 
               Address State: routable
          IPv4 Address State: routable
          IPv6 Address State: off
                Online State: online
         Required for Online: yes
           Activation Policy: up
                         MTU: 1420 (min: 0 max: 2147483552) 
                       QDISC: noqueue 
              Queues (Tx/Rx): 1/1 
             Tx Queue Length: 1000 
IPv6 Address Generation Mode: eui64 
                GSO Max Size: 65536 GSO Max Segments: 65535 
                     Address: 10.0.0.2/24
```

The following output is generated for WireGuard:

```
➜  wg

interface: wg99
  public key: lhR9C3iZGKC+CIibXsOxDql8m7YulZA5I2tqgU2PnhM=
  private key: (hidden)
  listening port: 34966

peer: d0AR4V68TJPA65ddKADmyTBbEgPTo75Xq/EVE1nsVFA=
  endpoint: 192.168.1.7:34966
  allowed ips: 10.0.0.1/32
  latest handshake: 20 minutes, 36 seconds ago
  transfer: 57.70 KiB received, 58.37 KiB sent
```

To generate the WireGuard configuration using `nmctl` for Site 2, use the following command: 

```
➜ nmctl create-wg wg99 private-key-file /etc/systemd/network/wg-private.key listen-port 34966 public-key d0AR4V68TJPA65ddKADmyTBbEgPTo75Xq/EVE1nsVFA= endpoint 192.168.1.7:34966 allowed-ips 10.0.0.1/32

➜ nmctl add-addr dev wg99 a 10.0.0.2/242
```

The following configuration is generated for `systemd-networkd`:

```
➜ cat 10-wg99.netdev 
                 
[NetDev]
Name=wg99
Kind=wireguard


[WireGuard]
PrivateKeyFile=/etc/systemd/network/wg-private.key
ListenPort=34966


[WireGuardPeer]
# Public key of Site #1
PublicKey=d0AR4V68TJPA65ddKADmyTBbEgPTo75Xq/EVE1nsVFA=
Endpoint=192.168.1.7:34966
AllowedIPs=10.0.0.1/32


➜ network cat 10-wg99.network
[Match]
Name=wg99


[Address]
Address=10.0.0.2/24


❯ nmctl status wg99
                       Flags: UP RUNNING NOARP LOWERUP 
                        Kind: wireguard
                        Type: wireguard
                      Driver: wireguard
                   Link File: /usr/lib/systemd/network/99-default.link
                Network File: /etc/systemd/network/wg99.network
                       State: routable (configured) 
               Address State: routable
          IPv4 Address State: routable
          IPv6 Address State: off
                Online State: online
         Required for Online: yes
           Activation Policy: up
                         MTU: 1420 (min: 0 max: 2147483552) 
                       QDISC: noqueue 
              Queues (Tx/Rx): 1/1 
             Tx Queue Length: 1000 
IPv6 Address Generation Mode: eui64 
                GSO Max Size: 65536 GSO Max Segments: 65535 
                     Address: 10.0.0.2/24
                                                

➜ wg

interface: wg9
  public key: lhR9C3iZGKC+CIibXsOxDql8m7YulZA5I2tqgU2PnhM=
  private key: (hidden)
  listening port: 34966


peer: d0AR4V68TJPA65ddKADmyTBbEgPTo75Xq/EVE1nsVFA=
  endpoint: 192.168.1.7:34966
  allowed ips: 10.0.0.1/32
  latest handshake: 23 minutes, 57 seconds ago
  transfer: 57.70 KiB received, 58.37 KiB sent9
```

To verify the connectivity of Site 1, use the following command to ping and confirm the connectivity:

```
❯ ip a show wg99
```

Response:

```
25: wg99: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state 
UNKNOWN group default qlen 1000link/none 
    inet 10.0.0.1/24 brd 10.0.0.255 scope global wg99
       valid_lft forever preferred_lft forever

❯ ping 10.0.0.2

PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=4.90 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=3.77 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=23.0 ms
```

To verify the connectivity of Site 2, use the following command to ping and confirm the connectivity:

```
➜  ip a show wg
```

Response:

```
209: wg99: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000 link/none     inet 10.0.0.2/24 scope global wg99       valid_lft forever preferred_lft forever

➜  ping 10.0.0.1

PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
64 bytes from 10.0.0.1: icmp_seq=1 ttl=64 time=1.92 ms99
```

