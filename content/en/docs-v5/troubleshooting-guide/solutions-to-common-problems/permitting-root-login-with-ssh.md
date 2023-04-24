---
title:  Permitting Root Login with SSH
weight: 4
---

The full version of Photon OS prevents root login with SSH by default. To permit root login over SSH, open `/etc/ssh/sshd_config` with the vim text editor and set `PermitRootLogin` to `yes`. 

Vim is the default text editor available in Photon OS. The developer version also contains Nano. After you modify the SSH daemon's configuration file, you must restart the sshd daemon for the changes to take effect. 

Example: 

```console
vim /etc/ssh/sshd_config
```
```ini
# override default of no subsystems
Subsystem       sftp    /usr/libexec/sftp-server

# Example of overriding settings on a per-user basis
#Match User anoncvs
#       X11Forwarding no
#       AllowTcpForwarding no
#       PermitTTY no
#       ForceCommand cvs server
PermitRootLogin yes
UsePAM yes
```

Save your changes in vim and then restart the sshd daemon: 

```console
systemctl restart sshd
```

You can then connect to the Photon OS machine with the root account over SSH:

```console
user@ubuntu:~$ ssh root@10.0.0.131
```
