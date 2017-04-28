
Summary:	SELinux library and simple utilities
Name:		libselinux
Version:	2.6
Release:	1%{?dist}
License:	Public Domain
Group:		System Environment/Libraries
Source0:	https://raw.githubusercontent.com/wiki/SELinuxProject/selinux/files/releases/20160107/%{name}-%{version}.tar.gz
%define sha1 libselinux=38213c5f3298c980a399ea73e47498e7a393e4f7
Url:		https://github.com/SELinuxProject/selinux/wiki
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	libsepol-devel
BuildRequires:	pcre-devel, swig
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
%setup -qn %{name}-%{version}

%build

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}/%{_prefix}/lib/tmpfiles.d
mkdir -p %{buildroot}/var/run/setrans
echo "d /var/run/setrans 0755 root root" > %{buildroot}/%{_prefix}/lib/tmpfiles.d/libselinux.conf
mv %{buildroot}/lib/libselinux.so.* %{buildroot}%{_libdir}/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%ghost /var/run/setrans
%{_libdir}/*
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

%changelog
*	Wed Apr 19 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.6-1
-	Upgraded to version 2.6
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-2
-	GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-1
-   Updated to version 2.5
*	Wed Feb 25 2015 Divya Thaluru <dthaluru@vmware.com> 2.4-1
-	Initial build.	First version
