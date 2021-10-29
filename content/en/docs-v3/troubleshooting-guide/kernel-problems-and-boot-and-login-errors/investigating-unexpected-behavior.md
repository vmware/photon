---
title:  Investigating Unexpected Behavior
weight: 4
---

If you rebooted to address unexpected behavior before the reboot or if you encountered unexpected behavior during the reboot but have reached the shell, you must analyze what happened since the previous boot. 

1. Run the following command to check the logs:
    ```
	   journalctl
    ```
2. Run the following command to look at what happened since the penultimate reboot:
    ```
	journalctl --boot=-1
    ```
    Look at the log from the reboot: 
    ```
	journalctl -b
    ```
3. If required, examine the logs for the kernel:
    ```
	journalctl -k
    ```
4. Check which kernel is in use:
    ```
	uname -r
    ```
    As example for Photon OS 1.0, the kernel version in the full version is 4.4.8. The kernel version of in the OVA version is 4.4.8-esx. With the ESX version of the kernel, some services might not start. 

5. Run this command to check the overall status of services:
    ```
	systemctl status
    ```
    If a service is in red, check it: 
    ```    
	systemctl status service-name
    ```    
    Start it if required: 
    ```    
	systemctl start service-name
    ```
6. If looking at the journal and checking the status of services does not resolve your error, run the following `systemd-analyze` commands to examine the boot time and the speed with which services start.
	
    ```
	systemd-analyze time
	systemd-analyze blame
	systemd-analyze critical-chain
    ```

 
**Note**: The output of these commands might be misleading because one service might just be waiting for another service to finish initializing.
