# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Summary:	A Distributed init System
Name:		fleet
Version:	0.11.5
Release:	3%{?dist}
License:	Apache 2.0
URL:		https://coreos.com/using-coreos/clustering/
Group:		OS/ClusterManagement
BuildRequires:	go
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/coreos/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1 fleet=df90c76e7c6458a05a77078993d9bd705a25b8c5
Source1:	fleet.conf
Source2:	fleet.rules
Requires:	systemd
BuildRequires:	systemd

%description
fleet ties together systemd and etcd into a simple distributed init system.

%prep
%setup -q

%build
./build

%install
mkdir -p %{buildroot}%{_bindir}
cp bin/* %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/fleet
install -p -m 0644 %{SOURCE1} %{buildroot}/etc/fleet
mkdir -p %{buildroot}/run/fleet
mkdir -p %{buildroot}/lib/systemd/system
cat << EOF >> %{buildroot}/lib/systemd/system/fleet.service
[Unit]
Description=Fleet Server
After=network.target
After=etcd.service
Wants=etcd.service

[Service]
Type=simple
WorkingDirectory=/run/fleet
User=fleet
Group=fleet
ExecStart=/usr/bin/fleetd

[Install]
WantedBy=multi-user.target
EOF
mkdir -p %{buildroot}/lib/tmpfiles.d
cat << EOF >> %{buildroot}/lib/tmpfiles.d/fleet.conf
d /run/fleet 0755 fleet fleet -
EOF
mkdir -p %{buildroot}/usr/share/polkit-1/rules.d/
install -p -m 0644 %{SOURCE2} %{buildroot}/usr/share/polkit-1/rules.d/

%pre
getent group fleet >/dev/null || /usr/sbin/groupadd fleet
getent passwd fleet >/dev/null || /usr/sbin/useradd -c "fleet user" -s /sbin/nologin -g fleet -d /run/fleet fleet

%post
/sbin/ldconfig
%systemd_post fleet.service

%preun
%systemd_preun fleet.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart fleet.service

%files
%defattr(-,root,root)
%{_bindir}/*
/etc/fleet/fleet.conf
/run/fleet
/lib/systemd/system/fleet.service
/lib/tmpfiles.d/fleet.conf
/usr/share/polkit-1/rules.d/fleet.rules

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.11.5-3
-	GA - Bump release of all rpms
*       Mon May 09 2016 Nick Shi <nshi@vmware.com> 0.11.5-2
-       Configure fleet and add fleet to systemd service.
*       Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 0.11.5-1
-       Updated version.
*	Mon Jul 13 2015 Danut Moraru <dmoraru@vmware.com> 0.11.1-1
-	Initial build.

