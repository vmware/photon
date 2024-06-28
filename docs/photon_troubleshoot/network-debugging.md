# Network Debugging

You can set `systemd-networkd` to work in debug mode so that you can analyze log files with debugging information to help troubleshoot networking problems. 

The following procedure turns on network debugging by adding a drop-in file in `/etc/systemd` to customize the default systemd configuration in `/usr/lib/systemd`.

1. Run the following command as root to create a directory with this exact name, including the `.d` extension:

	`mkdir -p /etc/systemd/system/systemd-networkd.service.d/`

1. Run the following command as root to establish a systemd drop-in unit with a debugging configuration for the network service:

    ```
    cat > /etc/systemd/system/systemd-networkd.service.d/10-loglevel-debug.conf << "EOF"
    	[Service]
    	Environment=SYSTEMD_LOG_LEVEL=debug
    	EOF
    ```
 
1. Reload the `systemctl` daemon and restart the `systemd-networkd` service for the changes to take effect:
	
    ```
    systemctl daemon-reload
    	systemctl restart systemd-networkd
    ```

1. Verify that your changes took effect:

	   `systemd-delta --type=extended`

1. View the log files by running this command:

	   `journalctl -u systemd-networkd`

1. After debugging the network connections, turn debugging off by deleting the drop-in file:

   	`rm /etc/systemd/system/systemd-networkd.service.d/10-loglevel-debug.conf`
	