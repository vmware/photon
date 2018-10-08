RPM-OSTree Host default server repo installation option in Photon 1.0 or 1.0 Revision 2 will setup a profile similar to Photon Minimal, with the added benefit of being able to self-upgrade.  
Photon OS 2.0 does not offer a 'default host' installation. See chapter 7 and 12 for other options. 

### 2.1 Who is this for?  
The RPM-OSTree 'default host' is the easiest way to deploy a Photon RPM-OSTree host from ISO/cdrom, without the need to deploy and maintain an RPM-OSTree server. It is targeted at the user who relies on VMware Photon OS team to keep his or her system up-to-date, configured to get its updates from the official Photon 1.0 OSTree repository.

This is also the fastest way to install a host (18 seconds on my Mac with SSD after all UI choices have been entered by user), as we've included in the ISO/cdrom an identical copy of the Photon 1.0 "starter" RPM-OSTree repository that is published online by VMware Photon OS team. So rather than pulling from the online repository, the installer pulls the repo from cdrom, which saves bandwidth and also reduces to zero the chances of failing due to a networking problem. After successful installation, any updates are going to be pulled from the official online repository, when Photon OS team will make them available.    

Note: It is also possible to install an RPM-OSTree host against the official online repo via PXE boot, without the benefit of fast, local pull from cdrom. This will be covered in the PXE boot/kickstart chapter, as it requires additional configuration.

### 2.2 Installing the ISO, step by step
User will first download [[Photon 1.0 ISO file|https://bintray.com/artifact/download/vmware/photon/photon-1.0-13c08b6.iso]] or the newer [[Photon 1.0 Rev2 ISO file|https://bintray.com/artifact/download/vmware/photon/photon-1.0-62c543d.iso]] that contains the installer, which is able to deploy any of the supported Photon installation profiles.

There are some steps common to all Photon installation profiles, starting with adding a VM in VMware Fusion, Workstation or ESXi, selecting the OS family, then customizing for disk size, CPU, memory size, network interface etc. (or leaving the defaults) and selecting the ISO image as cdrom. The installer will launch, that will go through disk partitioning and accepting the license agreement screens, followed by selecting an installation profile.
These steps are described at the page linked below, so I won't repeat them, just that instead of setting up a Photon Minimal profile, we will install a Photon OSTree host:   

[[Running Project Photon on Fusion|Running-Project-Photon-on-Fusion]].  

Select the **Photon OSTree Host** option.

![PhotonChooseHost](https://cloud.githubusercontent.com/assets/13158414/14757883/15742dce-08ad-11e6-9486-4fe08b4bf7f2.png)  

Continue with setting up a host name like **photon1-def** and a root password, re-confirm.   
Then, select "Default OSTree Server" and continue.  

![PhotonChooseHostDefault](https://cloud.githubusercontent.com/assets/13158414/14757878/1557500a-08ad-11e6-9cb7-f917cb0fdaca.png)

![PhotonHostDefaultFinish](https://cloud.githubusercontent.com/assets/13158414/14757882/1571cde0-08ad-11e6-8e07-47258ca4e8d9.png)  

When installation is over, the VM will reboot and will show in grub VMWare Photon/Linux 1.0_minimal (ostree), which will reassure that it's booting from an OSTree image!  

![PhotonHostFirstRebootGrub](https://cloud.githubusercontent.com/assets/13158414/14757877/155614ec-08ad-11e6-9e36-b43f77b6fb69.png)  

Boot, login and you are ready to use it!  The next chapters are about experimenting first hand and understanding in detail how everything works. If you just want to learn how to [[upgrade your host|Photon-RPM-OSTree:-5-Host-updating-operations]] when new updates are available, skip to [[Chapter 5|Photon-RPM-OSTree:-5-Host-updating-operations]].

Note: If you ran Photon 1.0 Rev2 installer rather than Photon 1.0, you may notice in grub **1.0_minimal.1** rather than **1.0_minimal**, hinting of an updated, newer version installed. This will be also explained in [[Chapter 5|Photon-RPM-OSTree:-5-Host-updating-operations]].  

[[Back to main page|Photon-RPM-OSTree:-a-simple-guide]] | [[Previous page|Photon-RPM-OSTree:-1-Introduction#photon-with-rpm-ostree-installation-profiles]] | [[ Next page >|Photon-RPM-OStree:-3-Concepts-in-action]] 