# Kernel Log Replication with VProbes

Replicating the Photon OS kernel logs on the VMware ESXi host is an advanced but powerful method of troubleshooting a kernel problem. 


- [Replication Method](#replication-method)
- [Using VProbes Script with a Hard-Coded Address](#using-vprobes-script- with-a-hard-coded-address)
- [A Reusable VProbe Script Using the kallsyms File](#a-reusable-vprobe-script-using-the-kallsyms-file)

## Replication Method

This method is applicable when the virtual machine running Photon OS is hanging or inaccessible because, for instance, the hard disk has failed.

As a prerequisite, you must have preemptively enabled the VMware VProbes facility on the VM before an error rendered it inaccessible. You must also create a VProbes script on the ESXi host, but you can do that after the error. 

The method is useful in analyzing kernel issues when testing an application or appliance that is running on Photon OS.   

There are two similar ways in which you can replicate the Photon OS kernel logs on ESXi by using VProbes. 

- The first modifies the VProbes script so that it works only for the VM that you set. It uses a hard-coded address.

- The second uses an abstraction instead of a hard-coded address so that the same VProbes script can be used for any VM on an ESXi host that you have enabled for VProbe and copied its kernel symbol table (kallsyms) to ESXi.

For more information on VMware VProbes, see [VProbes: Deep Observability Into the ESXi Hypervisor](https://labs.vmware.com/vmtj/vprobes-deep-observability-into-the-esxi-hypervisor) and the [VProbes Programming Reference](http://www.vmware.com/pdf/ws7_f3_vprobes_reference.pdf).

## Using VProbes Script with a Hard-Coded Address

Perform the following steps to set a VProbe for an individual VM: 

1. Power off the VM so that you can turn on the VProbe facility. 

    Edit the `.vmx` configuration file for the VM. The file resides in the directory that contains the VM in the ESXi data store. Add the following line of code to the `.vmx` file and then power the VM on:
    
    	vprobe.enable = "TRUE"
    
    When you edit the `.vmx` file to add the above line of code, you must first turn off the VM--otherwise, your changes will not persist. 

1. Obtain the kernel `log_store` function address by connecting to the VM with SSH and running the following commands as root. 

    Photon OS uses the `kptr_restrict` setting to place restrictions on the kernel addresses exposed through `/proc` and other interfaces. This setting hides exposed kernel pointers to prevent attackers from exploiting kernel write vulnerabilities. When you are done using VProbes, you should return `kptr_restrict` to the original setting of `2` by rebooting.)
    
    	echo 0 > /proc/sys/kernel/kptr_restrict
    	grep log_store /proc/kallsyms
    
    The output of the `grep` command will look similar to the following string. The first set of characters (without the `t`) is the log_store function address:
    
    	ffffffff810bb680 t log_store

1. Connect to the ESXi host with SSH so that you can create a VProbes script. 

    Below is the template for the script. `log_store` in the first line is a placeholder for the VM's log_store function address:
    	
    ```
    GUEST:ENTER:log_store {
        	   string dst;
        	   getgueststr(dst, getguest(RSP+16) & 0xff, getguest(RSP+8));
        	   printf("%s\n", dst);
        	}
    ```

    On the ESXi host, create a new file, add the template to it, and then change `log_store` to the function address that was the output from the grep command on the VM. 

1. Add a `0x` prefix to the function address. In this example, the modified template looks like this:
	
    ```
    GUEST:ENTER:0xffffffff810bb680 {
    	   string dst;
    	   getgueststr(dst, getguest(RSP+16) & 0xff, getguest(RSP+8));
    	   printf("%s\n", dst);
    	}
    ```

1. Save your VProbes script as `console.emt` in the `/tmp` directory. (The file extension for VProbe scripts is `.emt`.)

    While still connected to the ESXi host with SSH, run the following command to obtain the ID of the virtual machine that you want to troubleshoot: 
    
    	vim-cmd vmsvc/getallvms
    
    This command lists all the VMs running on the ESXi host. Find the VM you want to troubleshoot in the list and make a note of its ID. 

1. Run the following command to print all the kernel messages from Photon OS in your SSH console; replace `<VM ID>` with the ID of your VM:

	`vprobe -m <VM ID> /tmp/console.emt`

    When you're done, type `Ctrl-C` to stop the loop. 

## A Reusable VProbe Script Using the kallsyms File

Perform the following steps to create one VProbe script and use for all the VMs on your ESXi host. 

1. Power off the VM and turn on the VProbe facility on each VM that you want to be able to analyze. 

    Add `vprobe.enable = "TRUE"` to the VM's `.vmx` configuration file. See the instructions above.

1. Power on the VM, connect to it with SSH, and run the following command as root:
	
	   `echo 0 > /proc/sys/kernel/kptr_restrict`

1. Connect to the ESXi host with SSH to create the following VProbes script and save it as `/tmp/console.emt`:
	
    ```
    GUEST:ENTER:log_store {
    	   string dst;
    	   getgueststr(dst, getguest(RSP+16) & 0xff, getguest(RSP+8));
    	   printf("%s\n", dst);
    	}
    ```

1. From the ESXi host, run the following command to copy the VM's `kallysms` file to the `tmp` directory on the ESXi host:

	   `scp root@<vm ip address>:/proc/kallsyms /tmp`

    While still connected to the ESXi host with SSH, run the following command to obtain the ID of the virtual machine that you want to troubleshoot: 
    
    	`vim-cmd vmsvc/getallvms`
    
    This command lists all the VMs running on the ESXi host. Find the VM you want to troubleshoot in the list and make a note of its ID. 

1. Run the following command to print all the kernel messages from Photon OS in your SSH console.

    Replace `<VM ID>` with the ID of your VM. When you're done, type `Ctrl-C` to stop the loop.

	`vprobe -m <VM ID> -k /tmp/kallysyms /tmp/console.emt`

    You can use a directory other than `tmp` if you want.

<!--
### Deep Kernel Analysis with the Crash Utility

-->

<!-- 

### Go to the Debug Shell

‘ panic=1 init=/bin/bash’
mount –o rw,remount /
cd /lib/systemd/system/multi-user.target.wants
ln –s ../debug-shell.service
umount /
sync
exit

After reboot debug-shell will be available on tty9. No password required.

-->