Name:          rabbitmq-server
Summary:       RabbitMQ messaging server
Version:       3.6.15
Release:       3%{?dist}
Group:         Applications
Vendor:        VMware, Inc.
Distribution:  Photon
License:       MPLv1.1
URL:           https://github.com/rabbitmq/rabbitmq-server
Source0:       http://www.rabbitmq.com/releases/rabbitmq-server/v%{version}/%{name}-%{version}.tar.xz
%define sha1 rabbitmq=617cfba3406804b7cdc9999b88c06086e3705904
Source1:       rabbitmq.config
Requires:      erlang >= 21.0
Requires:      /bin/sed
Requires:      socat
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
BuildRequires: erlang >= 21.0
BuildRequires: rsync
BuildRequires: zip
BuildRequires: libxslt
BuildRequires: python-xml
BuildRequires: python2
BuildArch:     noarch

%description
rabbitmq messaging server

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT \
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
make tests

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
%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %attr(0750, rabbitmq, rabbitmq) /var/opt/rabbitmq/log
%attr(0750, rabbitmq, rabbitmq) /var/log/rabbitmq
%{_libdir}/*
%{_sysconfdir}/*
/var/lib/*

%changelog
* Tue Jan 22 2019 Alexey Makhalov <amakhalov@vmware.com> 3.6.15-3
- Added BuildRequires python2.
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
