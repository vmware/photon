# Controlling Services

To control services on Photon OS, use `systemctl` command. 

For example, instead of running the `/etc/init.d/ssh` script to stop and start the OpenSSH server on a init.d-based Linux system, run the following `systemctl` commands on Photon OS: 

	systemctl stop sshd
	systemctl start sshd

The systemctl tool includes a range of commands and options for inspecting and controlling the state of systemd and the service manager. For more information, see the [systemctl man page](https://www.freedesktop.org/software/systemd/man/systemctl.html).
