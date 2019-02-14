# Installing the Packages for `tcpdump` and `netcat` with `tdnf`

Photon OS includes the following networking tools:

- **tcpdump**. A networking tool that captures and analyzes packets on a network interface. `tcpdump` is not available with the minimal version of Photon OS but available in the repository. The minimal version includes the `iproute2` tools by default.  
     
    You can install `tcpdump` and its accompanying package `libpcap`, a C/C++ library for capturing network traffic, by using `tdnf`: 

    ```
tdnf install tcpdump
```

- **netcat**. A tool to send data over network connections with TCP or UDP. This tool is not included in either the minimal or the full version of Photon OS. But since `netcat` furnishes powerful options for analyzing, troubleshooting, and debugging network connections, you might want to install it. To install `netcat', run the following command: 

    ```
tdnf install netcat
```
