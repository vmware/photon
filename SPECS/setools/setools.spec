Summary:        Policy analysis tools for SELinux
Name:           setools
Version:        4.4.1
Release:        2%{?dist}
License:        GPLv2, LGPLv2.1
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/SELinuxProject/setools/releases/download/%{version}/%{name}-%{version}.tar.bz2
%define sha512 %{name}=af1844f7f7232729eb7e93f6680775818cda93532c62524c5385a4ac7437c51bdb58ebd970a9f61f6e1b018367853d35303d3c5ee1cc087e0e26e893be42d559

BuildRequires:  cython3
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  libselinux-devel

Requires:       python3
Requires:       libselinux
Requires:       libsepol
Requires:       python3-networkx

%description
Policy analysis tools for SELinux

%prep
%autosetup -p1 -n %{name}
sed -i "s/, 'networkx>=2.0'//" setup.py

%build
python3 setup.py build_ext
%py3_build

%install
%py3_install
# do not package ru man pages
rm -rf %{buildroot}%{_mandir}/ru

%files
%defattr(-,root,root,-)
%{_bindir}/sesearch
%{_bindir}/sechecker
%{_bindir}/apol
%{_bindir}/seinfoflow
%{_bindir}/sedta
%{_bindir}/seinfo
%{_bindir}/sediff
%{python3_sitelib}/*
%{_mandir}/man1/*

%changelog
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.4.1-2
- Fix requires
* Fri Feb 10 2023 Gerrit Photon <photon-checkins@vmware.com> 4.4.1-1
- Automatic Version Bump
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 4.4.0-2
- Update release to compile with python 3.11
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 4.4.0-1
- Automatic Version Bump
* Fri Nov 06 2020 Tapas Kundu <tkundu@vmware.com> 4.3.0-2
- Build with python 3.9
* Fri May 01 2020 Alexey Makhalov <amakhalov@vmware.com> 4.3.0-1
- Initial build.
