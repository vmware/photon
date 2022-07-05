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
%define sha1    %{name}=ec19f65e881d4b3822afe7ce723478cc442fb519

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
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.2-1
- Automatic Version Bump
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Sun Jul 05 2020 Vikash Bansal <bvikas@vmware.com> 3.0-2
- Add libselinux-utils in requires
* Thu Apr 30 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
