Summary:	DBus for systemd
Name:		dbus
Version:	1.8.8
Release:	1
License:	GPLv2+ or AFL
URL:		http://www.freedesktop.org/wiki/Software/dbus
Group:		Applications/File
Source0:	http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	expat
BuildRequires:	systemd
BuildRequires:	xz-devel
Requires:	expat
Requires:	systemd
Requires:	xz
%description
The dbus package contains dbus.
%prep
%setup -q
%build
./configure --prefix=%{_prefix}                 \
            --sysconfdir=%{_sysconfdir}         \
            --localstatedir=%{_var}             \
            --docdir=%{_datadir}/doc/dbus-1.8.8  \
            --with-console-auth-dir=/run/console

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm755 %{buildroot}%{_lib}
mv -v %{buildroot}%{_libdir}/libdbus-1.so.* %{buildroot}%{_lib}
ln -sfv ../../lib/$(readlink %{buildroot}%{_libdir}/libdbus-1.so) %{buildroot}%{_libdir}/libdbus-1.so
rm -f %{buildroot}%{_sharedstatedir}/dbus/machine-id
#ln -sv %{buildroot}%{_sysconfdir}/machine-id %{buildroot}%{_sharedstatedir}/dbus
%files
%defattr(-,root,root)
/etc/*
%{_libdir}/dbus-1.0/include/dbus/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_oldincludedir}/*
%{_bindir}/*
%{_lib}/*
%{_libexecdir}/*
%{_docdir}/*
%{_sharedstatedir}/*
%changelog
*	Sun Apr 06 2014 Sharath George <sharathg@vmware.com> 1.8.8
-	Initial build. First version
