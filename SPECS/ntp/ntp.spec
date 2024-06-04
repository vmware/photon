Summary:        Network Time Protocol reference implementation
Name:           ntp
Version:        4.2.8p18
Release:        1%{?dist}
License:        NTP
URL:            http://www.ntp.org
Group:          System Environment/NetworkingPrograms
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz
%define sha512  %{name}=c314f645d7d85e1028327657f30557cdfd86d417565b6c9fcbb40fca8a4c22a97b70908e8b73c6b31e14915b5b910ae0055fd42e819dd3cb48583b2a826c3fc4

# https://github.com/darkhelmet/ntpstat
Source1:        ntpstat-master.zip
%define sha512  ntpstat=79e348e93683f61eb97371f62bcb3b74cedfe6fd248a86d294d65ce4dc3649ce923bdf683cb18604fe47c4e854a6970c4ae1577e20b1febc87c3009888025ed0

Source2:        %{name}.sysconfig
Source3:        %{name}.sysusers

BuildRequires:  which
BuildRequires:  libcap-devel
BuildRequires:  unzip
BuildRequires:  systemd
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  libevent-devel

Requires:       systemd
Requires:       openssl
Requires:       libcap >= 2.24
Requires:       libevent
Requires(pre):  systemd-rpm-macros
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
The ntp package contains a client and server to keep the time
synchronized between various computers over a network. This
package is the official reference implementation of the
NTP protocol.

%package        perl
Summary:        Perl scripts for ntp
Group:          Utilities
Requires:       %{name} = %{version}-%{release}
Requires:       perl >= 5
Requires:       perl-Net-SSLeay
Requires:       perl-IO-Socket-SSL

%description    perl
Perl scripts for ntp.

%package -n     ntpstat
Summary:        Utilities
Group:          Utilities

%description -n ntpstat
ntpstat is a utility which reports the synchronisation
state of the NTP daemon running on the local machine.

%prep
%autosetup -p1 -a1

%build
%configure \
    --disable-silent-rules \
    --with-binsubdir=sbin \
    --enable-linuxcaps

%make_build
%make_build -C ntpstat-master

