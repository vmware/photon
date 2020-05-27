# Photon OS Logs

On Photon OS, all the system logs except the installation logs and the cloud-init logs are written into the systemd journal. The `journalctl` command queries the contents of the systemd journal.

The installation log files and the cloud-init log files reside in `/var/log`. If Photon OS is running on a virtual machine in a VMware hypervisor, the log file for the VMware tools, `vmware-vmsvc.log`, also resides in `/var/log`. 