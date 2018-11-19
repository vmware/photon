# Installing Sendmail

Before you install Sendmail, you should set the fully qualified domain name (FQDN) of your Photon OS machine.

By default, Sendmail is not installed with either the minimal or full version of Photon OS. When you install Sendmail, it provides Photon OS with a `systemd` service file that typically enables Sendmail. If the service is not enabled after installation, you must enable it. 

Sendmail resides in the Photon extras repository. You can install it with `tdnf` after setting the machine's FQDN. 

## Procedure

1. Check whether the FQDN of the machine is set by running the `hostnamectl status` command:  
         
    ```
hostnamectl status
       Static hostname: photon-d9ee400e194e
             Icon name: computer-vm
               Chassis: vm
            Machine ID: a53b414142f944319bd0c8df6d811f36
               Boot ID: 1f75baca8cc249f79c3794978bd82977
        Virtualization: vmware
      Operating System: VMware Photon/Linux
                Kernel: Linux 4.4.8
          Architecture: x86-64
```

    In the results above, the FQDN is not set. The Photon OS machine only has a short name. If the FQDN were set, the hostname would be in its full form, typically with a domain name. 
    
1. If the machine does not have an FQDN, set one by running `hostnamectl set-hostname new-name`, replacing `new-name` with the FQDN that you want. For example:  
     
    ```
hostnamectl set-hostname photon-d9ee400e194e.corp.example.com
```

    The `hostnamectl status` command now shows that the machine has an FQDN: 
    
    ```
root@photon-d9ee400e194e [ ~ ]# hostnamectl status
       Static hostname: photon-d9ee400e194e.corp.example.com
             Icon name: computer-vm
               Chassis: vm
            Machine ID: a53b414142f944319bd0c8df6d811f36
               Boot ID: 1f75baca8cc249f79c3794978bd82977
        Virtualization: vmware
      Operating System: VMware Photon/Linux
                Kernel: Linux 4.4.8
          Architecture: x86-64
```

1. Install Sendmail: 
    
    ```
tdnf install sendmail
```

1. Verify if Sendmail is enabled: 
    
    ```
systemctl status sendmail
```

1. Enable Sendmail if it is disabled and then start it: 
    
    ```
systemctl enable sendmail
 systemctl start sendmail
```
