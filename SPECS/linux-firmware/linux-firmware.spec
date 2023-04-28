%global debug_package %{nil}
%global __os_install_post %{nil}
%global _firmwarepath /lib/firmware
%define _binaries_in_noarch_packages_terminate_build 0

Summary: Linux Firmware
Name: linux-firmware
Version: 20230320
Release: 1%{?dist}
License: GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted
URL: http://www.kernel.org/
Group: System Environment/Kernel
Vendor: VMware, Inc.
Distribution: Photon
# Generate the source using
# https://github.com/vmware/photon/blob/4.0/tools/scripts/generate-linux-firmware-tarball.sh
Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=b40114c48533df8698fd6f1991028d25bf88439b0e2bfee6f21f35f4c511b08150fa1152fc036e51deb63fd3ee8dcc3fe632f185be2b197a3d2c44c35b072b93
BuildArch: noarch

%description
This package includes firmware files required for some devices to operate.

%prep
%autosetup -p1

%build

%install
mkdir -p %{buildroot}%{_firmwarepath}
# Copy entire tree as is
cp -r * %{buildroot}%{_firmwarepath}

%files
%defattr(-,root,root)
%{_firmwarepath}/*

%changelog
* Mon Mar 20 2023 Ankit Jain <ankitja@vmware.com> 20230320-1
- Updated ice firmware version as per linux.spec
* Tue Aug 02 2022 Alexey Makhalov <amakhalov@vmware.com> 20220802-1
- Added amdgpu vega10 firmware.
- Deprecated NXP firmware.
- Use "set -e" for error checking.
- Fix nonfree firmware location (branch name).
* Tue Aug 17 2021 Ajay Kaher <akaher@vmware.com> 20210817-1
- Updated to fix rpi wi-fi issue
* Tue Feb 09 2021 Ankit Jain <ankitja@vmware.com> 20210209-1
- Added firmware for Intel's ice-1.3.2 driver
* Wed Dec 02 2020 Ankit Jain <ankitja@vmware.com> 20201202-1
- Added NVRAM config file for the BCM43455 for rpi4b firmware
- Added regulatory db for rpi4b firmware
* Wed Jan 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 20200115-1
- Added ilo4 nic firmware
* Thu Oct 24 2019 Ajay Kaher <akaher@vmware.com> 20191030-1
- Added Dell 5K Gateway firmware.
* Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 20190830-1
- Added ath10k firmware for ls1046a.
* Tue Feb 05 2019 Alexey Makhalov <amakhalov@vmware.com> 20190205-1
- Added ath10k firmware (for ls1012a).
- Use 1:1 folder layout for ppfe firmware.
* Wed Jan 09 2019 Alexey Makhalov <amakhalov@vmware.com> 20190109-1
- Added Compulab Fitlet2 firmware.
* Thu Nov 29 2018 Srinidhi Rao <srinidhir@vmware.com> 20181129-1
- Updated pfe firmware files for NXP LS1012A FRWY board
* Wed Oct 10 2018 Ajay Kaher <akaher@vmware.com> 20181010-1
- Updated brcm firmwares for Rpi B and Rpi B+
* Thu Aug 23 2018 Alexey Makhalov <amakhalov@vmware.com> 20180823-1
- Initial version. RPi3 and Dell Edge Gateway 3001 support.
