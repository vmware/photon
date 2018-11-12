# Photon OS Administration Guide



- [Photon OS Administration Guide](README.md)
-   [Introduction](introduction.md)
    -   [Examining the Packages in the SPECS Directory on Github](examining_packages_spec_dir.md)
    -   [Looking at the Differences Between the Minimal and the Full
        Version](differences_between_minimal_and_full_version.md)
    -   [The Root Account and the `sudo` and `su`
        Commands](root_account_and_sudo_commands.md)
-   [Tiny DNF for Package
    Management](tiny-dnf-for-package-management.md)
    -   [Configuration Files and
        Repositories](configuration-files-and-repositories.md)
    -   [Options for Commands](options-for-commands.md)
    -   [Commands](commands.md)
    -   [Adding a New Repository](adding-a-new-repository.md)
    -   [Adding the Dev Repository to Get New Packages from the
        GitHub Dev
        Branch](adding-the-dev-repository.md)
-   [Managing Services with
    systemd](managing-services-with-systemd.md)
    -   [Viewing Services](viewing-services.md)
    -   [Controlling Services](controlling-services.md)
    -   [Creating a Startup Service](creating-a-startup-service.md)
    -   [Disabling the Photon OS
        httpd.service](disabling-the-photon-os-httpd.service.md)
    -   [Auditing System Events with
        auditd](auditing-system-events-with-auditd.md)
    -   [Analyzing systemd Logs with
        journalctl](analyzing-systemd-logs-with-journalctl.md)
    -   [Migrating Scripts to
        systemd](migrating-scripts-to-systemd.md)
-   [Managing the Network
    Configuration](managing-the-network-configuration.md)
    -   [Using the Network Configuration Manager](using-the-network-configuration-manager.md)
    -   [Use `ip` and `ss` Commands Instead of `ifconfig` and
        `netstat`](use-ip-and-ss-commands.md)
    -   [Configuring Network
        Interfaces](configuring-network-interfaces.md)
    -   [Setting a Static IP Address](setting-a-static-ip-address.md)
    -   [Turning Off DHCP](turning-off-dhcp.md)
    -   [Adding a DNS Server](adding-a-dns-server.md)
    -   [Setting Up Networking for Multiple
        NICs](setting-up-networking-for-multiple-nics.md)
    -   [Combining DHCP and Static IP Addresses with IPv4 and
        IPv6](combining-dhcp-and-static-ip-addresses-with-ipv4-and-ipv6.md)
    -   [Clearing the Machine ID of a Cloned Instance for
        DHCP](clearing-the-machine-id-of-a-cloned-instance-for-dhcp.md)
    -   [Using Predictable Network Interface
        Names](using-predictable-network-interface-names.md)
    -   [Inspecting the Status of Network Links with
        `networkctl`](inspecting-the-status-of-network-links-with-networkctl.md)
    -   [Turning on Network
        Debugging](turning-on-network-debugging.md)
    -   [Mounting a Network File
        System](mounting-a-network-file-system.md)
    -   [Installing the Packages for tcpdump and netcat with
        tdnf](installing-the-packages-for-tcpdump-and-netcat-with-tdnf.md)
-   [Cloud-Init on Photon OS](cloud-init-on-photon-os.md)
    -   [Creating a Stand-Alone Photon Machine with
        cloud-init](creating-a-stand-alone-photon-machine-with-cloud-init.md)
    -   [Customizing a Photon OS Machine on
        EC2](customizing-a-photon-os-machine-on-ec2.md)
    -   [Running a Photon OS Machine on
        GCE](running-a-photon-os-machine-on-gce.md)
-   [Docker Containers](docker-containers.md)
-   [Kubernetes](kubernetes.md)
-   [Installing Sendmail](installing-sendmail.md
-   [Changing the Locale](changing-the-locale.md)
-   [The Default Security Policy of Photon
    OS](default-security-policy-of-photon-os.md)
    -   [Default Firewall Settings](default-firewall-settings.md)
    -   [Default Permissions and
        umask](default-permissions-and-umask.md)
-   [Disabling TLS 1.0 to Improve Transport Layer
    Security](disabling-tls.md)
-   [Working with Repositories and
    Packages](working-with-repositories-and-packages.md)
    -   [Photon OS Package
        Repositories](photon-os-package-repositories.md)
    -   [Examining Signed Packages](signed-packages.md)
    -   [Building a Package from a Source
        RPM](building-a-package-from-a-source-rpm.md)
    -   [Compiling C++ Code on the Minimal Version of Photon
        OS](compiling-c-code-on-the-minimal-version-of-photon-os.md)
- [Photon Management Daemon Command-line Interface (pmd-cli)](pmd-cli.md)
- [Network Configuration Manager - C API](netmgr.c.md)
- [Photon Network Manager Command-line Interface (netmgr)](netmgr-cli.md)
- [Network Configuration Manager - Python API](netmgr.python.md)
- [Managing Packages in Photon OS with tdnf](tdnf.md)        
