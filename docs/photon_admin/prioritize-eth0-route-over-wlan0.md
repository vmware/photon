# Prioritize eth0 Route Over WLAN

You can prioritise the eth0 route over the WLAN route. Perform the following steps:

1. Modify the `/etc/systemd/network/99-dhcp-en.network` file and add the following content:

    ```
    [DHCP]
    RouteMetric=512
    ```

1. Restart `systemd-networkd`.
