Summary:        SELinux policy management libraries
Name:           libsemanage
Version:        3.4
Release:        4%{?dist}
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=831dc789545bb9a0b009bdb4f7fe52f6197ad8325946640f886a960d08e40b8a69eccd5a70cce51466bb5cb7f742feb78d19a9ec63383fbd03aa451508677e73

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libselinux-devel = %{version}
BuildRequires:  libsepol-devel = %{version}
BuildRequires:  swig
BuildRequires:  audit-devel
BuildRequires:  python3-devel
BuildRequires:  bison

Requires:       libselinux = %{version}
Requires:       libsepol = %{version}
Requires:       audit

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

%package        devel
Summary:        Header files and libraries for libsemanage
Group:          Development/Libraries
Requires:       libsemanage = %{version}-%{release}
Requires:       libselinux-devel = %{version}
Requires:       libsepol-devel = %{version}
Provides:       pkgconfig(libsemanage)

%description    devel
The libsemanage-devel package contains the libraries and header files
needed for developing SELinux policy management applications.

%package        python3
Summary:        SELinux python3 bindings for libsemanage
Group:          Development/Libraries
Requires:       libsemanage = %{version}-%{release}
Requires:       python3
Requires:       python3-libs

%description    python3
The libsemanage-python package contains the python3 bindings for developing
SELinux applications.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}
make LIBDIR="%{_libdir}" %{?_smp_mflags} PYTHON=%{_bindir}/python3 pywrap

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" install %{_smp_mflags}
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" \
     BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" PYTHON=%{_bindir}/python3 install install-pywrap \
     %{_smp_mflags}

# do not package ru man pages
rm -rf %{buildroot}%{_mandir}/ru

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libsemanage.so.*
%{_sysconfdir}/selinux/semanage.conf
%{_mandir}/man5/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libsemanage.so
%{_libdir}/pkgconfig
%dir %{_includedir}/semanage
%{_includedir}/semanage/*
%{_libdir}/libsemanage.a
%{_mandir}/man3/*

%files python3
%defattr(-,root,root,-)
%{_libexecdir}/selinux/semanage_migrate_store
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.4-4
- Release bump for SRP compliance
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.4-3
- Bump up version no. as part of swig upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.4-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.4-1
- Upgrade v3.4
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Upgrade v3.3
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.2-1
- Automatic Version Bump
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 3.0-3
- Mass removal python2
* Tue Apr 28 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-2
- Move migrate store python script to python subpackage.
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
