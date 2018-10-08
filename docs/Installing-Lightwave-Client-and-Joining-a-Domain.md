# Installing the Lightwave Client on a Photon Image and Joining the Client to a Domain

After you have set up a Lightwave domain controller, you can join Photon clients to that domain. You install the Lightwave client first. After the client is installed, you join the client to the domain.

## Prerequisites

- Prepare a Photon OS client for the Lightwave client installation.
- Verify that the hostname of the client can be resolved.
- Verify that you have 184 MB free for the Lightwave client installation.

## Procedure

1. Log in to your Photon OS client over SSH.
2. Install the Lightwave client by running the following command. 
	
	`# tdnf install lightwave-client -y`

3. Edit the `iptables` firewall rules configuration file to allow connections on port `2020` as a default setting.
	
	The default Photon OS 2.0 firewall settings block all incoming, outgoing, and forwards so that you must configure the rules.

	1. Open the  iptables settings file.
	
	`# vi /etc/systemd/scripts/iptables`

	2. Add allow information over tcp for port 2020 in the end of the file, save, and close the file.

	`iptables -A INPUT -p tcp -m tcp --dport 2020 -j ACCEPT`

	3. Run the following command to allow the required connections without restarting the client.

	`# iptables -A INPUT -p tcp -m tcp --dport 2020 -j ACCEPT`

4. Join the client to the domain by running the `domainjoin.sh` script and configuring the domain controller FQDN, domain, and the password for the `administrator` user.

	`# domainjoin.sh --domain-controller <lightwave-server-FQDN> --domain <your-domain> --password '<administrator-user-password>`

5. In a browser, go to https://*Lightwave-Server-FQDN* to verify that the client appears under the tenants list for the domain.