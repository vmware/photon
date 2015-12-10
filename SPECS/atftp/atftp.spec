Summary:        Advanced Trivial File Transfer Protocol (ATFTP) - TFTP server
Name:           atftp
Version:        0.7.1
Release:        3%{?dist}
URL:            http://sourceforge.net/projects/atftp
License:        GPLv2+ and GPLv3+ and LGPLv2+
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://sourceforge.net/projects/atftp/files/latest/download/%{name}-%{version}.tar.gz

%define sha1 atftp=fc9e9f821dfd2f257b4a5c32b948ed60b4e31fd1

BuildRequires:  systemd
Requires:       systemd
Provides: tftp-server
Obsoletes: tftp-server

%description
Multithreaded TFTP server implementing all options (option extension and
multicast) as specified in RFC1350, RFC2090, RFC2347, RFC2348 and RFC2349.
Atftpd also support multicast protocol knowed as mtftp, defined in the PXE
specification. The server supports being started from inetd(8) as well as
a deamon using init scripts.

%package client
Summary: Advanced Trivial File Transfer Protocol (ATFTP) - TFTP client
Group: Applications/Internet
Provides: tftp
Obsoletes: tftp

%description client
Advanced Trivial File Transfer Protocol client program for requesting
files using the TFTP protocol.


%prep
%setup

%build
%configure
make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != '/' ] && rm -rf $RPM_BUILD_ROOT
%makeinstall

mkdir -p %{buildroot}/%{_var}/lib/tftpboot
mkdir -p %{buildroot}/lib/systemd/system
cat << EOF >> %{buildroot}/lib/systemd/system/atftpd.service
[Unit]
Description=The tftp server serves files using the trivial file transfer protocol. 

[Service]
EnvironmentFile=/etc/sysconfig/atftpd
ExecStart=/usr/sbin/atftpd --user \$ATFTPD_USER --group \$ATFTPD_GROUP \$ATFTPD_DIRECTORY
StandardInput=socket

[Install]
Also=atftpd.socket
EOF

cat << EOF >> %{buildroot}/lib/systemd/system/atftpd.socket
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
getent group tftp 2>/dev/null >/dev/null || /usr/sbin/groupadd -r tftp
/usr/sbin/useradd --comment "tftp" --shell /bin/bash -M -r --groups tftp tftp

%preun
/bin/systemctl disable atftpd.socket

%post
/bin/systemctl enable atftpd.socket

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != '/' ] && rm -rf $RPM_BUILD_ROOT

%files
%dir %attr(0750,nobody,nobody) %{_var}/lib/tftpboot
%{_mandir}/man8/atftpd.8.gz
%{_sbindir}/atftpd
%{_mandir}/man8/in.tftpd.8.gz
%{_sbindir}/in.tftpd
/lib/systemd/system/atftpd.service
/lib/systemd/system/atftpd.socket
%{_sysconfdir}/sysconfig/atftpd



%files client
%{_mandir}/man1/atftp.1.gz
%{_bindir}/atftp


%changelog
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  0.7.1-3
-   Add systemd to Requires and BuildRequires.
-   Use systemctl to enable/disable service.
*	Mon Nov 23 2015 Xiaolin Li <xiaolinl@vmware.com> 0.7.1-2
-	Chang tftpd from xinetd service to systemd service.
*       Thu Nov 12 2015 Kumar Kaushik <kaushikk@vmware.com> 0.7.1-1
-       Initial build.  First version

