---
title:  Creating a Stand-Alone Photon Machine With cloud-init
weight: 4
---

Cloud-init can customize a Photon OS virtual machine by using the `nocloud` data source. The `nocloud` data source bundles the `cloud-init` metadata and user data into an ISO that acts as a seed when you boot the machine. The `seed.iso` delivers the metadata and the user data without requiring a network connection. 

**Procedure**


1. Create the metadata file with the following lines in the [YAML](http://www.yaml.org/start.html) format and name it `meta-data`:
          
    ```yaml
    instance-id: iid-local01
       local-hostname: cloudimg
    ```

1. Create the user data file with the following lines in [YAML](http://www.yaml.org/start.html) and name it `user-data`: 

      ```yaml
        #cloud-config
    	hostname: testhost
    	packages:
    	 - vim
      ```	 

1. Generate the ISO that will serve as the seed. The ISO must have the volume ID set to `cidata`. In the following example, the ISO is generated on an Ubuntu 14.04 computer containing the files named `meta-data` and `user-data` in the local directory: 

    ```console
    genisoimage -output seed.iso -volid cidata -joliet -rock user-data meta-data
    ```

    The ISO now appears in the current directory: 

    ```console
    steve@ubuntu:~$ ls
    meta-data seed.iso user-data
    ```

1. Optionally, check the ISO that you generated on Ubuntu by transferring the ISO to the root directory of your Photon OS machine and then running the following command: 
	
    ```console
    cloud-init --file seed.iso --debug init
    ```

    After running the `cloud-init` command above, check the `cloud-init` log file: 

    ```console
    more /var/log/cloud-init.log
    ```

1. Attach the ISO to the Photon OS virtual machine as a CD-ROM and reboot it so that the changes specified by seed.iso take effect. In this case, `cloud-init` sets the `hostname` and adds the `vim` package.