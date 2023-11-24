Summary:        Next generation system logger facilty
Name:           syslog-ng
Version:        3.37.1
Release:        3%{?dist}
License:        GPL + LGPL
URL:            https://syslog-ng.org/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/balabit/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=beebd89c54a415469dc58630ac1900d632ef351f6a13fad4a95ce7bb1760b16d6cfdcede02225a35e97ebce7dae151c6aa228f3d378463e8b873c4f71ed86ab7
Source1:        60-syslog-ng-journald.conf
Source2:        syslog-ng.service
Source3:        cve-2022-38725.patches
Patch0:         fix_autogen_issue.patch
# cve-2022-38725: [1]..[9]
%include        %{SOURCE3}

Requires:       glib >= 2.58.3
Requires:       openssl
Requires:       glibc
Requires:       json-glib
Requires:       json-c
Requires:       systemd
Requires:       paho-c
BuildRequires:  which
BuildRequires:  git
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  eventlog
BuildRequires:  glib-devel >= 2.58.3
BuildRequires:  json-glib-devel
BuildRequires:  json-c-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  curl-devel
BuildRequires:  paho-c-devel
BuildRequires:  bison
Obsoletes:      eventlog

%description
The syslog-ng application is a flexible and highly scalable
system logging tool. It is often used to manage log messages and implement
centralized logging, where the aim is to collect the log messages of several
devices to a single, central log server.

%package -n     python3-syslog-ng
Summary:        python3-syslog-ng
Requires:       python3
Requires:       python3-libs

%description -n python3-syslog-ng
Python 3 version.

%package        devel
Summary:        Header and development files for syslog-ng
Requires:       %{name} = %{version}-%{release}
%description    devel
syslog-ng-devel package contains header files, pkgconfig files, and libraries
needed to build applications using syslog-ng APIs.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
autoreconf -i --force
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
       --localstatedir=%{_localstatedir} \
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
    --with-python=3 \
    --enable-mqtt \
    --disable-static \
    --enable-dynamic-linking \
    PYTHON=%{python3} \
    PKG_CONFIG_PATH={%_libdir}/pkgconfig/
GCCVERSION=$(rpm -q gcc | cut -d'-' -f2)
$(dirname $(gcc -print-prog-name=cc1))/install-tools/mkheaders

%make_build

%install
install -vdm755 %{buildroot}%{_unitdir}
%make_install
find %{buildroot} -name "*.la" -exec rm -f {} \;
rm -rf %{buildroot}/%{_unitdir}/syslog-ng@.service %{buildroot}/%{_infodir}
install -vd %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/
%{_fixperms} %{buildroot}/*
sed -i 's/eventlog//g'  %{buildroot}%{_libdir}/pkgconfig/syslog-ng.pc

install -vdm755 %{buildroot}%{_presetdir}
echo "disable syslog-ng.service" > %{buildroot}%{_presetdir}/50-syslog-ng.preset

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
  mkdir -p /usr/var/
fi
%systemd_post syslog-ng.service

%preun
%systemd_preun syslog-ng.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart syslog-ng.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/syslog-ng/syslog-ng.conf
%config(noreplace) %{_sysconfdir}/syslog-ng/scl.conf
%{_sysconfdir}/systemd/journald.conf.d/*
%{_unitdir}/syslog-ng.service
%{_presetdir}/50-syslog-ng.preset
%{_bindir}/*
%{_sbindir}/syslog-ng
%{_sbindir}/syslog-ng-ctl
%{_sbindir}/syslog-ng-debun
%{_libdir}/libsyslog-ng-*.so.*
%{_libdir}/libevtlog-*.so.*
%{_libdir}/libloggen_helper*
%{_libdir}/libloggen_plugin*
%{_libdir}/libsecret-storage*
%{_libdir}/%{name}/loggen/*
%{_libdir}/syslog-ng/lib*.so
%{_datadir}/syslog-ng/*
%{_mandir}/*

%files -n python3-syslog-ng
%defattr(-,root,root,-)
%{_libdir}/syslog-ng/libmod-python.so
%{_libdir}/syslog-ng/python

%files devel
%defattr(-,root,root)
%{_includedir}/syslog-ng/*
%{_libdir}/libsyslog-ng.so
%{_libdir}/libevtlog.so
%{_libdir}/libsyslog-ng-native-connector.a
%{_libdir}/pkgconfig/*

%changelog
* Fri Nov 24 2023 Ankit Jain <ankitja@vmware.com> 3.37.1-3
- Fix for CVE-2022-38725
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.37.1-2
- Version bump due to glib change
* Thu Jun 30 2022 Oliver Kurth <okurth@vmware.com> 3.37.1-1
- Bump version
* Mon Mar 21 2022 Oliver Kurth <okurth@vmware.com> 3.36.1-1
- Bump version, add MQTT support
* Thu Oct 07 2021 Tapas Kundu <tkundu@vmware.com> 3.17.2-2
- Fix build with updated python symlink changes
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
