# General Best Practices

When troubleshooting, it is recommended that you follow some general best practices:

* **Take a snapshot.** Before you do anything to a virtual machine running Photon OS, take a snapshot of the VM so that you can restore it if need be. 

* **Make a backup copy.** Before you change a configuration file, make a copy of the original file. For example: `cp /etc/tdnf/tdnf.conf /etc/tdnf/tdnf.conf.orig`

* **Collect logs.** Save the log files associated with a Photon OS problem. Include not only the log files on the guest but also the `vmware.log` file on the host. The `vmware.log` file is in the host's directory that contains the VM.

* **Know what is in your toolbox.** View the man page for a tool before you use it so that you know what your options are. The options can help focus the command's output on the problem you're trying to solve.

* **Understand the system.** The more you know about the operating system and how it works, the better you can troubleshoot.