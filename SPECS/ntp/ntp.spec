Summary:        Network Time Protocol reference implementation
Name:           ntp
Version:        4.2.8p14
Release:        5%{?dist}
License:        NTP
URL:            http://www.ntp.org/
Group:          System Environment/NetworkingPrograms
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz
%define sha512    ntp=b0183b4b2f2c6ea0a49d0aca1fa28a7b5cd21e20696a2f633f5afa37c4ea2c59fa7769af82a55c626db49b9eb5a531608710dc1977c4d518583577ef95940ae8
#https://github.com/darkhelmet/ntpstat
Source1:        ntpstat-master.zip
%define sha512 ntpstat=79e348e93683f61eb97371f62bcb3b74cedfe6fd248a86d294d65ce4dc3649ce923bdf683cb18604fe47c4e854a6970c4ae1577e20b1febc87c3009888025ed0
Source2:        ntp.sysconfig

Patch0:         ntp-CVE-2020-15025.patch

BuildRequires:  which
BuildRequires:  libcap-devel
BuildRequires:  unzip
BuildRequires:  systemd
BuildRequires:  openssl-devel
BuildRequires:  libevent-devel

Requires:       systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires:       openssl
Requires:       libevent
Requires:       libcap >= 2.24

%description
The ntp package contains a client and server to keep the time
synchronized between various computers over a network. This
package is the official reference implementation of the
NTP protocol.

%package        perl
Summary:        Perl scripts for ntp
Group:          Utilities
Requires:       ntp = %{version}-%{release}, perl >= 5
Requires:       perl-Net-SSLeay
Requires:       perl-IO-Socket-SSL
%description    perl
Perl scripts for ntp.

%package -n ntpstat
Summary:    Utilities
Group:      Utilities
%description -n ntpstat
ntpstat is a utility which reports the synchronisation
state of the NTP daemon running on the local machine.

%prep
%autosetup -p1 -a 1

%build
sh ./configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc \
    --with-binsubdir=sbin \
    --enable-system-libevent \
    --enable-linuxcaps
%make_build
make -C ntpstat-master CFLAGS="$CFLAGS" %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}
install -v -m755    -d %{buildroot}%{_datadir}/doc/%{name}-%{version}
cp -v -R html/*     %{buildroot}%{_datadir}/doc/%{name}-%{version}/
install -vdm 755 %{buildroot}/etc

mkdir -p %{buildroot}/var/lib/ntp/drift
mkdir -p %{buildroot}/etc/sysconfig
cp %{SOURCE2} %{buildroot}/etc/sysconfig/ntp
pushd ntpstat-master
install -m 755 ntpstat %{buildroot}/%{_bindir}
install -m 644 ntpstat.1 %{buildroot}/%{_mandir}/man8/ntpstat.8
popd

cat > %{buildroot}/etc/ntp.conf <<- "EOF"
tinker panic 0
restrict default kod nomodify notrap nopeer noquery
restrict 127.0.0.1
restrict -6 ::1
driftfile /var/lib/ntp/drift/ntp.drift
EOF
install -D -m644 COPYRIGHT %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
rm -rf %{buildroot}/etc/rc.d/*

%{_fixperms} %{buildroot}/*
mkdir -p %{buildroot}/lib/systemd/system
cat << EOF >> %{buildroot}/lib/systemd/system/ntpd.service
[Unit]
Description=Network Time Service
After=syslog.target network.target
Documentation=man:ntpd
Conflicts=systemd-timesyncd.service

[Service]
Type=forking
EnvironmentFile=/etc/sysconfig/ntp
ExecStart=/usr/bin/ntpd -g -u ntp:ntp
Restart=always

[Install]
WantedBy=multi-user.target
EOF

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable ntpd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-ntpd.preset

%check
make -k check %{?_smp_mflags} |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%pre
if ! getent group ntp >/dev/null; then
    groupadd -g 87 ntp
fi
if ! getent passwd ntp >/dev/null; then
    useradd -c "Network Time Protocol" -d /var/lib/ntp -u 87 -g ntp -s /bin/false ntp
fi
%post
%{_sbindir}/ldconfig
%systemd_post ntpd.service

%preun
%systemd_preun ntpd.service

%postun
%systemd_postun_with_restart ntpd.service

%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%dir /var/lib/ntp/drift
%attr(0755, ntp, ntp) /var/lib/ntp/drift
%config(noreplace) /etc/ntp.conf
%config(noreplace) /etc/sysconfig/ntp
/lib/systemd/system/ntpd.service
%{_libdir}/systemd/system-preset/50-ntpd.preset
%{_bindir}/ntpd
%{_bindir}/ntpdate
%{_bindir}/ntpdc
%{_bindir}/ntp-keygen
%{_bindir}/ntpq
%{_bindir}/ntptime
%{_bindir}/sntp
%{_bindir}/tickadj
%{_datadir}/doc/%{name}-%{version}/*
%{_datadir}/doc/ntp/*
%{_datadir}/doc/sntp/*
%{_datadir}/licenses/ntp/LICENSE
%{_mandir}/man1/ntpd.1.gz
%{_mandir}/man1/ntpdc.1.gz
%{_mandir}/man1/ntp-keygen.1.gz
%{_mandir}/man1/ntpq.1.gz
%{_mandir}/man1/sntp.1.gz
%{_mandir}/man5/*

%files perl
%{_bindir}/calc_tickadj
%{_bindir}/ntptrace
%{_bindir}/ntp-wait
%{_bindir}/update-leap
%{_datadir}/ntp/lib/NTP/Util.pm
%{_mandir}/man1/calc_tickadj.1.gz
%{_mandir}/man1/ntptrace.1.gz
%{_mandir}/man1/ntp-wait.1.gz
%{_mandir}/man1/update-leap.1.gz

%files -n ntpstat
%defattr(-,root,root)
%{_bindir}/ntpstat
%{_mandir}/man8/ntpstat.8*

%changelog
* Wed Apr 12 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.2.8p14-5
- Bump version as a part of libevent upgrade
* Fri Oct 28 2022 Harinadh D <hdommaraju@vmware.com> 4.2.8p14-4
- remove executable permission to ntp.conf
* Thu Apr 14 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.2.8p14-3
- Use system libevent instead of bundled libevent source
- to fix CVE-2016-10195
* Wed Aug 26 2020 Dweep Advani <dadvani@vmware.com> 4.2.8p14-2
- Patched for CVE-2020-15025
* Wed Apr 29 2020 Dweep Advani <dadvani@vmware.com> 4.2.8p14-1
- Upgrade to version 4.2.8p14, addresses CVE-2020-11868.
* Tue Jul 16 2019 Srinidhi Rao <srinidhir@vmware.com> 4.2.8p13-1
- Upgrade to version 4.2.8p13
* Wed May 29 2019 Siju Maliakkal <smaliakkal@vmware.com> 4.2.8p12-2
- PR#2355310  created drift directory owning ntp user
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
