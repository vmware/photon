# Prerequisites for Running Photon OS on GCE

Before you use Photon OS within GCE, verify that you have the following resources:

1. [Google Compute Engine account](#google-compute-engine-account)
1. [GCE tools](#gce-tools)
1. [Photon OS Image](#photon-os-image)

## Google Compute Engine Account

Working with GCE requires a Google Compute Engine account with valid payment information. Keep in mind that, if you try the examples in this document, you will be charged by Google. The GCE-ready version of Photon OS is free to use.

## GCE Tools

GCE is a service that lets you run virtual machines on Google's infrastructure. You can customize the virtual machine as much as you want, and you can even install your own custom operating system image. Or, you can adopt one of the public [images](https://cloud.google.com/compute/docs/operating-systems/) provided by Google. For any operating system to work with GCE, it must match Google's infrastructure needs. Google provides tools that VM instances require to work correctly on GCE:

 *   __[Google startup scripts](https://cloud.google.com/compute/docs/startupscript)__: You can provide some startup script to configure your instances at startup.
 *   __[Google Daemon](https://cloud.google.com/compute/docs/metadata)__: Google Daemon creates new accounts and configures ssh to accept public keys using the metadata server.
 *   __[Google Cloud SDK](https://cloud.google.com/sdk/)__: Command line tools to manage your images, instances and other objects on GCE.

Perform the following tasks to make Photon OS work on GCE:

 1. Install Google Compute Engine Image packages
 1. Install Google Cloud SDK
 1. Change GPT partition table to MBR
 1. Update the Grub config for new MBR and serial console output
 1. Update ssh configuration
 1. Delete ssh host keys
 1. Set the time zone to UTC
 1. Use the Google NTP server
 1. Delete the hostname file.
 1. Add Google hosts /etc/hosts
 1. Set MTU to 1460. SSH will not work without it.
 1. Create `/etc/ssh/sshd_not_to_be_run` with just the contents “GOOGLE\n”.
 
 For more information see [Importing Boot Disk Images to Compute Engine](https://cloud.google.com/compute/docs/tutorials/building-images).

For information about upgrading the Photon OS Linux kernel see [Upgrading the Kernel Version Requires Grub Changes for AWS and GCE Images](Upgrading-the-Kernel-Version-Requires-Grub-Changes-for-AWS-and-GCE-Images.md)

## Photon OS Image

VMware recommends that administrators use the Photon OS image for Google Compute Engine (GCE) to create Photon OS instances on GCE. Photon OS bundles the Google startup scripts, daemon, and cloud SDK into a GCE-ready image that has been modified to meet the configuration requirements of GCE. You can download the Photon OS image for GCE from the following URL: 
[https://bintray.com/vmware/photon](https://bintray.com/vmware/photon)

For instructions, see [Downloading Photon OS](Downloading-Photon-OS.md).

Optionally you can customize Photon OS to work with GCE. 

### Creating Photon image for GCE

Perform the following tasks: 

1. Prepare Photon Disk
    
    1. Install Photon Minimal on Fusion/Workstation and install some required packages.
          
        ```
        mount /dev/cdrom /media/cdrom
        tdnf install python2-libs ntp sudo wget tar which gptfdisk sed findutils grep gzip -y
    ```

1. Convert GPT to MBR and update the grub
    
        Photon installer installs GPT partition table by default but GCE only accepts an MBR (msdos) type partition table. So, you must convert GPT to MBR and update the grub. Use the following commands to update the grub:
        
             ```
           # Change partition table to MBR from GPT
           sgdisk -m 1:2 /dev/sda
           grub2-install /dev/sda
           
           # Enable serial console on grub for GCE.
           cat << EOF >> /etc/default/grub
           GRUB_CMDLINE_LINUX="console=ttyS0,38400n8"
           GRUB_TERMINAL=serial
           GRUB_SERIAL_COMMAND="serial --speed=38400 --unit=0 --word=8 --parity=no --stop=1"
           EOF
           
           # Create new grub.cfg based on the settings in /etc/default/grub
           grub2-mkconfig -o /boot/grub2/grub.cfg
             ```
      
1. Install Google Cloud SDK and GCE Packages
      
    ```
          tdnf install -y google-compute-engine google-compute-engine-services
          cp /usr/lib/systemd/system/google* /lib/systemd/system/
          cd /lib/systemd/system/multi-user.target.wants/
          
          # Create links in multi-user.target to auto-start these scripts and services.
          for i in ../google*; do  ln -s $i `basename $i`; done
          
          cd /tmp/; wget https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz
          tar -xf google-cloud-sdk.tar.gz
          cd google-cloud-sdk
          ./install.sh
    ```

1. Update /etc/hosts file with GCE values as follows:
     
    ```
          echo "169.254.169.254 metadata.google.internal metadata" >> /etc/hosts
    ```
      
1. Remove all servers from ntp.conf and add Google's ntp server.
      
    ```
          sed -i -e "/server/d" /etc/ntp.conf
          cat /etc/ntp.conf
          echo "server 169.254.169.254" >> /etc/ntp.conf
          # Create ntpd.service to auto starting ntp server.
          cat << EOF >> /lib/systemd/system/ntpd.service
          [Unit]
          Description=Network Time Service
          After=network.target nss-lookup.target
    
          [Service]
          Type=forking
          PrivateTmp=true
          ExecStart=/usr/sbin/ntpd -g -u ntp:ntp
          Restart=always
          
          [Install]
          WantedBy=multi-user.target
          EOF
          
          # Add link in multi-user.target.wants to auto start this service.
          cd /lib/systemd/system/multi-user.target.wants/
          ln -s ../ntpd.service ntpd.service
    ```
      
1. Set UTC timezone
      
    ```
          ln -sf /usr/share/zoneinfo/UTC /etc/localtime
    ```

1. Update /etc/resolv.conf
      
    ```
          echo "nameserver 8.8.8.8" >> /etc/resolv.conf
    ```

1. Remove ssh host keys and add script to regenerate them at boot time.
      
    ```
          rm /etc/ssh/ssh_host_*
          # Depending on the installation, you may need to purge the following keys
          rm /etc/ssh/ssh_host_rsa_key*
          rm /etc/ssh/ssh_host_dsa_key*
          rm /etc/ssh/ssh_host_ecdsa_key*
    
          sed -i -e "/exit 0/d" /etc/rc.local
          echo "[ -f /etc/ssh/ssh_host_key ] && echo 'Keys found.' || ssh-keygen -A" >> /etc/rc.local
          echo "exit 0" >> /etc/rc.local
          printf "GOOGLE\n" > /etc/ssh/sshd_not_to_be_run
          
          # Edit sshd_config and ssh_config as per instructions on [this link](https://cloud.google.com/compute/docs/tutorials/building-images).
    ```
      
1.  Change MTU to 1460 for network interface.
     
    ```
     # Create a startup service in systemd that will change MTU and exits
          cat << EOF >> /lib/systemd/system/eth0.service
          [Unit]
          Description=Network interface initialization
          After=local-fs.target network-online.target network.target
          Wants=local-fs.target network-online.target network.target
    
          [Service]
          ExecStart=/bin/ifconfig eth0 mtu 1460 up
          Type=oneshot
    
          [Install]
          WantedBy=multi-user.target
          EOF
          # Make this service auto-start at boot.
          cd /lib/systemd/system/multi-user.target.wants/
          ln -s ../eth0.service eth0.service
    ```

1. Pack and upload to GCE.

    Shut down the Photon VM and copy its disk to THE `tmp` folder.       
             
       ```
       # You will need to install Google Cloud SDK on host machine to upload the image and play with GCE.
             cp Virtual\ Machines.localized/photon.vmwarevm/Virtual\ Disk.vmdk /tmp/disk.vmdk
             cd /tmp
             # GCE needs disk to be named as disk.raw with raw format.
             qemu-img convert -f vmdk -O raw disk.vmdk disk.raw
             
             # ONLY GNU tar will work to create acceptable tar.gz file for GCE. MAC's default tar is BSDTar which will not work. 
             # On Mac OS X ensure that you have gtar "GNU Tar" installed. exmaple: gtar -Szcf photon.tar.gz disk.raw 
       
             gtar -Szcf photon.tar.gz disk.raw 
             
             # Upload
             gsutil cp photon.tar.gz gs://photon-bucket
             
             # Create image
             gcloud compute --project "<project name>" images create "photon-beta-vYYYYMMDD" --description "Photon Beta" --source-uri https://storage.googleapis.com/photon-bucket/photon032315.tar.gz
             
             # Create instance on GCE of photon image
             gcloud compute --project "photon" instances create "photon" --zone "us-central1-f" --machine-type "n1-standard-1" --network "default" --maintenance-policy "MIGRATE" --scopes "https://www.googleapis.com/auth/devstorage.read_only" "https://www.googleapis.com/auth/logging.write" --image "https://www.googleapis.com/compute/v1/projects/photon/global/images/photon" --boot-disk-type "pd-standard" --boot-disk-device-name "photon"
       
       ```
