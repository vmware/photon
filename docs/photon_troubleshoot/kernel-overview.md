# Kernel Overview

You can use `dmesg` command to troubleshooting kernel errors. The `dmesg` command prints messages from the kernel ring buffer. 

The following command, for example, presents kernel messages in a human-readable format: 

	dmesg --human --kernel

To examine kernel messages as you perform actions, such as reproducing a problem, in another terminal, you can run the command with the `--follow` option, which waits for new messages and prints them as they occur: 

	dmesg --human --kernel --follow

The kernel buffer is limited in memory size. As a result, the kernel cyclically overwrites the end of the information in the buffer from which `dmesg` pulls information. The systemd journal, however, saves the information from the buffer to a log file so that you can access older information. 

To view it, run the following command: 

	journalctl -k

If required, you can check the modules that are loaded on your Photon OS machine by running the `lsmod` command. For example:  

	lsmod
	Module                  Size  Used by
	vmw_vsock_vmci_transport    28672  1
	vsock                  36864  2 vmw_vsock_vmci_transport
	coretemp               16384  0
	hwmon                  16384  1 coretemp
	crc32c_intel           24576  0
	hid_generic            16384  0
	usbhid                 28672  0
	hid                   106496  2 hid_generic,usbhid
	xt_conntrack           16384  1
	iptable_nat            16384  0
	nf_conntrack_ipv4      16384  2
	nf_defrag_ipv4         16384  1 nf_conntrack_ipv4
	nf_nat_ipv4            16384  1 iptable_nat
	nf_nat                 24576  1 nf_nat_ipv4
	iptable_filter         16384  1
	ip_tables              24576  2 iptable_filter,iptable_nat
	