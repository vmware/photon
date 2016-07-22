- [v1.0](#v1)
  - [Downloads](#downloads)
  - [Highlights](#highlights)
  - [Known Issues](#known-issues)
  
# v 1.0

## Downloads
| Download | Size | sha1 checksum | md5 checksum |
| --- | --- | --- | --- |
| [Full ISO](https://bintray.com/artifact/download/vmware/photon/photon-1.0-13c08b6.iso) | 2.1GB | a3acb6922c93e2b0cdc186abd5352bb0e61b986b | 60225fb97e6a702864795743db197335 |
| [OVA with virtual hardware v10](https://bintray.com/artifact/download/vmware/photon/photon-custom-hw10-1.0-13c08b6-GA.ova) | 199.8MB | 91760496427b277942fb9492fd48938cfc374edd | d8d02667a869c973ef7aa5c25d207748 |
| [OVA with virtual hardware v11](https://bintray.com/artifact/download/vmware/photon/photon-custom-hw11-1.0-13c08b6-GA.ova) | 199.8MB | 2cd6e4ff31f901f1b97aca279404d7ddaf42f44d | d30309abb4bec167d8c79daee6045dd4 |
| [Amazon AMI] (https://bintray.com/artifact/download/vmware/photon/photon-ami-1.0-13c08b6.tar.gz) | 148.5MB | e111281baabe82beaafcb6a3e17e6aec86c4acf6 | 0d2b86deca6d29323dc4877cf05c6bcc |
| [Google GCE] (https://bintray.com/artifact/download/vmware/photon/photon-gce-1.0-13c08b6.tar.gz) | 411.7MB | 6d0e6f52379fedeb22b744aabaf681e8cc5e4fbe | af9d0e8e44c4d0a031b694885acde540 |

## Highlights
- tdnf adds support for "distro-sync" - giving a single operation to apply updates to all installed packages that have updates in the Photon OS repos.
- Many new packages available for Photon OS!
- Photon OS 1.0 contains the 4.4 LTS kernel

## Known Issues

- Photon OS 1.0 does not respond immediately to the new FQDN after changing the hostname. This issue will occur when there is no valid DNS system configured. This is being investigated.
 - Workaround: To resolve this issue, restart systemd-resolved.

- Photon OS 1.0 requires at least 512MB of RAM when installing from ISO on ESXi. 
 - Workaround:  While on VMware Workstation and VMware Fusion, Photon OS 1.0 can install ISO and run in as little as 384MB of RAM (default). assign at least 512MB of RAM when installing from ISO on ESXi, as installer may fail in less memory. The default for ESXi is 2GB and most users will not be affected by this issue. The root cause is being investigated.

- When using a combination of different network cards in Photon OS 1.0, the interfaces may be swapped after a reboot. 
 - Workaround: Use the same type of virtual NIC for all interfaces. This happens because the devices are probed in increasing PCI slot address order upon boot. E1000 devices reside in 02:00.0 and above, while VMXNET3 devices will be placed into 03:00.0 and above. Upon reboot, the E1000 device(s) will always be assigned eth numbers than VMXNET3, regardless of configuration. Users might encounter this issue because VMXNET3 is the default adapter type within Photon OS, but older versions of VMware products might offer only E1000 devices when adding a secondary interface.

- When using multiple network cards without a valid DNS configuration and functional DNS server, initiating a ping might take 7-8 seconds to start. This happens because of multiple DNS timeouts on the interfaces.
 - Workaround: To avoid this issue, ensure that you've got a valid DNS configuration and a functioning DNS server that is capable of resolving the hostname(s) that are being pinged. 

- When using vSphere Guest Customization to set the hostname of a Photon OS 1.0 instance, the hostname may revert to the randomly-generated hostname after a reboot. 
 - Workaround: We are testing an update to our open-vm-tools rpm to resolve this issue. In the meantime, you can manually resolve this issue by deleting /var/lib/cloud/seed folder after applying guest customization. 

- Ordering within /etc/hosts makes IPv6 preferred, which impacts connectivity for applications that are not configured for IPv6.
 - Workaround: To make IPv4 the preferred connection, edit /etc/hosts and ensure that an IPv4 address is first on the list. Alternatively, configuring the application within Photon OS to use IPv6 will work. 

- The default umask permissions are 0027 and may cause some permissions issues with operations executed as root or through sudo.
 - Workaround: Change the umask settings to 022 by entering, "umask 022" within a Photon OS instance. To make the umask change persistent across reboots, edit /etc/profile and change the umask setting to 0022. 

- In the 1.0 release, Photon OS firewall settings have been changed to a default of DROP, which might cause services installed in Photon OS to be unreachable externally.
 - Workaround: To address this, administrators must configure their firewall rules appropriately to expose service ports as required for installed applications or containers. 
