%global _rabbit_libdir  %{_libdir}/rabbitmq
%global _rabbit_user    rabbitmq

# Be careful while doing major version upgrades of this package
# Refer https://www.rabbitmq.com/upgrade.html
# The above page captures upgrade compatibiltiy of rabbitmq versions
# Also better to take a look at https://www.rabbitmq.com/feature-flags.html#version-compatibility
# A word of advice here is, don't jump multiple versions in one shot; for example
# 3.8.x --> 3.11.x (not recommended)
# 3.8.x --> 3.9.x (recommended & probably okay)

Name:          rabbitmq-server
Summary:       RabbitMQ messaging server
Version:       3.11.0
Release:       1%{?dist}
Group:         Applications
Vendor:        VMware, Inc.
Distribution:  Photon
License:       MPLv1.1
URL:           https://github.com/rabbitmq/rabbitmq-server

# use only .xz bundle from release page of github
Source0: https://github.com/rabbitmq/rabbitmq-server/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 rabbitmq=2cbdeb9288dd5b18ab97ba941075e96c51c258bc6ffb49a97b7bf5dee9e8ebd033d449c94b7ce305976478d1a142c82d1aaf0a2b64a14f802ac4c21b72858e4d

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
export RMQ_ROOTDIR="%{_rabbit_libdir}"
export DIST_AS_EZS=1
%make_install %{?_smp_mflags}

install -vdm755 %{buildroot}%{_sharedstatedir}/rabbitmq
install -vdm755 %{buildroot}%{_sysconfdir}/rabbitmq

mkdir -p %{buildroot}%{_var}/log \
         %{buildroot}%{_var}/opt/rabbitmq/log \
         %{buildroot}%{_unitdir}

ln -sfv %{_var}/opt/rabbitmq/log %{buildroot}%{_var}/log/rabbitmq

cat << EOF >> %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=RabbitMQ broker
After=network.target epmd@0.0.0.0.socket
Wants=network.target epmd@0.0.0.0.socket

[Service]
Type=notify
User=%{_rabbit_user}
Group=%{_rabbit_user}
NotifyAccess=all
TimeoutStartSec=3600
WorkingDirectory=%{_sharedstatedir}/rabbitmq
ExecStart=%{_rabbit_libdir}/lib/rabbitmq_server-%{version}/sbin/%{name}
ExecStop=%{_rabbit_libdir}/lib/rabbitmq_server-%{version}/sbin/rabbitmqctl stop

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
if ! getent group %{_rabbit_user} >/dev/null; then
  groupadd -r %{_rabbit_user}
fi

if ! getent passwd %{_rabbit_user} >/dev/null; then
  useradd -r -g %{_rabbit_user} -d %{_sharedstatedir}/rabbitmq %{_rabbit_user} \
      -s /sbin/nologin -c "RabbitMQ messaging server"
fi

%post
/sbin/ldconfig
chown -R %{_rabbit_user}:%{_rabbit_user} %{_sharedstatedir}/rabbitmq
chown -R %{_rabbit_user}:%{_rabbit_user} %{_sysconfdir}/rabbitmq
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
%dir %attr(0750, %{_rabbit_user}, %{_rabbit_user}) %{_var}/opt/rabbitmq/log
%{_var}/log/rabbitmq
%{_rabbit_libdir}/*
%{_unitdir}/*
%{_tmpfilesdir}/%{name}.conf
%{_sharedstatedir}/*
%config(noreplace) %attr(0644, %{_rabbit_user}, %{_rabbit_user}) %{_sysconfdir}/rabbitmq/rabbitmq.conf

%changelog
* Sat Apr 01 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.11.0-1
- Upgrade to v3.11.0
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
