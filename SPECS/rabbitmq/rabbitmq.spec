Name:          rabbitmq-server
Summary:       RabbitMQ messaging server
Version:       3.10.7
Release:       1%{?dist}
Group:         Applications
Vendor:        VMware, Inc.
Distribution:  Photon
License:       MPLv1.1
URL:           https://github.com/rabbitmq/rabbitmq-server
source0:       https://github.com/rabbitmq/rabbitmq-server/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512  rabbitmq=34b7d0cbc8dafe8d7394aa3f6002f19bceea30266dc19d00bff367ec526fa528c9a3eb4a6da5e6054454d361e7bf14adc6a88e4178dc2fa9bcd6425819cdeccb
Source1:       rabbitmq.config
Requires:      erlang >= 24
Requires:      erlang-sd_notify
Requires:      /bin/sed
Requires:      socat
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
BuildRequires: erlang
BuildRequires: python3
BuildRequires: python3-xml
BuildRequires: rsync
BuildRequires: zip
BuildRequires: git
BuildRequires: libxslt
BuildRequires: xmlto
BuildRequires: python-xml
BuildRequires: elixir
BuildArch:     noarch

%description
rabbitmq messaging server

%prep
%autosetup -p1

%build
LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
%make_build

%install
%make_install RMQ_ROOTDIR=/usr/lib/rabbitmq/

install -vdm755 %{buildroot}/var/lib/rabbitmq/
install -vdm755 %{buildroot}/%{_sysconfdir}/rabbitmq/
install -vdm755 %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/var/log
mkdir -p %{buildroot}/var/opt/rabbitmq/log
ln -sfv /var/opt/rabbitmq/log %{buildroot}/var/log/rabbitmq

cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/rabbitmq/
mkdir -p %{buildroot}/usr/lib/systemd/system
cat << EOF >>  %{buildroot}/usr/lib/systemd/system/rabbitmq-server.service
[Unit]
Description=RabbitMQ broker
After=network.target epmd@0.0.0.0.socket
Wants=network.target epmd@0.0.0.0.socket

[Service]
Type=notify
User=rabbitmq
Group=rabbitmq
NotifyAccess=all
TimeoutStartSec=3600
WorkingDirectory=/var/lib/rabbitmq
ExecStart=/usr/lib/rabbitmq/lib/rabbitmq_server-%{version}/sbin/rabbitmq-server
ExecStop=/usr/lib/rabbitmq/lib/rabbitmq_server-%{version}/sbin/rabbitmqctl stop

[Install]
WantedBy=multi-user.target
EOF

%check
make %{?_smp_mflags} tests

%pre
if ! getent group rabbitmq >/dev/null; then
  groupadd -r rabbitmq
fi

if ! getent passwd rabbitmq >/dev/null; then
  useradd -r -g rabbitmq -d %{_localstatedir}/lib/rabbitmq rabbitmq \
  -s /sbin/nologin -c "RabbitMQ messaging server"
fi

%post
chown -R rabbitmq:rabbitmq /var/lib/rabbitmq
chown -R rabbitmq:rabbitmq /etc/rabbitmq
chmod g+s /etc/rabbitmq
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %attr(0750, rabbitmq, rabbitmq) /var/opt/rabbitmq/log
%attr(0750, rabbitmq, rabbitmq) /var/log/rabbitmq
%{_libdir}/*
%{_sysconfdir}/*
/var/lib/*

%changelog
* Mon Sep 05 2022 Harinadh D <hdommaraju@vmware.com> 3.10.7-1
- Version update
* Sun Jun 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.8.9-3
- Bump version as a part of libxslt upgrade
* Thu Dec 16 2021 Nitesh Kumar <kunitesh@vmware.com> 3.8.9-2
- Bump up version to use fips enable erlang.
* Wed Nov 11 2020 Harinadh D <hdommaraju@vmware.com> 3.8.9-1
- Version update
* Mon Apr 27 2020 Tapas Kundu <tkundu@vmware.com> 3.7.20-2
- Fix rabbitmq server issue when we enable rabbitmq plugin.
* Tue Oct 29 2019 Keerthana K <keerthanak@vmware.com> 3.7.20-1
- Update to version 3.7.20
* Mon Aug 19 2019 Keerthana K <keerthanak@vmware.com> 3.7.3-1
- Update to version 3.7.3
* Thu Jan 31 2019 Siju Maliakkal <smaliakkal@vmware.com> 3.6.15-3
- Consuming erlang 19.3
* Mon Sep 24 2018 Dweep Advani <dadvani@vmware.com> 3.6.15-2
- Consuming updated erlang version of 21.0
* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 3.6.15-1
- Update to version 3.6.15
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  3.6.10-3
- Fixed the log file directory structure
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.6.10-2
- Remove shadow from requires and use explicit tools for post actions
* Wed May 31 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.6.10-1
- Updated to latest and fixed service start issue
* Wed Apr 26 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.9-2
- Fix arch
* Wed Apr 5 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.6.9-1
- Updating package to the latest
* Mon Dec 12 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.6-1
- Initial.
