%define debug_package %{nil}
Summary:        Device trees and overlays for Raspberry Pi
Name:           dtb-raspberrypi
Version:        6.1.10.2023.02.28
# Version Scheme: {kernel_ver}.{year}.{month}.{day}
Release:        2%{?dist}
%define rpi_linux_branch rpi-6.1.y
%define rpi_linux_req 6.1.10
URL:            https://github.com/raspberrypi/linux
Source0:        https://github.com/raspberrypi/linux/archive/rpi-linux-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Group:          System/Boot
Vendor:         VMware, Inc.
Distribution:   Photon

# enable fb to fix HDMI issue
Patch1:         0001-upstream-pi4-overlay-enable-fb.patch
# spi and audio overlays
Patch2:         0001-spi0-overlays-files.patch
Patch3:         0002-audio-overlays-files.patch

BuildRequires:  dtc
BuildRequires:  bison
Requires:       dtb-rpi3 = %{version}-%{release}
Requires:       dtb-rpi4 = %{version}-%{release}
Requires:       dtb-rpi-overlay = %{version}-%{release}
BuildArch:      aarch64

%description
Metapackage to install all Kernel Device Tree and Overlay Blobs for Raspberry Pi

%package -n dtb-rpi3
Summary:        Kernel Device Tree Blob files for Raspberry Pi3
Group:          System Environment/Kernel
Conflicts:      linux < %{rpi_linux_req}
Conflicts:      dtb-rpi-overlay < %{version}-%{release}
Conflicts:      dtb-rpi-overlay > %{version}-%{release}
%description -n dtb-rpi3
Kernel Device Tree Blob files for Raspberry Pi3

%package -n dtb-rpi4
Summary:        Kernel Device Tree Blob files for Raspberry Pi4
Group:          System Environment/Kernel
Conflicts:      linux < %{rpi_linux_req}
Conflicts:      dtb-rpi-overlay < %{version}-%{release}
Conflicts:      dtb-rpi-overlay > %{version}-%{release}
%description -n dtb-rpi4
Kernel Device Tree Blob files for Raspberry Pi4

%package -n dtb-rpi-overlay
Summary:        Kernel Device Tree Overlay Blob files for Raspberry Pi
Group:          System Environment/Kernel
Conflicts:      linux < %{rpi_linux_req}
%description -n dtb-rpi-overlay
Kernel Device Tree Overlay Blob files for Raspberry Pi

%prep
%autosetup -p1 -n rpi-linux-%{version}

%build
# make doesn't support _smp_mflags
make mrproper
# make doesn't support _smp_mflags
make bcm2711_defconfig
make %{?_smp_mflags} dtbs

%install
# make doesn't support _smp_mflags
make dtbs_install INSTALL_DTBS_PATH=%{buildroot}/boot/efi
pushd %{buildroot}/boot/efi
mv broadcom excluded
mv excluded/bcm2837-rpi-3-*.dtb ./
mv excluded/bcm2711-rpi-4-*.dtb ./
rm -rf excluded
popd

%files
%defattr(-,root,root)

%files -n dtb-rpi3
%defattr(-,root,root)
/boot/efi/bcm2837-rpi-3-*.dtb

%files -n dtb-rpi4
%defattr(-,root,root)
/boot/efi/bcm2711-rpi-4-*.dtb

%files -n dtb-rpi-overlay
%defattr(-,root,root,0755)
/boot/efi/overlays

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.10.2023.02.28-2
- Release bump for SRP compliance
* Mon Mar 06 2023 Ajay Kaher <akaher@vmware.com> 6.1.10.2023.02.28-1
- Update to v6.1.10.2023.02.28
* Fri Mar 03 2023 Piyush Gupta <gpiyush@vmware.com> 5.10.4.2021.01.07-3
- Added bison as BuildRequires.
* Thu Jan 21 2021 Ajay Kaher <akaher@vmware.com> 5.10.4.2021.01.07-2
- Adding audio and spi overlay
* Thu Jan 07 2021 Ajay Kaher <akaher@vmware.com> 5.10.4.2021.01.07-1
- Update to v5.10.4.2021.01.07
- Enable fb in upstream-pi4 overlay
* Fri Sep 11 2020 Bo Gan <ganb@vmware.com> 5.9.0.2020.09.23-1
- Initial packaging
