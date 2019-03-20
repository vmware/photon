Summary:        Network Time Protocol reference implementation
Name:           ntp
Version:        4.2.8p12
Release:        4%{?dist}
License:        NTP
URL:            http://www.ntp.org/
Group:          System Environment/NetworkingPrograms
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz
%define sha1    ntp=316a0c823beb3ea12c8ce125442a0cda15c45d73

#https://github.com/darkhelmet/ntpstat
Source1: ntpstat-master.zip
%define sha1 ntpstat=729cf2c9f10da43554f26875e91e1973d4498761
Source2: ntp.sysconfig
BuildRequires:  which
BuildRequires:  libcap-devel
BuildRequires:  unzip
BuildRequires:  systemd
BuildRequires:  openssl-devel
Requires:       systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires:       openssl
Requires:       libcap >= 2.24
Requires:       perl-Net-SSLeay
Requires:       perl-IO-Socket-SSL

%description
The ntp package contains a client and server to keep the time 
synchronized between various computers over a network. This 
package is the official reference implementation of the 
NTP protocol.

%package -n ntpstat
Summary:    Utilities
Group:      Utilities
%description -n ntpstat
ntpstat is a utility which reports the synchronisation
state of the NTP daemon running on the local machine.

%prep
%setup -q -a 1

%build
./configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc \
    --with-binsubdir=sbin \
    --enable-linuxcaps
make %{?_smp_mflags}
make -C ntpstat-master CFLAGS="$CFLAGS"
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
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
After=network.target
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
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
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
%attr(0750, root, root) %config(noreplace) /etc/ntp.conf
%attr(0750, root, root) %config(noreplace) /etc/sysconfig/ntp
/lib/systemd/system/ntpd.service
%exclude %{_bindir}/ntpstat
%exclude %{_mandir}/man8/ntpstat.8*
%{_bindir}/*
%{_datadir}/doc/%{name}-%{version}/*
%{_datadir}/doc/ntp/*
%{_datadir}/doc/sntp/*
%{_datadir}/licenses/ntp/LICENSE
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/ntp/lib/NTP/Util.pm

%files -n ntpstat
%defattr(-,root,root)
%{_bindir}/ntpstat
%{_mandir}/man8/ntpstat.8*

%changelog
*   Mon Mar 25 2019 Tapas Kundu <tkundu@vmware.com> 4.2.8p12-4
-   Bumped up to use latest openssl
*   Thu Mar 21 2019 Siju Maliakkal <smaliakkal@vmware.com> 4.2.8p12-3
-   Created drift directory owned by ntp
*   Tue Mar 19 2019 Siju Maliakkal <smaliakkal@vmware.com> 4.2.8p12-2
-   Created directory for drift file
*   Wed Aug 22 2018 Srinidhi Rao <srinidhir@vmware.com> 4.2.8p12-1
-   Upgrade version to 4.2.8p12.
*   Wed Aug 1 2018 Srinidhi Rao <srinidhir@vmware.com> 4.2.8p11-2
-   Update requires tag in the ntp spec file to include the
-   perl-IO-Socket and perl-Net-SSLeay dependencies.
*   Thu Jun 28 2018 Srinidhi Rao <srinidhir@vmware.com> 4.2.8p11-1
-   Upgrade version to 4.2.8p11.
-   Remove shadow from requires and use explicit tools for post actions.
*   Wed Sep 27 2017 Anish Swaminathan <anishs@vmware.com> 4.2.8p10-4
-   Add patch to remove call to OpenSSL's list digest method in ntpq
*   Thu Jul 27 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.2.8p10-3
-   Remove syslog.target from service file
*   Mon Apr 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.8p10-2
-   add noquery to conf
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 4.2.8p10-1
-   Upgrade version to 4.2.8p10 - fix for CVE-2017-6458, CVE-2017-6460
*   Tue Jan 24 2017 Xiaolin Li <xiaolinl@vmware.com> 4.2.8p9-1
-   Updated to version 4.2.8p9.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.8p6-4
-   GA - Bump release of all rpms
*   Thu May 12 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.8p6-3
-   Adding ntp sysconfig file
*   Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 4.2.8p6-2
-   Edit scriptlets.
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 4.2.8p6-1
-   Upgrade version
*   Thu Jan 7 2016 Xiaolin Li <xiaolinl@vmware.com>  4.2.8p3-4
-   Add ntpstat package.
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  4.2.8p3-3
-   Add systemd to Requires and BuildRequires.
*   Fri Oct 30 2015 Xiaolin Li <xiaolinl@vmware.com> 4.2.8p3-2
-   Add ntpd to systemd service.
*   Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.8p3-1
-   Updating to version 4.2.8p3
*   Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.6p5-1
-   Initial build.  First version
