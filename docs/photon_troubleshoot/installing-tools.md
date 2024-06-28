# Installing Tools from Repositories

You can install several troubleshooting tools from the Photon OS repositories by using the default package management system, `tdnf`. 

If a tool you require is not installed, search the repositories to see if it is available. 

For example, the traceroute tool is not installed by default. You can search for it in the repositories as follows:   

	tdnf search traceroute
	traceroute : Traces the route taken by packets over an IPv4/IPv6 network

The results of the above command show that traceroute exists in the repository. You install it with `tdnf`: 

	tdnf install traceroute

The following tools are not installed by default but are in the repository and can be installed with `tdnf`: 

* `net-tools`. Networking tools.
* `ltrace`. Tool for intercepting and recording dynamic library calls. It can identify the function an application was calling when it crashed, making it useful for debugging.
* `nfs-utils`. Client tools for the kernel Network File System, or NFS, including showmount. These are installed by default in the full version of Photon OS but not in the minimal version. 
* `pcstat`. A tool that inspects which pages of a file or files are being cached by the Linux kernel.
* `sysstat` and `sar`. Utilities to monitor system performance and usage activity. Installing sysstat also installs sar.
* `systemtap` and `crash`. The systemtap utility is a programmable instrumentation system for diagnosing problems of performance or function. Installing systemtap also installs crash, which is a kernel crash analysis utility for live systems and dump files.
* `dstat`. Tool for viewing and analyzing statistics about system resources.

    The `dstat` tool can help troubleshoot system performance. The tool shows live, running list of statistics about system resources: 
    
    	dstat
    	You did not select any stats, using -cdngy by default.
    	----total-cpu-usage---- -dsk/total- -net/total- ---paging-- ---system--
    	usr sys idl wai hiq siq| read  writ| recv  send|  in   out | int   csw
    	  1   0  98   1   0   0|4036B   42k|   0     0 |   0     0 |  95   276
    	  1   0  98   1   0   0|   0    64k|  60B  940B|   0     0 | 142   320
    	  1   1  98   0   0   0|   0    52k|  60B  476B|   0     0 | 149   385
