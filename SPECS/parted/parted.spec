Summary:	My summary.
Name:		parted
Version:	3.2
Release:	1%{?dist}
License:	GPLv3+
URL:		http://ftp.gnu.org/gnu/parted/parted-3.2.tar.xz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
%description
My lib
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--infodir=%{_infodir}/%{name}-%{version} \
	--without-readline \
	--disable-debug \
	--disable-nls \
	--disable-device-mapper
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_infodir}/%{name}-%{version}/*
%{_datadir}/*
%changelog
*	Thu Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.2-1
	Initial version
