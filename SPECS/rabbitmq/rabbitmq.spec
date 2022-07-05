Name:          rabbitmq-server
Summary:       RabbitMQ messaging server
Version:       3.9.15
Release:       2%{?dist}
Group:         Applications
Vendor:        VMware, Inc.
Distribution:  Photon
License:       MPLv1.1
URL:           https://github.com/rabbitmq/rabbitmq-server
source0:       https://github.com/rabbitmq/rabbitmq-server/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 rabbitmq=614e0f39efb12e7098342cc0d4a69aa94cc62a71f19506aa14f00f6db66ad332e3e36bb46d9ac67880f3fa9a7c2b423a382f87b43ab052f12bfc022803e977f8
Source1:       rabbitmq.config
Requires:      erlang
Requires:      erlang-sd_notify
Requires:      /bin/sed
Requires:      socat
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd
BuildRequires: erlang
BuildRequires: rsync
BuildRequires: zip
BuildRequires: git
BuildRequires: libxslt
BuildRequires: xmlto
BuildRequires: python3-xml
BuildRequires: python3
BuildRequires: elixir
BuildArch:     noarch

%description
rabbitmq messaging server

%prep
%autosetup

%build
LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot} \
                     PREFIX=%{_prefix} \
                     RMQ_ROOTDIR=/usr/lib/rabbitmq/

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
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.9.15-2
- Bump version as a part of libxslt upgrade
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 3.9.15-1
- Automatic Version Bump
* Tue Jan 11 2022 Nitesh Kumar <kunitesh@vmware.com> 3.8.14-2
- Bump up version to use fips enable erlang.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.8.14-1
- Automatic Version Bump
* Thu Sep 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.9-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.8-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.7-1
- Automatic Version Bump
* Wed Jul 29 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.6-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 3.7.20-3
- Build with python3
- Mass removal python2
* Mon Apr 27 2020 Tapas Kundu <tkundu@vmware.com> 3.7.20-2
- Fix rabbitmq server issue when we enable rabbitmq plugin.
* Tue Oct 29 2019 Keerthana K <keerthanak@vmware.com> 3.7.20-1
- Update to version 3.7.20
* Mon Aug 19 2019 Keerthana K <keerthanak@vmware.com> 3.7.3-1
- Update to version 3.7.3
* Tue Feb 05 2019 Alexey Makhalov <amakhalov@vmware.com> 3.6.15-4
- Added BuildRequires python2.
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
