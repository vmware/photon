Summary:          WPA client
Name:             wpa_supplicant
Version:          2.10
Release:          3%{?dist}
License:          BSD
URL:              https://w1.fi
Group:            Applications/Communications
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://w1.fi/releases/%{name}-%{version}.tar.gz
%define sha512 wpa=021c2a48f45d39c1dc6557730be5debaee071bc0ff82a271638beee6e32314e353e49d39e2f0dc8dff6e094dcc7008cfe1c32d0c7a34a1a345a12a3f1c1e11a1

BuildRequires:    libnl-devel
BuildRequires:    openssl-devel
BuildRequires:    readline-devel
BuildRequires:    systemd-devel

Requires:         systemd
Requires:         readline
Requires:         libnl
Requires:         openssl

%description
WPA Supplicant is a Wi-Fi Protected Access (WPA) client and IEEE 802.1X supplicant

%prep
%autosetup -p1

%build
cat > %{name}/.config << "EOF"
CONFIG_BACKEND=file
CONFIG_CTRL_IFACE=y
CONFIG_DEBUG_FILE=y
CONFIG_DEBUG_SYSLOG=y
CONFIG_DEBUG_SYSLOG_FACILITY=LOG_DAEMON
CONFIG_DRIVER_NL80211=y
CONFIG_DRIVER_WEXT=y
CONFIG_DRIVER_WIRED=y
CONFIG_EAP_GTC=y
CONFIG_EAP_LEAP=y
CONFIG_EAP_MD5=y
CONFIG_EAP_MSCHAPV2=y
CONFIG_EAP_OTP=y
CONFIG_EAP_PEAP=y
CONFIG_EAP_TLS=y
CONFIG_EAP_TTLS=y
CONFIG_IEEE8021X_EAPOL=y
CONFIG_IPV6=y
CONFIG_LIBNL32=y
CONFIG_PEERKEY=y
CONFIG_PKCS12=y
CONFIG_READLINE=y
CFLAGS += -I%{_includedir}/libnl3
EOF

cd %{name}
make BINDIR=%{_sbindir} LIBDIR=%{_libdir} %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_sbindir} \
         %{buildroot}%{_mandir}/man5 \
         %{buildroot}%{_mandir}/man8 \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_sysconfdir}/%{name}

cd %{name}
install -v -m755 wpa_{cli,passphrase,supplicant} %{buildroot}%{_sbindir}/
install -v -m644 doc/docbook/%{name}.conf.5 %{buildroot}%{_mandir}/man5/
install -v -m644 doc/docbook/wpa_{cli,passphrase,supplicant}.8 %{buildroot}%{_mandir}/man8/

cat > %{buildroot}%{_unitdir}/%{name}@.service << "EOF"
[Unit]
Description=WPA supplicant (%I)
BindsTo=sys-subsystem-net-devices-%i.device
After=sys-subsystem-net-devices-%i.device

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=%{_sbindir}/ip link set dev %I up
ExecStart=%{_sbindir}/%{name} -c %{_sysconfdir}/%{name}/%{name}-%I.conf -B -i %I
ExecStop=%{_sbindir}/ip link set dev %I down

[Install]
WantedBy=multi-user.target
EOF

cat > %{buildroot}%{_sysconfdir}/%{name}/%{name}-wlan0.conf << "EOF"
ctrl_interface=/run/%{name}
update_config=1

# Add network= entry below
EOF

%files
%defattr(-,root,root)
%{_sbindir}/wpa_cli
%{_sbindir}/wpa_passphrase
%{_sbindir}/%{name}
%{_mandir}/*
%{_unitdir}/%{name}@.service
%{_sysconfdir}/%{name}/%{name}-wlan0.conf

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.10-3
- Bump version as a part of openssl upgrade
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.10-2
- Bump version as a part of readline upgrade
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 2.10-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.9-3
- Bump up release for openssl
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.9-2
- openssl 1.1.1
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 2.9-1
- Automatic Version Bump
* Wed Oct 23 2019 Shreyas B. <shreyasb@vmware.com> 2.7-2
- Fixes for CVE-2019-16275.
* Thu Jan 3 2019 Michelle Wang <michellew@vmware.com> 2.7-1
- Update version to 2.7.
* Fri Aug 17 2018 Alexey Makhalov <amakhalov@vmware.com> 2.6-2
- Improve .service file: wait wlanX to appear, run daemon in background.
- Added skeleton for wlan0 conf file.
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.6-1
- Initial build. First version.
