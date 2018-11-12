# Installing Sendmail

Before you install Sendmail, you should set the fully qualified domain name (FQDN) of your Photon OS machine.

Neither the full nor the minimal version of Photon OS installs Sendmail by default. When you install Sendmail, it provides Photon OS with a systemd service file that typically enables Sendmail. If, however, the service is not enabled after installation, you must enable it. 

Sendmail resides in the Photon extras repository. You can install it with `tdnf` after setting the machine's FQDN. Here's how: 

First, check whether the machine's FQDN is set by running the `hostnamectl status` command:  

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

In the results above, the FQDN is not set; the Photon OS machine has only a short name. If the FQDN were set, the hostname would be in its full form, typically with a domain name. 

If the machine does not have an FQDN, set one by running `hostnamectl set-hostname new-name`, replacing `new-name` with the FQDN that you want. Example:  

     hostnamectl set-hostname photon-d9ee400e194e.corp.example.com

The `hostnamectl status` command now shows that the machine has an FQDN: 

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

Next, install Sendmail: 

    tdnf install sendmail

Make sure it is enabled: 

    systemctl status sendmail

Enable Sendmail if it's disabled and then start it: 

    systemctl enable sendmail
    systemctl start sendmail