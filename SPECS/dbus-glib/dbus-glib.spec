Summary:	Glib interfaces to D-Bus API 
Name:		dbus-glib
Version:	0.104
Release:	1%{?dist}
License: 	AFL and GPLv2+
Group: 		System Environment/Libraries
Source0:	http://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
%define sha1 dbus-glib=776a0e843f5c04cb58225962d623e82f283aed68
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	glib-devel
BuildRequires:	dbus
Requires:	glib
Requires:	dbus
Provides:	pkgconfig(dbus-glib-1)

%description
The D-Bus GLib package contains GLib interfaces to the D-Bus API.

%package devel
Summary:	Libraries and headers for the D-Bus GLib bindings
Requires:	glib-devel
Requires:	%{name} = %{version}

%description devel
Headers and static libraries for the D-Bus GLib bindings

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --disable-static \
	--disable-gtk-doc
 
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_sysconfdir}/bash_completion.d/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.la
%{_libexecdir}/*
%{_mandir}/man1/*
%{_datadir}/gtk-doc/*

%files devel
%defattr(-,root,root)
%{_includedir}/dbus-1.0/dbus/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc



%changelog
*	Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 0.104-1
-	Initial build.
