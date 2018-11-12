# Introduction to Photon OS

Photon OS, is an open-source minimalist Linux operating system from VMware that is optimized for cloud computing platforms, VMware vSphere deployments, and applications native to the cloud. 

Photon OS is a Linux container host optimized for vSphere and cloud-computing platforms such as Amazon Elastic Compute and Google Compute Engine. As a lightweight and extensible operating system, Photon OS works with the most common container formats, including Docker, Rocket, and Garden. Photon OS includes a yum-compatible, package-based lifecycle management system called tdnf.

When used with development tools and environments such as VMware Fusion, VMware Workstation, and production runtime environments (vSphere, vCloud Air), Photon OS lets you seamlessly migrate container-based applications from development to production. With a small footprint and fast boot and run times, Photon OS is optimized for cloud computing and cloud  applications.  

Photon OS consists of a minimal version and a full version. 

The minimal version of Photon OS is lightweight container host runtime environment that is suited to managing and hosting containers. The minimal version contains just enough packaging and functionality to manage and modify containers while remaining a fast runtime environment. The minimal version is ready to work with appliances. 

The full version of Photon OS includes additional packages to help you customize the system and create containerized applications. For running containers, the full version is excessive. The full version is helps you create, develop, test, and package an application that runs a container. 

The two distinguishing features of Photon OS are as follows:

- It manages services with systemd. 
    
    By using systemd, Photon OS adopts a contemporary Linux standard to manage system services. Photon OS bootstraps the user space and concurrently starts services with systemd. The systemctl utility controls services on Photon OS. For example, instead of running the /etc/init.d/ssh script to stop and start the OpenSSH server on a init.d-based Linux system, you run the following systemctl commands on Photon OS: 
    
    - systemctl stop sshd
    - systemctl start sshd

- It manages packages with an open source, yum-compatible package manager called tdnf for Tiny DNF.
    
    Tdnf keeps the operating system as small as possible while preserving yum's robust package-management capabilities. On Photon OS, tdnf is the default package manager for installing new packages. It is a C implementation of the DNF package manager. 
