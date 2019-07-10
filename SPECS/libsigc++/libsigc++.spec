Summary:	My summary.
Name:		libsigc++
Version:	2.6.2
Release:	2%{?dist}
License:	LGPLv2+
URL:		http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.6/libsigc++-2.6.2.tar.xz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.6/%{name}-%{version}.tar.xz
%define sha1 libsigc=c9bc6459756d0316b149cdf5db3a296e74cc5f4f
%description
My lib
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/sigc++-2.0/include/*.h
%{_includedir}/*
%{_datadir}/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.6.2-2
-	GA - Bump release of all rpms
*   Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 2.6.2-1
-   Updated to version 2.6.2
*	Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.4.0-1
	Initial version
