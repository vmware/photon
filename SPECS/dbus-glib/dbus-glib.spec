Summary:	Glib interfaces to D-Bus API 
Name:		dbus-glib
Version:	0.106
Release:	5%{?dist}
License: 	AFL and GPLv2+
Group: 		System Environment/Libraries
Source0:	http://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
%define sha1 dbus-glib=660f1c1d511eb72384c10df37118bdc0f65dd927
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	glib-devel
BuildRequires:	dbus-devel
Requires:	glib
Requires:	dbus
Provides:	pkgconfig(dbus-glib-1)

%description
The D-Bus GLib package contains GLib interfaces to the D-Bus API.

%package devel
Summary:	Libraries and headers for the D-Bus GLib bindings
Requires:	glib-devel
Requires:	dbus-devel
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

%check
make %{?_smp_mflags} check

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
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.106-5
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.106-4
-	GA - Bump release of all rpms
*   Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 0.106-1
-   Updated to version 0.106
*   	Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 0.104-3
-   	Add requires to dbus-glib-devel
* 	Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.104-2
-	Updated build requires after creating devel package for dbus
*	Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 0.104-1
-	Initial build.
