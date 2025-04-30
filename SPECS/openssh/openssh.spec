%define blfs_systemd_units_ver  20140907
%define privsep_path            %{_sharedstatedir}/sshd

Summary:        Free version of the SSH connectivity tools
Name:           openssh
Version:        7.8p1
Release:        20%{?dist}
License:        BSD
URL:            https://www.openssh.com
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/%{name}-%{version}.tar.gz
%define sha512 %{name}=8e5b0c8682a9243e4e8b7c374ec989dccd1a752eb6f84e593b67141e8b23dcc8b9a7322b1f7525d18e2ce8830a767d0d9793f997486339db201a57986b910705

Source1: http://www.linuxfromscratch.org/blfs/downloads/systemd/blfs-systemd-units-%{blfs_systemd_units_ver}.tar.bz2
%define sha512 blfs-systemd-units=e8214d2f05c74ee2dc40b357097de4bd6ea068538d215419d7fab37fad22a0ca5900cb50127808480274ef4e4c7c0c7492bcc1bd907e5c1049ee2c004c6beaf9

Source2: sshd.service
Source3: sshd-keygen.service

Patch0:         blfs_systemd_fixes.patch
Patch1:         openssh-7.8p1-fips.patch
Patch2:         openssh-7.8p1-configure-fips.patch
Patch3:         openssh-CVE-2018-20685.patch
Patch4:         openssh-CVE-2019-6109.patch
Patch5:         openssh-CVE-2019-6109-progressmeter.patch
Patch6:         openssh-CVE-2019-6111.patch
Patch7:         openssh-CVE-2019-6111-filenames.patch
Patch8:         scp-name-validator-CVE-2019-6110.patch
Patch9:         openssh-CVE-2019-16905.patch
Patch10:        openssh-CVE-2020-12062.patch
Patch11:        openssh-CVE-2020-12062-another-case.patch
Patch12:        openssh-Fix-error-message-close.patch
Patch13:        openssh-expose-vasnmprintf.patch
Patch14:        openssh-fix-ssh-keyscan.patch
Patch15:        openssh-CVE-2021-41617.patch
Patch16:        openssh-CVE-2020-14145.patch
Patch17:        0001-sshd_config-Avoid-duplicate-entry.patch
Patch18:        CVE-2023-38408-1.patch
Patch19:        CVE-2023-38408-2.patch
Patch20:        CVE-2023-38408-3.patch
Patch21:        0001-Support-for-overriding-algorithms-for-ssh-keyscan.patch
Patch22:        CVE-2023-51385.patch
Patch23:        CVE-2025-26465.patch
Patch24:        CVE-2025-32728.patch

BuildRequires:  openssl-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  krb5-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  systemd
BuildRequires:  groff
BuildRequires:  systemd-devel

Requires:       openssl
Requires:       %{name}-clients = %{version}-%{release}
Requires:       %{name}-server = %{version}-%{release}

%description
The OpenSSH package contains ssh clients and the sshd daemon. This is
useful for encrypting authentication and subsequent traffic over a
network. The ssh and scp commands are secure implementions of telnet
and rcp respectively.

%package clients
Summary: openssh client applications.
Requires: e2fsprogs-libs
Requires: krb5
Requires: zlib

%description clients
This provides the ssh client utilities.

%package server
Summary: openssh server applications
Requires:   systemd
Requires:   Linux-PAM
Requires:   shadow
Requires:   ncurses-terminfo
Requires:   %{name}-clients = %{version}-%{release}
Requires(post): /bin/chown
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

%description server
This provides the ssh server daemons, utilities, configuration and service files.

%prep
# Using autosetup is not feasible
%setup -q -a0 -a1
%patch0 -p0
%autopatch -p1 -m1 -M24

%build
sh ./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir}/ssh \
    --datadir=%{_datadir}/sshd \
    --with-md5-passwords \
    --with-privsep-path=%{privsep_path} \
    --with-pam \
    --enable-strip=no \
    --with-kerberos5=%{_usr}

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm755 %{buildroot}%{privsep_path}

