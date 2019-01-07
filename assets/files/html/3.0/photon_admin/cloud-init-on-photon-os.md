# Cloud-Init on Photon OS

The minimal and full versions of Photon OS include the cloud-init service as a built-in component. Cloud-init is a set of Python scripts that initialize cloud instances of Linux machines. The cloud-init scripts configure SSH keys and run commands to customize the machine without user interaction. The commands can set the root password, create a hostname, configure networking, write files to disk, upgrade packages, run custom scripts, and restart the system. 

- [Cloud-Init Overview](cloud-init.md)
- [Deploy Photon OS With cloud-init](deploy_photon_with_cloud-init.md)
- [Creating a Stand-Alone Photon Machine with cloud-init](creating-a-stand-alone-photon-machine-with-cloud-init.md)
- [Customizing a Photon OS Machine on EC2](customizing-a-photon-os-machine-on-ec2.md)
- [Running a Photon OS Machine on GCE](running-a-photon-os-machine-on-gce.md)