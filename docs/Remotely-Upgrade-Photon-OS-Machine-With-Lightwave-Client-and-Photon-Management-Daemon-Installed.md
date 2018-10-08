**Remotely Upgrade Multiple Photon OS Machines With Lightwave Client and Photon Management Daemon Installed**

After you have a configured the Photon Management Daemon (PMD) on multiple machines, you can remotely upgrade any installed package on these machines.

Upgrade process uses `copenapi_cli` that is supported from both Lightwave and Photon Management Daemon. You can initiate the upgrade process from any machine that has Photon Management Daemon installed.   

**Prerequisites**

- Have an installed Lightwave server with configured domain controller on it.
- Have installed Lightwave clients that are joined to the domain.
- Have installed Photon Management Daemon on the clients.

**Procedure**

1. To initiate remote upgrade, log in to a Photon OS machine over SSH to install the Photon Management Daemon CLI.

	`# tdnf install pmd-cli` 
2. Edit the `copenapi_cli` spec files so that you can specify the machines you want to upgrade and credentials to be used.
	1. Edit the `.netrc` file to specify machines to be upgraded and credentials for the PMD service.

		`# vi ~/.netrc`  
	2. In the file, enter the IP addresses for the machines and administrative credentials, save and close the file.

		`# machine <IP-address> login <pmd-administrative-user> password <pmd-administrative user-password>`

	3. Go to [https://raw.githubusercontent.com/vmware/pmd/master/conf/restapispec.json](https://raw.githubusercontent.com/vmware/pmd/master/conf/restapispec.json "the following link") and save the `restapispec.json` file locally to the `root` folder.

 
	4. Edit the `restapispec.json` file to enter the IP address of the machine to be upgraded.
	
		`# vi /root/restapispec.json`
	5. Change the `host` value to the IP address or the hostname of the machine, leave the port number, and save and close the file.
	
		`"host":"<ip-address>:2081"` 
	

4. Initiate the upgrade, in this example of the `sed` package and wait for the command to complete.

	Specify `-k` to force blind trust of certificates and `-n` to use the credentials from the `.netrc` file. 
	`# copenapi_cli pkg update  --packages sed -kn`

5. (Optional) Verify that the client machine package was upgraded successfully.
	1. Log in to the machine that was upgraded over SSH.
	2. List the installed version of the `sed` package.
		
		`# tdnf list installed sed`