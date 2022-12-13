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
Version:       3.10.12
Release:       1%{?dist}
Group:         Applications
Vendor:        VMware, Inc.
Distribution:  Photon
License:       MPLv1.1
URL:           https://github.com/rabbitmq/rabbitmq-server

# use only .xz bundle from release page of github
Source0: https://github.com/rabbitmq/rabbitmq-server/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 rabbitmq=792026780c9cc9a53c7815b43e5a53d204dea2bbac27fe0414a609f330c3f6ea6596096bb7ca185022f16918de526009543581d0756e948d5f2caaadfe8d8f3c

Source1: %{name}.tmpfiles

Requires:      erlang
Requires:      erlang-sd_notify
Requires:      socat
Requires:      systemd
Requires:      /bin/sed
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

BuildRequires: erlang
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

BuildArch:     noarch

%description
rabbitmq messaging server

%prep
%autosetup -p1

%build
export LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
export PROJECT_VERSION="%{version}"
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

%clean
rm -rf %{buildroot}

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
* Tue Dec 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.10.12-1
- Introduce v3.10.x to make migration from v3.8.x to v3.11.x possible
