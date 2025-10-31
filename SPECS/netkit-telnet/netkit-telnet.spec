%global security_hardening none

Summary:        Programs to parse command-line options
Name:           netkit-telnet
Version:        0.17
Release:        8%{?dist}
URL:            http://rpm5.org/files/popt
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.linux.org.uk/pub/linux/Networking/netkit/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0:         CVE-2022-39028.patch
Patch1:         CVE-2020-10188.patch
Patch2:         CVE-2004-0911.patch

BuildRequires: ncurses-devel

Requires: ncurses

%description
Telnet is an protocal that allows you to connect to remote comuters over internet. This package provides a telnet client.

%package server
Summary: telent server applications
%description server
This provides the telnet server daemons.

%prep
%autosetup -p1

%build
sed -i 's/MANDIR="$PREFIX\/man"/MANDIR="$PREFIX\/share\/man"/g' configure
sed -i 's/LIBS += $(LIBTERMCAP)/LIBS += $(LIBTERMCAP) -lstdc++/g' telnet/Makefile
sed -i 's/install -s/install/' telnet/Makefile
sed -i 's/install -s/install/' telnetd/Makefile
sed -i '/#include <termios.h>/{s/.*/&\n#include <stdlib.h>\n#include <string.h>/;:a;n;ba}' telnet/externs.h
sed -i '/#include <stdlib.h>/{s/.*/&\n#include <string.h>/;:a;n;ba}' telnet/netlink.cc
sh ./configure --installroot=%{buildroot}

make %{?_smp_mflags}

%install
export MANDIR=%{_mandir}
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_mandir}/man1 \
         %{buildroot}%{_mandir}/man5 \
         %{buildroot}%{_mandir}/man8 \
         %{buildroot}%{_sbindir}

make install %{?_smp_mflags}

#%%check
#Commented out %check due to no test existence

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
* Fri Oct 31 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.17-8
- Fix CVE-2004-0911 and CVE-2020-10188
* Tue Aug 26 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.17-7
- Bump version as a part of ncurses upgrade
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 0.17-6
- Release bump for SRP compliance
* Tue Oct 03 2023 Shivani Agarwal <shivania2@vmware.com> 0.17-5
- Fix CVE-2022-39028
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 0.17-4
- Bump version as a part of ncurses upgrade to v6.4
* Wed Jun 28 2017 Chang Lee <changlee@vmware.com> 0.17-3
- Removed %check due to no test existence
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.17-2
- Ensure non empty debuginfo
* Mon Jan 09 2017 Xiaolin Li <xiaolinl@vmware.com> 0.17-1
- Initial build. First version
