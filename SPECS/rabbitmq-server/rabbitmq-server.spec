%define erlang_minver       26.2.5
%define erlang_maxver       27.0
%define _rabbitmq_user      rabbitmq
%define _rabbitmq_group     rabbitmq
%define _rabbit_libdir      %{_libdir}/rabbitmq
%define _rabbit_erllibdir   %{_rabbit_libdir}/lib/rabbitmq_server-%{version}
%define _plugins_state_dir  %{_sharedstatedir}/rabbitmq/plugins

# Be careful while doing major version upgrades of this package
# Refer https://www.rabbitmq.com/upgrade.html
# The above page captures upgrade compatibiltiy of rabbitmq versions
# Also better to take a look at https://www.rabbitmq.com/feature-flags.html#version-compatibility
# A word of advice here is, don't jump multiple versions in one shot; for example
# 3.8.x --> 3.11.x (not recommended)
# 3.8.x --> 3.9.x (recommended & probably okay)
# Enable all feauture flags before upgrade from 3.11.x to 3.12.4
# 3.11.0 --> 3.11.18 --> 3.12.4

Name:          rabbitmq-server
Summary:       RabbitMQ messaging server
Version:       3.13.3
Release:       3%{?dist}
Group:         Applications
Vendor:        VMware, Inc.
Distribution:  Photon
License:       MPLv1.1
URL:           https://github.com/rabbitmq/rabbitmq-server

# use only .xz bundle from release page of github
Source0: https://github.com/rabbitmq/rabbitmq-server/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 rabbitmq=3d06926e4068ef8d0a832e6d32267a6fc3d098a59583266e5c419e421cdf3c5dd60b77859778232289b80e1e3ff3e35ce9959ea53fefa269d7b1afe5f686c068

Source1: %{name}.tmpfiles
Source2: %{name}.logrotate
Source3: %{name}.service

BuildRequires: erlang >= %{erlang_minver}, erlang < %{erlang_maxver}
BuildRequires: rsync
BuildRequires: zip
BuildRequires: git
BuildRequires: libxslt-devel
BuildRequires: xmlto
BuildRequires: python3-xml
BuildRequires: python3-devel
BuildRequires: elixir
BuildRequires: systemd-rpm-macros
BuildRequires: which

Requires:      erlang >= %{erlang_minver}, erlang < %{erlang_maxver}
Requires:      erlang-sd_notify
Requires:      socat
Requires:      systemd
Requires:      /bin/sed
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd
BuildArch:     noarch

%description
rabbitmq messaging server

%prep
%autosetup -p1

%build
export LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
export PROJECT_VERSION="%{version}"

# some intermittent build failure
# retry if first run fails
%make_build || %make_build

%install
export PROJECT_VERSION="%{version}"
export RMQ_ROOTDIR=%{_rabbit_libdir}
export RMQ_ERLAPP_DIR=%{_rabbit_erllibdir}

mkdir -p %{buildroot}%{_sharedstatedir}/rabbitmq/mnesia \
         %{buildroot}%{_var}/log/rabbitmq \
         %{buildroot}%{_sysconfdir}/rabbitmq
%make_install %{?_smp_mflags}

install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service

sed -i \
    -e "s|@RMQ_USER@|%{_rabbitmq_user}|" \
    -e "s|@RMQ_GROUP@|%{_rabbitmq_group}|" \
    -e "s|@RMQ_ROOTDIR@|%{_rabbit_libdir}/lib/rabbitmq_server-%{version}|" \
    %{buildroot}%{_unitdir}/%{name}.service

install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -p -D -m 0755 scripts/rabbitmqctl-autocomplete.sh \
            %{buildroot}%{_datadir}/bash-completion/completions/rabbitmqctl-autocomplete.sh

install -p -D -m 0644 ./deps/rabbit/docs/rabbitmq.conf.example \
            %{buildroot}%{_sysconfdir}/rabbitmq/rabbitmq.conf

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%check
%make_build tests

%pre
[ -L /var/log/rabbitmq ] && rm -f /var/log/rabbitmq

# create rabbitmq group
if ! getent group %{_rabbitmq_group} > /dev/null; then
  groupadd -r %{_rabbitmq_group}
fi

# create rabbitmq user
if ! getent passwd %{_rabbitmq_user} > /dev/null; then
  useradd -r -g %{_rabbitmq_group} -d %{_sharedstatedir}/rabbitmq -s /sbin/nologin \
      %{_rabbitmq_user} -c "RabbitMQ messaging server"
fi

%post
/sbin/ldconfig
chown -R %{_rabbitmq_user}:%{_rabbitmq_group} %{_sharedstatedir}/rabbitmq
chown -R %{_rabbitmq_user}:%{_rabbitmq_group} %{_sysconfdir}/rabbitmq
chmod g+s %{_sysconfdir}/rabbitmq
chmod -R o-rwx,g-w %{_sharedstatedir}/rabbitmq/mnesia
chgrp %{_rabbitmq_group} %{_sysconfdir}/rabbitmq

%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service
# Clean out plugin activation state, both on uninstall and upgrade
rm -rf %{_plugins_state_dir} \
       %{_rabbit_erllibdir}/ebin/rabbit.{rel,script,boot}

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE*
%doc deps/rabbit/docs/set_rabbitmq_policy.sh.example
%attr(0755,%{_rabbitmq_user},%{_rabbitmq_group}) %dir %{_sharedstatedir}/rabbitmq
%attr(0750,%{_rabbitmq_user},%{_rabbitmq_group}) %dir %{_sharedstatedir}/rabbitmq/mnesia
%attr(0755,%{_rabbitmq_user},%{_rabbitmq_group}) %dir %{_var}/log/rabbitmq
%attr(2755,-,%{_rabbitmq_group}) %dir %{_sysconfdir}/rabbitmq
%config(noreplace) %{_sysconfdir}/logrotate.d/rabbitmq-server
%config(noreplace) %attr(0644,%{_rabbitmq_user},%{_rabbitmq_group}) %{_sysconfdir}/rabbitmq/rabbitmq.conf
%{_unitdir}/*
%{_tmpfilesdir}/*
%{_rabbit_libdir}/*
%{_datadir}/bash-completion/completions/rabbitmqctl-autocomplete.sh

%changelog
* Tue Apr 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 3.13.3-3
- Bump release for updating erlang
* Thu Apr 10 2025 Tapas Kundu <tapas.kundu@broadcom.com> 3.13.3-2
- Bump release for updating erlang
* Tue Jun 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.13.3-1
- Upgrade to v3.13.3
* Tue Mar 19 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.12.4-2
- Bump version as a part of rsync upgrade
* Wed Dec 20 2023 Harinadh D <hdommaraju@vmware.com> 3.12.4-1
- Upgrade to v3.12.4
* Thu Dec 07 2023 Harinadh D <hdommaraju@vmware.com> 3.11.18-1
- Upgrade to v3.11.18
- Modified spec similar to below page
- https://github.com/rabbitmq/rabbitmq-packaging/blob/main/RPMS/Fedora/rabbitmq-server.spec
- Disabled DIST_AS_EZS to add schema files in rpm deliverables
* Wed Nov 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.11.0-2
- Set project version while packaging
* Tue Nov 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.11.0-1
- Upgrade to v3.11.0
* Tue Jan 11 2022 Nitesh Kumar <kunitesh@vmware.com> 3.8.9-3
- Bump up version to use fips enable erlang.
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.8.9-2
- Bump up to compile with python 3.10
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
