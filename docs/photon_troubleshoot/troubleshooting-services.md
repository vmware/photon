# Troubleshooting Services With 'systemctl`

To view a description of all the active, loaded units, execute the systemctl command without any options or arguments: 

	systemctl

To see all the loaded, active, and inactive units and their description, run this command: 

	systemctl --all

To see all the unit files and their current status but no description, run this command: 

	systemctl list-unit-files

The `grep` command filters the services by a search term, a helpful tactic to recall the exact name of a unit file without looking through a long list of names. Example: 

	systemctl list-unit-files | grep network
	org.freedesktop.network1.busname           static
	dbus-org.freedesktop.network1.service      enabled
	systemd-networkd-wait-online.service       enabled
	systemd-networkd.service                   enabled
	systemd-networkd.socket                    enabled
	network-online.target                      static
	network-pre.target                         static
	network.target  


For example, to list all the services that you can manage on Photon OS, you run the following command instead of `ls /etc/rc.d/init.d/`: 

	systemctl list-unit-files --type=service

Similarly, to check whether the `sshd` service is enabled, on Photon OS you run the following command instead of `chkconfig sshd`:

	systemctl is-enabled sshd

The `chkconfig --list` command that shows which services are enabled for which runlevel on a SysVinit computer becomes substantially different on Photon OS because there are no runlevels, only targets: 

	ls /etc/systemd/system/*.wants

You can also display similar information with the following command: 

	systemctl list-unit-files --type=service

The following is list of some of the systemd commands that take the place of `SysVinit` commands on Photon OS: 

	USE THIS SYSTEMD COMMAND 	INSTEAD OF THIS SYSVINIT COMMAND
	systemctl start sshd 		service sshd start
	systemctl stop sshd 		service sshd stop
	systemctl restart sshd 		service sshd restart
	systemctl reload sshd 		service sshd reload
	systemctl condrestart sshd 	service sshd condrestart
	systemctl status sshd 		service sshd status
	systemctl enable sshd 		chkconfig sshd on
	systemctl disable sshd 		chkconfig sshd off
	systemctl daemon-reload		chkconfig sshd --add
