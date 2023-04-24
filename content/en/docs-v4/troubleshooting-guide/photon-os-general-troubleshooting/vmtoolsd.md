---
title:  Open-vm-tools/Vmtoolsd
weight: 5
---

Vmtoolsd is a systemd service, using which we can set guestinfo properties metadata, userdata and vendordata etc., which in turn are consumed by cloud-init.
VMwareGuestInfo Datasource uses this guestinfo properties and applies them to the system.

vmware-rpctool is a utility provided by open-vm-tools to set metadata, userdata and vendordata.
vmware-rpctool provides info.set and info.get options to set and get the guestinfo properties respectively.

##Debugging
To check the status of the vmtoolsd service (vmtoolsd is dependant on vgauthd), run the following commands:
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

A YAML file can be used as input to the **rpctool** using following commands:

```
vmware-rpctool "info-set guestinfo.userdata.encoding base64"
vmware-rpctool "info-set guestinfo.metadata.encoding base64"

vmware-rpctool "info-set guestinfo.metadata ${metadata file contents}"

vmware-rpctool "info-set guestinfo.userdata ${userdata file contents}"
```

**Note**:Include the cloud-init log tarball and the vmtoolsd logs when you raise an issue.

1. Collect cloud-init log tarball by running the `cloud-init collect-logs` command.
1. Collect the vmtoolsd logs from **/var/log/vmware-imc/toolsDeployPkg.log** file.
1. Attach the logs collected to the issue ticket.
