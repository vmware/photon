%global build_if %{photon_subrelease} <= 90

Summary:       Team driver
Name:          libteam
Version:       1.31
Release:       6.1%{?dist}
URL:           http://www.libteam.org
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       http://libteam.org/files/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: libnl-devel
BuildRequires: libdaemon-devel
BuildRequires: jansson-devel
BuildRequires: systemd-rpm-macros

Requires: libnl
Requires: libdaemon

%description
The libteam package contains the user-space components of the Team driver.
It provides a mechanism to team multiple NICs into one logical port at the L2 layer.

%package devel
Summary:    Development libraries and header files for libteam
Requires:   %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use libteam

%package -n teamd
Summary:        Team network device control daemon
Requires:       %{name} = %{version}-%{release}

%description -n teamd
The teamd package contains the team network device control daemon

%package -n teamd-devel
Summary:        Development files for teamd
Requires:       %{name} = %{version}-%{release}

%description -n teamd-devel
The package contains libraries and header files for
developing applications that use teamd and libteamdctl

%prep
%autosetup -p1

%build
%configure \
  --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

install -D -m 0644 teamd/redhat/systemd/teamd@.service \
    %{buildroot}%{_unitdir}/teamd@.service

install -D -m 0755 utils/bond2team \
    %{buildroot}%{_bindir}/bond2team

pushd teamd/redhat/initscripts_systemd/network-scripts
install -D -m 0755 \
    ifup-Team \
    ifdown-Team \
    ifup-TeamPort \
    ifdown-TeamPort \
    -t %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/
popd

install -D -m 0644 teamd/example_configs/* \
    -t %{buildroot}%{_datadir}/teamd/example_configs/

install -Dm 644 teamd/dbus/teamd.conf \
    %{buildroot}%{_sysconfdir}/dbus-1/system.d/teamd.conf

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%preun -n teamd
/sbin/ldconfig
%systemd_preun teamd@.service

%post -n teamd
/sbin/ldconfig

%postun -n teamd
/sbin/ldconfig
%systemd_postun teamd@.service

%files
%defattr(-,root,root)
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/team.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n teamd
%defattr(-,root,root)
%{_libdir}/libteamdctl.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sysconfdir}/*
%config(noreplace) %attr(644,root,root) %{_unitdir}/teamd@.service
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/teamd.conf

%files -n teamd-devel
%defattr(-,root,root)
%{_includedir}/teamdctl.h
%{_libdir}/libteamdctl.so
%{_libdir}/pkgconfig/libteamdctl.pc
%{_datadir}/teamd/*

%changelog
* Mon May 11 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 1.31-6.1
- Move to /90
* Sat Nov 01 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.31-6
- Add systemd-rpm-macros to build requires
* Fri Jul 18 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 1.31-5
- Bump up to build with latest jansson
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.31-4
- Release bump for SRP compliance
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.31-3
- Remove .la files
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 1.31-2
- Use autosetup and ldconfig scriptlets
* Tue Dec 08 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.31-1
- Initial build. First version
