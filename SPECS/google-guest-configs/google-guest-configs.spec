%define debug_package %{nil}
%global dracutdir %(pkg-config --variable=dracutdir dracut)

Summary:        Linux Guest Environment for Google Compute Engine
Name:           google-guest-configs
Version:        20250207.00
Release:        2%{?dist}
Group:          Tools/System Environment
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/GoogleCloudPlatform/guest-configs

Source0:        https://github.com/GoogleCloudPlatform/guest-configs/archive/refs/tags/google-guest-configs-%{version}.tar.gz
%define sha512  google-guest-configs=ecee30253b2265f79abfa77a5034ad019212ef7097b9befb0e87975b1733245d89c0b59d23165a4e49a4d8598231330c6658f931fe3d1583f025ae2adf6b6fe4

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  systemd-rpm-macros
BuildRequires:  dracut

Requires:       google-guest-oslogin
Requires:       dracut
Requires:       rsyslog
Requires:       curl
Requires:       jq
Requires:       nvme-cli
Requires:       ethtool

Obsoletes:      google-compute-engine
Provides:       google-compute-engine = %{version}

%description
This repository holds the sources and packaging artifacts for the google-compute-engine package. This package contains configuration files and scripts used to support the Google Compute Engine guest environment, and also depends on the other packages needed to provide all guest functionality.

%prep
%autosetup -n guest-configs-%{version}

%build

%install
cp -a src/{etc,usr} %{buildroot}
install -d %{buildroot}%{_udevrulesdir}
cp -a src/lib/udev/rules.d/* %{buildroot}%{_udevrulesdir}
cp -a src/lib/udev/google_nvme_id %{buildroot}%{_udevrulesdir}/../
install -d  %{buildroot}%{dracutdir}

cp -a src/lib/dracut/* %{buildroot}%{dracutdir}/

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/dracut.conf.d/gce.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/gce-blacklist.conf
%config(noreplace) %{_sysconfdir}/rsyslog.d/90-google.conf
%config(noreplace) %{_sysconfdir}/sysctl.d/60-gce-network-security.conf
%config(noreplace) %{_sysconfdir}/systemd/resolved.conf.d/gce-resolved.conf
%exclude %{_sysconfdir}/apt/apt.conf.d/01autoremove-gce
%{_sysconfdir}/dhcp/dhclient.d/google_hostname.sh
%{_sysconfdir}/sysconfig/network/scripts/google_up.sh
%{dracutdir}/modules.d/30gcp-udev-rules/module-setup.sh
%{_bindir}/gce-nic-naming
%{_bindir}/google_optimize_local_ssd
%{_bindir}/google_set_hostname
%{_bindir}/google_set_multiqueue
%{_libdir}/networkd-dispatcher/routable.d/google_hostname.sh
%{_libdir}/udev/google_nvme_id
%{_udevrulesdir}/65-gce-disk-naming.rules
%{_udevrulesdir}/75-gce-network.rules
%exclude %{_sysconfdir}/NetworkManager/dispatcher.d/google_hostname.sh

%changelog
* Wed Mar 05 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20250207.00-2
- Add ethtool to requires
- Exclude apt files
* Thu Feb 13 2025 Tapas Kundu <tapas.kundu@broadcom.com> 20250207.00-1
- Package https://github.com/GoogleCloudPlatform/guest-configs
