Summary:        SELinux policy core utilities
Name:           policycoreutils
Version:        3.1
Release:        1%{?dist}
License:        Public Domain
Group:          System Environment/Libraries
Source0:        https://github.com/SELinuxProject/selinux/releases/download/20200710/%{name}-%{version}.tar.gz
%define sha1    policycoreutils=8fb3bc30cdff1d48dd66e89489a0c59201a7c986
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libsemanage-devel = %{version}
Requires:       libsemanage = %{version}

%description
policycoreutils contains the policy core utilities that are required for
basic operation of a SELinux system.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" install
rm -rf %{buildroot}%{_datadir}/locale
# do not package ru man pages
rm -rf %{buildroot}%{_mandir}/ru

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/*
%{_sysconfdir}/sestatus.conf
%{_datadir}/bash-completion/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*


%changelog
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
