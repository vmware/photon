**Installing the Lightwave Server and Configuring It as a Domain Controller on a Photon Image**

You can configure Lightwave server as domain controller on a Photon client. You install the Lightwave server first. After the server is installed, you configure a new domain. 

**Prerequisites**

- Prepare a Photon OS client for the Lightwave server installation.
- Verify that the hostname of the client can be resolved.
- Verify that you have 500 MB free for the Lightwave server installation.

**Procedure**

1. Log in to your Photon OS client over SSH as an administrator.
2. Install the Lightwave server by running the following command. 
	
	`# tdnf install lightwave -y`
3. Configure the Lightwave server as domain controller by selecting a domain name and password for the `administrator` user.
	
	The minimum required password complexity is 8 characters, one symbol, one upper case letter, and one lower case letter. 
	Optionally, if you want to access the domain controller over IP, configure the ip under the `--ssl-subject-alt-name` parameter.
	`# configure-lightwave-server --domain <your-domain> --password '<administrator-user-password>' --ssl-subject-alt-name <machine-ip-address>`
4. Edit `iptables` rules to allow connections to and from the client.

	The default Photon OS 2.0 firewall settings block all incoming, outgoing, and forwards so that you must reconfigure them.
	
	`# iptables -P INPUT ACCEPT`

	`# iptables -P OUTPUT ACCEPT`

	`# iptables -P FORWARD ACCEPT`

5. In a browser, go to https://*lightwave-server-FQDN* to verify that you can log in to the newly created domain controller.
	1. On the Cascade Identity Services page, enter the domain that you configured and click **Take me to Lightwave Admin**.
	2. On the Welcome page, enter administrator@your-domain as user name and the password that you set during the domain controller configuration and click **LOGIN**.