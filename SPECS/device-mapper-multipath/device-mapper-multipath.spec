Summary:	Provide tools to manage multipath devices
Name:		device-mapper-multipath
Version:	0.5.0
Release:	2%{?dist}
License:	GPL+
Group:		System Environment/Base
URL:		http://christophe.varoqui.free.fr/
Source0:	http://christophe.varoqui.free.fr/multipath-tools/multipath-tools-0.5.0.tar.bz2
%define sha1 multipath-tools=dcd889c09bcb1f2b89900838da6ac1ed970104cb
BuildRequires:	libaio-devel
BuildRequires:	device-mapper-devel
BuildRequires:	libselinux-devel
BuildRequires:	libsepol-devel
BuildRequires: 	readline-devel
BuildRequires:	ncurses-devel
BuildRequires: 	systemd
Requires:	libaio
Requires:	device-mapper
Requires:	libselinux
Requires:	libsepol
Requires: 	readline
Requires:	ncurses
Requires: 	kpartx = %{version}-%{release}

%description
Device-mapper-multipath provides tools to manage multipath devices by
instructing the device-mapper multipath kernel module what to do. 

%package -n kpartx
Summary:	Partition device manager for device-mapper devices

%description -n kpartx
kpartx manages partition creation and removal for device-mapper devices.

%prep
%setup -qn multipath-tools-0.5.0

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} bindir=%{_sbindir} syslibdir=%{_libdir} libdir=%{_libdir}/multipath
install -vd %{buildroot}/etc/multipath
ln -sfv libmpathpersist.so.0 %{buildroot}/%{_libdir}/libmpathpersist.so
rm -rf %{buildroot}/%{_initrddir}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
/etc/udev/rules.d/*
%{_sbindir}/*
%{_libdir}/systemd/system/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/multipath/*.so
%{_includedir}/*.h
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir /etc/multipath

%files -n kpartx
%defattr(-,root,root,-)
%{_sbindir}/kpartx
/lib/udev/*
%{_mandir}/man8/kpartx.8.gz

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5.0-2
-	GA - Bump release of all rpms
*	Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 0.5.0-1
-	Initial build. First version

