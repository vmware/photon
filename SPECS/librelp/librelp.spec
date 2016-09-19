Summary:	RELP Library
Name:		librelp
Version:	1.2.9
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.librelp.com
Source0:	http://download.rsyslog.com/librelp/%{name}-%{version}.tar.gz
%define sha1 librelp=d8b61789a2775bbff08c1ac05b658a52afa4d729
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	gnutls-devel
BuildRequires:	autogen
Requires:	gnutls
Requires:	gmp
%description
Librelp is an easy to use library for the RELP protocol. RELP (stands
for Reliable Event Logging Protocol) is a general-purpose, extensible
logging protocol.

%package devel
Summary:	Development libraries and header files for librelp
Requires:	librelp

%description devel
The package contains libraries and header files for
developing applications that use librelp.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.la
%{_libdir}/*.a
%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.9-2
-	GA - Bump release of all rpms
* 	Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.2.9-1
- 	Upgrade to 1.2.9
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.2.7-1
-	Initial build. First version

