Summary:        Shell script to auto detect free size on disk and grow partition.
Name:           cloud-utils
Version:        0.32
Release:        3%{?dist}
URL:            https://launchpad.net/cloud-utils
License:        GPLv3
Group:          System Environment
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://launchpad.net/cloud-utils/trunk/%{version}/+download/cloud-utils-%{version}.tar.gz
%define sha512 %{name}=e501ac4503c1d4086a89c966a263bc3a9d25c5454a7dcedd854baa17885247f85db720fd124c2a6e47c27d17a1fa33d914073ff05d0d3da1ea7befe35056ab9c

Requires:       gptfdisk
Requires:       gawk
Requires:       util-linux

BuildArch:      noarch

%description
Cloud-utils brings in growpart script. This script is very useful for
detecting available disk size and grow the partition.
This is generally used by cloud-init for disk space manangement on cloud images.

%prep
%autosetup -p1

%build
%install
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_mandir}/man1

cp -p bin/growpart %{buildroot}%{_bindir}/
cp -p man/growpart.* %{buildroot}%{_mandir}/man1/

%files
%defattr(-,root,root)
%{_bindir}/growpart
%doc %{_mandir}/man1/growpart.*

%changelog
* Mon Apr 01 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.32-3
- Bump version as a part of util-linux upgrade
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.32-2
- Fix requires
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 0.32-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.31-1
- Automatic Version Bump
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 0.30-3
- Requires util-linux or toybox
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.30-2
- Fix arch
* Wed Mar 29 2017 Kumar Kaushik <kaushikk@vmware.com> 0.30-1
- Initial build.  First version
