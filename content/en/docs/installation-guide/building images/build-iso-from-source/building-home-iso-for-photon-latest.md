---
title: "Building your home ISO for Photon OS latest"
weight: 3
---

Building your home ISO for Photon OS latest is the integration of kernel security patches and packages updates into the Photon OS installation medium. Latest availability refers to pre-tested Photon OS packages stored in non-dev branches.

For continuously updated, latest Photon OS Docker images, see [the relevant manifest file ( library/photon )](https://github.com/docker-library/official-images/blob/master/library/photon).

A home ISO for Photon OS latest enables the direct installation of Photon OS without having to install the said kernel security patches and packages updates afterwards.

Host environment
Accept a subscription eligible, recreatable, granular reproducible, purposed host environment.

Administer e.g. a vSphere 8.0 environment with provisioned   
- [Photon OS 3.0 Rev.2](https://github.com/vmware/photon/wiki/Downloading-Photon-OS#photon-os-30-revision-2-binaries) photon-hw13_uefi-3.0-9355405.ova   
  The created virtual machine runs in ESXi 6.5 virtual machine compatibility mode. Upgrade the virtual machine hardware as needed. See [Some older Linux VMs created with Hardware version 20 will fail to start installation when Secure Boot is enabled](https://kb.vmware.com/s/article/88737)
  Add sufficient RAM. For a build process with e.g. 4 threads configure at least 16GB RAM.   
  Higher CPU capacity e.g. 8 CPU is recommended.   
  Make sure the virtual machine has enough disk capacity e.g. 64GB disk space. See [expanding disk partition](https://vmware.github.io/photon/assets/files/html/3.0/photon_troubleshoot/expanding-disk-partition.html)


On the provisioned Photon OS, perform the following steps for a home ISO creation for Photon OS latest.

  
1. Photon OS home configuration

   Login and change the initial root password. Also, see [reset a forgotten root password](https://vmware.github.io/photon/assets/files/html/3.0/photon_troubleshoot/resetting-a-lost-root-password.html).   
  
   Assign a [static ip address](https://vmware.github.io/photon/assets/files/html/3.0/photon_admin/setting-a-static-ip-address.html).

   Configure [locale settings](https://vmware.github.io/photon/assets/files/html/3.0/photon_admin/changing-the-locale.html).
  
   Configure NTP.
  
   Allow SSH access. Also, see [permitting root login with ssh](https://vmware.github.io/photon/assets/files/html/3.0/photon_troubleshoot/permitting-root-login-with-ssh.html).
  
   Configure additional network settings to your needs e.g. allow icmp.  
  
   Ensure repository connectivity. The public packages repository is https://packages.vmware.com/photon.

   For Photon OS older than Photon OS 3.0 Revision 3, use the following commands to remediate the public packages repository information.
   ```
   if [ `cat /etc/yum.repos.d/photon.repo | grep -o "packages.vmware.com/photon" | wc -l` -eq 0 ]; then
     cd /etc/yum.repos.d/
     sed -i 's/dl.bintray.com\/vmware/packages.vmware.com\/photon\/$releasever/g' photon.repo photon-updates.repo photon-extras.repo photon-debuginfo.repo
   fi
   ```
  
   Prepare the home directory accordingly to your needs.
   ```
   mkdir $HOME/workspaces
   ```  
  
2. Install latest packages and build essentials
 
   Run a distro-sync.
   ```
   tdnf distro-sync -y
   reboot
   ```

   If after the reboot the system stops with invalid signature, disable uefi secure boot in virtual machine settings.
   Also, see [Wiki - After updating Kernel rpm, VM fails to boot with Secure Boot?](https://github.com/vmware/photon/wiki/Frequently-Asked-Questions#q-after-updating-kernel-rpm-vm-fails-to-boot-with-secure-boot)

   As UEFI related boot parameters evolve fast, it is recommended to use the latest Photon OS installer source as well.

   ```
   tdnf install -y kpartx git bc build-essential createrepo_c texinfo curl wget python3-pip tar dosfstools cdrkit linux-secure-devel
   curl -L https://git.io/v1boE | xargs -I {} tdnf install -y {}
   tdnf -y install createrepo
   wget -qO- https://get.docker.com/ | sh
   pip3 install docker==2.3.0
   cd $HOME/workspaces
   pip3 install git+https://github.com/vmware/photon-os-installer.git
   reboot
   ```


3. Option: Modify Kernel parameters   
   Kernel parameters can be modified e.g. for additional devices interoperability.
   Check `uname -r`. The sources to the matching linux-headers are stored in the directory `/usr/src`. 
   E.g. the kernel parameter file is store in `/usr/src/linux-headers-[identification]/.config`. `identification` may not correlate to `uname -r`.

4. Photon OS git clone

   The [Photon OS github repository](https://github.com/vmware/photon) has a per-release branch structure. 
   Clone the desired Photon OS release.

   ```
   cd $HOME/workspaces
   git clone -b 4.0 https://github.com/vmware/photon.git
   cd $HOME/workspaces/photon
   ```

5. Option: Add a new package

   Add your package e.g. foo-1.0.tar.gz.   
   ```
   mkdir -p $HOME/workspaces/photon/stage/SOURCES
   mkdir -p $HOME/workspaces/photon/SPECS/foo/
   cp foo-1.0.tar.gz $HOME/workspaces/photon/stage/SOURCES
   cp foo.spec $HOME/workspaces/photon/SPECS/foo
   cd $HOME/workspaces/photon
   make foo
   ```

6. Build

   Be aware, the build process may take hours. Consider that the more RAM the virtual machine has, the more threads (-jX and THREADS=X) can be handled. 
   Run the following commands for a full ISO Photon OS 4.0 build. 
   ```
   cd $HOME/workspaces/photon
   make -j1 image IMG_NAME=iso THREADS=1 LOGLEVEL=debug >makephoton.log 2>&1
   ```
   As the process with latest packages can reveal build issues, the debug loglevel is enabled.

   The ISO is created at $HOME/workspaces/photon/stage/photon.iso.

7. Troubleshooting history   

   11/07/2022 - vSphere 8.0 IA - photon-hw13_uefi-3.0-9355405.ova - latest (4.19.261-1.ph3-secure): disable uefi secure boot
   
   
   During the build process, log files are stored in $HOME/workspaces/photon/stage/LOGS.   
   If the creation of a package fails, analyze the logfile $HOME/workspaces/photon/stage/LOGS/[package-version]/[package].log.   
   Check the debug log $HOME/workspaces/photon/makephoton.log as well.
  

   
