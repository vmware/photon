Summary:        DBus message bus
Name:           dbus
Version:        1.15.4
Release:        6%{?dist}
URL:            http://www.freedesktop.org/wiki/Software/dbus
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

Patch0: CVE-2023-34969.patch

BuildRequires:  expat-devel
BuildRequires:  systemd-devel
BuildRequires:  xz-devel

Requires:       expat
Requires:       systemd
Requires:       xz

%description
The dbus package contains dbus.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       expat-devel

%description    devel
It contains the libraries and header files to create applications

%package        user-session
Summary:        simple interprocess messaging system (systemd --user integration)

Requires:       %{name} = %{version}-%{release}

%description    user-session
simple interprocess messaging system (systemd --user integration)

%prep
%autosetup -p1

%build
%configure \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --enable-libaudit=no \
    --enable-selinux=no \
    --with-console-auth-dir=/run/console \
    --enable-user-session

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm755 %{buildroot}%{_lib}

rm -f %{buildroot}%{_libdir}/*.la

mkdir -p %{buildroot}%{_userunitdir}

rm -f %{buildroot}%{_userunitdir}/sockets.target.wants/dbus.socket

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_sysconfdir}/%{name}-1
%{_bindir}/*
%{_libdir}/libdbus-1.so.*
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/*
%exclude %{_sysusersdir}
%{_libexecdir}/*
%{_datadir}/%{name}-1

%files devel
%defattr(-,root,root)
%{_docdir}/*
%{_includedir}/*
%{_datadir}/xml/%{name}-1
%{_libdir}/cmake/DBus1
%dir %{_libdir}/%{name}-1.0
%{_libdir}/%{name}-1.0/include/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so

%files user-session
%defattr(-,root,root)
%{_userunitdir}/%{name}.service
%{_userunitdir}/%{name}.socket

%changelog
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.15.4-6
- Release bump for SRP compliance
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 1.15.4-5
- Remove standalone license exceptions
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.15.4-4
- Release bump for SRP compliance
* Mon Feb 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.15.4-3
- Fix CVE-2023-34969
* Tue Mar 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.15.4-2
- Enable user-session config flag
* Thu Feb 16 2023 Susant Sahani <ssahani@vmware.com> 1.15.4-1
- Version bump
* Thu Jan 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.15.2-3
- Add dbus-user-session sub package, needed by rootless containers
* Fri Dec 23 2022 Oliver Kurth <okurth@vmware.com> 1.15.2-2
- bump version as part of xz upgrade
* Tue Nov 01 2022 Susant Sahani <ssahani@vmware.com> 1.15.2-1
- Version bump
* Sat Oct 01 2022 Susant Sahani <ssahani@vmware.com> 1.15.0-1
- Version bump
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.0-2
- Remove .la files
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.14.0-1
- Automatic Version Bump
* Thu Jan 13 2022 Susant Sahani <ssahani@vmware.com> 1.13.20-1
- Update to 1.13.20
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.13.18-1
- Automatic Version Bump
* Wed May 06 2020 Susant Sahani <ssahani@vmware.com> 1.13.14-1
- Update to 1.13.14
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.13.6-2
- Cross compilation support
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 1.13.6-1
- Update to 1.13.6
* Fri Apr 21 2017 Bo Gan <ganb@vmware.com> 1.11.12-1
- Update to 1.11.12
* Tue Dec 20 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.8-8
- Move all header files to devel subpackage.
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.8.8-7
- Change systemd dependency
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.8.8-6
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.8-5
- GA - Bump release of all rpms
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.8-4
- Created devel sub-package
* Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 1.8.8-3
- Remove debug files.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.8.8-2
- Update according to UsrMove.
* Sun Apr 06 2014 Sharath George <sharathg@vmware.com> 1.8.8
- Initial build. First version
