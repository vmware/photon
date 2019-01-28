# Configure Wireless Networking

You can configure wireless networking in Photon OS. Connect to an open network or a WPA2 protected network using `wpa_cli` and configure `systemd-networkd` to assign an IP address to the network.

* [Connect using `wpa_cli`](#connect-using-wpa-cli)
* [Assign IP address to network](#assign-ip-address-to-network)

## Connect Using wpa_cli

When you connect using `wpa_cli`, you can scan for available networks and associate the network with a network ID. 

Perform the following steps:

1. Ensure that the `wpa_supplicant service` is running on the WLAN interface:

    `Systemctl status wpa_supplicant@<wlan-interface>.service`

1. Connect to `wpa_cli`:
    
    `wpa_cli -I wlan0`

1. Scan for available networks:

    `scan`

1. To see the list of networks, use the following command:
    
    `scan_results`

1. Add the network:

    `add_network`
    
    This command returns a network ID. 

1. Associate the network with the network ID. 

    `set_network  <network ID> ssid “<ssid-name>”`
    
1. For a WPA2 network, set the passphrase:

    `set_network <network ID> psk “<passphrase>”`
    
1. Enable the network:

    `enable_network <network ID>`
    
1. Save the configuration file: 

    `save_config`
    
    To exit the `wpa_cli`, type 'quit`. 


## Assign IP Address To Network

Configure `systemd-networkd` to assign IP address to network. Perform the following steps:


1. Create a `/etc/systemd/network/98-dhcp-wlan.network` file with the following contents:
    
    ```
    [Match]
    Name=wlan*
    [Network]
    DHCP=yes
    IPv6AcceptRA=no
    ```

1. Restart systemd-networkd using:

    `Systemctl restart systemd-networkd`






