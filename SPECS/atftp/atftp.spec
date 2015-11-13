Summary:        Advanced Trivial File Transfer Protocol (ATFTP) - TFTP server
Name:           atftp
Version:        0.7.1
Release:        1%{?dist}
URL:            http://sourceforge.net/projects/atftp
License:        GPLv2+ and GPLv3+ and LGPLv2+
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://sourceforge.net/projects/atftp/files/latest/download/%{name}-%{version}.tar.gz

%define sha1 atftp=fc9e9f821dfd2f257b4a5c32b948ed60b4e31fd1

%description
Multithreaded TFTP server implementing all options (option extension and
multicast) as specified in RFC1350, RFC2090, RFC2347, RFC2348 and RFC2349.
Atftpd also support multicast protocol knowed as mtftp, defined in the PXE
specification. The server supports being started from inetd(8) as well as
a deamon using init scripts.

%package client
Summary: Advanced Trivial File Transfer Protocol (ATFTP) - TFTP client
Group: Applications/Internet


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


%files
%{_mandir}/man8/atftpd.8.gz
%{_sbindir}/atftpd
%{_mandir}/man8/in.tftpd.8.gz
%{_sbindir}/in.tftpd


%files client
%{_mandir}/man1/atftp.1.gz
%{_bindir}/atftp


%preun


%post


%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != '/' ] && rm -rf $RPM_BUILD_ROOT


%changelog
*       Thu Nov 12 2015 Kumar Kaushik <kaushikk@vmware.com> 0.7.1-1
-       Initial build.  First version

