Summary:        SELinux policy module utils
Name:           semodule-utils
Version:        3.3
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=76aa0c9322889c7de100f3c5789bdf27b7073827fe2af371bd50a4517baa8442f35e53f16a93227dce93da0ceb054bea7e5ee17a46fe05e06f3c2d9925cf59dc

BuildRequires:  libsepol-devel = %{version}
Requires:       libsepol = %{version}
Requires:       libselinux-utils

%description
semodule-utils is set of tools for SELinux policy module manipulations.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" \
     BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" %{?_smp_mflags} install
# do not package ru man pages
rm -rf %{buildroot}%{_mandir}/ru

%files
%defattr(-,root,root,-)
%{_bindir}/semodule_expand
%{_bindir}/semodule_link
%{_bindir}/semodule_package
%{_bindir}/semodule_unpackage
%{_mandir}/man8/semodule_expand.8.gz
%{_mandir}/man8/semodule_link.8.gz
%{_mandir}/man8/semodule_package.8.gz
%{_mandir}/man8/semodule_unpackage.8.gz

%changelog
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Upgrade v3.3
* Fri Sep 03 2021 Vikash Bansal <bvikas@vmware.com> 3.2-1
- Update to version 3.2
* Sun Jul 05 2020 Vikash Bansal <bvikas@vmware.com> 3.0-2
- Add libselinux-utils in requires
* Thu Apr 30 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
