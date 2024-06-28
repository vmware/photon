# Fixing Permissions on Network Config Files

When you create a new network configuration file as root user, the network service might be unable to process it until you set the file mode bits to `644`.

If you query the journal with `journalctl -u systemd-networkd`, you might see the following error message along with an indication that the network service did not start: 

	`could not load configuration files. permission denied`

The permissions on the network files might cause this problem. Without the correct permissions, `networkd-systemd` cannot parse and apply the settings, and the network configuration that you created will not be loaded. 

After you create a network configuration file with a `.network` extension, you must run the `chmod` command to set the new file's mode bits to `644`. Example: 

    `chmod 644 10-static-en.network`

For Photon OS to apply the new configuration, you must restart the `systemd-networkd` service by running the following command: 

	`systemctl restart systemd-networkd`

