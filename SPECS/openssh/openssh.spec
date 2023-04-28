%define privsep_path %{_datadir}/empty.sshd
%global sshd_services sshd.service sshd.socket sshd-keygen.service

Summary:        Free version of the SSH connectivity tools
Name:           openssh
Version:        9.1p1
Release:        8%{?dist}
License:        BSD
URL:            https://www.openssh.com
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/%{name}-%{version}.tar.gz
%define sha512 %{name}=a1f02c407f6b621b1d0817d1a0c9a6839b67e416c84f3b76c63003b119035b24c19a1564b22691d1152e1d2d55f4dc7eb1af2d2318751e431a99c4efa77edc70

# These sources are taken from:
# http://www.linuxfromscratch.org/blfs/downloads/systemd/blfs-systemd-units-<version>.tar.xz
# And are modified to Photon's needs
Source1: sshd.socket
Source2: sshd.service
Source3: sshd-keygen.service
Source4: sshdat.service
Source5: %{name}.sysusers
Patch0: 0001-sshd_config-Avoid-duplicate-entry.patch

# Add couple more syscalls to seccomp filter to support glibc-2.31
BuildRequires:  openssl-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  krb5-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  systemd-devel
BuildRequires:  groff

Requires:       %{name}-clients = %{version}-%{release}
Requires:       %{name}-server = %{version}-%{release}
Requires:       systemd
Requires:       openssl
Requires(pre):  systemd-rpm-macros

%description
The OpenSSH package contains ssh clients and the sshd daemon. This is
useful for encrypting authentication and subsequent traffic over a
network. The ssh and scp commands are secure implementions of telnet
and rcp respectively.

%package clients
Summary: openssh client applications.
Requires: zlib
Requires: krb5

%description clients
This provides the ssh client utilities.

%package server
Summary: openssh server applications
Requires:   Linux-PAM
Requires:   shadow
Requires:   ncurses-terminfo
Requires:   e2fsprogs-libs
Requires:   %{name}-clients = %{version}-%{release}
Requires(post): /usr/bin/chown
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

%description server
This provides the ssh server daemons, utilities, configuration and service files.

%prep
%autosetup -p1

%build
sh ./configure --host=%{_host} --build=%{_build} \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --program-prefix= \
    --disable-dependency-tracking \
    --prefix=%{_prefix} \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir}/ssh \
    --datadir=%{_datadir}/sshd \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --with-md5-passwords \
    --with-privsep-path=%{privsep_path} \
    --with-pam \
    --with-maintype=man \
    --enable-strip=no \
    --with-kerberos5=%{_prefix} \
    --with-sandbox=seccomp_filter

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm755 %{buildroot}%{privsep_path}

mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}/sshd.socket
install -m644 %{SOURCE2} %{buildroot}%{_unitdir}/sshd.service
install -m644 %{SOURCE3} %{buildroot}%{_unitdir}/sshd-keygen.service
install -m644 %{SOURCE4} %{buildroot}%{_unitdir}/sshd@.service
install -m755 contrib/ssh-copy-id %{buildroot}%{_bindir}/
install -m644 contrib/ssh-copy-id.1 %{buildroot}%{_mandir}/man1/
install -p -D -m 0644 %{SOURCE5} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
%check
if ! getent passwd sshd >/dev/null; then
   useradd sshd
fi
if [ ! -d %{privsep_path} ]; then
  mkdir %{privsep_path}
  chmod 0755 %{privsep_path}
fi
cp %{buildroot}%{_bindir}/scp %{_bindir}
chmod g+w . -R
useradd test -G root -m
sudo -u test -s /bin/bash -c "PATH=$PATH make tests -j$(nproc)"
%endif

%pre server
%sysusers_create_compat %{SOURCE5}

%preun server
%systemd_preun %{sshd_services}

%post server
/sbin/ldconfig
if [ $1 -eq 1 ]; then
    chown -v root:sys %{privsep_path}
