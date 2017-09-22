Summary:	Connection pooler for PostgreSQL.
Name:		pgbouncer
Version:	1.7.2
Release:	7%{?dist}
License:	BSD
URL:		https://wiki.postgresql.org/wiki/PgBouncer
Source0:        https://pgbouncer.github.io/downloads/files/1.7.2/%{name}-%{version}.tar.gz
%define sha1 pgbouncer=d9bb29da15d90713e2399af3ebf5019da5cbe2d6
Source1:        pgbouncer.service
Group:		Application/Databases.
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  libevent-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  pkg-config
Requires:		libevent
Requires:		openssl
Requires(pre):  /sbin/useradd /sbin/groupadd
Requires(postun):/sbin/userdel /sbin/groupdel
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
install -m 0644 %{SOURCE1} %{buildroot}/etc/systemd/system/%{name}.service

%check
pushd test
make all
popd

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

%changelog
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.7.2-7
-   Remove shadow from requires and use explicit tools for post actions
*   Mon Jul 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.7.2-6
-   Seperate the service file from the spec file
*   Wed May 31 2017 Rongrong Qiu <rqiu@vmware.com> 1.7.2-5
-   Add RuntimeDirectory and Type=forking
*   Thu Apr 13 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.7.2-4
-   Fixed the requires.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.2-3
-   GA - Bump release of all rpms
*   Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 1.7.2-2
-   Edit scriptlets.
*   Thu Apr 28 2016 Kumar Kaushik <kaushikk@vmware.com> 1.7.2-1
-   Initial Version.
