Summary:	Libraries for Transport Independent RPC
Name:		libtirpc
Version:	1.0.1
Release:	5%{?dist}
Source0:	http://downloads.sourceforge.net/project/libtirpc/libtirpc/0.3.2/%{name}-%{version}.tar.bz2
%define sha1 libtirpc=8da1636f98b5909c0d587e7534bc1e91f5c1a970
Patch0:         libtirpc-1.0.1-bindrsvport-blacklist.patch
Patch1:         libtirpc-CVE-2017-8779.patch
Patch2:		libtirpc-CVE-2018-14621.patch		
License:	BSD
Group:		System Environment/Libraries
URL:		http://nfsv4.bullopensource.org/
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	krb5
BuildRequires:	automake
BuildRequires:  e2fsprogs-devel
Requires:	krb5

%description
This package contains SunLib's implementation of transport-independent
RPC (TI-RPC) documentation.  This library forms a piece of the base of Open Network
Computing (ONC), and is derived directly from the Solaris 2.3 source.

TI-RPC is an enhanced version of TS-RPC that requires the UNIX System V
Transport Layer Interface (TLI) or an equivalent X/Open Transport Interface
(XTI).  TI-RPC is on-the-wire compatible with the TS-RPC, which is supported
by almost 70 vendors on all major operating systems.  TS-RPC source code
(RPCSRC 4.0) remains available from several internet sites.

%package	devel
Summary:	Development files for the libtirpc library
Group:		Development/Libraries
Requires:	libtirpc

%description 	devel
This package includes header files and libraries necessary for developing programs which use the tirpc library.

%prep
%setup -q
%patch0
%patch1 -p1
%patch2 -p1

%build
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_sysconfdir}/netconfig
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_libdir}/*.la

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/tirpc/*
   

%changelog
*	Fri Nov 30 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.0.1-5
-	Apply patch for CVE-2018-14621
*	Thu May 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.1-4
-	Fix CVE-2017-8779
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-3
-	GA - Bump release of all rpms
* 	Mon Feb 08 2016 Anish Swaminathan <anishs@vmware.com>  1.0.1-2
- 	Added patch for bindresvport blacklist
* 	Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.1-1
- 	Updated to version 1.0.1
* 	Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 0.3.2-1
- 	Initial version
