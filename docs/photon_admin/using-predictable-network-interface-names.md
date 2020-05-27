# Using Predictable Network Interface Names

When you run Photon OS on a virtual machine or a bare-metal machine, the Ethernet network interface name might shift from one device to another if you add or remove a card and reboot the machine. For example, a device named `eth2` might become `eth1` after you remove a NIC and restart the machine.

You can prevent interface names from reordering by turning on [predictable network interface names](https://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames/). The naming schemes that Photon OS uses can then assign fixed, predictable names to network interfaces even after you add or remove cards or other firmware and the restart the system. 

When you enable predictable network interface names, you can use one of the following options to assign persistent names to network interfaces:

* Apply the `slot` name policy to set the name of networking devices in the `ens` format with a statically assigned PCI slot number.
* Apply the `mac` name policy to set the name of networking devices in the `enx` format a unique MAC address. 
* Apply the `path` name policy to set the name of networking devices in the `enpXsY` format derived from a device connector's physical location.

Though Photon OS supports the `onboard` name policy to set the name of networking devices from index numbers given by the firmware in the `eno` format, the policy might result in nonpersistent names. 

The option to choose depends on your use case and your unique networking requirements. For example, when you clone virtual machines and require the MAC addresses to be different from one another but the interface name to be the same, consider using `ens` to keep the slot the same after system reboots. 

Alternatively, if the cloning function supports `enx`, you can use it to set a MAC address which persists after reboots. 

Perform the following steps to turn on predictable network interface names: 

1. Make a backup copy of the following file in case you need to restore it later:
    
    ```
    cp /boot/grub/grub.cfg /boot/grub/grub.cfg.original
    ``` 

2. To turn on predictable network interface names, edit `/boot/grub/grub.cfg` to remove the following string: 

    
    ```
    net.ifnames=0Item
    ```
    The string appears near the bottom of the file in the `menuentry` section:

    
    ```
    menuentry "Photon" {
       linux "/boot/"$photon_linux root=$rootpartition net.ifnames=0 $photon_cmdline
       if [ "$photon_initrd" ]; then
            initrd "/boot/"$photon_initrd
       fi
    }
    # End /boot/grub2/grub.cfg
    ```

    Edit out `net.ifnames=0`, but make no other changes to the file, and then save it. 

1. Specify the types of policies that you want to use for predictable interface names by modifying the `NamePolicy` option in `/lib/systemd/network/99-default.link`. The file contents are as follows: 

    
    ```
    cat /lib/systemd/network/99-default.link
    [Link]
    NamePolicy=kernel database
    MACAddressPolicy=persistent

    ```

To use the `ens` or `enx` option, the `slot` policy or the `mac` policy can be added to the space-separated list of policies that follow the `NamePolicy` option in the default link file, `/lib/systemd/network/99-default.link`. The order of the policies matters. Photon OS applies the policy listed first before proceeding to the next policy if the first one fails. 

For example: 
    
```
/lib/systemd/network/99-default.link
    [Link]
    NamePolicy=slot mac kernel database
    MACAddressPolicy=persistent
```

With the name policy specified in the above example, you might still have an Ethernet-style interface name if the two previous policies, `slot` and `mac`, fail. 

For information on setting name policies, see [systemd.link--network device configuration](https://www.freedesktop.org/software/systemd/man/systemd.link.html). 