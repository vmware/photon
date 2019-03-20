Summary:	Connection pooler for PostgreSQL.
Name:		pgbouncer
Version:	1.9.0
Release:	1%{?dist}
License:	BSD
URL:		https://wiki.postgresql.org/wiki/PgBouncer
Source0:        https://pgbouncer.github.io/downloads/files/1.7.2/%{name}-%{version}.tar.gz
%define sha1 pgbouncer=284dd692437f4454e4f787832f4912d2eb219b25
Group:		Application/Databases.
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  libevent-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  pkg-config
Requires:		libevent
Requires:		openssl

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
if ! getent group %{name} >/dev/null; then
    /sbin/groupadd -r %{name}
fi
if ! getent passwd %{name} >/dev/null; then
    /sbin/useradd -g %{name} %{name}
fi

%post
if [ $1 -eq 1 ] ; then
    chown %{name}:%{name} /var/log/%{name}
    chown %{name}:%{name} /var/run/%{name}
fi

%postun
if [ $1 -eq 0 ] ; then
    if getent passwd %{name} >/dev/null; then
        /sbin/userdel %{name}
    fi
    if getent group %{name} >/dev/null; then
        /sbin/groupdel %{name}
    fi
    rm -rf /var/log/%{name}
    rm -rf /var/run/%{name}
fi

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
*       Sun Mar 10 2019 Tapas Kundu <tkundu@vmware.com> 1.9.0-1
-       Updated to 1.9.0
*	Thu	Apr 20	2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.7.2-4
-	Updated the requires + release bump for building with new libevent
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.2-3
-	GA - Bump release of all rpms
*	Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 1.7.2-2
-	Edit scriptlets.
*       Thu Apr 28 2016 Kumar Kaushik <kaushikk@vmware.com> 1.7.2-1
-       Initial Version.
