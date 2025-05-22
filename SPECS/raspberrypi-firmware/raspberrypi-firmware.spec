%global debug_package %{nil}
%global __os_install_post %{nil}
%define _binaries_in_noarch_packages_terminate_build   0

Name:       raspberrypi-firmware
Summary:    Raspberry Pi firmware
Version:    1.20230106
Release:    3%{?dist}
URL:        https://github.com/raspberrypi/firmware
Group:      System Environment/Boot
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz

Source1:    rpi-config-txt.txt

Source2: license.txt
%include %{SOURCE2}

BuildArch:  noarch

%description
Firmware files for Raspberry Pi

%package pi3
Summary:    Raspberry Pi 3 firmware
Group:      System Environment/Boot
Requires:   raspberrypi-firmware = %{version}-%{release}
Requires(preun): coreutils >= 9.1-10
Requires(post): coreutils >= 9.1-10

%description pi3
Firmware files for Raspberry Pi 3

%package pi3-extra
Summary:    Extra files for Raspberry Pi 3 firmware
Group:      System Environment/Boot
Requires:   raspberrypi-firmware-pi3 = %{version}-%{release}
Requires(preun): coreutils >= 9.1-10
Requires(post): coreutils >= 9.1-10

%description pi3-extra
Extra Firmware files for Raspberry Pi 3

%package pi4
Summary:    Raspberry Pi 4 firmware
Group:      System Environment/Boot
Requires:   raspberrypi-firmware = %{version}-%{release}
Requires(preun): coreutils >= 9.1-10
Requires(post): coreutils >= 9.1-10

%description pi4
Firmware files for Raspberry Pi 4

%package pi4-extra
Summary:    Extra files for Raspberry Pi 4 firmware
Group:      System Environment/Boot
Requires:   raspberrypi-firmware-pi4 = %{version}-%{release}
Requires(preun): coreutils >= 9.1-10
Requires(post): coreutils >= 9.1-10

%description pi4-extra
Extra Firmware files for Raspberry Pi 4

%prep
%autosetup -p1

%build

%install
mkdir -p %{buildroot}/boot/efi
for s in boot/start*.elf; do
  install -vm 755 "$s" %{buildroot}/boot/efi/
done
for f in boot/fixup*.dat; do
  install -vm 644 "$f"  %{buildroot}/boot/efi/
done
install -vm 755 boot/bootcode.bin %{buildroot}/boot/efi/
install -vm 644 boot/LICENCE.broadcom %{buildroot}/boot/efi/
install -vm 644 %{SOURCE1} %{buildroot}/boot/efi/config.txt

%files
%defattr(-,root,root)
/boot/efi/LICENCE.broadcom
%config /boot/efi/config.txt

%files pi3
%defattr(-,root,root)
/boot/efi/bootcode.bin
/boot/efi/start.elf
/boot/efi/fixup.dat

%files pi3-extra
%defattr(-,root,root)
/boot/efi/start_cd.elf
/boot/efi/start_db.elf
/boot/efi/start_x.elf
/boot/efi/fixup_cd.dat
/boot/efi/fixup_db.dat
/boot/efi/fixup_x.dat

%files pi4
%defattr(-,root,root)
/boot/efi/start4.elf
/boot/efi/fixup4.dat

%files pi4-extra
%defattr(-,root,root)
/boot/efi/start4cd.elf
/boot/efi/start4db.elf
/boot/efi/start4x.elf
/boot/efi/fixup4cd.dat
/boot/efi/fixup4db.dat
/boot/efi/fixup4x.dat

%changelog
* Fri May 09 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.20230106-3
- Require coreutils only
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.20230106-2
- Release bump for SRP compliance
* Fri Feb 10 2023 Gerrit Photon <photon-checkins@vmware.com> 1.20230106-1
- Automatic Version Bump
* Wed Jan 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.20210303-2
- Fix requires
* Thu May 06 2021 Gerrit Photon <photon-checkins@vmware.com> 1.20210303-1
- Automatic Version Bump
* Mon Nov 02 2020 Bo Gan <ganb@vmware.com> 1.2020.09.02-2
- Use miniuart-bt and fixed core_freq to accommodate for rpi3 uart
* Mon Sep 21 2020 Bo Gan <ganb@vmware.com> 1.2020.09.02-1
- Initial packaging
