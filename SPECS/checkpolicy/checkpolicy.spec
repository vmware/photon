Summary:        SELinux policy compiler
Name:           checkpolicy
Version:        3.2
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Libraries
Source0:        https://github.com/SELinuxProject/selinux/releases/download/20200710/%{name}-%{version}.tar.gz
%define sha1    checkpolicy=71262b34fd4147bbe34ba00433cfd74850c645b0
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libsemanage-devel = %{version}

%description
checkpolicy is a program that checks and compiles a SELinux security policy configuration
into a binary representation that can be loaded into the kernel.

%prep
%autosetup

%build
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" install
# do not package ru man pages
rm -rf %{buildroot}%{_mandir}/ru

%files
%defattr(-,root,root,-)
%{_bindir}/checkpolicy
%{_bindir}/checkmodule
%{_mandir}/man8/checkpolicy.8.gz
%{_mandir}/man8/checkmodule.8.gz

%changelog
* Fri Sep 03 2021 Vikash Bansal <bvikas@vmware.com> 3.2-1
- Update to version 3.2
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Thu Apr 30 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
