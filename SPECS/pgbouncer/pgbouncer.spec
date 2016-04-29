Summary:	Connection pooler for PostgreSQL.
Name:		pgbouncer
Version:	1.7.2
Release:	1%{?dist}
License:	BSD
URL:		https://wiki.postgresql.org/wiki/PgBouncer
Source0:        https://pgbouncer.github.io/downloads/files/1.7.2/%{name}-%{version}.tar.gz
%define sha1 pgbouncer=d9bb29da15d90713e2399af3ebf5019da5cbe2d6
Group:		Application/Databases.
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  libevent-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  pkg-config

%description
Pgbouncer is a light-weight, robust connection pooler for PostgreSQL.

%prep
%setup

%build
%configure --datadir=%{_datadir}
make %{?_smp_mflags} V=1

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm 744 %{buildroot}/var/log/pgbouncer
install -vdm 755 %{buildroot}/var/run/pgbouncer
install -p -d %{buildroot}%{_sysconfdir}/
install -p -d %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/
mkdir -p %{buildroot}/etc/systemd/system/
cat << EOF >> %{buildroot}/etc/systemd/system/%{name}.service
[Unit]
Description=Connection poller for PostgreSQL.
After=syslog.target network.target

[Service]
ExecStart=/usr/bin/pgbouncer --quiet --user pgbouncer /etc/pgbouncer.ini
ExecReload=/bin/kill -USR2 $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

%pre
/sbin/groupadd -r %{name}
/sbin/useradd -g %{name} %{name}

%post
chown %{name}:%{name} /var/log/%{name}
chown %{name}:%{name} /var/run/%{name}

%postun
/sbin/userdel pgbouncer
/sbin/groupdel pgbouncer
rm -rf /var/log/%{name}
rm -rf /var/run/%{name}

%files
%defattr(-,root,root,-)
%{_bindir}/*
/etc/systemd/system/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}.ini
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*
/usr/share/doc/pgbouncer/*
/var/log/pgbouncer
/var/run/pgbouncer

%changelog
*       Thu Apr 28 2016 Kumar Kaushik <kaushikk@vmware.com> 1.7.2-1
-       Initial Version.
