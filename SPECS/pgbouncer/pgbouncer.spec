Summary:	Connection pooler for PostgreSQL.
Name:		pgbouncer
Version:	1.9.0
Release:	2%{?dist}
License:	BSD
URL:		https://wiki.postgresql.org/wiki/PgBouncer
Group:		Application/Databases.
Vendor:		VMware, Inc.
Distribution:	Photon

Source0:        https://%{name}.github.io/downloads/files/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=b127f4cb60ca5cdf339da76727918f0a3797a3e0a89f8ed6fdcaa80f3391d2c5bb51e19731915775210c0e5070dd611ee2e410c9a947624e45b5cf11aecdacf9
Source1:        pgbouncer.service

BuildRequires:  libevent-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  pkg-config

Requires:	libevent
Requires:	openssl
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

Patch0:         0001-Recognize-GSSENCRequest-packet.patch
Patch1:         pgbouncer-CVE-2021-3935.patch

%description
Pgbouncer is a light-weight, robust connection pooler for PostgreSQL.

%prep
%autosetup -p1

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

%check
pushd test
make all %{?_smp_mflags}
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
* Tue Oct 18 2022 Ankit Jain <ankitja@vmware.com> 1.9.0-2
- Fixes CVE-2021-3935
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.9.0-1
- Updated to version 1.9.0
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.7.2-7
- Remove shadow from requires and use explicit tools for post actions
* Mon Jul 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.7.2-6
- Seperate the service file from the spec file
* Wed May 31 2017 Rongrong Qiu <rqiu@vmware.com> 1.7.2-5
- Add RuntimeDirectory and Type=forking
* Thu Apr 13 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.7.2-4
- Fixed the requires.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.2-3
- GA - Bump release of all rpms
* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 1.7.2-2
- Edit scriptlets.
* Thu Apr 28 2016 Kumar Kaushik <kaushikk@vmware.com> 1.7.2-1
- Initial Version.
