%global frr_libdir %{_libexecdir}/%{name}

Summary:        Internet Routing Protocol
Name:           frr
Version:        9.1
Release:        1%{?dist}
License:        GPLv2+
URL:            https://frrouting.org
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/FRRouting/frr/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=77b278a3ea87da9dfd7b87e4f9ae67f08ed0f24809f6dd228d2ab2e2c29e2b3191d59d50fc474e53e159ac6c79c302481b462125d0657889516f07b8e05e8562

Source1: %{name}-tmpfiles.conf
Source2: %{name}-sysusers.conf

Patch0: 0000-remove-babeld-and-ldpd.patch
Patch1: 0002-enable-openssl.patch
Patch2: 0003-disable-eigrp-crypto.patch
Patch3: 0004-fips-mode.patch

%if 0%{?with_check}
Patch4: 0005-remove-grpc-test.patch
%endif

BuildRequires: build-essential
BuildRequires: c-ares-devel
BuildRequires: python3-devel
BuildRequires: python3-sphinx
BuildRequires: systemd-devel
BuildRequires: flex
BuildRequires: json-c-devel
BuildRequires: libcap-devel
BuildRequires: ncurses-devel
BuildRequires: readline-devel
BuildRequires: texinfo
BuildRequires: libyang-devel
BuildRequires: elfutils-devel
BuildRequires: pcre2-devel
BuildRequires: openssl-devel
BuildRequires: net-snmp-devel
BuildRequires: which
BuildRequires: protobuf-devel
BuildRequires: protobuf-c-devel

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires: libcap
Requires: json-c
Requires: pcre2
Requires: libyang
Requires: elfutils
Requires: readline
Requires: systemd
Requires: texinfo
Requires: c-ares
Requires: perl-libintl
Requires: libyang
Requires: pcre2-libs
Requires: ncurses-libs
Requires: openssl
Requires: glibc
Requires: python3
Requires: protobuf
Requires: protobuf-c
Requires(pre): shadow
Requires(postun): shadow

%description
FRRouting is free software that manages TCP/IP based routing protocols. It takes
a multi-server and multi-threaded approach to resolve the current complexity
of the Internet.

FRRouting supports BGP4, OSPFv2, OSPFv3, ISIS, RIP, RIPng, PIM, NHRP, PBR, EIGRP and BFD.

FRRouting is a fork of Quagga.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

autoreconf -ivf

