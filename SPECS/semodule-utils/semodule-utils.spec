Summary:        SELinux policy module utils
Name:           semodule-utils
Version:        3.0
Release:        2%{?dist}
License:        GPLv2
Group:          System Environment/Libraries
Source0:        https://github.com/SELinuxProject/selinux/releases/download/20191204/%{name}-%{version}.tar.gz
%define sha1    semodule-utils=1559edd76608a758f98898736a170178ac501570
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libsepol-devel = %{version}
Requires:       libsepol = %{version}
Requires:       libselinux-utils

%description
semodule-utils is set of tools for SELinux policy module manipulations.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" install
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
* Sun Jul 05 2020 Vikash Bansal <bvikas@vmware.com> 3.0-2
- Add libselinux-utils in requires
* Thu Apr 30 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
