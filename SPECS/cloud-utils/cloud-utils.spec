Summary:        Shell script to auto detect free size on disk and grow partition.
Name:           cloud-utils
Version:        0.31
Release:        2%{?dist}
License:        GPLv3
Group:          System Environment
Source0:        https://launchpad.net/cloud-utils/trunk/%{version}/+download/cloud-utils-%{version}.tar.gz
%define sha512  cloud-utils=4ca22def9564e101e228ca363d7f2da593f0644a09581bf862d4aeb4b320cc7c8af5a5e7af6283966ee1a8828715bb94725c0aab584b77e97f77a3ad593c2629
URL:            https://launchpad.net/cloud-utils
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       gptfdisk
Requires:       gawk
Requires:       util-linux
BuildArch:      noarch

%description
Cloud-utils brings in growpart script. This script is very useful for
detecting available disk size and grow the partition.
This is generally used by cloud-init for disk space manangement on cloud images.

%prep
%autosetup -p1 -n cloud-utils-%{version}

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
* Sat Apr 29 2023 Harinadh D <hdommaraju@vmware.com> 0.31-2
- Fix for requires
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.31-1
- Automatic Version Bump
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 0.30-3
- Requires util-linux or toybox
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.30-2
- Fix arch
* Wed Mar 29 2017 Kumar Kaushik <kaushikk@vmware.com> 0.30-1
- Initial build.  First version
