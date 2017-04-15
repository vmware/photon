Summary:        DBus for systemd
Name:           dbus
Version:        1.8.8
Release:        8%{?dist}
License:        GPLv2+ or AFL
URL:            http://www.freedesktop.org/wiki/Software/dbus
Group:          Applications/File
Source0:        http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
%define sha1    dbus=e0d10e8b4494383c7e366ac80a942ba45a705a96
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  expat-devel
BuildRequires:  systemd-devel
BuildRequires:  xz-devel
Requires:       expat
Requires:       systemd
Requires:       xz
%description
The dbus package contains dbus.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}
%description    devel
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

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
/etc/*
%{_bindir}/*
%{_lib}/libdbus-1.so.*
/lib/*
%{_libexecdir}/*
%{_docdir}/*
%{_sharedstatedir}/*

%files  devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/dbus-1.0/include/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
*   Tue Dec 20 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.8-8
-   Move all header files to devel subpackage.
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.8.8-7
-   Change systemd dependency
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.8.8-6
-   Modified %check
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
