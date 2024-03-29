# Boot in Emergency Mode

If you encounter problems during normal boot, you can boot in Emergency Mode. 

Perform the following steps to boot in Emergency Mode:

1. Restart the Photon OS machine or the virtual machine running Photon OS. 
    
    When the Photon OS splash screen appears, as it restarts, type the letter `e` quickly. 

1. Append `emergency` to the kernel command line. 

1. Press `F10` to proceed with the boot.

1. At the command prompt, provide the root password to log in to Emergency Mode.

    By default, `/` is mounted as read-only. 
    
    To make modifications, run the following command to remount with write access:
    
    `mount -o remount,rw /`

 