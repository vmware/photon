%define _unitdir        %{_libdir}/systemd/system
%define _udevrulesdir   %{_libdir}/udev/rules.d
%define _tmpfilesdir    %{_libdir}/tmpfiles.d

Summary:    Provide tools to manage multipath devices
Name:       device-mapper-multipath
Version:    0.9.1
Release:    1%{?dist}
License:    GPL+
Group:      System Environment/Base
Vendor:     VMware, Inc.
URL:        http://christophe.varoqui.free.fr
Distribution: Photon

Source0: https://github.com/opensvc/multipath-tools/archive/refs/tags/multipath-tools-%{version}.tar.gz
%define sha1 multipath-tools=ab5995b851f8b9403612c9aaab0b2d848e05dc09

# fix for CVE-2022-41973, CVE-2022-41974
Patch0: CVE-fixes.patch

BuildRequires:  userspace-rcu-devel
BuildRequires:  libaio-devel
BuildRequires:  device-mapper-devel
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
BuildRequires:  systemd-devel
BuildRequires:  json-c-devel

Requires:   userspace-rcu
Requires:   libaio
Requires:   device-mapper
Requires:   libselinux
Requires:   libsepol
Requires:   readline
Requires:   ncurses
Requires:   systemd
Requires:   kpartx = %{version}-%{release}

%description
Device-mapper-multipath provides tools to manage multipath devices by
instructing the device-mapper multipath kernel module what to do.

%package -n kpartx
Summary:    Partition device manager for device-mapper devices
Requires:   device-mapper
%description -n kpartx
kpartx manages partition creation and removal for device-mapper devices.

%package devel
Summary: Development libraries and headers for %{name}
Requires: %{name} = %{version}-%{release}
%description devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1 -n multipath-tools-%{version}

%build
%make_build

%install
%make_install %{?_smp_mflags} \
    SYSTEMDPATH=%{_libdir} \
    bindir=%{_sbindir} \
    syslibdir=%{_libdir} \
    usrlibdir=%{_libdir} \
    libdir=%{_libdir}/multipath \
    pkgconfdir=%{_libdir}/pkgconfig

install -vd %{buildroot}%{_sysconfdir}/multipath

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_sbindir}/mpathpersist
%{_sbindir}/multipath
%{_sbindir}/multipathd
%{_sbindir}/multipathc
%{_udevrulesdir}/*
%{_unitdir}/*
%{_libdir}/*.so.*
%{_libdir}/multipath/*.so
%{_mandir}/man5/*
%{_mandir}/man8/mpathpersist.8.gz
%{_mandir}/man8/multipath.8.gz
%{_mandir}/man8/multipathd.8.gz
%dir %{_sysconfdir}/multipath
%config(noreplace) %{_libdir}/modules-load.d/multipath.conf
%{_mandir}/man8/multipathc.8.gz
%{_tmpfilesdir}/multipath.conf

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files -n kpartx
%defattr(-,root,root,-)
%{_sbindir}/kpartx
%{_libdir}/udev/kpartx_id
%{_mandir}/man8/kpartx.8.gz

%changelog
* Tue Oct 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.9.1-1
- Upgrade to v0.9.1
* Mon Apr 23 2018 Xiaolin Li <xiaolinl@vmware.com> 0.7.3-2
- Build with librados-devel 12.2.4
* Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.3-1
- Update to 0.7.3
* Tue May 9  2017 Bo Gan <ganb@vmware.com> 0.7.1-1
- Update to 0.7.1
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  0.5.0-3
- Change systemd dependency
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5.0-2
- GA - Bump release of all rpms
* Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 0.5.0-1
- Initial build. First version
