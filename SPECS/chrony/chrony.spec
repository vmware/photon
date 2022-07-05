Name:           chrony
Version:        4.2
Release:        1%{?dist}
Summary:        An NTP client/server
License:        GPLv2
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/NetworkingPrograms
URL:            https://chrony.tuxfamily.org
Source0:        https://download.tuxfamily.org/chrony/chrony-%{version}.tar.gz
%define sha512    %{name}=7f946b27de605b3ebea62cf23916dfad77c99e8b2338ba239ede6b8216ce436b3d4d87770f371c8d8e006507c51d5c831b51f067957abd2935adfdec3f5aa67d

BuildRequires:  systemd
BuildRequires:  libcap-devel
BuildRequires:  nettle-devel
BuildRequires:  libseccomp-devel

Requires:       nettle
Requires:       libcap
Requires:       libseccomp

%description
chrony is a versatile implementation of the Network Time Protocol (NTP).
It can synchronise the system clock with NTP servers, reference clocks
(e.g. GPS receiver), and manual input using wristwatch and keyboard. It
can also operate as an NTPv4 (RFC 5905) server and peer to provide a time
service to other computers in the network.

%prep
%autosetup -p1

cp examples/chrony.conf.example2 chrony.conf

# regenerate the file from getdate.y
rm -f getdate.c

%build
%configure \
        --enable-ntp-signd \
        --enable-scfilter \
        --docdir=%{_docdir} \
        --with-ntp-era=$(date -d '1970-01-01 00:00:00+00:00' +'%s')

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

mkdir -p %{buildroot}%{_sysconfdir}/{sysconfig,logrotate.d}
mkdir -p %{buildroot}%{_localstatedir}/{lib,log}/chrony
mkdir -p %{buildroot}%{_sysconfdir}/dhcp/dhclient.d
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}{%{_unitdir},%{_prefix}/lib/systemd/ntp-units.d}

install -m 644 -p chrony.conf %{buildroot}%{_sysconfdir}/chrony.conf

install -m 640 -p examples/chrony.keys.example \
        %{buildroot}%{_sysconfdir}/chrony.keys
install -m 644 -p examples/chrony.logrotate \
        %{buildroot}%{_sysconfdir}/logrotate.d/chrony

install -m 644 -p examples/chronyd.service \
        %{buildroot}%{_unitdir}/chronyd.service
install -m 644 -p examples/chrony-wait.service \
        %{buildroot}%{_unitdir}/chrony-wait.service

cat > %{buildroot}%{_sysconfdir}/sysconfig/chronyd <<EOF
# Command-line options for chronyd
OPTIONS=""
EOF

touch %{buildroot}%{_localstatedir}/lib/chrony/{drift,rtc}

echo 'chronyd.service' > \
        %{buildroot}%{_prefix}/lib/systemd/ntp-units.d/50-chronyd.list

%check
make %{?_smp_mflags}
make quickcheck %{?_smp_mflags}

%post
%systemd_post chronyd.service chrony-wait.service

%preun
%systemd_preun chronyd.service chrony-wait.service

%postun
%systemd_postun_with_restart chronyd.service

%files
%license COPYING
%doc FAQ NEWS README
%config(noreplace) %{_sysconfdir}/chrony.conf
%config(noreplace) %verify(not md5 size mtime) %attr(640,root,root) %{_sysconfdir}/chrony.keys
%config(noreplace) %{_sysconfdir}/logrotate.d/chrony
%config(noreplace) %{_sysconfdir}/sysconfig/chronyd
%{_bindir}/chronyc
%{_sbindir}/chronyd
%{_prefix}/lib/systemd/ntp-units.d/*.list
%{_unitdir}/chrony*.service
%{_mandir}/man[158]/%{name}*.[158]*
%dir %attr(-,root,root) %{_localstatedir}/lib/chrony
%ghost %attr(-,root,root) %{_localstatedir}/lib/chrony/drift
%ghost %attr(-,root,root) %{_localstatedir}/lib/chrony/rtc
%dir %attr(-,root,root) %{_localstatedir}/log/chrony

%changelog
*  Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 4.2-1
-  Automatic Version Bump
*  Tue Aug 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.0-4
-  Bump version as a part of nettle upgrade
*  Wed Jul 07 2021 Tapas Kundu <tkundu@vmware.com> 4.0-3
-  Added requires
*  Thu Nov 19 2020 Piyush Gupta <gpiyush@vmware.com> 4.0-2
-  Make check fix
*  Mon Jul 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.0-1
-  Initial version for Photon
