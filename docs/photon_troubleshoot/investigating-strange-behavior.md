# Investigating Unexpected Behavior

If you rebooted to address unexpected behavior before the reboot or if you encountered unexpected behavior during the reboot but have reached the shell, you must analyze what happened since the previous boot. 

1. Run the following command to check the logs:

	   `journalctl`

1. Run the following command to look at what happened since the penultimate reboot:

	`journalctl --boot=-1`

    Look at the log from the reboot: 

	`journalctl -b`

1. If required, examine the logs for the kernel:

	   `journalctl -k`

1. Check which kernel is in use:

	`uname -r`

    The kernel version of Photon OS in the full version is 4.4.8. The kernel version of in the OVA version is 4.4.8-esx. With the ESX version of the kernel, some services might not start. 

1. Run this command to check the overall status of services:

	`systemctl status` 

    If a service is in red, check it: 
    
    	systemctl status service-name
    
    Start it if required: 
    
    	systemctl start service-name

1. If looking at the journal and checking the status of services does not resolve your error, run the following `systemd-analyze` commands to examine the boot time and the speed with which services start.
	
    ```
    systemd-analyze time
    	systemd-analyze blame
    	systemd-analyze critical-chain
    ```

 
**Note**: The output of these commands might be misleading because one service might just be waiting for another service to finish initializing.
