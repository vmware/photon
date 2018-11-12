# Viewing Services 

To view a description of all the loaded and active units, run the `systemctl` command without any options or arguments: 

	systemctl

To see all the loaded, active, and inactive units and their description, run the following command: 

	systemctl --all

To see all the unit files and their current status but no description, run thie following command: 

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
	network.target                             static