- [Updated OVAs for CVE-2016-5333](#updated-ovas-for-CVE20165333)

- [v3.0rev2](#v3.0rev2)
  - [Downloads](#downloads)
  - [Highlights](#highlights)
  - [Known Issues](#known-issues)
  
## Updated OVAs for CVE-2016-5333

A public ssh key used in the Photon OS build environment was inadvertently left in the original Photon OS 3.0 OVAs.
This issue would have allowed the corresponding private key to access any Photon OS system built from the original 3.0 OVAs.

The issue was discovered internally and the original OVAs have been replaced by updated OVAs. All instances of this private key have been deleted within VMware. 
 
Customers that have downloaded the PhotonOS 3.0 OVAs before August 14, 2016 should take either of the following procedures to ensure the security of their systems:

- Remove the left-over public key from all Photon OS 3.0 systems built from the original PhotonOS 3.0 OVAs by executing the following command:
  - On a freshly installed Photon OS system: 
  
    ```rm –f /root/.ssh/authorized_keys```
  - On a Photon OS system which contains user-installed ssh keys:
  
    ```sed –i '/photon-jenkins/d' /root/.ssh/authorized_keys```
- Alternatively, download the new OVA and replace all existing instances with new instances built from the updated Photon OS 3.0 OVAs.
 
To confirm that the left-over public key is not present and that the issue is resolved, the following command should not produce any output:

  ```cat /root/.ssh/authorized_keys | grep photon-jenkins```

This issue is only present in the original Photon OS 3.0 OVAs and is not present in other Photon OS deliverables.

The Common Vulnerabilities and Exposures project (cve.mitre.org) has assigned the identifier CVE-2016-5333 to this issue.

# v 3.0rev2

## Downloads
| Download | Size | sha1 checksum | md5 checksum |
| --- | --- | --- | --- |
| [Full ISO x86_64](https://packages.vmware.com/photon/3.0/Rev2/iso/photon-3.0-58f9c74.iso) | 5.2G | 545a9d0d53cb2109381bd9ae9eb837579f2ef1ee | 2ece2dfcdcdf098e36100a2085937dca |
| [Minimal ISO x86_64](https://packages.vmware.com/photon/3.0/Rev2/iso/photon-minimal-3.0-58f9c74.iso) | 280M | ae28558e57f5d8aefb8b479c9fac7473079156e1 | 187dfb1e6bc5e47606c667e9042f86a4 |
| [Full ISO arm64](https://packages.vmware.com/photon/3.0/Rev2/iso/photon-3.0-58f9c743-aarch64.iso) | 3.5G | 16848687d4d7cf393a413f3a24728b2cf042191d | 46d929c644debd27ee9fd37d35046921 |
| [OVA with virtual hardware v11](https://packages.vmware.com/photon/3.0/Rev2/ova/photon-hw11-3.0-9355405.ova) | 169M | f4c22463e4567e6cd9becdbb2a178b4b916ffff9 | 514e9d9597eea5f1694df9717cffb80b |
| [OVA with virtual hardware v13 (UEFI Secure Boot)](https://packages.vmware.com/photon/3.0/Rev2/ova/photon-hw13_uefi-3.0-9355405.ova) | 165M | 7cea6b552c66a6ceb6e8023938f9788179d8f697 | 6a24a68b1e56ee35c4a20$
| [Amazon AMI](https://packages.vmware.com/photon/3.0/Rev2/ami/photon-ami-3.0-9355405.tar.gz ) | 172M | 85949657c857fee6a4417ca72ec010da81ed09e9  | e80bd2f0991a5091d83b3b3ae6e100df |
| [Google GCE](https://packages.vmware.com/photon/3.0/Rev2/gce/photon-gce-3.0-9355405.tar.gz) | 456M | a97425523518a54a6e20114419cb6fb0e5900039 | c5cffb418372b72bb48a66549ee25fbf |
| [Azure VHD](https://packages.vmware.com/photon/3.0/Rev2/azure/photon-azure-3.0-9355405.vhd.tar.gz) | 180M | c2a5438574f0b8b62d792042c7edfb655f61acdf | 24b70b81f7e3cb026e4e43bcb0650a5f |
| [Raspberry Pi3 Image](https://packages.vmware.com/photon/3.0/Rev2/rpi3/photon-rpi3-3.0-9355405.tar.xz) | 61M | 9f44bde819862eeb0c6cbfcd06fab6a48ba36594| 2ca56e575e37fc7b911dd934e5089432 |

## Highlights
- tdnf adds support for "distro-sync" - giving a single operation to apply updates to all installed packages that have updates in the Photon OS repos.
- Many new packages available for Photon OS!
- Photon OS 3.0 contains the 4.4 LTS kernel

## Known Issues

- Photon OS 3.0 does not respond immediately to the new FQDN after changing the hostname. This issue will occur when there is no valid DNS system configured. This is being investigated.
 - Workaround: To resolve this issue, restart systemd-resolved.

- Photon OS 3.0 requires at least 512MB of RAM when installing from ISO on ESXi.
 - Workaround:  While on VMware Workstation and VMware Fusion, Photon OS 3.0 can install ISO and run in as little as 384MB of RAM (default). assign at least 512MB of RAM when installing from ISO on ESXi, as installer may fail in less memory. The default for ESXi is 2GB and most users will not be affected by this issue. The root cause is being investigated.

- When using a combination of different network cards in Photon OS 3.0, the interfaces may be swapped after a reboot.
 - Workaround: Use the same type of virtual NIC for all interfaces. This happens because the devices are probed in increasing PCI slot address order upon boot. E1000 devices reside in 02:00.0 and above, while VMXNET3 devices will be placed into 03:00.0 and above. Upon reboot, the E1000 device(s) will always be assigned eth numbers than VMXNET3, regardless of configuration. Users might encounter this issue because VMXNET3 is the default adapter type within Photon OS, but older versions of VMware products might offer only E1000 devices when adding a secondary interface.

- When using multiple network cards without a valid DNS configuration and functional DNS server, initiating a ping might take 7-8 seconds to start. This happens because of multiple DNS timeouts on the interfaces.
 - Workaround: To avoid this issue, ensure that you've got a valid DNS configuration and a functioning DNS server that is capable of resolving the hostname(s) that are being pinged. 

- When using vSphere Guest Customization to set the hostname of a Photon OS 3.0 instance, the hostname may revert to the randomly-generated hostname after a reboot.
 - Workaround: We are testing an update to our open-vm-tools rpm to resolve this issue. In the meantime, you can manually resolve this issue by deleting /var/lib/cloud/seed folder after applying guest customization. 

- Ordering within /etc/hosts makes IPv6 preferred, which impacts connectivity for applications that are not configured for IPv6.
 - Workaround: To make IPv4 the preferred connection, edit /etc/hosts and ensure that an IPv4 address is first on the list. Alternatively, configuring the application within Photon OS to use IPv6 will work. 

- The default umask permissions are 0027 and may cause some permissions issues with operations executed as root or through sudo.
 - Workaround: Change the umask settings to 022 by entering, "umask 022" within a Photon OS instance. To make the umask change persistent across reboots, edit /etc/profile and change the umask setting to 0022. 

- In the 3.0 release, Photon OS firewall settings have been changed to a default of DROP, which might cause services installed in Photon OS to be unreachable externally.
 - Workaround: To address this, administrators must configure their firewall rules appropriately to expose service ports as required for installed applications or containers. 
