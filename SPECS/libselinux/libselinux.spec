
Summary:	SELinux library and simple utilities
Name:		libselinux
Version:	2.5
Release:	2%{?dist}
License:	Public Domain
Group:		System Environment/Libraries
Source0:	https://raw.githubusercontent.com/wiki/SELinuxProject/selinux/files/releases/20160107/%{name}-%{version}-rc1.tar.gz
%define sha1 libselinux=ca50f64f5996c6c4c80a9f80a9adf038231ba211
Url:		https://github.com/SELinuxProject/selinux/wiki
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	libsepol-devel
BuildRequires:	pcre-devel, swig
BuildRequires:	python2-devel, python2-libs
Requires:	pcre

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

libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions.  Required for any applications that use the SELinux API.

%package	utils
Summary:	SELinux libselinux utilies
Group:		Development/Libraries
Requires:	libselinux = %{version}-%{release} 

%description	utils
The libselinux-utils package contains the utilities

%package	python
Summary:	SELinux python bindings for libselinux
Group:		Development/Libraries
Requires:	libselinux = %{version}-%{release}
Requires:	python2 
Requires:	python2-libs

%description	python
The libselinux-python package contains the python bindings for developing 
SELinux applications. 

%package	devel
Summary:	Header files and libraries used to build SELinux
Group:		Development/Libraries
Requires:	libselinux = %{version}-%{release}
Requires:	pcre-devel
Requires:	libsepol-devel 
Provides:	pkgconfig(libselinux)

%description	devel
The libselinux-devel package contains the libraries and header files
needed for developing SELinux applications. 

%prep
%setup -qn %{name}-%{version}-rc1

%build

make clean
make LIBDIR="%{_libdir}" %{?_smp_mflags} swigify
make LIBDIR="%{_libdir}" %{?_smp_mflags} all
make LIBDIR="%{_libdir}" %{?_smp_mflags} pywrap

%install
make DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" SHLIBDIR="%{buildroot}/%{_lib}" BINDIR="%{buildroot}%{_bindir}" SBINDIR="%{buildroot}%{_sbindir}" install install-pywrap

mkdir -p %{buildroot}/%{_prefix}/lib/tmpfiles.d
mkdir -p %{buildroot}/var/run/setrans
echo "d /var/run/setrans 0755 root root" > %{buildroot}/%{_prefix}/lib/tmpfiles.d/libselinux.conf

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_lib}/libselinux.so.*
%ghost /var/run/setrans
%{_prefix}/lib/tmpfiles.d/libselinux.conf

%files utils
%defattr(-,root,root,-)
%{_sbindir}/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libselinux.so
%{_libdir}/pkgconfig/libselinux.pc
%dir %{_includedir}/selinux
%{_includedir}/selinux/*
%{_libdir}/libselinux.a
%{_mandir}/man3/*

%files python
%defattr(-,root,root,-)
%dir %{python_sitearch}/selinux
%{python_sitearch}/selinux/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-2
-	GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-1
-   Updated to version 2.5
*	Wed Feb 25 2015 Divya Thaluru <dthaluru@vmware.com> 2.4-1
-	Initial build.	First version
