Photon OS 2.0 introduces new security and OS management capabilities, along with new and updated packages for Cloud native applications and VMware appliances. This topic summarizes what&#39;s new and different in Photon OS 2.0.

## Security Enhancements

- Security-hardened Linux kernel: In addition to the linux and linux-esx kernels, Photon OS 2.0 provides a new security-hardened kernel (linux-secure), which is configured according to the recommendations of the Kernel Self-Protection Project (KSPP), plus includes most of the Pax patches.
- Secure EFI boot: The operating system now boots with validated trust.
- Python 3 (Python 2 is deprecated)

## OS and Storage Management Enhancements

- The Network Configuration Manager provides a library of C, Python, and CLI APIs that simplify common configuration tasks for network resources, including network interfaces, IP addresses, routes, DNS servers and domains, DHCP DUID and IAID, NTP servers, and other service management operations.
- The Photon Management Daemon (PMD) provides the remote management of a Photon instance via a command line client (pmd-cli), Python, and REST API interfaces. The PMD provides the ability to manage network interfaces,  packages, firewalls, users, and user groups.
- Project Lightwave integration: The open source security platform from VMware authenticates and authorizes users and groups with AD or LDAP.
- Support for persistent volumes to store the data of cloud-native apps on VMware vSAN
- Update notification
- Guestinfo for cloud-init

## Package and Binary Maintenance

- Cloud-ready images for rapid deployment on Microsoft Azure (new), Google Compute Engine (GCE), Amazon Elastic Compute Cloud (EC2), and VMware products (vSphere, Fusion, and Workstation)
- New Linux OSS packages
- New packages, including Calico, Heapster, nginx-ingress, RabbitMQ, and the proxy for Wavefront by VMware
- Updates to key packages, including the LTS version of the Linux kernel (4.9) and systemd
- Support for multiple Java versions
