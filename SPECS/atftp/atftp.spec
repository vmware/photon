Summary:          Advanced Trivial File Transfer Protocol (ATFTP) - TFTP server
Name:             atftp
Version:          0.8.0
Release:          6%{?dist}
URL:              http://sourceforge.net/projects/atftp
License:          GPLv2+ and GPLv3+ and LGPLv2+
Group:            System Environment/Daemons
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: http://sourceforge.net/projects/%{name}/files/latest/download/%{name}-%{version}.tar.gz
%define sha512 %{name}=b700b3e4182970fb494ffabd49e39d3622b1aff5f69882549eff0b52a01c8c47babe51b451c4829f9b833ea2ea7c590a2f3819f8e3508176fa7d1b5c0e152b68

Source1: %{name}.sysusers
Source2: atftpd.socket
Source3: atftpd.service

BuildRequires:    systemd-devel
BuildRequires:    readline-devel
BuildRequires:    pcre2-devel

Requires:         systemd
Requires:         pcre2-libs
Requires(pre):    systemd-rpm-macros

Provides:         tftp-server
Provides:         tftp

%description
Multithreaded TFTP server implementing all options (option extension and
multicast) as specified in RFC1350, RFC2090, RFC2347, RFC2348 and RFC2349.
Atftpd also support multicast protocol knowed as mtftp, defined in the PXE
specification. The server supports being started from inetd(8) as well as
a deamon using init scripts.

%package client
Summary:    Advanced Trivial File Transfer Protocol (ATFTP) - TFTP client
Group:      Applications/Internet

%description client
Advanced Trivial File Transfer Protocol client program for requesting
files using the TFTP protocol.

%prep
%autosetup -p1

%build
sh ./autogen.sh
%configure
%make_build

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}%{_sharedstatedir}/tftpboot \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_sysconfdir}/sysconfig \
         %{buildroot}%{_sysusersdir}

install -p -m 644 %{SOURCE1} %{buildroot}%{_sysusersdir}/
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/

sed -i -e "s|@SBINDIR@|%{_sbindir}|" -e "s|@SYSCONFDIR@|%{_sysconfdir}|" %{SOURCE3}
install -p -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/

cat << EOF >> %{buildroot}%{_sysconfdir}/sysconfig/atftpd
ATFTPD_USER=tftp
ATFTPD_GROUP=tftp
ATFTPD_OPTIONS=
ATFTPD_USE_INETD=false
ATFTPD_DIRECTORY=%{_sharedstatedir}/tftpboot
ATFTPD_BIND_ADDRESSES=
EOF

%check
%make_build check

%pre
if [ $1 -eq 1 ] ; then
  %sysusers_create_compat %{SOURCE1}
fi

%preun
%systemd_preun atftpd.socket

%post
/sbin/ldconfig
%systemd_post atftpd.socket

%postun
/sbin/ldconfig
%systemd_postun_with_restart atftpd.socket

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %attr(0750,nobody,nobody) %{_sharedstatedir}/tftpboot
%{_mandir}/man8/atftpd.8.gz
%{_mandir}/man8/in.tftpd.8.gz
%{_sbindir}/atftpd
%{_sbindir}/in.tftpd
%{_unitdir}/atftpd.service
%{_unitdir}/atftpd.socket
%{_sysconfdir}/sysconfig/atftpd
%{_sysusersdir}/%{name}.sysusers

%files client
%defattr(-,root,root)
%{_mandir}/man1/atftp.1.gz
%{_bindir}/atftp

%changelog
* Fri Jan 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.8.0-6
- Fix service file, start socket unit automatically
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 0.8.0-5
- Resolving systemd-rpm-macros for group creation
* Mon Jul 24 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.8.0-4
- Version bump as part of pcre2 update
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 0.8.0-3
- Use systemd-rpm-macros for user creation
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.8.0-2
- Bump version as a part of readline upgrade
* Thu Dec 15 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.8.0-1
- Upgrade to v0.8.0
* Mon Sep 27 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.7.5-1
- Upgrade to v0.7.5, fixes CVE-2021-41054
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 0.7.4-1
- Automatic Version Bump
* Wed Jan 20 2021 Tapas Kundu <tkundu@vmware.com> 0.7.2-2
- Fix CVE-2020-6097
* Tue Jun 25 2019 Tapas Kundu <tkundu@vmware.com> 0.7.2-1
- Updated to release 0.7.2
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-8
- Remove shadow from requires and use explicit tools for post actions
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  0.7.1-7
- Fixed logic to restart the active services after upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.1-6
- GA - Bump release of all rpms
* Fri May 6 2016 Divya Thaluru <dthaluru@vmware.com>  0.7.1-5
- Adding post-install run time dependencies
* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  0.7.1-4
- Fixing spec file to handle rpm upgrade scenario correctly
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  0.7.1-3
- Add systemd to Requires and BuildRequires.
- Use systemctl to enable/disable service.
* Mon Nov 23 2015 Xiaolin Li <xiaolinl@vmware.com> 0.7.1-2
- Chang tftpd from xinetd service to systemd service.
* Thu Nov 12 2015 Kumar Kaushik <kaushikk@vmware.com> 0.7.1-1
- Initial build.  First version
