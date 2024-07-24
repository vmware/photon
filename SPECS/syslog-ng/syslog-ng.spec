Summary:        Next generation system logger facilty
Name:           syslog-ng
Version:        4.3.1
Release:        5%{?dist}
License:        GPL + LGPL
URL:            https://syslog-ng.org/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/balabit/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=571f6080765983326ee912f2a7e87cdc8527296ef555a0b16589c04ed332c0db58e24c70251dc39b1c79151ca7d463e6409835df99aa45c19734d7003a69ce61

Source1:        60-%{name}-journald.conf
Source2:        %{name}.service

Requires:       glib
Requires:       openssl
Requires:       glibc
Requires:       json-glib
Requires:       json-c
Requires:       systemd
Requires:       ivykis
Requires:       paho-c
Requires:       pcre2-libs >= 10.40-5

BuildRequires:  pcre2-devel
BuildRequires:  which
BuildRequires:  glib-devel
BuildRequires:  json-glib-devel
BuildRequires:  json-c-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  curl-devel
BuildRequires:  ivykis-devel
BuildRequires:  paho-c-devel
BuildRequires:  bison
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-cachetools
BuildRequires:  python3-certifi
BuildRequires:  python3-charset-normalizer
BuildRequires:  python3-google-auth
BuildRequires:  python3-idna
BuildRequires:  python3-kubernetes
BuildRequires:  python3-oauthlib
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pyasn1-modules
BuildRequires:  python3-dateutil
BuildRequires:  python3-PyYAML
BuildRequires:  python3-requests
BuildRequires:  python3-requests-oauthlib
BuildRequires:  python3-rsa
BuildRequires:  python3-six
BuildRequires:  python3-urllib3
BuildRequires:  python3-websocket-client
BuildRequires:  python3-boto3
BuildRequires:  python3-botocore

Obsoletes:      eventlog

%description
The syslog-ng application is a flexible and highly scalable
system logging tool. It is often used to manage log messages and implement
centralized logging, where the aim is to collect the log messages of several
devices to a single, central log server.

%package -n python3-%{name}
Summary:   python3-%{name}
Requires:  python3
Requires:  python3-cachetools
Requires:  python3-certifi
Requires:  python3-charset-normalizer
Requires:  python3-google-auth
Requires:  python3-idna
Requires:  python3-kubernetes
Requires:  python3-oauthlib
Requires:  python3-pyasn1
Requires:  python3-pyasn1-modules
Requires:  python3-dateutil
Requires:  python3-PyYAML
Requires:  python3-requests
Requires:  python3-requests-oauthlib
Requires:  python3-rsa
Requires:  python3-six
Requires:  python3-urllib3
Requires:  python3-websocket-client

%description -n python3-%{name}
Python 3 version.

%package        devel
Summary:        Header and development files for syslog-ng
Requires:       %{name} = %{version}-%{release}
Requires:       ivykis-devel
Requires:       glib-devel
Obsoletes:      eventlog-devel

%description    devel
syslog-ng-devel package contains header files, pkfconfig files, and libraries
needed to build applications using syslog-ng APIs.

%prep
%autosetup -p1

%build
autoreconf -vif

sh ./configure --host=%{_host} --build=%{_build} \
   CFLAGS="%{optflags}" \
   CXXFLAGS="%{optflags}" \
   --program-prefix= \
   --disable-dependency-tracking \
   --prefix=%{_prefix} \
   --exec-prefix=%{_prefix} \
   --bindir=%{_bindir} \
   --sbindir=%{_sbindir} \
   --sysconfdir=%{_sysconfdir}/%{name} \
   --datadir=%{_datadir} \
   --includedir=%{_includedir} \
   --libdir=%{_libdir} \
   --libexecdir=%{_libexecdir} \
   --localstatedir=%{_sharedstatedir}/%{name} \
   --sharedstatedir=%{_sharedstatedir} \
   --mandir=%{_mandir} \
   --infodir=%{_infodir} \
   --disable-silent-rules \
   --enable-systemd \
   --with-systemdsystemunitdir=%{_unitdir} \
   --enable-json=yes \
   --with-jsonc=system \
   --disable-java \
   --disable-redis \
   --enable-python \
   --with-ivykis=system \
   --enable-mqtt \
   --disable-static \
   --enable-dynamic-linking \
   --disable-cpp \
   --with-python=3 \
   --with-python-packages=system \
   PYTHON=%{python3} \
   PKG_CONFIG_PATH=%{_libdir}/pkgconfig/

