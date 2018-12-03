#  Troubleshooting Progression

If you encounter a problem running an application or appliance on Photon OS and you suspect it involves the operating system, you can troubleshoot by proceeding as follows. 

1. Check the services running on Photon OS:

	`systemctl status`

1. Check your application log files for errors. For VMware applications, see [Location of Log Files for VMware Products](https://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1021806).)

1. Check the service controller or service monitor for your application or appliance.

1. Check the network interfaces and other aspects of the network service with `systemd-network` commands.

1. Check the operating system log files:

	`journalctl`

    Next, run the following commands to view all services according to the order in which they were started:

	`systemd-analyze critical-chain`

1. Use the troubleshooting tool that you think is most likely to help with the issue at hand. For example, use `strace` to identify the location of the failure. 
