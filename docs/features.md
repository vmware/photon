# Features

The two distinguishing features of Photon OS are as follows:

- It manages services with systemd. 
    
    By using systemd, Photon OS adopts a contemporary Linux standard to manage system services. Photon OS bootstraps the user space and concurrently starts services with systemd. The systemctl utility controls services on Photon OS. For example, instead of running the /etc/init.d/ssh script to stop and start the OpenSSH server on a init.d-based Linux system, you run the following systemctl commands on Photon OS: 
        
    - systemctl stop sshd
    - systemctl start sshd


- It manages packages with an open source, yum-compatible package manager called tdnf for Tiny DNF.
    
    Tdnf keeps the operating system as small as possible while preserving yum's robust package-management capabilities. On Photon OS, tdnf is the default package manager for installing new packages. It is a C implementation of the DNF package manager. 
