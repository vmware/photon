%global security_hardening none

Summary:        Programs to parse command-line options
Name:           netkit-telnet
Version:        0.17
Release:        4%{?dist}
License:        BSD
URL:            http://rpm5.org/files/popt
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.linux.org.uk/pub/linux/Networking/netkit/%{name}-%{version}.tar.gz
%define sha1    netkit-telnet=41213dedaf242126b54a3ac51b905a351eb22b15
BuildRequires:  ncurses-devel
Requires:       ncurses
%description
Telnet is an protocal that allows you to connect to remote comuters over internet. This package provides a telnet client.

%package server
Summary: telent server applications
%description server
This provides the telnet server daemons.

%prep
%setup -q

%build 
sed -i 's/MANDIR="$PREFIX\/man"/MANDIR="$PREFIX\/share\/man"/g' configure
sed -i 's/LIBS += $(LIBTERMCAP)/LIBS += $(LIBTERMCAP) -lstdc++/g' telnet/Makefile
sed -i 's/install -s/install/' telnet/Makefile
sed -i 's/install -s/install/' telnetd/Makefile
sed -i '/#include <termios.h>/{s/.*/&\n#include <stdlib.h>\n#include <string.h>/;:a;n;ba}' telnet/externs.h
sed -i '/#include <stdlib.h>/{s/.*/&\n#include <string.h>/;:a;n;ba}' telnet/netlink.cc
./configure --installroot=%{buildroot}

make

%install
export MANDIR=%{_mandir}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/man1
mkdir -p %{buildroot}/%{_mandir}/man5
mkdir -p %{buildroot}/%{_mandir}/man8
mkdir -p %{buildroot}%{_sbindir}
make install

#%check
#make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/telnet
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/telnetd.8.gz

%files server
%defattr(-,root,root)
%{_sbindir}/in.telnetd
%{_mandir}/man8/in.telnetd.8.gz

%changelog
*   Wed Jul 10 2017 Chang Lee <changlee@vmware.com>  0.17-4
-   Restored %check and commented out %check for MakeCheck track
*   Wed Jun 28 2017 Chang Lee <changlee@vmware.com> 0.17-3
-   Removed %check due to no test existence
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.17-2
-   Ensure non empty debuginfo
*   Mon Jan 09 2017 Xiaolin Li <xiaolinl@vmware.com> 0.17-1
-   Initial build. First version    
