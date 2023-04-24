---
title:  Remotely Update a Single Photon OS Machine With Photon Management Daemon 
weight: 2
---

After you have a configured the Photon Management Daemon on a machine, you can remotely update any installed package on that machine. You can use the `root` user credentials.

The update process uses `pmd-cli` which is supported from Photon Management Daemon. You can initiate the update process from any machine that has Photon Management Daemon CLI installed.

## Prerequisites


- Have an installed Photon Management Daemon on the client.
- Have in installed Photon Management Daemon CLI (`pmd-cli`) on a machine from which you perform the updates.

## Procedure

1. To initiate remote update, log in to a machine that has Photon Management Daemon CLI installed over SSH.
2. Identify packages that can be updated on the client machine.

	- List the available updates for the machine.

```console
pmd-cli --server-name <machine-IP-address> --user root pkg list updates
```

3. Verify the currently installed version of a package, for example `sed`.

```console
pmd-cli --server-name <machine-IP-address> --user root pkg installed sed
```

The installed version number shows as earlier than the one listed under the available updates.

4. Initiate the update, in this example of the `sed` package, enter password, and wait for the command to complete.

```console
pmd-cli --server-name <machine-IP-address> --user root pkg update sed
```

5. (Optional) Verify that the client machine package was updated successfully.
	- Log in to the machine that was updated over SSH.
	- List the installed version of the `sed` package.
		
```console
pmd-cli --server-name <machine-IP-address> --user root pkg installed sed
```