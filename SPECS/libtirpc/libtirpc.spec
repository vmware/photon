Summary:	Libraries for Transport Independent RPC
Name:		libtirpc
Version:	0.3.2
Release:	1%{?dist}
Source0:	http://downloads.sourceforge.net/project/libtirpc/libtirpc/0.3.2/%{name}-%{version}.tar.bz2
%define sha1 libtirpc=af9b74d0c4d1499a7b1a43e396e5b7d62180ea65
Patch0:		http://www.linuxfromscratch.org/patches/blfs/svn/libtirpc-0.3.2-api_fixes-1.patch
License:	BSD
Group:		System Environment/Libraries
URL:		http://nfsv4.bullopensource.org/
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	krb5
BuildRequires:	automake
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
%patch0 -p1

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
* Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 0.3.2-1
- Initial version