%install
%make_install %{?_smp_mflags}
install -v -m755 -d %{buildroot}%{_docdir}/%{name}-%{version}
cp -v -R html/* %{buildroot}%{_docdir}/%{name}-%{version}/
install -vdm 755 %{buildroot}%{_sysconfdir}

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/drift \
         %{buildroot}%{_sysconfdir}/sysconfig \
         %{buildroot}%{_unitdir}

cp %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

pushd ntpstat-master
install -m 755 ntpstat %{buildroot}%{_bindir}
install -m 644 ntpstat.1 %{buildroot}%{_mandir}/man8/ntpstat.8
popd

install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.sysusers

cat > %{buildroot}%{_sysconfdir}/%{name}.conf <<- "EOF"
tinker panic 0
restrict default kod nomodify notrap nopeer noquery
restrict 127.0.0.1
restrict -6 ::1
driftfile %{_sharedstatedir}/%{name}/drift/%{name}.drift
EOF

install -D -m644 COPYRIGHT %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
rm -rf %{buildroot}%{_sysconfdir}/rc.d/*

%{_fixperms} %{buildroot}/*

cat << EOF >> %{buildroot}%{_unitdir}/ntpd.service
[Unit]
Description=Network Time Service
After=syslog.target network.target
Documentation=man:ntpd
Conflicts=systemd-timesyncd.service

[Service]
Type=forking
EnvironmentFile=%{_sysconfdir}/sysconfig/%{name}
ExecStart=%{_bindir}/ntpd -g -u %{name}:%{name}
Restart=always

[Install]
WantedBy=multi-user.target
EOF

install -vdm755 %{buildroot}%{_presetdir}
echo "disable ntpd.service" > %{buildroot}%{_presetdir}/50-ntpd.preset

%check
%make_build check

%pre
%sysusers_create_compat %{SOURCE3}

%post
/sbin/ldconfig
%systemd_post ntpd.service

%preun
%systemd_preun ntpd.service

%postun
%systemd_postun_with_restart ntpd.service
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%attr(0755,%{name},%{name}) %{_sharedstatedir}/%{name}/drift
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysusersdir}/%{name}.sysusers
%{_unitdir}/ntpd.service
%{_presetdir}/50-ntpd.preset
%{_bindir}/ntpd
%{_bindir}/ntpdate
%{_bindir}/ntpdc
%{_bindir}/%{name}-keygen
%{_bindir}/ntpq
%{_bindir}/ntptime
%{_bindir}/sntp
%{_bindir}/tickadj
%{_docdir}/%{name}-%{version}/*
%{_docdir}/%{name}/*
%{_docdir}/sntp/*
%{_datadir}/licenses/%{name}/LICENSE
%{_mandir}/man1/ntpd.1.gz
%{_mandir}/man1/ntpdc.1.gz
%{_mandir}/man1/%{name}-keygen.1.gz
%{_mandir}/man1/ntpq.1.gz
%{_mandir}/man1/sntp.1.gz
%{_mandir}/man5/*

%files perl
%defattr(-,root,root)
%{_bindir}/calc_tickadj
%{_bindir}/ntptrace
%{_bindir}/%{name}-wait
%{_bindir}/update-leap
%{_datadir}/%{name}/lib/NTP/Util.pm
%{_mandir}/man1/calc_tickadj.1.gz
%{_mandir}/man1/ntptrace.1.gz
%{_mandir}/man1/%{name}-wait.1.gz
%{_mandir}/man1/update-leap.1.gz

%files -n ntpstat
%defattr(-,root,root)
%{_bindir}/ntpstat
%{_mandir}/man8/ntpstat.8*

%changelog
* Wed Jun 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.2.8p18-1
- Upgrade to v4.2.8p18
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.2.8p17-2
- Bump version as a part of openssl upgrade
* Tue Jun 27 2023 Michelle Wang <michellew@vmware.com> 4.2.8p17-1
- Upgrade to 4.2.8p17 for CVE-2023-26551 ~ CVE-2023-26555
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.2.8p15-8
- Add libevent to buld requires
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 4.2.8p15-7
- Use systemd-rpm-macros for user creation
* Fri Oct 28 2022 Harinadh D <hdommaraju@vmware.com> 4.2.8p15-6
- remove executable permission to ntp.conf
* Sun Oct 02 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.2.8p15-5
- Fix build with latest toolchain
* Fri Jan 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.2.8p15-4
- Bump version as a part of perl-Net-SSLeay version upgrade
- Make ntp work when openssl fips enabled
* Thu Sep 02 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.2.8p15-3
- Bump up release for openssl
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.2.8p15-2
- openssl 1.1.1
* Tue Jul 14 2020 Gerrit Photon <photon-checkins@vmware.com> 4.2.8p15-1
- Automatic Version Bump
* Wed Apr 29 2020 Dweep Advani <dadvani@vmware.com> 4.2.8p14-1
- Upgrade version to 4.2.8p14, addresses CVE-2020-11868.
* Tue Jul 16 2019 Srinidhi Rao <srinidhir@vmware.com> 4.2.8p13-1
- Upgrade to version 4.2.8p13
- Ported fix to created drift directory owning ntp user.
* Fri Aug 24 2018 Srinidhi Rao <srinidhir@vmware.com> 4.2.8p12-1
- Upgrade version to 4.2.8p12.
* Mon Mar 05 2018 Xiaolin Li <xiaolinl@vmware.com> 4.2.8p11-1
- Upgrade version to 4.2.8p11 and move perl scripts to perl subpackage.
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.2.8p10-4
- Remove shadow from requires and use explicit tools for post actions
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  4.2.8p10-3
- Disabled ntpd service by default
* Mon Apr 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.8p10-2
- add noquery to conf
* Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 4.2.8p10-1
- Upgrade version to 4.2.8p10 - fix for CVE-2017-6458, CVE-2017-6460
* Tue Jan 24 2017 Xiaolin Li <xiaolinl@vmware.com> 4.2.8p9-1
- Updated to version 4.2.8p9.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.8p6-4
- GA - Bump release of all rpms
* Thu May 12 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.8p6-3
- Adding ntp sysconfig file
* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 4.2.8p6-2
- Edit scriptlets.
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 4.2.8p6-1
- Upgrade version
* Thu Jan 7 2016 Xiaolin Li <xiaolinl@vmware.com>  4.2.8p3-4
- Add ntpstat package.
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  4.2.8p3-3
- Add systemd to Requires and BuildRequires.
* Fri Oct 30 2015 Xiaolin Li <xiaolinl@vmware.com> 4.2.8p3-2
- Add ntpd to systemd service.
* Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.8p3-1
- Updating to version 4.2.8p3
* Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.6p5-1
- Initial build.  First version
