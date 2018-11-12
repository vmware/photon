# Using Predictable Network Interface Names

On a virtual machine running Photon OS, just as on a bare-metal machine, the Ethernet network interface name might shift from one device to another if you add or removed a card and reboot the machine. A device named `eth2`, for example, might become `eth1` after a NIC is removed and the machine is restarted.

You can prevent interface names from reordering by turning on [predictable network interface names](https://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames/). The naming schemes that Photon OS uses can then assign fixed, predictable names to network interfaces even after cards or other firmware are added or removed and the system is restarted. With predictable network interface names enabled, you can select among several options to assign persistent names to network interfaces:

* Apply the `slot` name policy to set the name of networking devices in the `ens` format with a statically assigned PCI slot number.
* Apply the `mac` name policy to set the name of networking devices in the `enx` format a unique MAC address. 
* Apply the `path` name policy to set the name of networking devices in the `enpXsY` format derived from a device connector's physical location.

(Although Photon OS also supports the `onboard` name policy to set in the `eno` format the name of networking devices from index numbers given by the firmware, the `onboard` policy might result in nonpersistent names.) 

The option that you choose depends on your use case and your unique networking requirements. If, for instance, you clone clones virtual machines in a use case that requires the MAC addresses to be different from one another but the interface name to be the same, you should consider using `ens` to keep the slot the same after reboots. 

Alternatively, if the cloning function supports it and it works for your use case, you can use `enx` to set a MAC address, which also persists after reboots. 

Here's how to turn on predictable network interface names.

First, make a backup copy of the following file in case you need to restore it later: 

    cp /boot/grub/grub.cfg /boot/grub/grub.cfg.original

Second, to turn on predictable network interface names, edit `/boot/grub/grub.cfg` to remove the following string: 

    net.ifnames=0

The string appears near the bottom of the file in the `menuentry` section:

    menuentry "Photon" {
        linux "/boot/"$photon_linux root=$rootpartition net.ifnames=0 $photon_cmdline
        if [ "$photon_initrd" ]; then
            initrd "/boot/"$photon_initrd
        fi
    }
    # End /boot/grub2/grub.cfg

Edit out `net.ifnames=0`, but make no other changes to the file, and then save it. 

Third, specify the types of policies that you want to use for predictable interface names by modifying the `NamePolicy` option in `/lib/systemd/network/99-default.link`. Here's what the file looks like: 

    cat /lib/systemd/network/99-default.link
    [Link]
    NamePolicy=kernel database
    MACAddressPolicy=persistent

To use the `ens` or `enx` option, the `slot` policy or the `mac` policy can be added to the space-separated list of policies that follow the `NamePolicy` option in the default link file, `/lib/systemd/network/99-default.link`. The order of the policies matters: Photon OS applies the policy listed first before proceeding to the next policy if the first one fails. Example: 

    /lib/systemd/network/99-default.link
    [Link]
    NamePolicy=slot mac kernel database
    MACAddressPolicy=persistent

With the name policy specified in the above example, it's possible that you could still end up with an Ethernet-style interface name if the two previous policies, `slot` and `mac`, fail. 

For information on setting name policies, see [systemd.link--network device configuration](https://www.freedesktop.org/software/systemd/man/systemd.link.html). 