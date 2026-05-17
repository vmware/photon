%global build_if %{photon_subrelease} >= 91

Summary:        Intrusion Detection System
Name:           suricata
Version:        7.0.6
Release:        7%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://suricata.io
Group:          System Environment/Security

Source0:        https://www.openinfosecfoundation.org/download/%{name}-%{version}.tar.gz

Source1: suricata.sysconfig
Source2: photon.notes
Source3: suricata-tmpfiles.conf

Source4: license.txt
%include %{SOURCE4}

# Patches from https://github.com/jasonish/suricata-rpms.git
# Irrelevant docs are getting installed, drop them
Patch0: 0001-suricata-docs.patch
# Suricata service file needs some options supplied
Patch1: 0002-suricata-service.patch
#Patches from Fedora
# The log path has an extra '/' at the end
Patch2: 0003-suricata-log-path-fixup.patch
Patch3: 0005-suricata-sysconfig.patch
Patch4: exclude-pawpatrules-from-source-yaml.patch

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
%configure \
   --enable-gccprotect \
   --enable-pie \
   --disable-gccmarch-native \
   --disable-coccinelle \
   --enable-nfqueue \
   --enable-af-packet \
   --with-libnss-includes=%{_includedir}/nss \
   --enable-jansson \
   --enable-lua \
   --enable-hiredis \
   --enable-python

%make_build

%install
%make_install bindir=%{_sbindir} %{?_smp_mflags}

mkdir -p %{buildroot}%{_sysconfdir}/%{name}/rules \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_var}/log/%{name} \
         %{buildroot}%{_sysconfdir}/logrotate.d \
         %{buildroot}%{_sysconfdir}/sysconfig \
         %{buildroot}%{_sharedstatedir}/%{name} \
         %{buildroot}%{_tmpfilesdir}

install -m 640 rules/*.rules %{buildroot}%{_sysconfdir}/%{name}/rules
install -m 600 etc/*.config %{buildroot}%{_sysconfdir}/%{name}
install -m 600 threshold.config %{buildroot}%{_sysconfdir}/%{name}
install -m 600 %{name}.yaml %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 etc/%{name}.service %{buildroot}%{_unitdir}/
install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Set up logging
install -m 644 etc/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Remove a couple things so they don't get picked up
rm -rf %{buildroot}%{_includedir} \
       %{buildroot}%{_libdir}/libhtp.a \
       %{buildroot}%{_libdir}/libhtp.so \
       %{buildroot}%{_libdir}/pkgconfig

# Setup tmpdirs
install -m 0644 %{SOURCE3} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%if 0%{?with_check}
%check
%make_build check
%endif

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
%attr(2770,root,root) %dir %{_sharedstatedir}/%{name}
%{_tmpfilesdir}/%{name}.conf
%{_datadir}/%{name}/rules

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 7.0.6-7
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.0.6-6
- Bump version as a part of python3.14 upgrade
* Mon Oct 27 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 7.0.6-5
- Bump up to build with latest jansson
* Thu Oct 09 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 7.0.6-4
- Bump to build with updated rust
* Thu Jul 24 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.0.6-3
- Cleanup licenses
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 7.0.6-2
- Release bump for SRP compliance
* Mon Jul 15 2024 Mukul Sikka <mukul.sikka@broadcom.com> 7.0.6-1
- Update to v7.0.6 to fix multiple CVEs
* Fri May 10 2024 Mukul Sikka <mukul.sikka@broadcom.com> 7.0.5-1
- Update to v7.0.5 to fix multiple CVEs
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
