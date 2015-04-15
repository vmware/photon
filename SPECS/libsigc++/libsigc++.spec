Summary:	My summary.
Name:		libsigc++
Version:	2.4.0
Release:	1
License:	LGPLv2+
URL:		http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.4/libsigc++-2.4.0.tar.xz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.4/%{name}-%{version}.tar.xz
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
*	Thu Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.4.0-1
	Initial version
