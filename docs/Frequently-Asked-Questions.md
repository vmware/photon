* [What is Photon OS?](#q-what-is-photon-os)
* [How do I get started with Photon OS?](#q-how-do-i-get-started-with-photon-os)
* [Can I upgrade my existing Photon OS 1.0 VMs?](#q-can-i-upgrade-my-existing-photon-os-10-vms)
* [What kind of support comes with Photon OS?](#q-what-kind-of-support-comes-with-photon-os)
* [How can I contribute to Photon OS?](#q-how-can-i-contribute-to-photon-os)
* [How is Photon OS patched?](#q-how-is-Photon-OS-patched)
* [How does Photon OS relate to Project Lightwave?](#q-how-does-photon-os-relate-to-project-lightwave)
* [Will VMware continue to support other container host runtime offerings on vSphere?](#q-will-vmware-continue-to-support-other-container-host-runtime-offerings-on-vsphere)
* [How to report a security vulnerability in Photon OS?](#q-how-to-report-a-security-vulnerability-in-photon-os)
* [What are the Docker improvements in Photon OS 2.0?](#q-what-are-the-docker-improvements-in-photon-os-20)
* [Why is VMware creating Photon OS?](#q-why-is-vmware-creating-photon-os)
* [Why is VMware open-sourcing Photon OS?](#q-why-is-vmware-open-sourcing-photon-os)
* [In what way is Photon OS "optimized for VMware?"](#q-in-what-way-is-photon-os-optimized-for-vmware)
* [Why can't I SSH in as root?](#q-why-cant-i-ssh-in-as-root)
* [Why isn't netstat working?](#q-why-is-netstat-not-working)
* [Why do all of my cloned Photon OS instances have the same IP address when using DHCP?](#q-why-do-all-of-my-cloned-photon-os-instances-have-the-same-ip-address-when-using-dhcp)
* [How to install new packages?](#how-to-install-new-packages)
* [Why is the yum command not working in a minimal installation?](#q-why-the-yum-command-not-working-in-a-minimal-installation)
* [How to install all build essentials?](#q-how-to-install-all-build-essentials)
* [How to build new package for Photon OS?](#q-how-to-build-new-package-for-photon-os)
* [I just booted into freshly installed Photon OS instance, why isn't "docker ps" working?](#q-i-just-booted-into-freshly-installed-photon-os-instance-why-isnt-docker-ps-working)
* [What is the difference between Minimal and Full installation?](#q-what-is-the-difference-between-minimal-and-full-installation)
* [What packages are included in Minimal and Full?](#q-what-packages-are-included-in-minimal-and-full)
* [How do I transfer or share files between Photon OS and my host machine?](#q-how-do-i-transfer-or-share-files-between-photon-and-my-host-machine)
* [Why is the ISO over 2GB, when I hear that Photon OS is a minimal container runtime?](#q-why-is-the-iso-over-2gb-when-i-hear-that-photon-os-is-a-minimal-container-runtime)

***

# Getting Started

## Q. What is Photon OS?
A. Photon OS™ is an open source Linux container host optimized for cloud-native applications, cloud platforms, and VMware infrastructure. Photon OS provides a secure run-time environment for efficiently running containers. For an overview, see [https://vmware.github.io/photon/](https://vmware.github.io/photon/).

## Q. How do I get started with Photon OS?
A. Start by deciding your target platform. Photon OS 2.0 has been certified in public cloud environments - Microsoft Azure (new), Google Compute Engine (GCE), Amazon Elastic Compute Cloud (EC2) - as well as on VMware vSphere, VMware Fusion, and VMware Workstation.
Next, download the latest binary distributions for your target platform. The binaries are hosted on [https://bintray.com/vmware/photon/](https://bintray.com/vmware/photon/). For download instructions, see [Downloading Photon OS](https://github.com/vmware/photon/wiki/Downloading-Photon-OS).
Finally, go to the installation instructions for your target platform, which are listed here: [https://github.com/vmware/photon/wiki](https://github.com/vmware/photon/wiki).

## Q. Can I upgrade my existing Photon OS 1.0 VMs?
A. Yes, there is an in-place upgrade path for Photon OS 1.0 implementations. You simply download an upgrade package, run a script, and reboot the VM. Refer to the instructions in [Upgrading to Photon OS 2.0](https://github.com/vmware/photon/wiki/Upgrading-to-Photon-OS-2.0).

## Q. What kind of support comes with Photon OS?
A. Photon OS is supported through community efforts and direct developer engagement in the communities. Potential users of Photon OS should start with the [Photon microsite](http://vmware.com/photon).

Developers who might want the source code, including those interested in making contributions, should visit the [Photon OS Github repository](https://github.com/vmware/photon). 

## Q. How can I contribute to Photon OS?
A. We welcome community participation in the development of Photon OS and look forward to broad ecosystem engagement around the project. Getting your idea into Photon OS is just a [GitHub](https://vmware.github.io/photon) pull request away. When you submit a pull request, you'll be asked to accept the Contributor License Agreement (CLA). 

## Q. How is Photon OS patched?
A. Within a major release, updates will be delivered as package updates. Security updates will be delivered on an as-needed basis. Non-security related updates will happen quarterly, but may not include every, single package update. The focus is on delivering a valid, functional updated stack every quarter.

Photon OS isn't "patched," as a whole - instead, individual packages are updated (potentially, with patches applied to that individual package). For instance, if a package releases a fix for a critical vulnerability, we'll update the package in the Photon OS repository, for critical issues probably within a day or two. At that point, customers get that updated package by running, "tdnf update <package>"
 
## Q. How does Photon OS relate to Project Lightwave?
A. Project Lightwave is an open-sourced project that provides enterprise-grade identity and access management services, and can be used to solve key security, governance, and compliance challenges for a variety of use cases within the enterprise.
Through integration between Photon OS and Project Lightwave, organizations can enforce security and 
governance on container workloads, for example, by ensuring only authorized containers are run on authorized hosts, by authorized users. For details about Lightwave, see [https://github.com/vmware/lightwave](https://github.com/vmware/lightwave).

## Q. Will VMware continue to support other container host runtime offerings on vSphere?
A. YES, VMware is committed to delivering an infrastructure for all workloads, and for vSphere to have the largest guest OS support in the industry and support customer choice. 
Toward those goals, VMware will continue to work with our technology partners to support new Guest Operating Systems and container host runtimes as they come to the market. Open-sourcing Photon OS will enable optimizations and enhancements for container host runtimes on VMware Platform are available as reference implementation for other container host runtimes as well.

# Photon OS
## Q. What is Photon OS?
A. Photon OS is an open source, Linux container host runtime optimized for VMware vSphere®. Photon OS is extensible, lightweight, and supports the most common container formats including Docker, Rocket and Garden. Photon OS includes a small footprint, yum-compatible, package-based lifecycle management system, and can support an rpm-ostree image-based system versioning. When used with development tools and environments such as VMware Fusion®, VMware Workstation™, HashiCorp (Vagrant and Atlas) and a production runtime environment (vSphere, VMware vCloud® Air™), Photon OS allows seamless migration of containers-based Apps from development to production.

## Q. How to report a security vulnerability in Photon OS?
A. VMware encourages users who become aware of a security vulnerability in VMware products to contact VMware with details of the vulnerability. VMware has established an email address that should be used for reporting a vulnerability. Please send descriptions of any vulnerabilities found to security@vmware.com. Please include details on the software and hardware configuration of your system so that we can duplicate the issue being reported.

Note: We encourage use of encrypted email. Our public PGP key is found at [kb.vmware.com/kb/1055](http://kb.vmware.com/kb/1055).

VMware hopes that users encountering a new vulnerability will contact us privately as it is in the best interests of our customers that VMware has an opportunity to investigate and confirm a suspected vulnerability before it becomes public knowledge.

In the case of vulnerabilities found in third-party software components used in VMware products, please also notify VMware as described above.

## Q. What are the Docker improvements in Photon OS 2.0?
In Photon OS 2.0, the Docker image size (compressed and uncompressed) was reduced to less than a third of its size in Photon OS 1.0. This gain resulted from:
- using toybox (instead of standard core tools), which brings the docker image size from 50MB (in 1.0) to 14MB (in 2.0)
- a package split - in Photon OS 2.0, the binary set contains only bash, tdnf, and toybox; all other installed packages are now libraries only.

## Q. Why is VMware creating Photon OS?
A. It's about workloads - VMware has always positioned our vSphere platform as a secure, highly-performant platform for enterprise applications. With containers, providing an optimized runtime ensures that customers can embrace these new workload technologies without disrupting existing operations. Over time, Photon OS will extend the capabilities of the software-defined data center such as security, identity and resource management to containerized workloads. Organizations can then leverage a single infrastructure architecture for both traditional and cloud-native Apps, and leverage existing investments in tools, skills and technologies. This converged environment will simplify operation and troubleshooting, and ease the adoption of Cloud-Native Apps. 

Photon OS can provide a reference implementation for optimizing containers on VMware platforms across compute, network, storage and management. For example, Photon OS can deliver performance through kernel tuning to remove redundant caching between the Linux kernel and the vSphere hypervisor, and advanced security services through network micro-segmentation delivered by VMware NSX™, and more.

## Q. Why is VMware open-sourcing Photon OS?
A. Open-sourcing Photon OS encourages discussion, innovation, and collaboration with others in the container ecosystem. In particular, we want to make sure the innovations we introduce to Photon to run containers effectively on VMware are also available to any other container runtime OS. 
Additionally, VMware is committed to supporting industry and de facto standards, as doing so also supports stronger security, interoperability, and choice for our customers. 

## Q. In what way is Photon OS "optimized for VMware?"

Photon OS 1.0 introduced extensive optimizations for VMware environments, which are described in detail in the following VMware white paper: [Deploying Cloud-Native Applications with Photon OS](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/whitepaper/vmware-deploying-cloud-native-apps-with-photon-os.pdf). Photon OS 2.0 enhances VMware optimization. The kernel message dumper (new in Photon OS 2.0) is a paravirt feature that extends debugging support. In case of a guest panic, the kernel (through the paravirt channel) dumps the entire kernel log buffer (including the panic message) into the VMware log file (vmware.log) for easy, consolidated access. Previously, this information was stored in a huge vmss (VM suspend state) file.

## Q. Why can't I SSH in as root?
A. By default Photon does not permit root login to ssh. To make yourself login as root using SSH set PermitRootLogin yes in /etc/ssh/sshd_config, and restart the sshd deamon.

## Q. Why is netstat not working?
A. netstat is deprecated, ss or ip (part of iproute2) should be used instead.

## Q. Why do all of my cloned Photon OS instances have the same IP address when using DHCP?
A. Photon OS uses the contents of /etc/machine-id to determine the duid that is used for DHCP requests. If you're going to use a Photon OS instance as the base system for cloning to create additional Photon OS instances, you should clear the machine-id with:
~~~~
    echo -n > /etc/machine-id
~~~~
With this value cleared, systemd will regenerate the machine-id and, as a result, all DHCP requests will contain a unique duid. 

# How to install new packages?
## Q. Why is the yum command not working in a minimal installation?
A. yum has package dependencies that make the system larger than it needs to be. Photon OS includes [tdnf](https://github.com/vmware/tdnf) - 'tiny' dandified yum - to provide package management and yum-functionality in a much, much smaller footprint. To install packages from cdrom, mount cdrom using following command
~~~~
     mount /dev/cdrom /media/cdrom
~~~~
Then, you can use tdnf to install new packages. For example, to install the vim editor, 
~~~~
     tdnf install vim
~~~~
## Q. How to install all build essentials?
A. Following command can be used to install all build essentials.
~~~~
curl -L https://git.io/v1boE | xargs -I {} tdnf install -y {}
~~~~
## Q. How to build new package for Photon OS??
A. Assuming you have an Ubuntu development environment, setup and get the latest code pull into /workspace. Lets assume your package name is foo with version 1.0.
~~~~
    cp foo-1.0.tar.gz /workspace/photon/SOURCES
    cp foo.spec /workspace/photon/SPECS/foo/
    cd /workspace/photon/support/package-builder
    sudo python ./build_package.py -i foo
~~~~
## Q. I just booted into freshly installed Photon OS instance, why isn't "docker ps" working?
A. Make sure docker daemon is running. By design and default in Photon OS, the docker daemon/engine is not started at boot time. To start the docker daemon for the current session, use the command:
~~~~
    systemctl start docker
~~~~
To start the docker daemon, on boot, use the command:
~~~~
    systemctl enable docker
~~~~
## Q. What is the difference between Minimal and Full installation?
A. Minimal is the minimal set of packages for a container runtime, plus cloud-init.
Full contains all the packages shipped with ISO.

## Q. What packages are included in Minimal and Full?
A. See [packages_minimal.json](https://github.com/vmware/photon/blob/dev/common/data/packages_minimal.json) as an example

## Q. How do I transfer or share files between Photon and my host machine?
A. Use vmhgfs-fuse to transfer files between Photon and your host machine:
1. Enable Shared folders in the Workstation or Fusion UI (edit the VM settings and choose Options->Enabled shared folders).
2. Make sure open-vm-tools is installed (it is installed by default in the Minimal installation and OVA import).
3. Run vmware-hgfsclient to list the shares.

Next, do one of the following:

- Run the following to mount:
~~~~
vmhgfs-fuse .host:/$(vmware-hgfsclient) /mnt/hgfs
~~~~
OR

- Add the following line to /etc/fstab:
~~~~
.host:/ /mnt/hgfs fuse.vmhgfs-fuse <options> 0 0
~~~~

## Q. Why is the ISO over 2GB, when I hear that Photon OS is a minimal container runtime?
A. ISO includes a repository with all Photon OS packages. When you mount the ISO to a machine and boot to the Photon installer, you'll be able to choose the Photon Minimal installation option and the hypervisor-optimized Linux kernel, which will reduce the storage size.