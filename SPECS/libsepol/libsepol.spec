Summary:	SELinux binary policy manipulation library
Name:		libsepol
Version:	2.5
Release:	3%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
Source0:	https://raw.githubusercontent.com/wiki/SELinuxProject/selinux/files/releases/20160107/%{name}-%{version}-rc1.tar.gz
%define sha1 libsepol=0bf77d9849f715b29a8ac901461df0cc46da750b
URL:		http://www.selinuxproject.org
Vendor:		VMware, Inc.
Distribution:	Photon
Patch0:         0001-libsepol-cil-Destroy-classperms-list-when-resetting.patch
Patch1:         0002-cil-Destroy-classperm-list-when-resetting-map-perms.patch
Patch2:         0003-cil-cil_reset_classperms_set-should-not-reset.patch
Requires:	systemd

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

libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package	devel
Summary:	Header files and libraries used to build policy manipulation tools
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	pkgconfig(libsepol)

%description	devel
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%prep
%setup -qn %{name}-%{version}-rc1
sed  -i 's/int rc;/int rc = SEPOL_OK;/' ./cil/src/cil_binary.c
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make clean
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/%{_lib}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man3
mkdir -p %{buildroot}%{_mandir}/man8
make DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" SHLIBDIR="%{buildroot}/%{_lib}" install
rm -f %{buildroot}%{_bindir}/genpolbools
rm -f %{buildroot}%{_bindir}/genpolusers
rm -f %{buildroot}%{_bindir}/chkcon
rm -rf %{buildroot}%{_mandir}/man8

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
[ -x /sbin/telinit ] && [ -p /dev/initctl ]  && /sbin/telinit U
exit 0

%postun -p /sbin/ldconfig

%files devel
%defattr(-,root,root)
%{_libdir}/libsepol.so
%{_libdir}/libsepol.a
%{_libdir}/pkgconfig/libsepol.pc
%dir %{_includedir}/sepol
%dir %{_includedir}/sepol/policydb
%{_includedir}/sepol/policydb/*.h
%{_includedir}/sepol/*.h
%{_includedir}/sepol/cil/*.h
%{_mandir}/man3/*.3.gz

%files
%defattr(-,root,root)
%{_lib}/libsepol.so.1

%changelog
*   Mon Sep 13 2021 Vikash Bansal <bvikas@vmware.com> 2.5-3
-   Fix CVE-2021-36084, CVE-2021-36085, CVE-2021-36086
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-2
-   GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-1
-   Updated to version 2.5
*   Wed Feb 25 2015 Divya Thaluru <dthaluru@vmware.com> 2.4-1
-   Initial build. First version
