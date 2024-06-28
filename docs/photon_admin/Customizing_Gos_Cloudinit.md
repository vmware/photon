# Customizing Guest OS using Cloud-Init

A guest operating system is an operating system that runs inside a virtual machine. You can install a guest operating system in a virtual machine and control guest operating system customization for virtual machines created from vApp templates.

When you customize your guest OS you can set up a virtual machine with the operating system that you want.

### Procedure
1. Perform the following steps before cloning or customizing the guest operating system:    
  1. Ensure that `disable_vmware_customization` is set to false in the `/etc/cloud/cloud.cfg` file.
  1. Set `manage_etc_hosts: true` in the `/etc/cloud/cloud.cfg` file.
  1. Make a backup of the `99-disable-networking-config.cfg` file and delete the file from `/etc/cloud/cloud.cfg.d` folder after backup.
1. Clone the VM or customize the guest operating system.
1. After you clone your VM or customize the guest operating system, perform the following steps:
  1. Ensure that `disable_vmware_customization` is set to true in the `/etc/cloud/cloud.cfg` file in the newly created VM and the VM from where cloning was initiated.
  1. Remove `manage_etc_hosts: true` from the `/etc/cloud/cloud.cfg` file in the newly created VM and the VM from where cloning was initiated.
  1. Add a copy of the backed up file `99-disable-networking-config.cfg` to its original folder `/etc/cloud/cloud.cfg.d` in the newly created VM and the VM from where cloning was initiated.
  
**Note**:

1. The `disable_vmware_customization` flag in `/etc/cloud/cloud.cfg.d` file decides which customization workflow to be initiated.
  - Setting this to **false** invokes the Cloud-Init GOS customization workflow.
  - Setting this to **true** invokes the traditional GOSC script based customization workflow. 
1. When the `manage_etc_hosts` flag is set to **true**, Cloud-Init can edit the `/etc/hosts` file with the updated values.
    
    When the flag is set to **true** Cloud-Init edits the `/etc/hosts` file, even when there is no cloud config metadata available. Remove this entry once the Cloud-Init GOS customization is done, to stop Cloud-Init from editing `/etc/hosts` file and set a fallback configuration.
1. The `99-disable-networking-config.cfg` file is packaged as part of Cloud-Init RPM in photon and it prevents Cloud-Init from configuring the network. Delete this file before starting the Cloud-Init customization and then paste the backup of the file in the `/etc/cloud/cloud.cfg.d/` folder once the cloud-init workflow is complete. It is important to replace this file after Cloud-Init customization to avoid removal of network configuration in the Cloud-Init instance.
 

### Result

Cloud-Init guest OS customization is now enabled.