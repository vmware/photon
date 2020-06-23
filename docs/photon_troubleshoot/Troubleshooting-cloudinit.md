# Cloud-init

Cloud-init is a set of Python scripts that initialize cloud instances of Linux machines. The cloud-init scripts configure SSH keys and run commands to customize the machine without user interaction. The commands can set the root password, create a hostname, configure networking, write files to disk, upgrade packages, run custom scripts, and restart the system.

##DataSources
Datasources are sources of configuration data for cloud-init that typically come from the user (For example: userdata) or come from the cloud that created the configuration drive (For example: metadata).
Typical userdata includes files, yaml, and shell scripts while typical metadata includes server name, instance id, display name and other cloud specific details.

There are two datasources used in Photon, its usage is described in the following sections:

- DataSourceOVF - Used for GuestOS customization in vsphere.
- VMwareGuestInfo - Used to read meta, user, and vendor data from VMware vSphere's GuestInfo interface and initialize the system.

###DataSourceOVF
The OVF (Open Virtualization Format) Datasource provides a datasource for reading data from an OVF transport ISO.
The VMtools plugin extracts the customization spec cab file from the OVF and calls either cloud-init or the GuestOS customization scripts. The `disable_vmware_customization` flag in **/etc/cloud/cloud.cfg** file determines if GOSC scripts or cloud-init is used.

- `disable_vmware_customization: false` : Cloud-init is used for Guest OS customization
- `disable_vmware_customization: true` : GuestOS customization scripts is used for Guest OS customization (The default value for `disable_vmware_customization` is set to `true` in the **/etc/cloud/cloud.cfg** file)

###VMwareGuestInfo
VMwareGuestInfo data source is configured by setting `guestinfo` properties on a VM. This can be set by performing one of the following:

- Using the vmware-rpctool provided by open-vmtools.
- Modifying the **vmx** file to set the guestinfo properties.

##Debugging Cloud-init Failures
Cloud-init has four services which are started in the following sequence:

1. cloud-init-local - This service locates local data sources and applies networking configurations provided n the metadata (If there is no metadata it applies Fallback). Use `$ systemctl status cloud-init-local` command to check its status.
1. cloud-init - This service processes any user-data that is found and runs the cloud_init_modules in **/etc/cloud/cloud.cfg**. Use `$ systemctl status cloud-init` command to check its status.
1. cloud-config - This service runs the cloud_config_modules in **/etc/cloud/cloud.cfg** file. Use `$ systemctl status cloud-config` command to check its status.
1. cloud-final - This service runs any script that a user is accustomed to running after logging into a system (For example: package installations, configs, user-scripts) and runs cloud_final_modules in **/etc/cloud/cloud.cfg** file. Use `$ systemctl status cloud-final` command to check its status.

Cloud-init logs are available in the **/var/log/cloud-init.log** file. Logs for GuestOS customization using DataSourceOVF are available in the **/var/log/vmware-imc/toolsDeployPkg.log** and **/var/log/cloud-init.log** files.

To analyze the cloud-init boot time performance, run the following commands:

- `$ cloud-init analyze blame` - The blame command prints in descending order, the units that took the longest to run. This output is useful for observe where cloud-init is spending its time during execution.
- `$ cloud-init analyze show` - The show command prints a list of units, the time they started and how long they took to complete. It also prints a summary of total time per boot.
- `$ cloud-init analyze dump` - The dump command dumps the cloud-init logs for the analyze modules and displays a list of dictionaries that can be consumed for other reporting needs.

Cloud-init doesn't configure the network if **/etc/cloud/cloud.cfg.d/99-disable-networking-config.cfg** file is present and has the following content:

- network:Item
- config: disabled

Take a backup of **/etc/cloud/cloud.cfg.d/99-disable-networking-config.cfg** file and remove it from its location. reconfigure the machine using metadata, userdata and vendordata. Once the configurations are done copy the backup file to the same location. Cloud-init will push its fallback configuration when service is restarted or rebooted and there is no local datasource to configure. To avoid this **/etc/cloud/cloud.cfg.d/99-disable-networking-config.cfg** file is required.

##Run Cloud-init Manually
To run cloud-init manually, run the following commands:
```
/usr/bin/cloud-init -d init  (-d for debug)
/usr/bin/cloud-init -d modules (run all modules)
```
When cloud-init is running, to force it to run with all configs engaged run the following command:
```
rm -rf /var/lib/cloud/*
```













