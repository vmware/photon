# Creating a Startup Service

Use `systemd` to create a sratup service. 

The following example shows you how to create a systemd startup service that changes the maximum transmission unit (MTU) of the default Ethernet connection, `eth0`.

1. Concatenate the following block of code into a file:
	
	
```
cat << EOF >> /lib/systemd/system/eth0.service
	[Unit]
	Description=Network interface initialization
	After=local-fs.target network-online.target network.target
	Wants=local-fs.target network-online.target network.target

	[Service]
	ExecStart=/usr/sbin/ifconfig eth0 mtu 1460 up
	Type=oneshot

	[Install]
	WantedBy=multi-user.target
	EOF
```

1. Set the service to auto-start when the system boots:
	
```
cd /lib/systemd/system/multi-user.target.wants/
	ln -s ../eth0.service eth0.service
```

