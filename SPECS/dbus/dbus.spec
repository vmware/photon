Summary:	DBus for systemd
Name:		dbus
Version:	1.8.8
Release:	6%{?dist}
License:	GPLv2+ or AFL
URL:		http://www.freedesktop.org/wiki/Software/dbus
Group:		Applications/File
Source0:	http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
%define sha1 dbus=e0d10e8b4494383c7e366ac80a942ba45a705a96
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
            --docdir=%{_datadir}/doc/dbus-1.8.8  \
            --with-console-auth-dir=/run/console

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm755 %{buildroot}%{_lib}
ln -sfv ../../lib/$(readlink %{buildroot}%{_libdir}/libdbus-1.so) %{buildroot}%{_libdir}/libdbus-1.so
rm -f %{buildroot}%{_sharedstatedir}/dbus/machine-id
#ln -sv %{buildroot}%{_sysconfdir}/machine-id %{buildroot}%{_sharedstatedir}/dbus
%files
%defattr(-,root,root)
/etc/*
%{_libdir}/dbus-1.0/include/dbus/*
#%{_libdir}/pkgconfig/*.pc
%{_oldincludedir}/*
%{_bindir}/*
%{_lib}/*
/lib/*
%{_libexecdir}/*
%{_docdir}/*
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
*   Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 1.8.8-6
-   Release bump for expat version update
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.8-5
-   GA - Bump release of all rpms
*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.8-4
-   Created devel sub-package
*   Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 1.8.8-3
-   Remove debug files.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.8.8-2
-   Update according to UsrMove.
*   Sun Apr 06 2014 Sharath George <sharathg@vmware.com> 1.8.8
-   Initial build. First version