%make_build

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

rm -rf %{buildroot}%{_unitdir}/%{name}@.service \
       %{buildroot}%{_infodir} \
       %{buildroot}%{_libdir}/libsyslog-ng-native-connector.a

install -vd %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -p -m 644 %{SOURCE2} %{buildroot}%{_libdir}/systemd/system/
sed -i 's/eventlog//g'  %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

install -vdm755 %{buildroot}%{_presetdir}
echo "disable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

%{_fixperms} %{buildroot}/*

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_sysconfdir}/systemd/journald.conf.d/*
%{_unitdir}/%{name}.service
%{_presetdir}/50-%{name}.preset
%{_bindir}/*
%{_sbindir}/%{name}
%{_sbindir}/%{name}-ctl
%{_sbindir}/%{name}-debun
%{_libdir}/libsyslog-ng-*.so.*
%{_libdir}/libevtlog-*.so.*
%{_libdir}/libloggen_helper*
%{_libdir}/libloggen_plugin*
%{_libdir}/libsecret-storage*
%{_libdir}/%{name}/loggen/*
%{_libdir}/%{name}/lib*.so
%exclude %{_libdir}/%{name}/libmod-python.so
%{_datadir}/%{name}/*
%{_mandir}/*
%dir %{_sharedstatedir}/%{name}

%files -n python3-%{name}
%defattr(-,root,root,-)
%{_sysconfdir}/%{name}/python/README.md
%{_libdir}/%{name}/libmod-python.so
%{_libdir}/%{name}/python

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/libsyslog-ng.so
%{_libdir}/libevtlog.so
%{_libdir}/pkgconfig/*

%changelog
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.3.1-5
- Do offline build
* Thu Apr 04 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.3.1-4
- Obsolete eventlog
* Mon Feb 26 2024 Nitesh Kumar <nitesh-nk.kumar@brodcom.com> 4.3.1-3
- Fixing localstatedir path
* Fri Nov 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.3.1-2
- Rebuild with jit enabled pcre2
* Mon Oct 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.3.1-1
- Upgrade to v4.3.1
* Mon Sep 11 2023 Ankit Jain <ankitja@vmware.com> 3.37.1-3
- Fix for CVE-2022-38725
* Thu Jul 28 2022 Oliver Kurth <okurth@vmware.com> 3.37.1-2
- add OCSP stapling support
* Thu Jun 09 2022 Oliver Kurth <okurth@vmware.com> 3.37.1-1
- Bump version
* Mon Mar 21 2022 Oliver Kurth <okurth@vmware.com> 3.36.1-1
- Bump version, add MQTT support
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.29.1-4
- Bump up release for openssl
* Fri Oct 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.29.1-3
- Fix GCC path issue
* Wed Sep 09 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.29.1-2
- Openssl 1.1.1 Compatibility
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 3.29.1-1
- Automatic Version Bump
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 3.28.1-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 3.17.2-2
- Mass removal python2
* Wed Oct 10 2018 Ankit Jain <ankitja@vmware.com> 3.17.2-1
- Update to version 3.17.2
* Mon Sep 11 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.11.1-3
- Obsolete eventlog.
* Mon Sep 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.11.1-2
- Use old service file.
* Fri Aug 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.11.1-1
- Update to version 3.11.1
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  3.9.1-3
- Disabled syslog-ng service by default
* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 3.9.1-2
- Move python2 requires to python2 subpackage and added python3 binding.
* Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.9.1-1
- Update to version 3.9.1
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.6.4-6
- Modified %check
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  3.6.4-5
- Fixed logic to restart the active services after upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.4-4
- GA - Bump release of all rpms
* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  3.6.4-3
- Fix for upgrade issues
* Wed Feb 17 2016 Anish Swaminathan <anishs@vmware.com>  3.6.4-2
- Add journald conf file.
* Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 3.6.4-1
- Upgrade version.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  3.6.2-5
- Change config file attributes.
* Wed Dec 09 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.6.2-4
- Moving files from devel rpm to the main package.
* Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 3.6.2-3
- Adding preun section.
* Sat Jul 18 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.6.2-2
- Split headers and unshared libs over to devel package.
* Thu Jun 4 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.6.2-1
- Add syslog-ng support to photon.
