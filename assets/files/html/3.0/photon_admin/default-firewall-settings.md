# Default Firewall Settings

The design of Photon OS emphasizes security. On the minimal and full versions of Photon OS, the default security policy turns on the firewall and drops packets from external interfaces and  applications. As a result, you might need to add rules to iptables to permit forwarding, allow protocols like HTTP, and open ports. You must configure the firewall for your applications and requirements. 

The default iptables on the full version have the following settings:

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

For more information on how to change the settings, see the man page for iptables. 

Although the default iptables policy accepts SSH connections, the `sshd` configuration file on the full version of Photon OS is set to reject SSH connections. See [Permitting Root Login with SSH](../photon_troubleshoot/permitting-root-login-with-ssh.md).

If you are unable to ping a Photon OS machine, check the firewall rules. To verify if the rules allow connectivity for the port and protocol, change the `iptables` commands by using `lsof` commands to see the processes listening on ports: 

    lsof -i -P -n