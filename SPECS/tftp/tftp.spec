Summary:	The client for the Trivial File Transfer Protocol (TFTP)
Name:		tftp
Version:	5.2
Release:	1%{?dist}
License:	BSD
URL:		http://www.kernel.org
Group:		Applications/Internet
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://www.kernel.org/pub/software/network/tftp/tftp-hpa-%{version}.tar.gz
%define sha1 tftp=2fe37983ffeaf4063ffaba514c4848635c622d8b
Source1:        tftpd-hpa.service
Source2:        tftpd-hpa.socket

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations.  The tftp package provides the user
interface for TFTP, which allows users to transfer files to and from a
remote machine.  This program and TFTP provide very little security,
and should not be enabled unless it is expressly needed.

%package server
Group: System Environment/Daemons
Summary: The server for the Trivial File Transfer Protocol (TFTP).
Requires: xinetd

%description server
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations.  The tftp-server package provides the
server for TFTP, which allows users to transfer files to and from a
remote machine. TFTP provides very little security, and should not be
enabled unless it is expressly needed.
%prep
%setup -q -n tftp-hpa-%{version}

%build

%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}}%{_bindir}
mkdir -p %{buildroot}}%{_mandir}/man{1,8}
mkdir -p %{buildroot}}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/xinetd.d

%makeinstall
make INSTALLROOT=%{buildroot} \
    SBINDIR=%{_sbindir} MANDIR=%{_mandir} \
	install
install -m755 -d %{buildroot}%{_sysconfdir}/xinetd.d/ %{buildroot}/var/lib/tftpboot
#pushd %{buildroot}
mkdir -p %{buildroot}/lib/systemd/system
cp %{SOURCE1} %{buildroot}/lib/systemd/system/tftpd-hpa.service
cp %{SOURCE2} %{buildroot}/lib/systemd/system/tftpd-hpa.socket
#popd
cat << EOF >> %{buildroot}%{_sysconfdir}/xinetd.d/tftp
# default: off
# description: The tftp server serves files using the trivial file transfer \
#	protocol.  The tftp protocol is often used to boot diskless \
#	workstations, download configuration files to network-aware printers, \
#	and to start the installation process for some operating systems.
service tftp
{
	socket_type		= dgram
	protocol		= udp
	wait			= yes
	user			= root
	server			= /usr/sbin/in.tftpd
	server_args		= -s /var/lib/tftpboot
	disable			= no
	per_source		= 11
	cps			= 100 2
	flags			= IPv4
}
EOF

%clean
rm -rf %{buildroot}

%post server
/sbin/ldconfig 
%systemd_post tftpd-hpa.service tftpd-hpa.socket

%preun server
%systemd_preun tftpd-hpa.service tftpd-hpa.socket

%postun server
/sbin/ldconfig
%systemd_postun_with_restart tftpd-hpa.service

%files
%defattr(-,root,root)
%{_bindir}/tftp
%{_mandir}/man1/

%files server
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xinetd.d/tftp
%dir %attr(0750,nobody,nobody) /var/lib/tftpboot
%{_sbindir}/in.tftpd
%{_mandir}/man8/*
/lib/systemd/system/tftpd-hpa.service
/lib/systemd/system/tftpd-hpa.socket

%changelog
*	Mon Jul 27 2015 Xiaolin Li <xiaolinl@vmware.com> 5.2-1
-	Initial build.	First version
