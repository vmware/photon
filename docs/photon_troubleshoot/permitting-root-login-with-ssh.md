# Permitting Root Login with SSH

The full version of Photon OS prevents root login with SSH by default. To permit root login over SSH, open `/etc/ssh/sshd_config` with the vim text editor and set `PermitRootLogin` to `yes`. 

Vim is the default text editor available in both the full and minimal versions of Photon OS. The full version also contains Nano. After you modify the SSH daemon's configuration file, you must restart the sshd daemon for the changes to take effect. Example: 

	vim /etc/ssh/sshd_config

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

Save your changes in vim and then restart the sshd daemon: 

	systemctl restart sshd

You can then connect to the Photon OS machine with the root account over SSH:

	steve@ubuntu:~$ ssh root@198.51.100.131
