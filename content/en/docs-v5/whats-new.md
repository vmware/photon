---
title: What is New in Photon OS 5
linkTitle: What is New in Photon 5
weight: 15
---

Photon OS 5.0  provides enhancements in Network Configuration Manager, PMD-nextgen, Container Runtime Security, Linux Real-Time Kernel, and TDNF Features. The release introduces the Photon OS Container Builder tool. This release of Photon OS also supports XFS and BTRFS filesystems, Control Group V2,  ARM64 on Linux-esx kernel, PostgreSQL. It contains installer improvements and critical updates to the OSS packages including Linux kernel version updates. This topic summarizes what's new and different in Photon OS 5.0.

## New Features

- **Enhancements in Network Configuration Manager:** You can now use Network Configuration Manager to perform the following tasks:

	- Configure multiple routes and addresses section
	- Configure WireGuard
	- Configure SR-IOV
	- Create NetDev, VLAN, VXLAN, Bridge, Bond, VETH (Virtual Ethernet), MacVLAN/MacVTap, IPvlan/IPvtap, tunnels (IPIP, SIT, GRE, VTI)
	- Create, configure, and remove virtual network devices
	- Generate more flexible netplan like network configuration from a YAML file

	You can run query or configure the following parameters of network devices:
	
	- Alias, Description, MTUBytes, WakeOnLan, WakeOnLanPassword, Port, BitsPerSecond, Duplex and Advertise
	- Offload parameters and other features
	- MACAddressPolicy or MACAddress
	- NamePolicy or Name
	- AlternativeNamesPolicy or AlternativeName
	- Pending packets receive a buffer
	- Queue size
	- Flow control
	- GSO
	- Channels
	- Coalesce
	- Coalesced frames
	- Coalesce packet rate

- **PMD-Nextgen Enhancement:** The capabilities to configure the following options are added to pmd-nextgen:
	- Configure system hostname
	- Configure network sriov
	- Configure Tun
	- Configure Tap
	- Configure TLS


- **Network-event-broker:** Network-event-broker now supports emitting network data in JSON format.

- **Photon OS Container Builder**: The `cntrctl` tool in Photon OS 5.0 allows you to build a lightweight Photon OS container. 


- **Kernel-Version Update:** The following Kernel flavors are updated to kernel version 6.1.10 in Photon OS:  
	- Linux  
	- Linux-esx  
	- Linux-secure  
	- Linux-rt  


- **Support for New Filesystems:** Support is added for the following filesystems in Photon OS:
	- XFS: With the support of the XFS filesystem, you can implement an environment that requires high performance, and scalability for data-intensive tasks.
	- BTRFS: You can use the BTRFS filesystem for high performance, better reliability, and efficient data storage capabilities.



- **Support for Control Group V2:** cgroup v2 is now available in Photon OS. With cgroup v2, you get improved resource management capabilities, a unified hierarchy scheme, and a safer sub-tree delegation to containers. Features like Pressure Stall Information and rootless containers in cgroup v2 ensure better management and security capabilities of the control groups.

- **Support for Kernel Live Patching**: With Kernel Live Patching, an administrator can patch a running kernel without rebooting.


- **Enhanced Container Runtime Security:** To improve the runtime security of the containers, the following enhancements are added to Photon OS:
	- Support for SELinux policy: You can now enable and configure the SELinux policy to manage access to files, directories, and other system resources. This drastically reduces the risk of a security breach.
	- Support for rootless containers: Photon OS supports rootless containers. An unprivileged user can now create and manage containers. Since unprivileged users do not have root privileges on the host machine, it prevents any security threat to the host machine.



- **Improved Linux Real-Time Kernel:** The linux-rt kernel flavor comes with improvements such as low-latency optimizations, stability enhancements, and debugging enhancements. Linux-rt now also supports the Intel Sapphire Rapids CPUs including the Telco-specific 5G ISA.


- **Support for ARM64:** Support for ARM64 is now available for the linux-esx kernel in Photon OS.
 

- **PostgreSQL versions:** The following PostgreSQL versions are supported on Photon OS:
	- PostgreSQL 13
	- PostgreSQL 14
	- PostgreSQL 15

- **TDNF Feature Enhancements:** The metalink functionality in tdnf is now available as a plugin. In tdnf, support is added for the following:

	- history (`list`, `rollback`, `undo` and `redo`)
	- `mark` command
	- checking the available cache size of a download
	- multiple base URLs
	- `--skip-broken` option
	- `--alldeps` option when downloading
	- `--testonly` option
	- `--nodeps` option for `--downloadonly`
	- `--source` and `--builddeps` options
	- `dnf_check_update_compat` config file option
	- support for `tsflags=nodocs`
	- `--repofromdir` option
	- `--arch` option to repoquery
	- Configuration tool: Set of commands to change tdnf's configuration files and repository files.

- **OVA Updates**: UEFI OVA is built with hardware version 15.


### Installer and Build System Updates
- Support Pre-install script in photon installer
- A tool is now available to generate a custom initial RAM disk (initrd)
- A tool is now available to generate a custom installer ISO
- A tool is now available to generate a custom RPM-OSTree ISO
- Support is added for the following features in Kickstart:   <p>
	- `sizepercent`: specifies the size of the partition in percent of the total disk space. 
	- `repos`: Specifies the RPM repositories to install the RPMs.
- Support for A/B Partition System: Photon OS 5.0 supports seamless updates and rollback with the A/B storage partition system.
- **Kickstart Network Configuration**: Improved flexibility for network configuration that allows multiple interfaces and facilitates better handling of the VLAN interfaces. 


### Package Updates:

The following OS packages are updated:

- Linux kernel 6.1.10
- Gcc : 12.2
- Glibc 2.36
- Systemd 253
- Python3 3.11
- Openjdk : 11 and 17
- Openssl : 3.0.8
- Cloud-init: 23.1.1
- Rubygem: 3.1.2
- Perl: 5.36
- Kubernetes 1.26.1
- Go 1.20.2

## Notes
 
The following OS packages are removed in this release.

- Photon Management Daemon (PMD)
- lightwave
- likewise-open
- openjdk8
- fcgi
- libnss-ato
- tiptop
- ndsend
- ulogd
- lightstep-tracer-cpp
- json_spirit
- cgroup-utils
- c-rest-engine
- dcerpc
- gssapi-unix
- python3-PyPAM
- python3-backports_abc
- sshfs