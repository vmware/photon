#Photon OS on GCE
## Google Compute Engine (GCE) Image background
GCE is a service that lets you run virtual machines on Google's infrastructure. You can customize the virtual machine as much as you want, and you can even install your own custom operating system image. Or, you can adopt one of the public [images](https://cloud.google.com/compute/docs/operating-systems/) provided by Google. For any operating system to work with GCE, it must match Google's infrastructure needs. 
Google provides tools that VM instances require to work correctly on GCE:

 *   __[Google startup scripts](https://cloud.google.com/compute/docs/startupscript)__: User can provide some startup script to configure their instances at startup.
 *   __[Google Daemon](https://cloud.google.com/compute/docs/metadata)__: Google Daemon creates new accounts and configures ssh to accept public keys using the metadata server.
 *   __[Google Cloud SDK](https://cloud.google.com/sdk/)__: Command line tools to manage your images, instances and other objects on GCE.

Following is the list (extracted from [this link](https://cloud.google.com/compute/docs/tutorials/building-images)) of items that must be done to make Photon OS work on GCE:

 *   Install Google Compute Engine Image packages
 *   Install Google Cloud SDK
 *   Change GPT partition table to MBR 
 *   Update the Grub config for new MBR and serial console output
 *   Update ssh configuration
 *   Delete ssh host keys
 *   Set the time zone to UTC
 *   Use the Google NTP server
 *   Delete the hostname file.
 *   Add Google hosts /etc/hosts
 *   Set MTU to 1460. SSH will not work without it.
 *   Create /etc/ssh/sshd_not_to_be_run with just the contents “GOOGLE\n”.

## The GCE-Ready Image of Photon OS 

The latest version of Photon OS does all of this for you. It bundles the Google startup scripts, daemon, and cloud SDK into a GCE-ready image that has been modified to meet the configuration requirements of GCE. To download the GCE-ready image of Photon OS for free, go to [Bintray](https://bintray.com/vmware/photon/). To use Photon OS with GCE, you do not need to perform the following steps unless you want to go through the exercise of customizing Photon OS to work with GCE. The Photon OS team has already done it for you. For more information, see [Running Photon OS on Google Compute Engine](https://github.com/vmware/photon/wiki/Running-Photon-OS-on-Google-Compute-Engine). 

## Creating Photon image for GCE
##### 1. Prepare Photon Disk
###### Install Photon Minimal on Fusion/Workstation and install some required packages.
      mount /dev/cdrom /media/cdrom
      tdnf install yum
      tdnf install python2-libs
      yum install ntp sudo wget tar which gptfdisk sed findutils grep gzip --nogpgcheck -y

###### Photon installer installs GPT partition table by default but GCE only accepts MBR(msdos) type partition table. We need to convert GPT to MBR and update the grub. Following are commands to do that.
  
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
      
##### 2. Install Google Cloud SDK and GCE Packages
      yum install google-daemon google-startup-scripts
      cp /usr/lib/systemd/system/google* /lib/systemd/system/
      cd /lib/systemd/system/multi-user.target.wants/
      
      # Create links in multi-user.target to auto-start these scripts and services.
      for i in ../google*; do  ln -s $i `basename $i`; done
      
      cd /tmp/; wget https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz --no-check-certificate
      tar -xf google-cloud-sdk.tar.gz
      cd google-cloud-sdk
      ./install.sh
##### 3. Update /etc/hosts file with GCE values
      echo "169.254.169.254 metadata.google.internal metadata" >> /etc/hosts
##### 4. Remove all servers from ntp.conf and add Google's ntp server.
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
      
##### 5. Set UTC timezone
      ln -sf /usr/share/zoneinfo/UTC /etc/localtime

##### 6. Update /etc/resolv.conf
      echo "nameserver 8.8.8.8" >> /etc/resolv.conf

##### 7. Remove ssh host keys and add script to regenerate them at boot time.
      rm /etc/ssh/ssh_host_*
      # Depending on the installation, you may need to purge the following keys
      rm /etc/ssh/ssh_host_rsa_key*
      rm /etc/ssh/ssh_host_dsa_key*
      rm /etc/ssh/ssh_host_ecdsa_key*

      sed -i -e "/exit 0/d" /etc/rc.local
      echo "[ -f /etc/ssh/ssh_host_key ] && echo 'Keys found.' || ssh-keygen -A" >> /etc/rc.local
      echo "exit 0" >> /etc/rc.local
      printf "GOOGLE\n" > /etc/ssh/sshd_not_to_be_run
      
      # Edit sshd_config and ssh_config as per instructions on [this link](https://cloud.google.com/compute/docs/tutorials/building-images ).
      
##### 8. Change MTU to 1460 for network interface.
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

##### 9. Pack and Upload to GCE.
###### Shutdown the Photon VM and copy its disk to tmp folder.       
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
