# Remotely Upgrade a Single Photon OS Machine With Lightwave Client and Photon Management Daemon Installed

After you have a configured the Photon Management Daemon on a machine, you can remotely upgrade any installed package on that machine. You can use the `root` user credentials.

Upgrade process uses `pmd-cli` that is supported from both Lightwave and Photon Management Daemon. You can initiate the upgrade process from any machine that has Photon Management Daemon CLI installed.

## Prerequisites

- Have an installed Lightwave server with configured domain controller on it.
- Have an installed Lightwave client that is joined to the domain.
- Have an installed Photon Management Daemon on the client.
- Have in installed Photon Management Daemon CLI (pmd-cli) on a machine from which you perform the updates.

## Procedure

1. To initiate remote upgrade, log in to a machine that has Photon Management Daemon CLI installed over SSH.
2. Identify packages that can be upgraded on the client machine.
	2. List the available updates for the machine.
		
		`# pmd-cli --server-name <machine-IP-address> --user root pkg list updates`
	3. Verify the currently installed version of a package, for example `sed`.

		`# `# pmd-cli --server-name <machine-IP-address> --user root pkg installed sed`
		The installed version number shows as earlier than the one listed under the available updates.


4. Initiate the upgrade, in this example of the `sed` package, enter password, and wait for the command to complete.
 
	`# pmd-cli --server-name <machine-IP-address> --user root pkg update sed`

5. (Optional) Verify that the client machine package was upgraded successfully.
	1. Log in to the machine that was upgraded over SSH.
	2. List the installed version of the `sed` package.
		
		`# pmd-cli --server-name <machine-IP-address> --user root pkg installed sed`