# Install daemon script
pushd blfs-systemd-units-%{blfs_systemd_units_ver}
make DESTDIR=%{buildroot} install-sshd %{?_smp_mflags}
popd

install -m644 %{SOURCE2} %{buildroot}%{_unitdir}/sshd.service
install -m644 %{SOURCE3} %{buildroot}%{_unitdir}/sshd-keygen.service
install -m755 contrib/ssh-copy-id %{buildroot}%{_bindir}
install -m644 contrib/ssh-copy-id.1 %{buildroot}%{_mandir}/man1/

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
getent group sshd >/dev/null || groupadd -g 50 sshd
getent passwd sshd >/dev/null || \
    useradd -c 'sshd PrivSep' -d %{privsep_path} -g sshd -s /bin/false -u 50 sshd

%preun server
%systemd_preun sshd.service sshd-keygen.service

%post server
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
  chown -v root:sys %{privsep_path}
fi
%systemd_post sshd.service sshd-keygen.service

%postun server
/sbin/ldconfig
%systemd_postun_with_restart sshd.service sshd-keygen.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)

%files server
%defattr(-,root,root)
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(700,root,sys) %{privsep_path}
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

%changelog
* Wed Apr 30 2025 Tapas Kundu <tapas.kundu@broadcom.com> 7.8p1-20
- Fix CVE-2025-32728
* Mon Feb 17 2025 Tapas Kundu <tapas.kundu@broadcom.com> 7.8p1-19
- Fix CVE-2025-26465
* Tue Dec 26 2023 Mukul Sikka <msikka@vmware.com> 7.8p1-18
- Fix for CVE-2023-51385
* Wed Aug 30 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.8p1-17
- Keyscan fips mode fix
* Tue Aug 01 2023 Shivani Agarwal <shivania2@vmware.com> 7.8p1-16
- Fix CVE-2023-38408
* Fri Mar 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.8p1-15
- Add systemd to Requires of server
* Thu Feb 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.8p1-14
- Set MaxAuthTries to 4
* Tue Apr 12 2022 Ankit Jain <ankitja@vmware.comm> 7.8p1-13
- Avoid duplicate entry in sshd_config
* Fri Apr 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.8p1-12
- Add systemd to Requires
* Wed Jan 12 2022 Dweep Advani <dadvani@vmware.comm> 7.8p1-11
- Fix for CVE-2020-14145
* Mon Oct 04 2021 Ankit Jain <ankitja@vmware.comm> 7.8p1-10
- Fix for CVE-2021-41617
* Mon Oct 05 2020 Keerthana K <keerthanak@vmware.com> 7.8p1-9
- Fix ssh-keyscan not skip RSA keys if SHA1 (ssh-rsa signature algorithm)
- is not enabled in server.
* Mon Jun 08 2020 Ankit Jain <ankitja@vmware.comm> 7.8p1-8
- Fix for CVE-2020-12062
* Wed Jan 08 2020 Prashant S Chauhan <psinghchauha@vmware.com> 7.8p1-7
- Added groff as a build requirement
* Fri Nov 29 2019 Ankit Jain <ankitja@vmware.comm> 7.8p1-6
- Fix for CVE-2019-16905
* Wed Aug 07 2019 Anish Swaminathan <anishs@vmware.com> 7.8p1-5
- Check for fips mode before setting
* Mon Jun 03 2019 Ankit Jain <ankitja@vmware.comm> 7.8p1-4
- Fix for CVE-2019-6110.
* Thu May 09 2019 Ankit Jain <ankitja@vmware.comm> 7.8p1-3
- Fix CVE-2019-6109 and CVE-2019-6111.
* Thu Feb 14 2019 Ankit Jain <ankitja@vmware.comm> 7.8p1-2
- Fix CVE-2018-20685.
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
