Summary:        Rocket-fast system for log processing
Name:           rsyslog
Version:        8.2202.0
Release:        1%{?dist}
License:        GPLv3+ and ASL 2.0
URL:            http://www.rsyslog.com/
Source0:        http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
%define sha512    rsyslog=b1c68099236cc0722f52822f8b46d7f2a4a023e0809907f2b0173d5593df3c6f914516310bd832ac028252fb2c467dc90756d4472950e4244f3919b328a8bd6e
Source1:        rsyslog.service
Source2:        50-rsyslog-journald.conf
Source3:        rsyslog.conf
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  systemd-devel
BuildRequires:  libestr-devel
BuildRequires:  libfastjson-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  liblogging-devel
BuildRequires:  librelp-devel
BuildRequires:  autogen
BuildRequires:  gnutls-devel
BuildRequires:  curl-devel
Requires:       gnutls
Requires:       systemd
Requires:       libestr
Requires:       libfastjson
Requires:       libgcrypt
Requires:       liblogging
Requires:       librelp

%description
RSYSLOG is the rocket-fast system for log processing.
It offers high-performance, great security features and a modular design.
While it started as a regular syslogd, rsyslog has evolved into a kind of swiss army knife of logging,
being able to accept inputs from a wide variety of sources, transform them,
and output to the results to diverse destinations.

%prep
%autosetup -p1
autoreconf -fvi

%build
sed -i 's/libsystemd-journal/libsystemd/' configure
%configure \
    --enable-relp \
    --enable-gnutls\
    --enable-imfile \
    --enable-imjournal \
    --enable-impstats \
    --enable-imptcp \
    --enable-imtcp \
    --enable-openssl

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -vd %{buildroot}%{_libdir}/systemd/system/
install -vd %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -vd %{buildroot}%{_sysconfdir}/rsyslog.d
rm -f %{buildroot}/lib/systemd/system/rsyslog.service
install -p -m 644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rsyslog.conf
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post rsyslog.service

%preun
%systemd_preun rsyslog.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart rsyslog.service

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/rsyslog/*.so
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_libdir}/systemd/system/rsyslog.service
%dir %{_sysconfdir}/rsyslog.d
%{_sysconfdir}/systemd/journald.conf.d/*
%config(noreplace) %{_sysconfdir}/rsyslog.conf

%changelog
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 8.2202.0-1
-   Automatic Version Bump
*   Mon Nov 15 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2110.0-2
-   Bump up release for openssl
*   Fri Nov 12 2021 Tapas Kundu <tkundu@vmware.com> 8.2110.0-1
-   Update to 8.2110.0
*   Thu Jun 24 2021 Tapas Kundu <tkundu@vmware.com> 8.2106.0-1
-   Update to 8.2106.0
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 8.2104.0-1
-   Automatic Version Bump
*   Mon Oct 05 2020 Keerthana K <keerthanak@vmware.com> 8.2008.0-2
-   Adding rsyslog.d directory
*   Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 8.2008.0-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 8.2006.0-1
-   Automatic Version Bump
*   Mon Jan 27 2020 Tapas Kundu <tkundu@vmware.com> 8.2001.0-1
-   Update to 8.2001.0
*   Mon Dec 23 2019 Tapas Kundu <tkundu@vmware.com> 8.1910.0-4
-   Fix typo in conf file.
*   Thu Nov 21 2019 Tapas Kundu <tkundu@vmware.com> 8.1910.0-3
-   Added config noreplace for rsyslog.conf
*   Mon Nov 04 2019 Tapas Kundu <tkundu@vmware.com> 8.1910.0-2
-   Built with imtcp and openssl
-   Added patch to fix openssl version in rsyslog source
*   Wed Oct 16 2019 Tapas Kundu <tkundu@vmware.com> 8.1910.0-1
-   Update to 8.1910.0 release
-   Fix CVE-2019-17041 and CVE-2019-17042
*   Fri Oct 04 2019 Keerthana K <keerthanak@vmware.com> 8.1907.0-1
-   Update to 8.1907.0
-   Fix CVE-2019-17040
*   Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> 8.37.0-1
-   Updated to version 8.37.0
*   Thu Apr 12 2018 Xiaolin Li <xiaolinl@vmware.com> 8.26.0-5
-   Add $IncludeConfig /etc/rsyslog.d/ to rsyslog.conf
*   Fri Dec 15 2017 Anish Swaminathan <anishs@vmware.com>  8.26.0-4
-   Remove kill SIGHUP from service file
*   Mon Nov 13 2017 Xiaolin Li <xiaolinl@vmware.com> 8.26.0-3
-   Add a default rsyslog.conf.
*   Tue Aug 15 2017 Dheeraj Shetty <dheerajs@vmware.com>  8.26.0-2
-   Fix CVE-2017-12588
*   Mon  Apr 24 2017 Siju Maliakkal <smaliakkal@vmware.com>  8.26.0-1
-   Update to latest
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  8.15.0-7
-   Change systemd dependency
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 8.15.0-6
-   Modified %check
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  8.15.0-5
-   Fixed logic to restart the active services after upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.15.0-4
-   GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  8.15.0-3
-   Use systemd macros for post, preun and postun to respect upgrades
*   Wed Feb 17 2016 Anish Swaminathan <anishs@vmware.com>  8.15.0-2
-   Add journald conf and new service file.
*   Mon Jan 11  2016 Xiaolin Li <xiaolinl@vmware.com> 8.15.0-1
-   Update rsyslog to 8.15.0
*   Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 8.10.0-1
-   Initial build. First version
