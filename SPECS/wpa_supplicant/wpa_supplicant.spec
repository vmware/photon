Summary:          WPA client
Name:             wpa_supplicant
Version:          2.7
Release:          5%{?dist}
License:          BSD
URL:              https://w1.fi
Group:            Applications/Communications
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          https://w1.fi/releases/%{name}-%{version}.tar.gz
%define sha1 wpa=3c3c2c6bc493fb32b919d9b410768324f3729e25
Patch0:           wpa_supplicant-CVE-2019-9496.patch
Patch1:           wpa_supplicant-CVE-2019-9497.patch
Patch2:           wpa_supplicant-CVE-2019-9498.patch
Patch3:           wpa_supplicant-CVE-2019-9499.patch
Patch4:           wpa_supplicant-CVE-2019-9495-0001-OpenSSL-Use-constant-time-operations-for-private-big.patch
Patch5:           wpa_supplicant-CVE-2019-9495-0003-OpenSSL-Use-constant-time-selection-for-crypto_bignu.patch
Patch6:           wpa_supplicant-CVE-2019-9495-0002-Add-helper-functions-for-constant-time-operations.patch
Patch7:           wpa_supplicant-CVE-2019-9495-0004-EAP-pwd-Use-constant-time-and-memory-access-for-find.patch
Patch8:           wpa_supplicant-CVE-2019-9494-0005-SAE-Minimize-timing-differences-in-PWE-derivation.patch
Patch9:           wpa_supplicant-CVE-2019-9494-0006-SAE-Avoid-branches-in-is_quadratic_residue_blind.patch
Patch10:          wpa_supplicant-CVE-2019-9494-0007-SAE-Mask-timing-of-MODP-groups-22-23-24.patch
Patch11:          wpa_supplicant-CVE-2019-9494-0008-SAE-Use-const_time-selection-for-PWE-in-FFC.patch
Patch12:          wpa_supplicant-CVE-2019-9494-0009-SAE-Use-constant-time-operations-in-sae_test_pwd_see.patch
Patch13:          wpa_supplicant-CVE-2019-11555-0001-EAP-pwd-server-Fix-reassembly-buffer-handling.patch
Patch14:          wpa_supplicant-CVE-2019-11555-0003-EAP-pwd-peer-Fix-reassembly-buffer-handling.patch
Patch15:          CVE-2019-16275_AP_Silently_ignore_management_frame_from_unexpected_source_address.patch

BuildRequires:    libnl-devel openssl-devel
Requires:         libnl
Requires:         openssl

%description
WPA Supplicant is a Wi-Fi Protected Access (WPA) client and IEEE 802.1X supplicant

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

%build
cat > wpa_supplicant/.config << "EOF"
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
CFLAGS += -I/usr/include/libnl3
EOF

cd wpa_supplicant
make BINDIR=%{_sbindir} LIBDIR=%{_libdir} %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/etc/wpa_supplicant
cd wpa_supplicant
install -v -m755 wpa_{cli,passphrase,supplicant} %{buildroot}%{_sbindir}/
install -v -m644 doc/docbook/wpa_supplicant.conf.5 %{buildroot}%{_mandir}/man5/
install -v -m644 doc/docbook/wpa_{cli,passphrase,supplicant}.8 %{buildroot}%{_mandir}/man8/

cat > %{buildroot}/usr/lib/systemd/system/wpa_supplicant@.service << "EOF"
[Unit]
Description=WPA supplicant (%I)
BindsTo=sys-subsystem-net-devices-%i.device
After=sys-subsystem-net-devices-%i.device

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/sbin/ip link set dev %I up
ExecStart=/usr/sbin/wpa_supplicant -c /etc/wpa_supplicant/wpa_supplicant-%I.conf -B -i %I
ExecStop=/usr/sbin/ip link set dev %I down

[Install]
WantedBy=multi-user.target
EOF

cat > %{buildroot}/etc/wpa_supplicant/wpa_supplicant-wlan0.conf << "EOF"
ctrl_interface=/run/wpa_supplicant
update_config=1

# Add network= entry below
EOF

%files
%defattr(-,root,root)
%{_sbindir}/wpa_cli
%{_sbindir}/wpa_passphrase
%{_sbindir}/wpa_supplicant
%{_mandir}/*
%{_libdir}/systemd/system/wpa_supplicant@.service
%{_sysconfdir}/wpa_supplicant/wpa_supplicant-wlan0.conf

%changelog
*   Wed Oct 23 2019 Shreyas B. <shreyasb@vmware.com> 2.7-5
-   Fixes for CVE-2019-16275.
*   Mon Jun 24 2019 Michelle Wang <michellew@vmware.com> 2.7-4
-   Add patch for CVE-2019-9494 and CVE-2019-11555
-   Skip 001, 002 and 003 patch of CVE-2019-9494
-   Since they are duplicate with those patches in CVE-2019-9495
*   Wed May 29 2019 Michelle Wang <michellew@vmware.com> 2.7-3
-   Fix CVE-2019-9495
*   Fri Apr 19 2019 Siju Maliakkal <smaliakkal@vmware.com> 2.7-2
-   Fix CVE-2019-9496 CVE-2019-9497 CVE-2019-9498 CVE-2019-9499
*   Thu Jan 3 2019 Michelle Wang <michellew@vmware.com> 2.7-1
-   Update version to 2.7.
*   Fri Aug 17 2018 Alexey Makhalov <amakhalov@vmware.com> 2.6-2
-   Improve .service file: wait wlanX to appear, run daemon in background.
-   Added skeleton for wlan0 conf file.
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.6-1
-   Initial build. First version.
