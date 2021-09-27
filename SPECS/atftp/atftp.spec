Summary:        Advanced Trivial File Transfer Protocol (ATFTP) - TFTP server
Name:           atftp
Version:        0.7.1
Release:        11%{?dist}
URL:            http://sourceforge.net/projects/atftp
License:        GPLv2+ and GPLv3+ and LGPLv2+
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://sourceforge.net/projects/atftp/files/latest/download/%{name}-%{version}.tar.gz
%define sha1 %{name}=fc9e9f821dfd2f257b4a5c32b948ed60b4e31fd1

Patch0:         atftpd-circumvent-tftp-size-restrictions.patch
Patch1:         CVE-2019-11365.patch
Patch2:         CVE-2019-11366.patch
Patch3:         CVE-2020-6097.patch
Patch4:         CVE-2021-41054.patch

BuildRequires:  systemd

Requires:       systemd
Requires:	    shadow

Provides:       tftp-server
Obsoletes:      tftp-server
Provides:       tftp
Obsoletes:      tftp

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

sed -i "s/-g -Wall -D_REENTRANT/-g -Wall -D_REENTRANT -std=gnu89/" configure.ac

%build
%configure
%make_build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != '/' ] && rm -rf %{buildroot}
%makeinstall

mkdir -p %{buildroot}/%{_var}/lib/tftpboot
mkdir -p %{buildroot}/lib/systemd/system
cat << EOF >> %{buildroot}/%{_unitdir}/atftpd.service
[Unit]
Description=The tftp server serves files using the trivial file transfer protocol.

[Service]
EnvironmentFile=/etc/sysconfig/atftpd
ExecStart=/usr/sbin/atftpd --user \$ATFTPD_USER --group \$ATFTPD_GROUP \$ATFTPD_DIRECTORY
StandardInput=socket

[Install]
Also=atftpd.socket
EOF

cat << EOF >> %{buildroot}/%{_unitdir}/atftpd.socket
[Unit]
Description=Tftp Server Socket

[Socket]
ListenDatagram=69

[Install]
WantedBy=sockets.target
EOF

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat << EOF >> %{buildroot}%{_sysconfdir}/sysconfig/atftpd
ATFTPD_USER=tftp
ATFTPD_GROUP=tftp
ATFTPD_OPTIONS=
ATFTPD_USE_INETD=false
ATFTPD_DIRECTORY=/var/lib/tftpboot
ATFTPD_BIND_ADDRESSES=
EOF

%pre
if [ $1 -eq 1 ]; then
  getent group  tftp > /dev/null || groupadd -r tftp
  getent passwd tftp > /dev/null || useradd  -c "tftp" -s /bin/false -g tftp -M -r tftp
fi

%preun
%systemd_preun atftpd.socket

%post
/sbin/ldconfig
%systemd_post atftpd.socket

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  if getent passwd tftp >/dev/null; then
    userdel tftp
  fi
  if getent group tftp >/dev/null; then
    groupdel tftp
  fi
fi
%systemd_postun_with_restart atftpd.socket

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != '/' ] && rm -rf %{buildroot}

%files
%dir %attr(0750,nobody,nobody) %{_var}/lib/tftpboot
%{_mandir}/man8/atftpd.8.gz
%{_mandir}/man8/in.tftpd.8.gz
%{_sbindir}/in.tftpd
%{_sbindir}/atftpd
%{_unitdir}/atftpd.service
%{_unitdir}/atftpd.socket
%{_sysconfdir}/sysconfig/atftpd

%files client
%{_bindir}/atftp
%{_mandir}/man1/atftp.1.gz

%changelog
* Mon Sep 27 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.7.1-11
- Fix CVE-2021-41054
* Wed Jan 20 2021 Tapas Kundu <tkundu@vmware.com> 0.7.1-10
- Fix CVE-2020-6097
* Fri Jun 26 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.7.1-9
- Fix CVE-2019-11365, CVE-2019-11366
* Wed Oct 18 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.1-8
- apply patch for large file support
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
- Change tftpd from xinetd service to systemd service.
* Thu Nov 12 2015 Kumar Kaushik <kaushikk@vmware.com> 0.7.1-1
- Initial build. First version
