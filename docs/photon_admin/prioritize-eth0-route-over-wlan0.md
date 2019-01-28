# Prioritize eth0 Route Over wlan0

You can prioritise the etho0 route over the wla0 route. Perform the following steps:

1. Modify the `/etc/systemd/network/99-dhcp-en.network` file and add the following content:

    ```
    [DHCP]
    RouteMetric=512 
    ```

1. Restart `systemd-networkd`.
