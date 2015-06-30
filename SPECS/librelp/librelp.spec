Summary:	RELP Library
Name:		librelp
Version:	1.2.7
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.librelp.com
Source0:	http://download.rsyslog.com/librelp/%{name}-%{version}.tar.gz
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	gnutls-devel
Requires:	gnutls
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
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
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
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.2.7-1
-	Initial build. First version

