Name:          rabbitmq-server
Summary:       RabbitMQ messaging server
Version:       3.10.7
Release:       5%{?dist}
Group:         Applications
Vendor:        VMware, Inc.
Distribution:  Photon
License:       MPLv1.1
URL:           https://github.com/rabbitmq/rabbitmq-server

# use only .xz bundle from release page of github
Source0: https://github.com/rabbitmq/rabbitmq-server/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 rabbitmq=34b7d0cbc8dafe8d7394aa3f6002f19bceea30266dc19d00bff367ec526fa528c9a3eb4a6da5e6054454d361e7bf14adc6a88e4178dc2fa9bcd6425819cdeccb

Source1: %{name}.tmpfiles

BuildRequires: erlang
BuildRequires: python3-devel
BuildRequires: python3-xml
BuildRequires: rsync
BuildRequires: zip
BuildRequires: git
BuildRequires: libxslt-devel
BuildRequires: xmlto
BuildRequires: elixir
BuildRequires: systemd-devel
BuildRequires: which

Requires:      erlang >= 24
Requires:      erlang-sd_notify
Requires:      /bin/sed
Requires:      socat
Requires:      systemd
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

BuildArch:     noarch

%description
rabbitmq messaging server

%prep
%autosetup -p1

%build
export LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
export PROJECT_VERSION="%{version}"
# https://github.com/rabbitmq/rabbitmq-server/discussions/5246
export DIST_AS_EZS=1
%make_build

%install
export PROJECT_VERSION="%{version}"
export RMQ_ROOTDIR="%{_libdir}/rabbitmq"
export DIST_AS_EZS=1
%make_install %{?_smp_mflags}

install -vdm755 %{buildroot}%{_sharedstatedir}/rabbitmq
install -vdm755 %{buildroot}%{_sysconfdir}/rabbitmq
install -vdm755 %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_var}/log \
         %{buildroot}%{_var}/opt/rabbitmq/log

ln -sfv %{_var}/opt/rabbitmq/log %{buildroot}%{_var}/log/rabbitmq

cat << EOF >> %{buildroot}%{_unitdir}/%{name}.service
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
WorkingDirectory=%{_sharedstatedir}/rabbitmq
ExecStart=%{_libdir}/rabbitmq/lib/rabbitmq_server-%{version}/sbin/%{name}
ExecStop=%{_libdir}/rabbitmq/lib/rabbitmq_server-%{version}/sbin/rabbitmqctl stop

[Install]
WantedBy=multi-user.target
EOF

install -p -D -m 0644 ./deps/rabbit/docs/rabbitmq.conf.example \
            %{buildroot}%{_sysconfdir}/rabbitmq/rabbitmq.conf

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%if 0%{?with_check}
%check
make %{?_smp_mflags} tests
%endif

%pre
if ! getent group rabbitmq >/dev/null; then
  groupadd -r rabbitmq
fi

if ! getent passwd rabbitmq >/dev/null; then
  useradd -r -g rabbitmq -d %{_sharedstatedir}/rabbitmq rabbitmq \
      -s /sbin/nologin -c "RabbitMQ messaging server"
fi

%post
/sbin/ldconfig
chown -R rabbitmq:rabbitmq %{_sharedstatedir}/rabbitmq
chown -R rabbitmq:rabbitmq %{_sysconfdir}/rabbitmq
chmod g+s %{_sysconfdir}/rabbitmq
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %attr(0750, rabbitmq, rabbitmq) %{_var}/opt/rabbitmq/log
%{_var}/log/rabbitmq
%{_libdir}/*
%{_unitdir}/*.service
%{_tmpfilesdir}/%{name}.conf
%{_sharedstatedir}/*
%config(noreplace) %attr(0644, rabbitmq, rabbitmq) %{_sysconfdir}/rabbitmq/rabbitmq.conf

%changelog
* Mon Nov 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.10.7-5
- Spec improvements & create conf file properly
* Tue Nov 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.10.7-4
- Fix build failure
- Spec improvements
* Fri Oct 14 2022 Ankit Jain <ankitja@vmware.com> 3.10.7-3
- Release Bump up to build with erlang-25.1-2
* Tue Oct 04 2022 Harinadh D <hdommaraju@vmware.com> 3.10.7-2
- Version bump to compile with new erlnag version
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
