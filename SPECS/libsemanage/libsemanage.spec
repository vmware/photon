%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        SELinux policy management libraries
Name:           libsemanage
Version:        3.0
Release:        2%{?dist}
License:        Public Domain
Group:          System Environment/Libraries
Source0:        https://github.com/SELinuxProject/selinux/releases/download/20191204/%{name}-%{version}.tar.gz
%define sha1    libsemanage=d26a69def1b79f009daf570d0b5de87a839a18fe
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libselinux-devel = %{version}
BuildRequires:  libsepol-devel = %{version}
BuildRequires:  audit-devel
BuildRequires:  python2-devel
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

%package        python
Summary:        SELinux python2 bindings for libsemanage
Group:          Development/Libraries
Requires:       libsemanage = %{version}-%{release}
Requires:       python2
Requires:       python2-libs

%description    python
The libsemanage-python package contains the python2 bindings for developing
SELinux applications.

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
make LIBDIR="%{_libdir}" %{?_smp_mflags} PYTHON=/usr/bin/python2 pywrap
make LIBDIR="%{_libdir}" %{?_smp_mflags} PYTHON=/usr/bin/python3 pywrap

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" PYTHON=/usr/bin/python2 install install-pywrap
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" PYTHON=/usr/bin/python3 install install-pywrap

# do not package ru man pages
rm -rf %{buildroot}%{_mandir}/ru

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libsemanage.so.1
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

%files python
%defattr(-,root,root,-)
%ghost %{_libexecdir}/selinux/semanage_migrate_store
%{python2_sitelib}/*

%files python3
%defattr(-,root,root,-)
%{_libexecdir}/selinux/semanage_migrate_store
%{python3_sitelib}/*

%changelog
* Tue Apr 28 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-2
- Move migrate store python script to python subpackage.
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
