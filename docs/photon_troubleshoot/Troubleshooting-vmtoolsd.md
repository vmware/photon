#Vmtoolsd

Vmtoolsd is a systemd service which is started after the cloud-final service in photon.
vmtools provides guestinfo properties using which you can set metadata, userdata and vendordata for cloud-init. the VMwareGuestInfo Datasource pulls this metadata, userdata and vendordata and applies the configuration to the system.
vmware-rpctool is a utility provided by open-vm-tools to set metadata, userdata and vendordata.
vmware-rpctool enables the info.set and info.get options to set and get the guestinfo properties respectively.

##Debugging
To check the status of the vmtoolsd service (vgauthd is used by vmtoolsd), run the following commands:
```
$ systemctl status vmtoolsd vgauthd

$ journalctl -u vmtoolsd

$ journalctl -u vgauthd
```
To set and get metadata, userdata and vendordata, run the following commands:
```
$ /usr/bin/vmware-rpctool 'info-get guestinfo.metadata'

$ /usr/bin/vmware-rpctool 'info-get guestinfo.userdata'

$ /usr/bin/vmware-rpctool 'info-get guestinfo.vendordata'
```