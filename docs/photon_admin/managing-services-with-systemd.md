# Managing Services with systemd

Photon OS manages services with `systemd`. By using `systemd`, Photon OS adopts a contemporary Linux standard to bootstrap the user space and concurrently start services. This is an architecture that differs from traditional Linux systems such as SUSE Linux Enterprise Server. 

A traditional Linux system contains an initialization system called SysVinit. With SLES 11, for instance, the SysVinit-style init programs control how the system starts up and shuts down. Init implements system runlevels. A SysVinit runlevel defines a state in which a process or service runs. 

In contrast to a SysVinit system, `systemd` defines no such runlevels. Instead, `systemd` uses a dependency tree of targets to determine which services to start when. Combined with the declarative nature of `systemd` commands, `systemd` targets reduce the amount of code needed to run a command, leaving you with code that is easier to maintain and probably faster to execute. For an overview of `systemd`, see [systemd System and Service Manager](https://www.freedesktop.org/wiki/Software/systemd/) and the [man page for systemd](https://www.freedesktop.org/software/systemd/man/systemd.html).

On Photon OS, you must manage services with systemd and `systemctl`, its command-line utility for inspecting and controlling the system, and not the deprecated commands of `init.d`. 

For more information, see the index of all the systemd man pages, including systemctl, at the following URL: 

[https://www.freedesktop.org/software/systemd/man/](https://www.freedesktop.org/software/systemd/man/)