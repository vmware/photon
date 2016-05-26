Summary:	The client for the Trivial File Transfer Protocol (TFTP)
Name:		tftp
Version:	5.2
Release:	6%{?dist}
License:	BSD
URL:		http://www.kernel.org
Group:		Applications/Internet
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://www.kernel.org/pub/software/network/tftp/tftp-hpa/tftp-hpa-%{version}.tar.gz
%define sha1 tftp=2fe37983ffeaf4063ffaba514c4848635c622d8b
BuildRequires:  systemd
Requires:       systemd
%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations.  The tftp package provides the user
interface for TFTP, which allows users to transfer files to and from a
remote machine.  This program and TFTP provide very little security,
and should not be enabled unless it is expressly needed.

%package server
Group: System Environment/Daemons
Summary: The server for the Trivial File Transfer Protocol (TFTP).

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
mkdir -p %{buildroot}/%{_var}/lib/tftpboot

%makeinstall
make INSTALLROOT=%{buildroot} \
    SBINDIR=%{_sbindir} MANDIR=%{_mandir} \
	install

mkdir -p %{buildroot}/lib/systemd/system
cat << EOF >> %{buildroot}/lib/systemd/system/tftpd.service
[Unit]
Description=The tftp server serves files using the trivial file transfer protocol. 

[Service]
ExecStart=/usr/sbin/in.tftpd -s /var/lib/tftpboot
StandardInput=socket

[Install]
Also=tftpd.socket
EOF

cat << EOF >> %{buildroot}/lib/systemd/system/tftpd.socket
[Unit]
Description=Tftp Server Socket

[Socket]
ListenDatagram=69

[Install]
WantedBy=sockets.target
EOF
%preun
%systemd_preun tftpd.socket

%post
%systemd_post tftpd.socket

%postun
%systemd_postun_with_restart tftpd.socket

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/tftp
%{_mandir}/man1/

%files server
%defattr(-,root,root)
%dir %attr(0750,nobody,nobody) %{_var}/lib/tftpboot
%{_sbindir}/in.tftpd
%{_mandir}/man8/*
/lib/systemd/system/tftpd.service
/lib/systemd/system/tftpd.socket

%changelog
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  5.2-6
-   Fixed logic to restart the active services after upgrade 
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.2-5
-	GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.2-4
-   Fix for upgrade issues
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  5.2-3
-   Add systemd to Requires and BuildRequires
-   Use systemctl to enable/disable service.
*	Mon Nov 23 2015 Xiaolin Li <xiaolinl@vmware.com> 5.2-2
-	Chang tftpd from xinetd service to systemd service.
*	Mon Jul 27 2015 Xiaolin Li <xiaolinl@vmware.com> 5.2-1
-	Add tftp library to photon.
* Tue Sep 14 2004 H. Peter Anvin <hpa@zytor.com>
- removed completely broken "Malta" patch.
- integrated into build machinery so rpm -ta works.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 11 2003 Elliot Lee <sopwith@redhat.com>
- 0.33
- Add /tftpboot directory (#88204)

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Feb 23 2003 Tim Powers <timp@redhat.com>
- add BuildPreReq on tcp_wrappers

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 11 2002 Elliot Lee <sopwith@redhat.com> 0.32-1
- Update to 0.32

* Wed Oct 23 2002 Elliot Lee <sopwith@redhat.com> 0.30-1
- Fix #55789
- Update to 0.30

* Thu Jun 27 2002 Elliot Lee <sopwith@redhat.com>
- Try applying HJ's patch from #65476

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 17 2002 Elliot Lee <sopwith@redhat.com>
- Update to 0.29

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Dec 18 2001 Elliot Lee <sopwith@redhat.com> 0.17-15
- Add patch4: netkit-tftp-0.17-defaultport.patch for bug #57562
- Update to tftp-hpa-0.28 (bug #56131)
- Remove include/arpa/tftp.h to fix #57259
- Add resource limits in tftp-xinetd (#56722)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Jun 12 2001 Helge Deller <hdeller@redhat.de> (0.17-13)
- updated tftp-hpa source to tftp-hpa-0.17
- tweaked specfile with different defines for tftp-netkit and tftp-hpa version
- use hpa's tftpd.8 man page instead of the netkits one

* Mon May 07 2001 Helge Deller <hdeller@redhat.de>
- rebuilt in 7.1.x

* Wed Apr 18 2001 Helge Deller <hdeller@redhat.de>
- fix tftp client's put problems (#29529)
- update to tftp-hpa-0.16

* Wed Apr  4 2001 Jakub Jelinek <jakub@redhat.com>
- don't let configure to guess compiler, it can pick up egcs

* Thu Feb 08 2001 Helge Deller <hdeller@redhat.de>
- changed "wait" in xinetd file to "yes" (hpa-tftpd forks and exits) (#26467)
- fixed hpa-tftpd to handle files greater than 32MB (#23725)
- added "-l" flag to hpa-tftpd for file-logging (#26467)
- added description for "-l" to the man-page 

* Thu Feb 08 2001 Helge Deller <hdeller@redhat.de>
- updated tftp client to 0.17 stable (#19640),
- drop dependency on xinetd for tftp client (#25051),

* Wed Jan 17 2001 Jeff Johnson <jbj@redhat.com>
- xinetd shouldn't wait on tftp (which forks) (#23923).

* Sat Jan  6 2001 Jeff Johnson <jbj@redhat.com>
- fix to permit tftp put's (#18128).
- startup as root with chroot to /tftpboot with early reversion to nobody
  is preferable to starting as nobody w/o ability to chroot.
- %%post is needed by server, not client. Add %%postun for erasure as well.

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- default to being disabled

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- correct group.

* Tue Jul 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- change user from root to nobody

* Sat Jul 22 2000 Jeff Johnson <jbj@redhat.com>
- update to tftp-hpa-0.14 (#14003).
- add server_args (#14003).
- remove -D_BSD_SOURCE (#14003).

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- cook up an xinetd config file for tftpd

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to 0.17.

* Fri May  5 2000 Matt Wilson <msw@redhat.com>
- use _BSD_SOURCE for hpa's tftpd so we get BSD signal semantics.

* Fri Feb 11 2000 Bill Nottingham <notting@redhat.com>
- fix description

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages (again).

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description and summary

* Tue Jan  4 2000 Bill Nottingham <notting@redhat.com>
- split client and server

* Tue Dec 21 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.16.

* Sat Aug 28 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.15.

* Wed Apr  7 1999 Jeff Johnson <jbj@redhat.com>
- tftpd should truncate file when overwriting (#412)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Fri Aug  7 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- added check for getpwnam() failure

* Tue Jul 15 1997 Erik Troan <ewt@redhat.com>
- initial build