fi
%systemd_post %{sshd_services}

%postun server
/sbin/ldconfig
%systemd_postun_with_restart %{sshd_services}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)

%files server
%defattr(-,root,root)
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%dir %attr(0711,root,root) %{privsep_path}
%{_unitdir}/sshd-keygen.service
%{_unitdir}/sshd.service
%{_unitdir}/sshd.socket
%{_unitdir}/sshd@.service
%{_sbindir}/sshd
%{_libexecdir}/sftp-server
%{_mandir}/man5/sshd_config.5.gz
%{_mandir}/man8/sshd.8.gz
%{_mandir}/man5/moduli.5.gz
%{_mandir}/man8/sftp-server.8.gz
%{_sysusersdir}/%{name}.sysusers

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%{_bindir}/ssh
%{_bindir}/scp
%{_bindir}/sftp
%{_bindir}/ssh-keygen
%{_bindir}/ssh-keyscan
%{_bindir}/ssh-add
%{_bindir}/ssh-agent
%{_bindir}/ssh-copy-id
%{_libexecdir}/ssh-keysign
%{_libexecdir}/ssh-pkcs11-helper
%{_libexecdir}/ssh-sk-helper
%{_mandir}/man1/scp.1.gz
%{_mandir}/man1/ssh-agent.1.gz
%{_mandir}/man1/ssh-keygen.1.gz
%{_mandir}/man1/ssh-keyscan.1.gz
%{_mandir}/man5/ssh_config.5.gz
%{_mandir}/man1/ssh-add.1.gz
%{_mandir}/man1/ssh.1.gz
%{_mandir}/man1/ssh-copy-id.1.gz
%{_mandir}/man1/sftp.1.gz
%{_mandir}/man8/ssh-keysign.8.gz
%{_mandir}/man8/ssh-pkcs11-helper.8.gz
%{_mandir}/man8/ssh-sk-helper.8.gz

