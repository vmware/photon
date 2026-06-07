%global build_if %{photon_subrelease} >= 91

Summary:       advanced key-value store (Redis-compatible)
Name:          valkey
Version:       9.0.3
Release:       3%{?dist}
URL:           https://valkey.io
Group:         Applications/Databases
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://github.com/valkey-io/valkey/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}

Source3: %{name}.service

Patch0: %{name}-conf.patch

BuildRequires: gcc
BuildRequires: make
BuildRequires: systemd-devel
BuildRequires: systemd-rpm-macros
BuildRequires: tcl-devel
BuildRequires: which

Requires: systemd
Requires: openssl-libs
Requires(pre): systemd-rpm-macros
Requires(pre): shadow-tools
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

Provides: redis
Obsoletes: redis

%description
Valkey is an open-source, Redis-compatible in-memory data structure store used as database, cache and message broker.

%prep
%autosetup -p1

%build
%make_build BUILD_TLS=yes BUILD_WITH_SYSTEMD=yes BUILD_RDMA=no

%install
%make_install PREFIX=%{buildroot}%{_prefix}
install -D -m 0640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

mkdir -p %{buildroot}%{_sharedstatedir}/%{name} \
          %{buildroot}%{_var}/log/%{name} \
          %{buildroot}%{_unitdir}

install -p -D -m 0640 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%pre
%sysusers_create_compat %{SOURCE1}

%post
/sbin/ldconfig
%systemd_post %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%dir %attr(0750, %{name}, root) %{_sharedstatedir}/%{name}
%dir %attr(0750, %{name}, root) %{_var}/log/%{name}
%{_bindir}/valkey-server
%{_bindir}/valkey-cli
%{_bindir}/valkey-benchmark
%{_bindir}/valkey-check-rdb
%{_bindir}/valkey-check-aof
%{_bindir}/valkey-sentinel
%{_bindir}/redis-server
%{_bindir}/redis-cli
%{_bindir}/redis-benchmark
%{_bindir}/redis-check-rdb
%{_bindir}/redis-check-aof
%{_bindir}/redis-sentinel
%{_unitdir}/%{name}.service
%config(noreplace) %attr(0640, %{name}, root) %{_sysconfdir}/%{name}/%{name}.conf
%{_sysusersdir}/%{name}.conf

%changelog
* Fri Jun 05 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 9.0.3-3
- Enable Obsoletes
* Tue May 12 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 9.0.3-2
- Move to subrelease >=91
* Thu Mar 05 2026 Packager <packager@broadcom.com> 9.0.3-1
- Initial Valkey package (Redis-compatible)
