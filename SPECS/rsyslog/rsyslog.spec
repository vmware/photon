Summary:        Rocket-fast system for log processing
Name:           rsyslog
Version:        8.37.0
Release:        1%{?dist}
License:        GPLv3+ and ASL 2.0
URL:            http://www.rsyslog.com/
Source0:        http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
%define sha1    rsyslog=7541e3cf6facbab19792ff8d9d7f4cd3fbb1c634
Source1:        rsyslog.service
Source2:        50-rsyslog-journald.conf
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  systemd
BuildRequires:  libestr-devel
BuildRequires:  json-c-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  liblogging-devel
BuildRequires:  librelp-devel
BuildRequires:  autogen
BuildRequires:  gnutls-devel
BuildRequires:  libfastjson-devel
BuildRequires:  curl
BuildRequires:  librelp-devel
Requires:       gnutls
Requires:       systemd
Requires:       libestr
Requires:       json-c
Requires:       libgcrypt
Requires:       liblogging
Requires:       librelp
Requires:       libfastjson
%description
RSYSLOG is the rocket-fast system for log processing.
It offers high-performance, great security features and a modular design. While it started as a regular syslogd, rsyslog has evolved into a kind of swiss army knife of logging, being able to accept inputs from a wide variety of sources, transform them, and output to the results to diverse destinations.
%prep
%setup -q
autoreconf -fvi
%build
sed -i 's/libsystemd-journal/libsystemd/' configure
./configure \
    --prefix=%{_prefix} \
    --enable-relp \
    --enable-gnutls\
    --enable-imfile \
    --enable-imjournal \
    --enable-impstats \
    --enable-imptcp

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vd %{buildroot}%{_libdir}/systemd/system/
install -vd %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
rm -f %{buildroot}/lib/systemd/system/rsyslog.service
install -p -m 644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
find %{buildroot} -name '*.la' -delete
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
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
%{_sysconfdir}/systemd/journald.conf.d/*
%changelog
*   Fri Mar 22 2019 Keerthana K <keerthanak@vmware.com> 8.37.0-1
-   Update to version 8.37.0
*   Thu Feb 14 2019 Keerthana K <keerthanak@vmware.com> 8.15.0-9
-   Fix for CVE-2018-16881
*   Thu Dec 21 2017 Xiaolin Li <xiaolinl@vmware.com> 8.15.0-8
-   Fix typos in change log.
*   Fri Dec 15 2017 Anish Swaminathan <anishs@vmware.com>  8.15.0-7
-   Remove kill SIGHUP from service file
*   Tue Aug 15 2017 Dheeraj Shetty <dheerajs@vmware.com>  8.15.0-6
-   Fixed CVE-2017-12588 
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

