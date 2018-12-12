# Enabling `systemd` Debug Shell During Boot

To diagnose `systemd` related boot issues, you can enable early shell access during boot.

Perform the following steps to enable early shell access:

1. Restart the Photon OS machine or the virtual machine running Photon OS. 
    
    When the Photon OS splash screen appears, as it restarts, type the letter `e` quickly. 

1. Append `systemd.debug-shell=1` to the kernel command line. 

    To change logging level to debug, you can append `systemd.log_level=debug`.

1. Press `F10` to proceed with the boot.

1. Press `Alt+Ctrl+F9` to switch to `tty9` to access the debug shell.