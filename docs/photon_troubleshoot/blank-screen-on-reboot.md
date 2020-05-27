# Blank Screen on Reboot

If the Photon OS kernel enters a state of panic during a reboot and all you see is a blank screen, note the name of the virtual machine running Photon OS and then power off the VM. 

In the host, open the `vmware.log` file for the VM. When a kernel panics, the guest VM prints the entire kernel log in  `vmware.log` in the host directory containing the VM. This log file contains the output of the `dmesg` command from the guest, and you can analyze it to help identify the cause of the boot problem. 

**Example**

After searching for `Guest:` in the following abridged `vmware.log`, this line appears, identifying the root cause of the reboot problem: 

    	
    ```
    2016-08-30T16:02:43.220-07:00| vcpu-0| I125: Guest: 
    	<0>[1.125804] Kernel panic - not syncing: 
    	VFS: Unable to mount root fs on unknown-block(0,0)
    ```

Further inspection finds the following lines: 

	2016-08-30T16:02:43.217-07:00| vcpu-0| I125: Guest: 
	<4>[    1.125782] VFS: Cannot open root device "sdc1" or unknown-block(0,0): error -6
	2016-08-30T16:02:43.217-07:00| vcpu-0| I125: Guest: 
	<4>[    1.125783] Please append a correct "root=" boot option; 
	here are the available partitions: 
	2016-08-30T16:02:43.217-07:00| vcpu-0| I125: Guest: 
	<4>[    1.125785] 0100            4096 ram0  (driver?)
	...
	0800         8388608 sda  driver: sd
	2016-08-30T16:02:43.220-07:00| vcpu-0| I125: Guest: 
	<4>[    1.125802]   0801         8384512 sda1 611e2d9a-a3da-4ac7-9eb9-8d09cb151a93
	2016-08-30T16:02:43.220-07:00| vcpu-0| I125: Guest: 
	<4>[    1.125803]   0802            3055 sda2 8159e59c-b382-40b9-9070-3c5586f3c7d6

In this unlikely case, the GRUB configuration points to a root device named `sdc1` instead of the correct root device, `sda1`. You can resolve the problem by restoring the GRUB GNU edit screen and the GRUB configuration file (`/boot/grub/grub.cfg`) to their original configurations. 