%changelog
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.1p1-8
- Bump version as a part of zlib upgrade
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 9.1p1-7
- Use systemd-rpm-macros for user creation
* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.1p1-6
- Add systemd to Requires of server
- Remove blfs tarball dependency
* Thu Feb 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.1p1-5
- Set MaxAuthTries to 4
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 9.1p1-4
- Bump version as a part of krb5 upgrade
* Mon Jan 23 2023 Ankit Jain <ankitja@vmware.com> 9.1p1-3
- Replace /usr/share/empty with /usr/share/empty.sshd
* Tue Jan 17 2023 Piyush Gupta <gpiyush@vmware.com> 9.1p1-2
- Use /usr/share/empty instead of /var/empty/sshd.
- Create sshd user with uid 1050.
* Tue Nov 29 2022 Srinidhi Rao <sshedi@vmware.com> 9.1p1-1
- Update to 9.1p1
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.8p1-2
- Fix binary path
* Mon Nov 29 2021 Satya Naga Vasamsetty <svasamsetty@vmware.comm> 8.8p1-1
- Update to 8.8p1
* Mon Nov 08 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5p1-2
- Bump up for openssl
* Thu Mar 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5p1-1
- Update to 8.5p1
* Wed Oct 07 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.4p1-2
- Fix ssh issue
* Mon Oct 05 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.4p1-1
- Update to 8.4p1
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.9p1-2
- openssl 1.1.1
* Mon Aug 03 2020 Satya Naga Vasamsetty<svasamsetty@vmware.com> 7.9p1-1
- Update the version to 7.9p1
* Mon Apr 06 2020 Anish Swaminathan <anishs@vmware.com> 7.8p1-7
- Remove the MaxAuthTries restriction and default to 6
* Fri Mar 27 2020 Alexey Makhalov <amakhalov@vmware.com> 7.8p1-6
- glibc-2.31 support.
* Mon Mar 16 2020 Ankit Jain <ankitja@vmware.comm> 7.8p1-5
- Fix CVE-2019-6109, CVE-2019-6110, CVE-2019-6111, CVE-2019-16905
* Wed Aug 07 2019 Anish Swaminathan <anishs@vmware.com> 7.8p1-4
- Check for fips mode before setting
* Thu Feb 14 2019 Ankit Jain <ankitja@vmware.comm> 7.8p1-3
- Fix CVE-2018-20685.
* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 7.8p1-2
- Added BuildRequires groff
- Use %configure
* Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 7.8p1-1
- Update version
* Tue Nov 28 2017 Xiaolin Li <xiaolinl@vmware.comm> 7.5p1-11
- Fix CVE-2017-15906.
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 7.5p1-10
- Fix: openssh-server requires(pre) shadow tools
* Tue Nov 14 2017 Anish Swaminathan <anishs@vmware.com> 7.5p1-9
- Add ciphers aes128-gcm, aes256-gcm and kex dh14/16/18 in fips mode
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 7.5p1-8
- No direct toybox dependency, shadow depends on toybox
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 7.5p1-7
- Requires shadow or toybox
* Thu Sep 14 2017 Alexey Makhalov <amakhalov@vmware.com> 7.5p1-6
- sshd config: revert MaxSessions to original value
* Thu Aug 31 2017 Alexey Makhalov <amakhalov@vmware.com> 7.5p1-5
- sshd config hardening based on lynis recommendations
* Thu Aug 10 2017 Chang Lee <changlee@vmware.com> 7.5p1-4
- Fixed %check
* Mon Jul 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 7.5p1-3
- Seperate the service file from the spec file
* Wed May 3  2017 Bo Gan <ganb@vmware.com> 7.5p1-2
- Fixed openssh-server dependency on coreutils
* Tue Mar 28 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.5p1-1
- Update version
* Thu Feb 09 2017 Anish Swaminathan <anishs@vmware.com> 7.4p1-3
- Add patch to configure openssh FIPS mode
* Thu Feb 02 2017 Anish Swaminathan <anishs@vmware.com> 7.4p1-2
- Add patch to support FIPS mode
* Fri Jan 06 2017 Xiaolin Li <xiaolinl@vmware.com> 7.4p1-1
- Updated to version 7.4p1.
* Wed Dec 14 2016 Xiaolin Li <xiaolinl@vmware.com> 7.1p2-10
- BuildRequires Linux-PAM-devel
* Mon Dec 12 2016 Anish Swaminathan <anishs@vmware.com> 7.1p2-9
- Add patch to fix CVE-2016-8858
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1p2-8
- openssh-devel requires ncurses-terminfo to provide extra terms
    for the clients
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1p2-7
- Required krb5-devel.
* Thu Nov 03 2016 Sharath George <sharathg@vmware.com> 7.1p2-6
- Split openssh into client and server rpms.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 7.1p2-5
- Modified %check
* Thu Sep 15 2016 Anish Swaminathan <anishs@vmware.com> 7.1p2-4
- Add patch to fix CVE-2016-6515
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.1p2-3
- GA - Bump release of all rpms
* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 7.1p2-2
- Edit scriptlets.
* Thu Mar 17 2016 Xiaolin Li <xiaolinl@vmware.com> 7.1p2-1
- Updated to version 7.1p2
* Fri Feb 05 2016 Anish Swaminathan <anishs@vmware.com> 6.6p1-6
- Add pre install scripts in the rpm
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  6.6p1-5
- Change config file attributes.
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com> 6.6p1-4
- Add systemd to Requires and BuildRequires.
- Use systemctl to enable/disable service.
* Fri Jul 17 2015 Divya Thaluru <dthaluru@vmware.com> 6.6p1-3
- Enabling ssh-keygen service by default and fixed service file to execute only once.
* Tue May 19 2015 Sharath George <sharathg@vmware.com> 6.6p1-2
- Bulding ssh server with kerberos 5.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 6.6p1-1
- Initial build. First version
