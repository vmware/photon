# Network Configuration

systemd-networkd is a system daemon that manages network configurations. It detects and configures network devices as they appear. It can also create virtual network devices.

##Configuration Examples
All configurations are stored as **foo.network** in the **/etc/systemd/network/**, **/lib/systemd/network/** and **/run/systemd/network/** folder. Use the `networkctl list` command to list all the devices on the system.

After making changes to a configuration file, restart the **systemd-networkd.service** if version is < 245, for other version run the following commands:
```
root@photon [ /home/sus ]# networkctl reload
root@photon [ /home/sus ]# networkctl reconfigure eth0
```
**Note**:

- The options mentioned in the configuration files are case sensitive.
- Set `DHCP=yes` to accept IPv4 and IPv6 DHCP requests.
- Set `DHCP=ipv4` to accept IPv4 DHCP requests.
- Set LinkLocalAddressing=no to deactivate IPv6. Please do not deactivate IPv6 via sysctl. When `LinkLocalAddressing=no` in the .network file, the kernel drops addresses starting with **fe80**, for example **fe80::20c:29ff:fe4c:7eca**. If IPv6LL address is not available networkd will not start IPv6 configurations.


To link network configurations using DHCPv4 (IPv6 deactivated), run the following command:
```
/etc/systemd/network/20-eth0.network
[Match]
Name=eth0

[Network]
LinkLocalAddressing=no

DHCP=ipv4
```

To link network configurations using DHCPv6, run the following command:
```
/etc/systemd/network/20-eth0.network
[Match]
Name=eth0

[Network]
IPv6AcceptRA=yes

DHCP=ipv6
```

To link network configurations using a static IP address, run the following command:
```
/etc/systemd/network/20-wired.network
[Match]
Name=enp1s0

[Network]
Address=10.1.10.9/24
Gateway=10.1.10.1
DNS=10.1.10.1
```
Here `Address=` can be used more than once to configure multiple IPv4 or IPv6 addresses.

A **.link** file can be used to rename an interface. For example, set a predictable interface name for a Ethernet adapter based on its MAC address by running the following command:
```
/etc/systemd/network/10-test0.link
[Match]
MACAddress=12:34:56:78:90:ab

[Link]
Description=my custom name
Name=test123
```

##Configuration Files
Configuration files are located in **/usr/lib/systemd/network/** folder, the volatile runtime network directory in **/run/systemd/network/** folder and the local administration network directory in  **/etc/systemd/network/** folder. Configuration files in **/etc/systemd/network/** folder have the highest priority.

There are three types of configuration files and they use a format similar to systemd unit files.

- **.network** : These files apply a network configuration to a matching device.
- **.netdev** : These files are used to create a virtual network device for a matching environment.
- **.link** : When a network device appears, udev looks for the first matching **.link** file.
These link files follow the following rules:

- Only if all conditions in the `[Match]` section are matched, the profile will be activated.
- An empty `[Match]` section means the profile can apply to any case (can be compared to the * wild card)
- All configuration files are collectively sorted and processed in lexical order, regardless of the directory it resides in.
- Files with identical names replace each other.

##Dupliate Matches
If we have multiple configuration files matching an interface, the first (in lexical order) network file matching a given device is applied. All other files are ignored even if they match. The following is an example of matching configuration files:
```
builder@localhost [ ~ ]$ cat /etc/systemd/network/10-eth0.network
[Match]
Name=eth0
[Network]
DHCP=yes
  
builder@localhost [ ~ ]$ cat /etc/systemd/network/99-dhcp-en.network
[Match]
Name=e*
 
[Network]
DHCP=yes
IPv6AcceptRA=no
```

##Network Files
These files are used to set network configuration variables for servers and containers.
**.network** files have the following sections:

###`[Match]`

| Parameter |Description  | Accepted Values |
|--|--|--|
|`Name=`  | Matches device names. For example: `en*`. By using `!` prefix the list can be inverted. | Device names separated by a white space, logical negation (!). |
|`MACAddress=`  |	Matches MAC addresses. For example: `MACAddress=01:23:45:67:89:ab 00-11-22-33-44-55 AABB.CCDD.EEFF`  | MAC addresses with full colon-, hyphen- or dot-delimited hexadecimal separated by a white space. |
| `Host=` | Matches the host name or the machine ID of the host. | Hostname string or Machine ID |
| `Virtualization=` |Checks whether the system is running in a virtual environment. `Virtualization=false` will only match your host machine, while `Virtualization=true` matches containers or VMs. It is also possible to check for a specific virtualization type or implementation.  |boolean, logical negation (!), type (vm, container), implementation (qemu, kvm, zvm, vmware, microsoft, oracle, xen, bochs, uml, bhyve, qnx, openvz, lxc, lxc-libvirt, systemd-nspawn, docker, podman, rkt, wsl, acrn)  |

###`[Link]`

- `MACAddress=` : Used to spoof MAC address.
- `MTUBytes=` : Setting a larger MTU value (For example: when using jumbo frames) can significantly speed up your network transfers.
- `Multicast` : Enables the use of multicast on interface(s).

###`[Network]`

| Parameter |Description  |Accepted Values  |Default Value  |
|--|--|--|--|
|`DHCP=`  |Controls DHCPv4 and/or DHCPv6 client support.  |Boolean, `ipv4`, `ipv6`  |false  |
|`DHCPServer=`  |If enabled, a DHCPv4 server will be started.  |Boolean  |false  |
|`MulticastDNS=`  |	Enables multicast DNS support. When set to `resolve`, only resolution is enabled.  |Boolean, `resolve`  |false  |
|`DNSSEC=`  |Controls the DNSSEC DNS validation support on the link. When set to `allow-downgrade`, compatibility with non-DNSSEC capable networks is increased, by automatically turning off DNSSEC.  |Boolean, `allow-downgrade`  |false  |
|`DNS=`  |Configures static DNS addresses. can be specified more than once.  |`	inet_pton`  |  |
|`Domains=	`  |Indicates domains which must be resolved using the DNS servers.  |	domain name, optionally prefixed with a **~**  |  |
|`IPForward=`  |	If enabled, incoming packets on any network interface will be forwarded to any other interfaces according to the routing table.  |Boolean, `ipv4`, `ipv6`  |false  |
|`IPMasquerade=`  |If enabled, packets forwarded from the network interface appear as if they are coming from the local host.  |Boolean  |false  |
|`IPv6PrivacyExtensions=`  |Configures use of stateless temporary addresses that change over time. When set to `prefer-public`, the privacy extensions are enabled, but prefers public addresses over temporary addresses. When set to `kernel`, the kernel's default setting will be left in place.  |Boolean, `prefer-public`, `kernel`  |false  |

###`[Address]`
`Address=` option is mandatory unless DHCP is used.

###`[Route]`

- `Gateway=` option is mandatory unless DHCP is used.
- `Destination=` option defines the destination prefix of the route, possibly followed by a slash and the prefix length.
If Destination is not present in `[Route]` section it is treated as a default route.
**Note:** You can add the `Address=` and `Gateway=` keys in the `[Network]` section as a short-hand, if the `[Address]` section contains only an Address key and `[Route]` section contains only a Gateway key.

###DHCP
| Parameter |Description  |Accepted Values  |Default Value  |
|--|--|--|--|
|`UseDNS=`  |Defines the DHCP server to be used.  |Boolean |true  |
|`Anonymize=`  |When set to `true`, the options sent to the DHCP server will follow RFC7844 (Anonymity Profiles for DHCP Clients) to minimize disclosure of identifying information.  |Boolean  |false  |
|`UseDomains=`  |Defines the DHCP server to be used as the DNS search domain. If set to `route`, the domain name received from the DHCP server will be used for routing DNS queries only and not for searching. This option can sometimes fix local name resolving when using systemd-resolved.  |Boolean, `route`  |false  |

###`[DHCPServer]`
The following is an example of a DHCP server configuration which works well with hostapd to create a wireless hotspot. `IPMasquerade` adds the firewall rules for NAT and `IPForward` enables packet forwarding.
```
/etc/systemd/network/wlan0.network
[Match]
Name=wlan0

[Network]
Address=10.1.1.1/24
DHCPServer=true
IPMasquerade=true
IPForward=true

[DHCPServer]
PoolOffset=100
PoolSize=20
EmitDNS=yes
DNS=9.9.9.9
```

##Netdev Files
These files create virtual network devices. They have the following two sections:

###`[Match]`

- `Host=` : The host name.
- `Virtualization=` : Checks if it is running in a virtual environment.

###`[NetDev]`

- `Name=` : The interface's name. This is a mandatory field.
- `Kind=` : For example: bridge, bond, vlan, veth, sit, etc. This is a mandatory field.

##Link Files
These files are an alternative to custom udev rules and will be applied by udev as the device appears. They have the following two sections:

###`[Match]`

- `MACAddress=` : The MAC address.
- `Host=` : The host name.
- `Virtualization=` : Checks if it is running in a virtual environment.
- `Type=` : the device type. For example: vlan.

###`[Link]`

- `MACAddressPolicy=` : Persistent or random addresses.
- `MACAddress=` : The MAC address.
**Note:** The system **/usr/lib/systemd/network/99-default.link** file is sufficient for most cases.

##Debugging Systemd-networkd
The log can be generated by creating a drop-in config. For example:
```
# /etc/systemd/system/systemd-networkd.service.d/override.conf
[Service]
Environment=SYSTEMD_LOG_LEVEL=debug
```

