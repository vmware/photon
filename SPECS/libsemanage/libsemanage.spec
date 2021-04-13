%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        SELinux policy management libraries
Name:           libsemanage
Version:        3.2
Release:        1%{?dist}
License:        Public Domain
Group:          System Environment/Libraries
Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha1    libsemanage=bc67f9118dcca5032919d25184899f9daf66b70b
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libselinux-devel = %{version}
BuildRequires:  libsepol-devel = %{version}
BuildRequires:  audit-devel
BuildRequires:  python3-devel swig
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
%setup -q

%build
make %{?_smp_mflags}
make LIBDIR="%{_libdir}" %{?_smp_mflags} PYTHON=/usr/bin/python3 pywrap

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" PYTHON=/usr/bin/python3 install install-pywrap

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
