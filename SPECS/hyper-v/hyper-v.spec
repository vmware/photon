Summary:        Hyper-V tools
Name:           hyper-v
Version:        4.9
Release:        1%{?dist}
License:        GPLv2+
URL:            https://elixir.bootlin.com/linux/v4.9/source/tools/hv
Group:          System/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    hyper-v=f7801636573dbdc679dba8eadce86cf408b6ffc1
Source1:        bondvf.sh
Source2:        hv_get_dns_info.sh
Source3:        hv_get_dhcp_info.sh
Source4:        hv_set_ifconfig.sh
Source5:        lsvmbus
BuildRequires:  systemd
Requires:       systemd
%description
Hyper-V tools.

%prep
%setup

%build
make

%install
install -vdm 755 %{buildroot}/%{_sbindir}
install -m 755  %{SOURCE5}  %{buildroot}/%{_sbindir}/lsvmbus
install -vdm 755 %{buildroot}/%{_bindir}
install -m 755  %{SOURCE1}  %{buildroot}/%{_bindir}/bondvf.sh
install -m 755  %{SOURCE2}  %{buildroot}/%{_bindir}/hv_get_dns_info.sh
install -m 755  %{SOURCE3}  %{buildroot}/%{_bindir}/hv_get_dhcp_info.sh
install -m 755  %{SOURCE4}  %{buildroot}/%{_bindir}/hv_set_ifconfig.sh
install -m 755  hv_fcopy_daemon  %{buildroot}/%{_bindir}/hv_fcopy_daemon
install -m 755  hv_kvp_daemon    %{buildroot}/%{_bindir}/hv_kvp_daemon
install -m 755  hv_vss_daemon    %{buildroot}/%{_bindir}/hv_vss_daemon
install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable hv_fcopy_daemon.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-hyper-v.preset
echo "disable hv_kvp_daemon.service" >> %{buildroot}%{_libdir}/systemd/system-preset/50-hyper-v.preset
echo "disable hv_vss_daemon.service" >> %{buildroot}%{_libdir}/systemd/system-preset/50-hyper-v.preset

install -vdm755 %{buildroot}/usr/lib/systemd/system
cat << EOF >> %{buildroot}/usr/lib/systemd/system/hv_fcopy_daemon.service
[Unit]
Description=Hyper-v file copy daemon
ConditionVirtualization=microsoft

[Service]
ExecStart=/usr/bin/hv_fcopy_daemon -n

[Install]
WantedBy=multi-user.target
EOF

cat << EOF >> %{buildroot}/usr/lib/systemd/system/hv_kvp_daemon.service
[Unit]
Description=Hyper-v key value pair daemon
ConditionVirtualization=microsoft

[Service]
ExecStart=/usr/bin/hv_kvp_daemon -n

[Install]
WantedBy=multi-user.target

EOF
cat << EOF >> %{buildroot}/usr/lib/systemd/system/hv_vss_daemon.service
[Unit]
Description=Hyper-v vss daemon
ConditionVirtualization=microsoft

[Service]
ExecStart=/usr/bin/hv_vss_daemon -n

[Install]
WantedBy=multi-user.target
EOF

%post
/sbin/ldconfig
%systemd_post  hv_fcopy_daemon.service
%systemd_post  hv_kvp_daemon.service
%systemd_post  hv_vss_daemon.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart  hv_fcopy_daemon.service
%systemd_postun_with_restart  hv_kvp_daemon.service
%systemd_postun_with_restart  hv_vss_daemon.service

%preun
%systemd_preun  hv_fcopy_daemon.service
%systemd_preun  hv_kvp_daemon.service
%systemd_preun  hv_vss_daemon.service

%files
%defattr(-,root,root)
%{_sbindir}/lsvmbus
%{_bindir}/bondvf.sh
%{_bindir}/hv_get_dns_info.sh
%{_bindir}/hv_get_dhcp_info.sh
%{_bindir}/hv_set_ifconfig.sh
%{_bindir}/hv_fcopy_daemon
%{_bindir}/hv_kvp_daemon
%{_bindir}/hv_vss_daemon
%{_libdir}/systemd/system-preset/50-hyper-v.preset
%{_libdir}/systemd/system/hv_fcopy_daemon.service
%{_libdir}/systemd/system/hv_kvp_daemon.service
%{_libdir}/systemd/system/hv_vss_daemon.service


%changelog
*   Tue Mar 13 2018 Xiaolin Li <xiaolinl@vmware.com> 4.9-1
-   Initial version.
