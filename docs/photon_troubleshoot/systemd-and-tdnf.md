# Systemd and TDNF

By using systemd, Photon OS adopts a contemporary Linux standard to bootstrap the user space and concurrently start services, an architecture that differs from traditional Linux systems such as SUSE Linux Enterprise Server 11.

A traditional Linux system contains an initialization system called SysVinit. With SLES 11, for instance, SysVinit-style init programs control how the system starts up and shuts down. Init implements system runlevels. A SysVinit runlevel defines a state in which a process or service runs. In contrast to a SysVinit system, systemd defines no such runlevels. Instead, systemd uses a dependency tree of _targets_ to determine which services to start when.

Because the systemd commands differ from those of an init.d-based Linux system, a section later in this guide illustrates how to troubleshoot by using systemctl commands instead of init.d-style commands. 

Tdnf keeps the operating system as small as possible while preserving yum's robust package-management capabilities. On Photon OS, tdnf is the default package manager for installing new packages. Since troubleshooting with tdnf differs from using yum, a later section of this guide describes how to solve problems with packages and repositories by using tdnf commands.
