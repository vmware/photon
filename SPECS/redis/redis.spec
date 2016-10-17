Summary:	advanced key-value store
Name:		redis
Version:	3.2.4
Release:	1%{?dist}
License:	BSD
URL:		http://redis.io/
Group:		Applications/Databases
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://download.redis.io/releases/%{name}-%{version}.tar.gz
%define sha1 redis=f0fe685cbfdb8c2d8c74613ad8a5a5f33fba40c9
BuildRequires:  gcc
BuildRequires:  make

%description
Redis is an in-memory data structure store, used as database, cache and message broker.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}
make PREFIX=%{buildroot}/usr install
install -D -m 0640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -D -m 0755 utils/redis_init_script %{buildroot}%{_sysconfdir}/init.d/%{name}

%check
#check requires tcl which is not supported in Photon OS right now.

%preun
%stop_on_removal %{name}

%postun
%restart_on_update
%insserv_cleanup

%files
%defattr(-,root,root)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/init.d/redis
%config(noreplace) %attr(0640, %{name}, %{name}) %{_sysconfdir}/%{name}/redis.conf

%changelog
*	Mon Oct 3 2016 Dheeraj Shetty <dheerajs@vmware.com> 3.2.4-1
-	initial version