sh ./configure --host=%{_host} --build=%{_build} \
        --program-prefix=%{?_program_prefix} \
        --disable-dependency-tracking \
        --prefix=%{_prefix} \
        --exec-prefix=%{_exec_prefix} \
        --bindir=%{_bindir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --sharedstatedir=%{_sharedstatedir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --sbindir=%{frr_libdir} \
        --sysconfdir=%{_sysconfdir}/%{name} \
        --libdir=%{_libdir}/%{name} \
        --libexecdir=%{_libexecdir}/%{name} \
        --localstatedir=%{_localstatedir}/run/%{name} \
        --enable-multipath=64 \
        --enable-vtysh=yes \
        --disable-ospfclient \
        --disable-ospfapi \
        --enable-snmp=agentx \
        --enable-user=%{name} \
        --enable-group=%{name} \
        --enable-vty-group=frrvty \
        --enable-rtadv \
        --disable-exampledir \
        --enable-systemd=yes \
        --enable-static=no \
        --disable-ldpd \
        --disable-babeld \
        --with-moduledir=%{_libdir}/%{name}/modules \
        --with-crypto=openssl \
        --enable-fpm

%build
%make_build PYTHON=%{python3}

%install
mkdir -p %{buildroot}%{_sysconfdir}/{%{name},rc.d/init.d,sysconfig,logrotate.d,pam.d,default} \
         %{buildroot}%{_localstatedir}/log/%{name} %{buildroot}%{_infodir} \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_libdir}/%{name} \
         %{buildroot}%{_tmpfilesdir} \
         %{buildroot}%{_sysusersdir}

%make_install %{?_smp_mflags}

install -p -m 644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf
install -p -m 644 tools/etc/%{name}/daemons %{buildroot}%{_sysconfdir}/%{name}/daemons
install -p -m 644 tools/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -p -m 755 tools/frrinit.sh %{buildroot}%{frr_libdir}/%{name}
install -p -m 755 tools/frrcommon.sh %{buildroot}%{frr_libdir}/frrcommon.sh
install -p -m 755 tools/watchfrr.sh %{buildroot}%{frr_libdir}/watchfrr.sh

install -p -m 644 redhat/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -m 644 redhat/%{name}.pam %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -d -m 775 %{buildroot}/run/%{name}

# Upstream does not maintain a stable API, these headers from -devel subpackage are no longer needed
rm -rf %{buildroot}%{_libdir}/%{name}/*.so \
       %{buildroot}%{_includedir}/%{name}/ \
       %{buildroot}%{_infodir}/dir

%if 0%{?with_check}
%check
%make_build check %{?_smp_mflags}
%endif

%pre
%sysusers_create_compat %{SOURCE2}

%post
/sbin/ldconfig
%systemd_post %{name}.service

mkdir -p %{_sysconfdir}/%{name}
# Create dummy files if they don't exist so basic functions can be used.
if [ ! -e %{_sysconfdir}/%{name}/%{name}.conf ]; then
  echo "hostname `hostname`" > %{_sysconfdir}/%{name}/%{name}.conf
  chown %{name}:%{name} %{_sysconfdir}/%{name}/%{name}.conf
  chmod 640 %{_sysconfdir}/%{name}/%{name}.conf
fi

#still used by vtysh, this way no error is produced when using vtysh
if [ ! -e %{_sysconfdir}/%{name}/vtysh.conf ]; then
  touch %{_sysconfdir}/%{name}/vtysh.conf
  chmod 640 %{_sysconfdir}/%{name}/vtysh.conf
  chown %{name}:frrvty %{_sysconfdir}/%{name}/vtysh.conf
fi

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig

if [ $1 -ne 0 ]; then
  %systemd_postun_with_restart %{name}.service
fi

if [ $1 -eq 0 ]; then
  %systemd_postun %{name}.service
fi

%files
%defattr(-,root,root)
%license COPYING
%doc doc/mpls
%dir %attr(750,%{name},%{name}) %{_sysconfdir}/%{name}
%dir %attr(755,%{name},%{name}) %{_localstatedir}/log/%{name}
%dir %attr(755,%{name},%{name}) /run/%{name}
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %attr(644,%{name},%{name}) %{_sysconfdir}/%{name}/daemons
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so.*
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*
%{_unitdir}/%{name}.service
%dir %{_datadir}/yang
%{_datadir}/yang/*.yang
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%{_infodir}/*info*
%{_bindir}/*
%dir %{frr_libdir}/
%{frr_libdir}/*
%{_datadir}/man/*
%{_libdir}/%{name}/modules/*.so
%{frr_libdir}/*.py

%changelog
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.1-1
- Upgrade to v9.1
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.5.2-3
- Bump version as a part of openssl upgrade
* Tue Sep 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.5.2-2
- Remove systemd_postun from postun section
* Wed Aug 09 2023 Mukul Sikka <msikka@vmware.com> 8.5.2-1
- Update to latest version
* Mon Jul 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.4.1-6
- Add protobuf to requires
* Mon Jul 24 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 8.4.1-5
- Version bump as part of pcre2 update
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.4.1-4
- Bump version as a part of elfutils upgrade
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 8.4.1-3
- Bump version as a part of ncurses upgrade to v6.4
* Tue Apr 11 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 8.4.1-2
- Bump version as part of libyang upgrade
* Tue Jan 31 2023 Gerrit Photon <photon-checkins@vmware.com> 8.4.1-1
- Automatic Version Bump
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 8.2.2-4
- Bump up due to change in elfutils
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 8.2.2-3
- Bump release as a part of readline upgrade
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.2.2-2
- Bump version as a part of libyang upgrade
* Wed Apr 20 2022 Roye Eshed <eshedr@vmware.com> 8.2.2-1
- First Version created. Based off the frrouting Redhat spec file and modified for photon.
- [sshedi: fix the spec file]
- Reference: https://src.fedoraproject.org/rpms/frr/raw/rawhide/f/frr.spec
