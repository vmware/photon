Summary: IPTraf is a console-based network statistics utility
Name:    iptraf
Version: 3.0.1
Release: 2%{?dist}
License: GPLv2
URL: ftp://iptraf.seul.org/pub/iptraf/%{name}-%{version}.tar.gz
Source: %{name}-%{version}.tar.gz
%define sha1 iptraf=9035b969868e49c276239d99964f427edfee87f3
Patch0: iptraf-2.4.0-Makefile.patch
Patch1: iptraf-2.7.0-install.patch
Patch2: iptraf-2.7.0-doc.patch
Patch4: iptraf-2.7.0-nostrip.patch
Patch5: iptraf-3.0.0-setlocale.patch
Patch6: iptraf-3.0.0-longdev.patch
Patch7: iptraf-3.0.1-compile.fix.patch
Patch8: iptraf-3.0.0-in_trafic.patch
Patch9: iptraf-3.0.1-incltypes.patch
Patch10: iptraf-3.0.0-ifname.patch
Patch11: iptraf-3.0.0-interface.patch
Patch12: iptraf-3.0.1-ipv6.patch
Patch13: iptraf-3.0.1-ipv6-fix.patch
Patch14: iptraf-3.0.1-servmon-fix.patch
Patch15: 0001-fix-strcpy-overlap-memory.patch
Patch16: iptraf-3.0.1-packet-fix.patch

Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:  Photon
BuildRequires: ncurses-devel

%description
IPTraf is a console-based network statistics utility for Linux. It gathers a variety of figures such as TCP connection packet and byte counts, interface statistics and activity indicators, TCP/UDP traffic breakdowns, and LAN station packet and byte counts.

%prep
%setup -q 
%patch7 -p1 -b .compile
%patch12 -p1 -b .ipv6
%patch13 -p1 -b .ipv6-fix
%patch14 -p1 -b .servmon-fix
%patch15 -p1 -b .fix-strcpy-overlap-memory
%patch0 -p1 -b .Makefile
%patch1 -p1 -b .install
%patch2 -p1 -b .doc
%patch4 -p1 -b .nostrip
%patch5 -p1 -b .setlocale
%patch6 -p1 -b .longdev
%patch8 -p1 -b .in_trafic
%patch9 -p1 -b .incltypes
%patch10 -p0 -b .ifname
%patch11 -p1 -b .interface
%patch16 -p1 -b .compile

%build
make -C src CFLAGS="-fno-strict-aliasing" \
	TARGET=%{_bindir}

%install
rm -rf %{buildroot}
install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_mandir}/man8
install -m644 Documentation/*.8 %{buildroot}/%{_mandir}/man8

make -C src TARGET=%{buildroot}%{_bindir} \
	install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_mandir}/*/*
%{_bindir}/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.1-2
-	GA - Bump release of all rpms
*   Mon Nov 30 2015 Xiaolin Li <xiaolinl@vmware.com> 3.0.1-1
-   Initial build.  First version
-   Patches from https://github.com/gooselinux/iptraf
