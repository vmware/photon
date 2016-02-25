Summary:	DBus for systemd
Name:		dbus
Version:	1.11.0
Release:	1%{?dist}
License:	GPLv2+ or AFL
URL:		http://www.freedesktop.org/wiki/Software/dbus
Group:		Applications/File
Source0:	http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
%define sha1 dbus=b53ba143b3bc1808eabd4628379f59ea6836694c
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	expat
BuildRequires:	systemd
BuildRequires:	xz-devel
BuildRequires:	libselinux-devel
Requires:	expat
Requires:	systemd
Requires:	xz
Requires:   shadow
Requires:	libselinux
%description
The dbus package contains dbus.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q
%build
./configure --prefix=%{_prefix}                 \
            --sysconfdir=%{_sysconfdir}         \
            --localstatedir=%{_var}             \
            --docdir=%{_datadir}/doc/dbus-1.11.0 \
            --with-console-auth-dir=/run/console \
            --without-systemdsystemunitdir \
            --disable-doxygen-docs         \
            --disable-xml-docs \
			--enable-libaudit \
			--with-system-socket=/run/dbus/system_bus_socket \
			--with-system-pid-file=/run/dbus/messagebus.pid \
			--with-dbus-user=dbus \
			--enable-user-session \
			--enable-selinux=yes
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

install -vdm755 %{buildroot}%{_lib}
#ln -sfv ../../lib/$(readlink %{buildroot}%{_libdir}/libdbus-1.so) %{buildroot}%{_libdir}/libdbus-1.so
#rm -f %{buildroot}%{_sharedstatedir}/dbus/machine-id
#ln -sv %{buildroot}%{_sysconfdir}/machine-id %{buildroot}%{_sharedstatedir}/dbus

%pre
if ! getent group dbus >/dev/null; then
	groupadd -g 18 messagebusruby
fi
if ! getent passwd messagebus >/dev/null; then
	useradd -c "D-Bus Message Daemon User" -d /var/run/dbus -u 18 -g messagebus -s /bin/false messagebus
fi

%post 
/sbin/ldconfig
chown -v      dbus  /usr/libexec/dbus-daemon-launch-helper
chmod -v      4750  /usr/libexec/dbus-daemon-launch-helper
%preun
%systemd_preun stop dbus.service dbus.socket

%postun
%systemd_postun

%files
%defattr(-,root,root)
/etc/*
%{_libdir}/dbus-1.0/include/dbus/*
#%{_libdir}/pkgconfig/*.pc
%{_oldincludedir}/*
%{_bindir}/*
%{_lib}/*
#/lib/*
%{_libexecdir}/*
%{_datadir}/*
%{_sharedstatedir}/*
%exclude %{_libdir}/debug/*
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig/*.pc

%files	devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
*   Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 1.11.0-1
-   Updated to version 1.11.0
*	Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.8-4
-	Created devel sub-package
*   Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 1.8.8-3
-   Remove debug files.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.8.8-2
-   Update according to UsrMove.
*	Sun Apr 06 2014 Sharath George <sharathg@vmware.com> 1.8.8
-	Initial build. First version
