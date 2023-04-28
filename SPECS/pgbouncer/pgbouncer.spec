Summary:          Connection pooler for PostgreSQL.
Name:             pgbouncer
Version:          1.17.0
Release:          2%{?dist}
License:          BSD
URL:              https://wiki.postgresql.org/wiki/PgBouncer
Source0:          https://%{name}.github.io/downloads/files/%{version}/%{name}-%{version}.tar.gz
%define sha512    pgbouncer=5913ce542f0f694f114db8a2f339e536fb2b5887efb160b7ce3c708ae3d638bee95943104eafb9fbc4fc225649bd5625da2ccf1b56489afe33ebf8aacac48863
Source1:          pgbouncer.service
Source2:          %{name}.sysusers
Group:            Application/Databases.
Vendor:           VMware, Inc.
Distribution:     Photon
BuildRequires:    libevent-devel
BuildRequires:    openssl-devel
BuildRequires:    systemd
BuildRequires:    systemd-devel
BuildRequires:    pkg-config
Requires:         libevent
Requires:         openssl
Requires(pre):    systemd-rpm-macros
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd

%description
Pgbouncer is a light-weight, robust connection pooler for PostgreSQL.

%prep
%autosetup

%build
%configure
make %{?_smp_mflags} V=1

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -vdm 744 %{buildroot}/var/log/pgbouncer
install -vdm 755 %{buildroot}/var/run/pgbouncer
install -p -d %{buildroot}%{_sysconfdir}/
install -p -d %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/
mkdir -p %{buildroot}/etc/systemd/system/
install -m 0644 %{SOURCE1} %{buildroot}/etc/systemd/system/%{name}.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%check
pushd test
make all %{?_smp_mflags}
popd

%pre
%sysusers_create_compat %{SOURCE2}

%post
if [ $1 -eq 1 ] ; then
    chown %{name}:%{name} /var/log/%{name}
    chown %{name}:%{name} /var/run/%{name}
fi

%postun
if [ $1 -eq 0 ] ; then
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
%{_sysusersdir}/%{name}.sysusers

%changelog
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.17.0-2
- Use systemd-rpm-macros for user creation
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.17.0-1
-   Automatic Version Bump
*   Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.15.0-2
-   Bump up release for openssl
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.15.0-1
-   Automatic Version Bump
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.14.0-2
-   openssl 1.1.1
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.0-1
-   Automatic Version Bump
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.9.0-1
-   Updated to version 1.9.0
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
