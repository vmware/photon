# Clearing the Machine ID of a Cloned Instance for DHCP

Photon OS uses the contents of `/etc/machine-id` to determine the DHCP unique identifier (duid) that is used for DHCP requests. If you use a Photon OS instance as the base system for cloning, to create additional Photon OS instances, you must clear the `machine-id` with this command: 

    echo -n > /etc/machine-id

When the value is cleared, `systemd` regenerates the machine-id and all DHCP requests will contain a unique duid. 