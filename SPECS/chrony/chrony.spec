Name:           chrony
Version:        4.3
Release:        2%{?dist}
Summary:        An NTP client/server
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/NetworkingPrograms
URL:            https://chrony.tuxfamily.org

Source0: https://download.tuxfamily.org/chrony/chrony-%{version}.tar.gz
%define sha512 %{name}=1394bac3ed684352fe89b7fef7da50e61f9f522abee807627ae1fc4c2dde891017bc8e5b13759fced028f3a1e875d5e4e5a4f85de65c63b5f83d0ca03bb4c5df

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  systemd
BuildRequires:  libcap-devel
BuildRequires:  nettle-devel
BuildRequires:  libseccomp-devel
BuildRequires:  bison

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

%make_build

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}%{_sysconfdir}/{sysconfig,logrotate.d} \
         %{buildroot}%{_localstatedir}/{lib,log}/chrony \
         %{buildroot}%{_sysconfdir}/dhcp/dhclient.d \
         %{buildroot}%{_libexecdir} \
         %{buildroot}{%{_unitdir},%{_libdir}/systemd/ntp-units.d}

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

touch %{buildroot}%{_sharedstatedir}/chrony/{drift,rtc}

echo 'chronyd.service' > \
        %{buildroot}%{_libdir}/systemd/ntp-units.d/50-chronyd.list

%if 0%{?with_check}
%check
make %{?_smp_mflags}
make quickcheck %{?_smp_mflags}
%endif

%post
%systemd_post chronyd.service chrony-wait.service

%preun
%systemd_preun chronyd.service chrony-wait.service

%postun
%systemd_postun_with_restart chronyd.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license COPYING
%doc FAQ NEWS README
%config(noreplace) %{_sysconfdir}/chrony.conf
%config(noreplace) %verify(not md5 size mtime) %attr(640,root,root) %{_sysconfdir}/chrony.keys
%config(noreplace) %{_sysconfdir}/logrotate.d/chrony
%config(noreplace) %{_sysconfdir}/sysconfig/chronyd
%{_bindir}/chronyc
%{_sbindir}/chronyd
%{_libdir}/systemd/ntp-units.d/*.list
%{_unitdir}/chrony*.service
%{_mandir}/man[158]/%{name}*.[158]*
%dir %attr(-,root,root) %{_sharedstatedir}/chrony
%ghost %attr(-,root,root) %{_sharedstatedir}/chrony/drift
%ghost %attr(-,root,root) %{_sharedstatedir}/chrony/rtc
%dir %attr(-,root,root) %{_localstatedir}/log/chrony

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 4.3-2
- Release bump for SRP compliance
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 4.3-1
- Automatic Version Bump
* Wed Aug 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.2-2
- Bump version as a part of nettle upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 4.2-1
- Automatic Version Bump
* Tue Aug 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.0-4
- Bump version as a part of nettle upgrade
* Wed Jul 07 2021 Tapas Kundu <tkundu@vmware.com> 4.0-3
- Added requires
* Thu Nov 19 2020 Piyush Gupta <gpiyush@vmware.com> 4.0-2
- Make check fix
* Mon Jul 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.0-1
- Initial version for Photon
