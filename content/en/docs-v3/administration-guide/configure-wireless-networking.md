---
title:  Configure Wireless Networking
weight: 4
---

Configure wireless networking in Photon OS. Connect to an open network or a WPA2 protected network using `wpa_cli` and configure `systemd-networkd` to assign an IP address to the network.

* [Configure pwa supplicant service](#configure-wpa-supplicant-service)
* [Connect using `wpa_cli`](#connect-using-wpa_cli)
* [Assign IP address to network](#assign-ip-address-to-network)

## Configure wpa supplicant service  

By default, Photon OS does not load unnecessary kernel modules. This applies for wireless network drivers as well.

Add firmware/drivers and test its functionality before configuring the wpa supplicant service.

1.  Install wireless network drivers

    Photon OS administrators may need to build a specific driver by themselves using driver source codes. Building from source code usually has similar procedure to the following step.
   
       - First, add build essential packages, and as helper tools usbutils/pciutils
   
            ```console
            tdnf install -y git build-essential linux-api-headers usbutils pciutils
            ```
   
       - Then, clone from the driver repository and build from source code.
   
            ```console
            git clone https://github.com/<repository-name>
            cd ./<repository-name>
            make
            make install
            ```
       - Load driver.  
            `modprobe <driver name>`
    
       - Check the driver status with `lsmod | grep <driver name>`.
    
    <br>
    The following example is for Intel iwlwifi driver (backported).  
    
       - Add build essential packages.
            
            For generic Photon OS Linux kernel, run
   
            ```console
            tdnf install -y git build-essential linux-api-headers usbutils pciutils linux-devel
            ```            
    
       - Reboot.  

       - With respect to the wireless networking device firmware dependency, add latest Intel iwlwifi firmware.
     
            ```console
            mkdir /lib/firmware
            git clone git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git --depth 1
            cd linux-firmware
            cp iwlwifi-*.{ucode,pnvm} /lib/firmware
            ```

       - Clone from the driver repository of Intel driver iwlwifi (backported) and build from source code.  
      
            ```console
            cd /lib/modules/`uname -r`
            git clone https://www.github.com/intel/backport-iwlwifi
            cd ./backport-iwlwifi/iwlwifi-stack-dev
            cp ./scripts/update-initramfs.sh ./scripts/update-initramfs.0
            sed 's/"Fedora"/"VMware Photon OS"/' ./scripts/update-initramfs.0 > ./scripts/update-initramfs.sh
            # rm ./scripts/update-initramfs.0
            make
            make install
            ```

       - Load kernel module.  
       
            ```console
            modprobe iwlwifi
            ```

       - Check the Intel iwlwifi driver status with `lsmod | grep iwlwifi`.
      
         Ensure driver functionality before proceeding to the wpa supplicant service configuration.  
       
         Use usbutils/pciutils helper tools to find details about wireless networking devices on the system.  
       
           ```console
           # usb devices
           lsusb
           lsusb xx:yy -nnvvv # allows you to see what firmware is being used and more details           
           # pci devices
           lspci
           lspci xx:yy -nnvvv # allows you to see what firmware is being used and more details
           ```
           
    For more information, see [Wireless Wiki Kernel Log](https://wireless.wiki.kernel.org/en/users/drivers/iwlwifi).
    <br><br>
    
1.  Install and configure `wpa_supplicant service` on the WLAN interface.

    ```console
    tdnf install -y wpa_supplicant
    ```
    
    `systemctl enable wpa_supplicant@<wlan-interface>.service`  
    `wpa_supplicant -B -i <wlan-interface> -c /etc/wpa_supplicant/wpa_supplicant-<wlan-interface>.conf`
    
    For example to configure wlan0, run:
    ```console
    systemctl enable wpa_supplicant@wlan0.service
    wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
    ```
    
1.  Ensure that the wpa_supplicant service is running on the WLAN interface.

    `systemctl status wpa_supplicant@<wlan-interface>.service`
    
  
## Connect Using wpa_cli

When you connect using `wpa_cli`, you can scan for available networks and associate the network with a network ID.   

1. Connect to `wpa_cli`, for example to wlan0:
    
    `wpa_cli -i wlan0`

1. Scan for available networks:

    `scan`

1. To see the list of networks, use the following command:
    
    `scan_results`

1. Add the network:

    `add_network`
    
    This command returns a network ID.
    
    For applying a specific network id, run `add_network <network ID>`.  
    As example, this adds network id 0: `add_network 0`.

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


1. Create a `/etc/systemd/network/98-dhcp-wlan.network` file with the following contents.
    
    ```
    [Match]
    Name=wlan*
    [Network]
    DHCP=yes
    IPv6AcceptRA=no
    ```
    
    Run `chmod 644 /etc/systemd/network/98-dhcp-wlan.network`.

1. Restart `systemd-networkd` using:

    `systemctl restart systemd-networkd`
