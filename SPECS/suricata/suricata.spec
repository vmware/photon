Summary:        Intrusion Detection System
Name:           suricata
Version:        7.0.4
Release:        1%{?dist}
License:        GPLv2
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://suricata.io
Group:          System Environment/Security
Source0:        https://www.openinfosecfoundation.org/download/%{name}-%{version}.tar.gz
%define sha512 %{name}=098364a5f0b2c14bf3a0c8895ec9c94a23edd990468f618fa35181c54405be6db012a6e97981e0024140864342764df97101be73308c835d6fabf6cd98a7ffc3

Source1: suricata.sysconfig
Source2: photon.notes
Source3: suricata-tmpfiles.conf

# Patches from https://github.com/jasonish/suricata-rpms.git
# Irrelevant docs are getting installed, drop them
Patch1: 0001-suricata-docs.patch
# Suricata service file needs some options supplied
Patch2: 0002-suricata-service.patch
#Patches from Fedora
# The log path has an extra '/' at the end
Patch3: 0003-suricata-log-path-fixup.patch
Patch4: 0005-suricata-sysconfig.patch

BuildRequires: build-essential
BuildRequires: libmnl-devel
BuildRequires: rust
BuildRequires: libyaml-devel
BuildRequires: libnfnetlink-devel
BuildRequires: libnetfilter_queue-devel
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: libcap-ng-devel
BuildRequires: lz4-devel
BuildRequires: libpcap-devel
BuildRequires: nss-devel
BuildRequires: file-devel
BuildRequires: jansson-devel
BuildRequires: python3-devel
BuildRequires: lua-devel
%ifarch x86_64
BuildRequires: hyperscan-devel
%endif
BuildRequires: systemd-devel
BuildRequires: hiredis-devel
BuildRequires: libevent-devel

Requires: python3-PyYAML
Requires: python3
Requires: libcap-ng
Requires: libevent
Requires: hiredis
%ifarch x86_64
Requires: hyperscan
%endif
Requires: jansson
Requires: lua
Requires: zlib
Requires: lz4
Requires: libmnl
Requires: libnfnetlink
Requires: libnetfilter_queue
Requires: glibc
Requires: file-libs
Requires: nspr
Requires: nss-libs
Requires: nss
Requires: libpcap
Requires: systemd
Requires: pcre-libs
Requires: libyaml

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The Suricata Engine is an open-source system designed for detecting
and preventing intrusion in computer networks.

%prep
%autosetup -p1
install -m 644 %{SOURCE2} doc/

%build

%configure --enable-gccprotect \
        --enable-pie \
        --disable-gccmarch-native \
        --disable-coccinelle \
        --enable-nfqueue \
        --enable-af-packet \
        --with-libnss-includes=/usr/include/nss \
        --enable-jansson \
        --enable-lua \
        --enable-hiredis \
        --enable-python

%make_build

%install
%make_install DESTDIR="%{buildroot}" "bindir=%{_sbindir}"  %{?_smp_mflags}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/rules
install -m 640 rules/*.rules %{buildroot}%{_sysconfdir}/%{name}/rules
install -m 600 etc/*.config %{buildroot}%{_sysconfdir}/%{name}
install -m 600 threshold.config %{buildroot}%{_sysconfdir}/%{name}
install -m 600 %{name}.yaml %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 etc/%{name}.service %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Set up logging
mkdir -p %{buildroot}%{_var}/log/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 etc/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Remove a couple things so they don't get picked up
rm -rf %{buildroot}%{_includedir} \
       %{buildroot}%{_libdir}/libhtp.a \
       %{buildroot}%{_libdir}/libhtp.so \
       %{buildroot}%{_libdir}/pkgconfig

# Setup suricata-update data directory
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

# Setup tmpdirs
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE3} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%doc doc/photon.notes
%attr(644,root,root) %{_mandir}/man1/*
%{_sbindir}/%{name}
%{_sbindir}/suricatasc
%{_sbindir}/suricatactl
%{_sbindir}/suricata-update
%{_libdir}/libhtp*
%{_libdir}/%{name}/python/%{name}/*
%{_libdir}/%{name}/python/suricatasc
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/%{name}/%{name}.yaml
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/%{name}/*.config
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/%{name}/rules/*.rules
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/%{name}
%attr(644,root,root) %{_unitdir}/%{name}.service
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%attr(750,root,root) %dir %{_var}/log/%{name}
%attr(750,root,root) %dir %{_sysconfdir}/%{name}
%attr(750,root,root) %dir %{_sysconfdir}/%{name}/rules
%attr(2770,root,root) %dir %{_var}/lib/%{name}
%{_tmpfilesdir}/%{name}.conf
%{_datadir}/%{name}/rules

%changelog
* Fri Apr 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 7.0.4-1
- Update to v7.0.4 to fix CVE-2024-28870
* Fri Sep 08 2023 Mukul Sikka <msikka@vmware.com> 7.0.0-1
- Update to v7.0.0 to fix multiple CVEs
* Thu Aug 03 2023 Piyush Gupta <gpiyush@vmware.com> 6.0.12-3
- Bump version as a part of rust upgrade.
* Tue Jun 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.0.12-2
- Bump version as a part of lua upgrade
* Fri Apr 28 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.0.12-1
- Initial packaging
