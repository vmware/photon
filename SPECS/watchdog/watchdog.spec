Summary:        Software and/or Hardware watchdog daemon
Name:           watchdog
Version:        5.16
Release:        1%{?dist}
License:        GPLv2+
URL:            http://sourceforge.net/projects/watchdog/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha512  watchdog=1c9c921570ec7ddc3e4ff88b2029f1c3865277e547fb8970575df4b61fdf1f06f443f49ad09f11c29d913ca7d6ab05c5b19ec049ac218a8bcebd20b1bf5f0bbd
Source1:        watchdog.service
BuildRequires:  systemd-devel

Requires:       systemd

%description
The watchdog program can be used as a powerful software watchdog daemon
or may be alternately used with a hardware watchdog device such as the
IPMI hardware watchdog driver interface to a resident Baseboard
Management Controller (BMC)

%prep
%autosetup -p1

%build
%configure

make %{?_smp_mflags}

%install
install -d -m 0755 %{buildroot}%{_sysconfdir}
install -d -m 0755 %{buildroot}%{_sysconfdir}/watchdog.d
make install DESTDIR=%{buildroot} %{?_smp_mflags}
install -Dd -m 0755 %{buildroot}%{_libexecdir}/watchdog/scripts
install -Dp -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/watchdog.service
rm %{name}.sysconfig

%check
%if 0%{?with_check}
make %{?_smp_mflags} check
%endif

%post
/sbin/ldconfig
%systemd_post watchdog.service

%preun
%systemd_preun watchdog.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart watchdog.service

%files
%defattr(-,root,root)
%{_sysconfdir}/watchdog.d
%{_sbindir}/watchdog
%{_sbindir}/wd_identify
%{_sbindir}/wd_keepalive
%{_mandir}/man5/watchdog.conf.5*
%{_mandir}/man8/watchdog.8*
%{_mandir}/man8/wd_identify.8*
%{_mandir}/man8/wd_keepalive.8*
%{_unitdir}/watchdog.service
%config(noreplace) %{_sysconfdir}/watchdog.conf

%changelog
*   Thu May 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.16-1
-   Initial version
