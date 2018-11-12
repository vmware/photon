# Inspecting the Status of Network Links with `networkctl`

The `networkctl` command shows information about network connections that helps you configure networking services and troubleshoot networking problems. You can, for example, progressively add options and arguments to the `networkctl` command to move from general information about network connections to specific information about a network connection. 

Running `networkctl` without options defaults to the list command:  

	networkctl
	IDX LINK             TYPE               OPERATIONAL SETUP
	  1 lo               loopback           carrier     unmanaged
	  2 eth0             ether              routable    configured
	  3 docker0          ether              routable    unmanaged
	 11 vethb0aa7a6      ether              degraded    unmanaged
	 4 links listed.

Running `networkctl` with the status command displays information that looks like this; you can see that there are active network links with IP addresses for not only the Ethernet connection but also a Docker container. 

	root@photon-rc [ ~ ]# networkctl status
	*      State: routable
	     Address: 198.51.100.131 on eth0
	              172.17.0.1 on docker0
	              fe80::20c:29ff:fe55:3ca6 on eth0
	              fe80::42:f0ff:fef7:bd81 on docker0
	              fe80::4c84:caff:fe76:a23f on vethb0aa7a6
	     Gateway: 198.51.100.2 on eth0
	         DNS: 198.51.100.2

You can then add a network link, such as the Ethernet connection, as the argument of the status command to show specific information about the link: 

	root@photon-rc [ ~ ]# networkctl status eth0
	* 2: eth0
	       Link File: /usr/lib/systemd/network/99-default.link
	    Network File: /etc/systemd/network/99-dhcp-en.network
	            Type: ether
	           State: routable (configured)
	            Path: pci-0000:02:01.0
	          Driver: e1000
	      HW Address: 00:0c:29:55:3c:a6 (VMware, Inc.)
	             MTU: 1500
	         Address: 198.51.100.131
	                  fe80::20c:29ff:fe55:3ca6
	         Gateway: 198.51.100.2
	             DNS: 198.51.100.2
	        CLIENTID: ffb6220feb00020000ab116724f520a0a77337

And you can do the same thing with the Docker container: 

	networkctl status docker0
	* 3: docker0
	       Link File: /usr/lib/systemd/network/99-default.link
	    Network File: n/a
	            Type: ether
	           State: routable (unmanaged)
	          Driver: bridge
	      HW Address: 02:42:f0:f7:bd:81
	             MTU: 1500
	         Address: 172.17.0.1
	                  fe80::42:f0ff:fef7:bd81

In the example above, it is OK that the state of the Docker container is unmanaged; Docker handles managing the networking for the containers without using systemd-resolved or systemd-networkd. Instead, Docker manages the container's connection by using its bridge drive.

For more information about `networkctl` commands and options, see https://www.freedesktop.org/software/systemd/man/networkctl.html.