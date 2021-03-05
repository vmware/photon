---
title:  Install Packages from CLI
weight: 7
---

You can install the packages from the command line. The package can be a file or a URL. The dependencies are installed automatically. 

For example:



- Using a URL:



        tdnf install https://packages.vmware.com/photon/4.0/photon_release_4.0_x86_64/x86_64/open-vm-tools-11.2.5-1.ph4.x86_64.rpm
    
        open-vm-tools-11.2.5-1.ph4.x86_64.rpm 763014   100%
        
        Installing:
    
        attrx86_642.4.48-1.ph4  photon  88.65k 90778
    
        nss x86_643.57-2.ph4photon  1.69M 1768005
    
        ...
    
        open-vm-tools   x86_6411.2.5-1.ph4  @cmdline2.65M 2779392
    
    
        Total installed size:  91.57M 96019175
    
    
        Upgrading:
    
        nss-libsx86_643.57-2.ph4photon  2.48M 2601790
    
        util-linux-libs x86_642.36-2.ph4photon752.75k 770816
    
        pcre-libs   x86_648.44-2.ph4photon275.60k 282216
    
    
    
        Total installed size:   3.49M 3654822
    
        Is this ok [y/N]: 
    




- Using a file:



        tdnf install ../lsof-4.91-1.ph4.x86_64.rpm 
    
       
        Installing:
    
        libtirpcx86_641.2.6-1.ph4   photon193.56k 198209
    
        lsofx86_644.91-1.ph4@cmdline  196.10k 200810

        Total installed size: 389.67k 399019