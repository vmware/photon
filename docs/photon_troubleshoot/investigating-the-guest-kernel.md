# Investigating the Guest Kernel

If a VM running Photon OS and an application or virtual appliance is behaving preventing you from logging in to the machine, you can troubleshoot by extracting the kernel logs from the guest's memory and analyzing them with `gdb`. 

This advanced troubleshooting method works when you are running Photon OS as the operating system for an application or appliance on VMware Workstation, Fusion, or ESXi. The procedure in this section assumes that the virtual machine running Photon OS is functioning normally. 

The process to use this troubleshooting method varies by environment. The examples in this section assume that the troublesome Photon OS virtual machine is running in VMware Workstation 12 Pro on a Microsoft Windows 8 Enterprise host. The examples also use an additional, fully functional Photon OS virtual machine running in Workstation.

You can use other hosts, hypervisors, and operating systems--but you will have to adapt the example process below to them. Directory paths, file names, and other aspects might be different on other systems. 

- [Prerequisites](#prerequisites)
- [Procedure Overview](#procedure-overview)
- [Procedure](#procedure)

## Prerequisites

Verify that you have the following resources: 

* Root access to a Linux machine other than the one you are troubleshooting. It can be another Photon OS machine, Ubuntu, or another Linux variant. 
* The `vmss2core` utility from VMware. It is installed by default in VMware Workstation and some other VMware products. If your system doesn't already contain it, you can download it for free from https://labs.vmware.com/flings/vmss2core.
* A local copy of the Photon OS ISO of the exact same version and release number as the Photon OS machine that you are troubleshooting. 

## Procedure Overview

The process to apply this troubleshooting method is as follows:

- On a local computer, you open a file on the Photon OS ISO that contains Linux debugging information. Then you suspend the troublesome Photon OS VM and extract the kernel memory logs from the VMware hypervisor running Photon OS.
- Next, you use the vmss2core tool to convert the memory logs into core dump files. The vmss2core utility converts VMware checkpoint state files into formats that third-party debugging tools understand. It can handle both suspend (.vmss) and snapshot (.vmsn) checkpoint state files (hereafter referred to as a _vmss file_) as well as monolithic and non-monolithic (separate .vmem file) encapsulation of checkpoint state data. See [Debugging Virtual Machines with the Checkpoint to Core Tool](http://www.vmware.com/pdf/snapshot2core_technote.pdf).
- Finally, you prepare to run the gdb tool by using the debug info file from the ISO to create a `.gdbinit` file, which you can then analyze with the gdb shell on your local Linux machine.

All three components must be in the same directory on a Linux machine.  

## Procedure

1. Obtain a local copy of the Photon OS ISO of the exact same version and release number as the Photon OS machine that you are troubleshooting and mount the ISO on a Linux machine (or open it on a Windows machine):

	   mount /mnt/cdrom

1. Locate the following file. (If you opened the Photon OS ISO on a Windows computer, copy the following file to the root folder of a Linux machine.)

	   /RPMS/x86_64/linux-debuginfo-4.4.8-6.ph1.x86_64.rpm

1. On a Linux machine, run the following `rpm2cpio` command to convert the RPM file to a cpio file and to extract the contents of the RPM to the current directory:
	
    ```
    rpm2cpio /mnt/cdrom/RPMS/x86_64/linux-debuginfo-4.4.8-6.ph1.x86_64.rpm | cpio -idmv
    ```

1. From the extracted files, copy the following file to your current directory:

    ```
    cp usr/lib/debug/lib/modules/4.4.8/vmlinux-4.4.8.debug
    ```

1. Run the following command to download the dmesg functions that will help extract the kernel log from the coredump: 

    ```
    wget https://www.kernel.org/doc/Documentation/kdump/gdbmacros.txt
    wget https://github.com/vmware/photon/blob/master/tools/scripts/gdbmacros-for-linux.txt
    ```

1. Move the file as follows:
	
    ```
    mv gdbmacros-for-linux.txt .gdbinit
    ```

1. Switch to your host machine so you can get the kernel memory files from the VM. Suspend the troublesome VM and locate the `.vmss` and `.vmem` files in the virtual machine's directory on the host. 

    Example:
	
    ```
    C:\Users\tester\Documents\Virtual Machines\VMware Photon 64-bit (7)>dir
    	 Volume in drive C is Windows
    	 Directory of C:\Users\tester\Documents\Virtual Machines\VMware Photon 64-bit
    	 (7)
    	09/20/2016  12:22 PM    <DIR>          .
    	09/20/2016  12:22 PM    <DIR>          ..
    	09/19/2016  03:39 PM       402,653,184 VMware Photon 64-bit (7)-f6b070cd.vmem
    	09/20/2016  12:11 PM         5,586,907 VMware Photon 64-bit (7)-f6b070cd.vmss
    	09/20/2016  12:11 PM     1,561,001,984 VMware Photon 64-bit (7)-s001.vmdk
    	...
    	09/20/2016  12:11 PM           300,430 vmware.log
    	...
    ```

1. Now that you have located the `.vmss` and `.vmem` files, convert them to one or more core dump files by using the vmss2core tool that comes with Workstation. Here is an example of how to run the command. Be careful with your pathing, escaping, file names, and so forth--all of which might be different from this example on your Windows machine.

    ```
    
    	C:\Users\shoenisch\Documents\Virtual Machines\VMware Photon 64-bit (7)>C:\"Program Files (x86)\VMware\VMware Workstation"\vmss2core.exe "VMware Photon 64-bit (7)-f6b070cd.vmss" "VMware Photon 64-bit (7)-f6b070cd.vmem"
    
    The result of this command is one or more files with a `.core` extension plus a digit. Truncated example: 
    
    	C:\Users\tester\Documents\Virtual Machines\VMware Photon 64-bit (7)>dir
    	 Directory of C:\Users\tester\Documents\Virtual Machines\VMware Photon 64-bit(7)
    	09/20/2016  12:22 PM       729,706,496 vmss.core0
    ```

1. Copy the `.core` file or files to the your current directory on the Linux machine where you so that you can analyze it with gdb.

    Run the following `gdb` command to enter the gdb shell attached to the memory core dump file. You might have to change the name of the `vmss.core` file in the example to match your `.core` file:

	
```
gdb vmlinux-4.4.8.debug vmss.core0

	GNU gdb (GDB) 7.8.2
	Copyright (C) 2014 Free Software Foundation, Inc.
	License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
	This is free software: you are free to change and redistribute it. 
	There is NO WARRANTY, to the extent permitted by law. ...
	Type "show configuration" for configuration details.
	For bug reporting instructions, please see:
	<http://www.gnu.org/software/gdb/bugs/>.
	Find the GDB manual and other documentation resources online at: <http://www.gnu.org/software/gdb/documentation/>.
	For help, type "help".
	Type "apropos word" to search for commands related to "word"...
	Reading symbols from vmlinux-4.4.8.debug...done.
	warning: core file may not match specified executable file.
	[New LWP 12345]
	Core was generated by `GuestVM'.
	Program terminated with signal SIGSEGV, Segmentation fault.
	#0  0xffffffff813df39a in insb (count=0, addr=0xffffc90000144000, port=<optimized out>)
	    at arch/x86/include/asm/io.h:316
	316     arch/x86/include/asm/io.h: No such file or directory.
	(gdb)
```

**Result** 

In the results above, the _(gdb)_ of the last line is the prompt of the gdb shell. You can now analyze the core dump by using commands like `bt`, to perform a backtrace, and `dmesg`, to view the Photon OS kernel log and see Photon OS kernel error messages.

