# What is New in Photon OS 3.0

Photon OS 3.0 introduces support for ARM64 (Raspberry Pi 3), installer improvements, and up-to-date OSS packages including Linux kernel, systemd and glibc. 

## Features

### ARM64

- Support for Raspberry Pi 3 pre-built image and the ability to build new images in the image builder.

### Installer Updates

- Ability to run the installer from multiple media, such as USB, CDROM, and Kickstart, on a wider range of storage devices.

### Package and Binary Maintenance

- Cloud-ready images for rapid deployment on Microsoft Azure (new), Google Compute Engine (GCE), Amazon Elastic Compute Cloud (EC2), and VMware products (vSphere, Fusion, and Workstation)
- New package versions for the following base OS packages:
    - Linux kernel 4.18
    - Glibc 2.28
    - systemd 239
    - Python3 3.7
    - Openjdk : 1.8.0.181, 1.9.0.181 and 1.10.0.23
- Up-to-date versions for most packages available in the repository.
- Ability to support multiple versions of the same package (For example, go-1.9 and go-1.10).
- Support for new packages including EdgeX, Liota, linux-firmware, wpa-supplicant for WLAN, consul, meson, and so on.


## Known Issues

- The OVA does not deploy on Workstation 14 but works on later and earlier versions.
- The Dialog package cannot be installed in 3.0.
- Not all packages in the x86-64 repo are available for ARM64. Notable ones include mysql, mariadb and dotnet libraries.