# Checking Firewall Rules

The design of Photon OS emphasizes security. On the minimal and full versions of Photon OS, the default security policy turns on the firewall and drops packets from external interfaces and  applications. As a result, you might need to add rules to iptables to permit forwarding, allow protocols like HTTP, and open ports. In other words, you must configure the firewall for your applications and requirements. 

The default iptables settings on the full version look like this:

	iptables --list
	Chain INPUT (policy DROP)
	target     prot opt source               destination
	ACCEPT     all  --  anywhere             anywhere
	ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
	ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:ssh

	Chain FORWARD (policy DROP)
	target     prot opt source               destination

	Chain OUTPUT (policy DROP)
	target     prot opt source               destination
	ACCEPT     all  --  anywhere             anywhere


To find out how to adjust the settings, see the man page for iptables. 

Although the default iptables policy accepts SSH connections, the `sshd` configuration file on the full version of Photon OS is set to reject SSH connections. See [Permitting Root Login with SSH](permitting-root-login-with-ssh.md).

If you are unable to ping a Photon OS machine, check the firewall rules. Verify if the rules allow connectivity for the port and protocol. 

You can supplement the `iptables` commands by using `lsof` to, for instance, see the processes listening on ports: 

	lsof -i -P -n
