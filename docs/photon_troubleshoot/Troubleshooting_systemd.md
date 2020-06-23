# systemd

systemd is a suite of basic building blocks for a Linux system. It provides a system and service manager that runs as Process ID 1 and starts the rest of the system.

To manage the services run the following commands:

- `systemctl` or `systemctl list-units` : This command lists the running units.
- `systemctl --failed` : This command lists failed units.
- `systemctl list-unit-files` : This command lists all the installed unit files. The unit files are usually present in **/usr/lib/systemd/system/** and **/etc/systemd/system/**.
- `systemctl status pid` : This command displays the cgroup slice, memory and parent for a PID.
- `systemctl start unit` : This command starts a unit immediately.
- `systemctl stop unit` : This command stops a unit.
- `systemctl restart unit` : This command restarts a unit.
- `systemctl reload unit` : This command asks a unit to reload its configuration.
- `systemctl status unit` : This command displays the status of a unit.
- `systemctl enable unit` : This command enables a unit to run on startup.
- `systemctl enable --now unit` : This command enables a unit to run on startup and start immediately.
- `systemctl disable unit` : This command disables a unit and removes it from the startup program.
- `systemctl mask unit` : This command masks a unit to make it impossible to start.
- `systemctl unmask unit` : This command unmasks a unit.

To get an overview of the system boot-up time, run the following command:
```
systemd-analyze
```

To view a list of all running units, sorted by the time they took to initialize (highest time on top), run the following command:
```
systemd-analyze blame
```
