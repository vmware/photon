Name:           memcached
Version:        1.6.15
Release:        2%{?dist}
Summary:        High Performance, Distributed Memory Object Cache
License:        BSD
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://www.memcached.org/
Source0:        https://www.memcached.org/files/%{name}-%{version}.tar.gz
%define sha512  %{name}=00ee15eb7932420a25f3ce973bc7fcc5ba77a514091883f8b4e58ea861073caa91c676c0020f03c768077e20c76f34bca96616be104af3fbc8e7e78303958f3d
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libevent-devel
BuildRequires:  systemd-devel
BuildRequires:  perl
Requires:       perl
Requires:       systemd
Requires:       libevent
Requires(pre):  shadow-tools

%description
%{name} is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.

%package devel
Summary: Files needed for development using %{name} protocol
Requires: %{name} = %{version}-%{release}

%description devel
Install %{name}-devel if you are developing C/C++ applications that require
access to the %{name} binary include files.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
install -Dp -m0755 scripts/%{name}-tool %{buildroot}%{_bindir}/%{name}-tool
install -Dp -m0644 scripts/%{name}-tool.1 %{buildroot}%{_mandir}/man1/%{name}-tool.1
install -Dp -m0644 scripts/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -Dp -m0644 scripts/%{name}.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

%if 0%{?with_check}
%check
make test %{?_smp_mflags}
%endif

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
       useradd -r -g %{name} -d /run/%{name} -s /sbin/nologin -c "Memcached daemon" %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README.md doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/%{name}-tool
%{_bindir}/%{name}
%{_mandir}/man1/%{name}-tool.1*
%{_mandir}/man1/%{name}.1*
%{_unitdir}/%{name}.service

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*

%changelog
* Wed Apr 12 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.6.15-2
- Bump version as a part of libevent upgrade
* Tue Jun 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.15-1
- Initial packaging for Photon OS.
