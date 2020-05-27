# Systemd

Photon OS manages services with `systemd` and `systemctl`, its command-line utility for inspecting and controlling the system. It does not use the deprecated commands of `init.d`. 

Basic system administration commands on Photon OS differ from those on operating systems that use SysVinit. Since Photon OS uses systemd instead of SysVinit, you must use systemd commands to manage services. 

For example, instead of running the /etc/init.d/ssh script to stop and start the OpenSSH server on a init.d-based Linux system, you control the service by running the following systemctl commands on Photon OS: 

	systemctl stop sshd
	systemctl start sshd

- [Enabling `systemd` Debug Shell During Boot](enabling-systemd-debug.md) 
- [Troubleshooting Services with `systemctl`](troubleshooting-services.md)
- [Analyzing System Logs with `journalctl`](analyzing-system-logs-with-journalctl.md)
- [Inspecting Services with `systemd-analyze`](inspecting-services-with-systemd-analyze.md)

For an overview of systemd, see [systemd System and Service Manager](https://www.freedesktop.org/wiki/Software/systemd/) and the [man page for systemd](https://www.freedesktop.org/software/systemd/man/systemd.html). The systemd man pages are listed at [https://www.freedesktop.org/software/systemd/man/](https://www.freedesktop.org/software/systemd/man/).



