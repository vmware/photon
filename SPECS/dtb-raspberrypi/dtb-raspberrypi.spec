%define debug_package %{nil}
Summary:        Device trees and overlays for Raspberry Pi
Name:           dtb-raspberrypi
Version:        5.9.0.2020.09.23
# Version Scheme: {kernel_ver}.{year}.{month}.{day}
Release:        1%{?dist}
License:        GPLv2
%define rpi_linux_branch rpi-5.9.y
%define rpi_linux_req 5.9.0
URL:            https://github.com/raspberrypi/linux
Source0:        https://github.com/raspberrypi/linux/archive/rpi-linux-%{version}.tar.gz
%define sha1    rpi-linux=c6891434a97740e5e1773029ca8a154128a65f3e
Group:          System/Boot
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  dtc
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
%setup -q -n rpi-linux-%{version}

%build
make mrproper
make bcm2711_defconfig
make %{?_smp_mflags} dtbs

%install
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
*   Fri Sep 11 2020 Bo Gan <ganb@vmware.com> 5.9.0.2020.09.23-1
-   Initial packaging
