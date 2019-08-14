Summary:	advanced key-value store
Name:		redis
Version:	4.0.14
Release:	1%{?dist}
License:	BSD
URL:		http://redis.io/
Group:		Applications/Databases
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://download.redis.io/releases/%{name}-%{version}.tar.gz
%define sha1 redis=21a4e37d532ff2469943864096db36fd1b8f43bb
Patch0:         redis-conf.patch
BuildRequires:  gcc
BuildRequires:  systemd
BuildRequires:  make
Requires:	systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
Redis is an in-memory data structure store, used as database, cache and message broker.

%prep
%setup -q
%patch0 -p1

%build
make %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}
make PREFIX=%{buildroot}/usr install
install -D -m 0640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
mkdir -p %{buildroot}/var/lib/redis
mkdir -p %{buildroot}/var/log/redis
mkdir -p %{buildroot}/usr/lib/systemd/system
cat << EOF >>  %{buildroot}/usr/lib/systemd/system/redis.service
[Unit]
Description=Redis in-memory key-value database
After=network.target

[Service]
ExecStart=/usr/bin/redis-server /etc/redis.conf --daemonize no
ExecStop=/usr/bin/redis-cli shutdown
User=redis
Group=redis

[Install]
WantedBy=multi-user.target
EOF

%check
#check requires tcl which is not supported in Photon OS right now.


%pre
getent group %{name} &> /dev/null || \
groupadd -r %{name} &> /dev/null
getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c 'Redis Database Server' %{name} &> /dev/null
exit 0

%post
/sbin/ldconfig
%systemd_post  redis.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart redis.service


%files
%defattr(-,root,root)
%dir %attr(0750, redis, redis) /var/lib/redis
%dir %attr(0750, redis, redis) /var/log/redis
%{_bindir}/*
%{_libdir}/systemd/*
%config(noreplace) %attr(0640, %{name}, %{name}) %{_sysconfdir}/redis.conf

%changelog
* Wed Aug 14 2019 Kuladeep Rayalla <krayalla@vmware.com> 4.0.14-1
- Upgrade redis to 4.0.14 to fix CVE-2019-10193
- Deleting the path for CVE-2019-10192, redis-4.0.14 includes the fix
* Thu Jul 25 2019 Kuladeep Rayalla <krayalla@vmware.com> 4.0.10-2
- Add patch for CVE-2019-10192
* Fri Jun 29 2018 Ajay Kaher <akaher@vmware.com> 4.0.10-1
- Upgrading to 4.0.10
* Thu Jan 11 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.0.6-1
- Initial build for photon
